#!/usr/bin/env python3
"""
Runner genérico de testes funcionais para o reveal.

Lê cenários JSON declarativos, executa steps HTTP, valida asserts,
gera relatório estruturado.

Uso:
    python3 lib/functional_test_runner.py TESTES_DIR/
    python3 lib/functional_test_runner.py TESTES_DIR/ --scenario CA1
    python3 lib/functional_test_runner.py TESTES_DIR/ --dry-run
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from http.client import HTTPConnection, HTTPSConnection
from pathlib import Path
from urllib.parse import urljoin, urlparse


# ═══════════════════════════════════════════════════════════════════════════════
# CORE: HTTP Client
# ═══════════════════════════════════════════════════════════════════════════════

def do_request(base_url, method, path, headers=None, body=None, timeout=10):
    """Executa uma requisição HTTP. Retorna (status_code, headers, body_str)."""
    parsed = urlparse(base_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    full_path = path
    if parsed.path and parsed.path != "/":
        full_path = parsed.path.rstrip("/") + "/" + path.lstrip("/")

    headers = headers or {}
    body_str = None
    if body is not None:
        body_str = json.dumps(body)
        headers.setdefault("Content-Type", "application/json")

    if parsed.scheme == "https":
        conn = HTTPSConnection(host, port, timeout=timeout)
    else:
        conn = HTTPConnection(host, port, timeout=timeout)

    try:
        conn.request(method, full_path, body=body_str, headers=headers)
        resp = conn.getresponse()
        resp_body = resp.read().decode("utf-8", errors="replace")
        resp_headers = dict(resp.getheaders())
        return resp.status, resp_headers, resp_body
    finally:
        conn.close()


# ═══════════════════════════════════════════════════════════════════════════════
# JSON PATH: Extração de valores do response
# ═══════════════════════════════════════════════════════════════════════════════

def resolve_path(obj, path):
    """Resolve um JSONPath simples: $.field.subfield ou $.arr[0].field"""
    stripped = path.lstrip("$").strip(".")
    if not stripped:
        return obj
    parts = stripped.split(".")
    current = obj
    for part in parts:
        if current is None:
            return None
        match = re.match(r"^(.+?)\[(\d+)\]$", part)
        if match:
            key, idx = match.group(1), int(match.group(2))
            if isinstance(current, dict):
                current = current.get(key)
            if isinstance(current, list) and idx < len(current):
                current = current[idx]
            else:
                return None
        else:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
    return current


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE: Substituição de {{variáveis}}
# ═══════════════════════════════════════════════════════════════════════════════

def render_template(obj, variables):
    """Renderiza {{variaveis}} recursivamente em strings, dicts e listas."""
    if isinstance(obj, str):
        result = obj
        for key, value in variables.items():
            result = result.replace("{{" + key + "}}", str(value))
        return result
    if isinstance(obj, dict):
        return {k: render_template(v, variables) for k, v in obj.items()}
    if isinstance(obj, list):
        return [render_template(item, variables) for item in obj]
    return obj


# ═══════════════════════════════════════════════════════════════════════════════
# ASSERTIONS: Validação de responses
# ═══════════════════════════════════════════════════════════════════════════════

def check_assertions(status_code, response_data, response_text, assertions):
    """Valida assertions contra o response. Retorna lista de erros (vazia = OK)."""
    errors = []
    if not assertions:
        return errors

    expected_status = assertions.get("status")
    if expected_status is not None and status_code != expected_status:
        errors.append(f"status: esperado {expected_status}, obtido {status_code}")

    expected_jsonpath = assertions.get("jsonpath", {})
    for path, expected in expected_jsonpath.items():
        actual = resolve_path(response_data, path)
        if actual != expected:
            errors.append(f"{path}: esperado {expected!r}, obtido {actual!r}")

    expected_contains = assertions.get("contains")
    if expected_contains is not None:
        if expected_contains not in response_text:
            errors.append(f"contains: '{expected_contains}' nao encontrado no response")

    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# STEP EXECUTION: Execução de um step
# ═══════════════════════════════════════════════════════════════════════════════

def execute_step(base_url, global_headers, step, variables, timeout):
    """Executa um step HTTP. Retorna (ok, new_vars, error_msg, response_data)."""
    req = render_template(step["request"], variables)
    method = req.get("method", "GET").upper()
    path = req["path"]
    headers = {**global_headers, **req.get("headers", {})}
    body = req.get("body")

    last_error = None
    for attempt in range(1, 4):
        try:
            status, _, resp_text = do_request(base_url, method, path, headers, body, timeout)
        except Exception as e:
            last_error = f"Erro de conexao: {e}"
            time.sleep(1)
            continue

        try:
            response_data = json.loads(resp_text)
        except (json.JSONDecodeError, ValueError):
            response_data = resp_text

        if status >= 500 and attempt < 3:
            last_error = f"Tentativa {attempt}: HTTP {status}"
            time.sleep(1)
            continue

        assertions = step.get("assert", {})
        errors = check_assertions(status, response_data, resp_text, assertions)
        if errors:
            return False, {}, " | ".join(errors), response_data

        new_vars = {}
        extract = step.get("extract", {})
        for var_name, extract_def in extract.items():
            if isinstance(extract_def, str):
                new_vars[var_name] = resolve_path(response_data, extract_def)
            elif isinstance(extract_def, dict):
                raw = resolve_path(response_data, extract_def.get("path", ""))
                filtros = extract_def.get("filter", {})
                rendered_filters = {}
                for fk, fv in filtros.items():
                    if isinstance(fv, str) and "{{" in fv:
                        rendered_val = render_template({"v": fv}, variables).get("v", fv)
                        rendered_filters[fk] = rendered_val
                    else:
                        rendered_filters[fk] = fv
                if isinstance(raw, list) and rendered_filters:
                    for item in raw:
                        match = True
                        for fk, fv in rendered_filters.items():
                            if str(item.get(fk)) != str(fv):
                                match = False
                                break
                        if match:
                            raw = item
                            break
                target = extract_def.get("field")
                if target and isinstance(raw, dict):
                    new_vars[var_name] = raw.get(target)
                else:
                    new_vars[var_name] = raw
        return True, new_vars, None, response_data

    return False, {}, last_error or "Maximo de tentativas atingido", None


def execute_step_with_poll(base_url, global_headers, step, variables, config):
    """Executa um step com polling (para asserts assíncronos)."""
    poll = step.get("poll")
    if not poll:
        return execute_step(base_url, global_headers, step, variables, config.get("requestTimeout", 10))

    max_attempts = poll.get("maxAttempts", 15)
    interval = poll.get("intervalSeconds", 2)
    timeout = config.get("requestTimeout", 10)

    last_error = None
    for attempt in range(1, max_attempts + 1):
        req = render_template(step["request"], variables)
        method = req.get("method", "GET").upper()
        path = req["path"]
        headers = {**global_headers, **req.get("headers", {})}
        body = req.get("body")

        try:
            status, _, resp_text = do_request(base_url, method, path, headers, body, timeout)
        except Exception as e:
            last_error = f"Tentativa {attempt}: erro de conexao: {e}"
            if attempt < max_attempts:
                time.sleep(interval)
            continue

        try:
            response_data = json.loads(resp_text)
        except (json.JSONDecodeError, ValueError):
            response_data = resp_text

        assertions = step.get("assert", {})
        errors = check_assertions(status, response_data, resp_text, assertions)

        if not errors:
            new_vars = {}
            extract = step.get("extract", {})
            for var_name, extract_def in extract.items():
                if isinstance(extract_def, str):
                    new_vars[var_name] = resolve_path(response_data, extract_def)
                elif isinstance(extract_def, dict):
                    raw = resolve_path(response_data, extract_def.get("path", ""))
                    filtros = extract_def.get("filter", {})
                    rendered_filters = {}
                    for fk, fv in filtros.items():
                        if isinstance(fv, str) and "{{" in fv:
                            rendered_val = render_template({"v": fv}, variables).get("v", fv)
                            rendered_filters[fk] = rendered_val
                        else:
                            rendered_filters[fk] = fv
                    if isinstance(raw, list) and rendered_filters:
                        for item in raw:
                            match = True
                            for fk, fv in rendered_filters.items():
                                if str(item.get(fk)) != str(fv):
                                    match = False
                                    break
                            if match:
                                raw = item
                                break
                    target = extract_def.get("field")
                    if target and isinstance(raw, dict):
                        new_vars[var_name] = raw.get(target)
                    else:
                        new_vars[var_name] = raw
            return True, new_vars, None, response_data

        last_error = f"Tentativa {attempt}: {' | '.join(errors)}"
        if attempt < max_attempts:
            time.sleep(interval)

    return False, {}, last_error, response_data if "response_data" in dir() else None


# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO: Execução de um cenário completo
# ═══════════════════════════════════════════════════════════════════════════════

def run_scenario(base_url, global_headers, scenario, config):
    """Executa todos os steps de um cenário. Retorna dict com resultado."""
    nome = scenario.get("nome", "Sem nome")
    variables = {**config.get("variables", {}), **scenario.get("variables", {})}
    timeout = config.get("requestTimeout", 10)
    step_delay = config.get("stepDelayMs", 500) / 1000.0
    steps = scenario.get("steps", [])

    step_results = []
    for i, step in enumerate(steps):
        step_name = step.get("name", f"Step {i+1}")

        delay = step.get("delayMs", step_delay * 1000) / 1000.0
        if delay > 0:
            time.sleep(delay)

        start = time.time()

        ok, new_vars, error, _ = execute_step_with_poll(
            base_url, global_headers, step, variables, config
        )

        elapsed = round(time.time() - start, 2)
        variables.update(new_vars)

        result = {
            "step": i + 1,
            "name": step_name,
            "ok": ok,
            "elapsed": elapsed,
        }
        if not ok:
            result["error"] = error
        step_results.append(result)

        if not ok:
            break

    all_ok = all(r["ok"] for r in step_results)
    return {
        "nome": nome,
        "ok": all_ok,
        "steps": step_results,
        "totalElapsed": round(sum(r["elapsed"] for r in step_results), 2),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT: Geração de relatório
# ═══════════════════════════════════════════════════════════════════════════════

def generate_report(results, test_dir):
    """Gera relatório JSON + output colorido no terminal."""
    resultados_dir = os.path.join(test_dir, "resultados")
    os.makedirs(resultados_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    passed = sum(1 for r in results if r["ok"])
    total = len(results)

    summary = {
        "timestamp": timestamp,
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "allPassed": passed == total,
        "scenarios": results,
    }

    summary_path = os.path.join(resultados_dir, "resumo.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    for r in results:
        slug = re.sub(r"[^a-z0-9]+", "_", r["nome"].lower()).strip("_")
        scenario_path = os.path.join(resultados_dir, f"{slug}.json")
        with open(scenario_path, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    print(f"\n{'='*60}")
    print(f"  RELATORIO DE TESTES FUNCIONAIS")
    print(f"  {timestamp}")
    print(f"{'='*60}\n")

    for r in results:
        icon = f"{GREEN}PASS{RESET}" if r["ok"] else f"{RED}FAIL{RESET}"
        print(f"  [{icon}] {r['nome']} ({r['totalElapsed']}s)")
        for s in r["steps"]:
            step_icon = f"{GREEN}✓{RESET}" if s["ok"] else f"{RED}✗{RESET}"
            print(f"    {step_icon} {s['name']} ({s['elapsed']}s)")
            if not s["ok"]:
                print(f"      {RED}{s.get('error', 'Erro desconhecido')}{RESET}")

    print(f"\n{'='*60}")
    color = GREEN if passed == total else RED
    print(f"  {color}{passed}/{total} cenarios PASSARAM{RESET}")
    if passed < total:
        print(f"  {YELLOW}{total - passed} cenario(s) FALHARAM{RESET}")
    print(f"{'='*60}\n")
    print(f"  Relatorio: {summary_path}")

    return passed == total


# ═══════════════════════════════════════════════════════════════════════════════
# DISCOVERY: Descoberta de cenários
# ═══════════════════════════════════════════════════════════════════════════════

def discover_scenarios(cenarios_dir):
    """Descobre e carrega todos os cenários JSON de um diretório."""
    scenarios = []
    if not os.path.isdir(cenarios_dir):
        return scenarios

    for fname in sorted(os.listdir(cenarios_dir)):
        if not fname.endswith(".json") or fname.startswith("_"):
            continue
        fpath = os.path.join(cenarios_dir, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                scenario = json.load(f)
            scenarios.append(scenario)
        except (json.JSONDecodeError, OSError) as e:
            print(f"  AVISO: Erro ao carregar {fname}: {e}", file=sys.stderr)

    return scenarios


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 functional_test_runner.py TESTES_DIR/ [--scenario NOME] [--dry-run]")
        sys.exit(1)

    test_dir = sys.argv[1].rstrip("/")
    scenario_filter = None
    dry_run = False

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--scenario" and i + 1 < len(args):
            scenario_filter = args[i + 1]
            i += 2
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        else:
            i += 1

    config_path = os.path.join(test_dir, "config.json")
    if not os.path.isfile(config_path):
        print(f"ERRO: config.json nao encontrado em {test_dir}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    base_url = config.get("baseUrl", "http://localhost:8080")
    global_headers = config.get("headers", {})
    cenarios_dir = os.path.join(test_dir, "cenarios")

    scenarios = discover_scenarios(cenarios_dir)
    if scenario_filter:
        scenarios = [s for s in scenarios if scenario_filter.lower() in s.get("nome", "").lower()
                     or scenario_filter.lower() in os.path.basename(scenarios[0].get("_file", "")).lower()]

    if not scenarios:
        print("Nenhum cenario encontrado.")
        sys.exit(0)

    print(f"  Base URL: {base_url}")
    print(f"  Cenarios: {len(scenarios)}")

    if dry_run:
        print("\n  [DRY RUN] Cenarios que seriam executados:")
        for s in scenarios:
            steps = len(s.get("steps", []))
            print(f"    - {s.get('nome', '?')} ({steps} steps)")
        sys.exit(0)

    results = []
    for scenario in scenarios:
        result = run_scenario(base_url, global_headers, scenario, config)
        results.append(result)

    ok = generate_report(results, test_dir)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
