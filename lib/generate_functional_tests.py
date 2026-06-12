#!/usr/bin/env python3
"""
Gerador de testes funcionais para o reveal.

Lê a documentação de um ticket (description.md, refinamento-tecnico.md,
openapi.yaml, status-tasks.json, projects-context/) e gera cenários
de teste funcional em JSON declarativo.

Uso:
    python3 lib/generate_functional_tests.py tickets/TICKET_ID/
"""

import json
import os
import re
import sys
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# I/O: Leitura de arquivos do ticket
# ═══════════════════════════════════════════════════════════════════════════════

def read_file(path):
    """Lê arquivo e retorna conteúdo, ou string vazia se não existir."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def load_json(path):
    """Lê JSON e retorna dict, ou dict vazio se não existir/inválido."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


# ═══════════════════════════════════════════════════════════════════════════════
# DETECTOR: Tipo de ticket
# ═══════════════════════════════════════════════════════════════════════════════

API_KEYWORDS = [
    "@PostMapping", "@GetMapping", "@PutMapping", "@DeleteMapping", "@PatchMapping",
    "@RequestMapping", "ResponseEntity", "adicionar-endpoint",
]

BPMN_KEYWORDS = [
    "BpmnException", "DelegateExecution", "JavaDelegate", "BPMN", "bpmn",
    "dmnOnb", "activiti:", "camunda:",
]


def detect_ticket_type(ticket_dir):
    """Detecta se o ticket é API, BPMN/híbrido, ou desconhecido."""
    refinamento = read_file(os.path.join(ticket_dir, "refinamento-tecnico.md"))
    description = read_file(os.path.join(ticket_dir, "description.md"))
    status_tasks = load_json(os.path.join(ticket_dir, "status-tasks.json"))
    all_text = refinamento + description

    api_score = sum(1 for kw in API_KEYWORDS if kw in all_text)
    bpmn_score = sum(1 for kw in BPMN_KEYWORDS if kw in all_text)

    has_openapi = os.path.isfile(os.path.join(ticket_dir, "openapi.yaml"))

    tasks = status_tasks.get("tarefas", [])
    endpoint_tasks = sum(1 for t in tasks if t.get("tipo") == "adicionar-endpoint")

    if has_openapi or endpoint_tasks > 0 or api_score > bpmn_score:
        return "api"
    if bpmn_score > 0:
        return "bpmn"
    return "api"


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACTOR: Critérios de aceitação de description.md
# ═══════════════════════════════════════════════════════════════════════════════

def extract_acceptance_criteria(description_text):
    """Extrai critérios de aceitação (CA1, CA2, ...) do description.md"""
    criteria = []
    patterns = [
        r"CA\d+[:\s]+(.+?)(?:\n|$)",
        r"\*\*CA\d+\*?[:\s]+(.+?)(?:\n|$)",
        r"Criterio\s+\d+[:\s]+(.+?)(?:\n|$)",
        r"Cenario\s+\d+[:\s]+(.+?)(?:\n|$)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, description_text, re.IGNORECASE)
        for m in matches:
            criteria.append(m.strip())
    return criteria


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACTOR: Endpoints de openapi.yaml
# ═══════════════════════════════════════════════════════════════════════════════

def extract_openapi_endpoints(openapi_text):
    """Extrai endpoints de um YAML OpenAPI (parse manual, sem pyyaml)."""
    endpoints = []
    current_path = None
    current_method = None

    for line in openapi_text.split("\n"):
        path_match = re.match(r'^  (/[^:]+):', line)
        if path_match:
            current_path = path_match.group(1).strip()
            continue

        method_match = re.match(r'^    (get|post|put|delete|patch):', line, re.IGNORECASE)
        if method_match and current_path:
            current_method = method_match.group(1).upper()
            endpoints.append({"path": current_path, "method": current_method})

    return endpoints


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACTOR: Erros de refinamento-tecnico.md
# ═══════════════════════════════════════════════════════════════════════════════

def extract_error_codes(refinamento_text):
    """Extrai códigos de erro e fluxos de exceção."""
    errors = []
    for match in re.finditer(r"ERROR_[A-Z_]+", refinamento_text):
        code = match.group(0)
        if code not in [e["code"] for e in errors]:
            errors.append({"code": code, "context": ""})
    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# EXTRACTOR: Endpoints de projects-context/
# ═══════════════════════════════════════════════════════════════════════════════

def extract_project_endpoints(context_text):
    """Extrai endpoints de projects-context/*.md."""
    endpoints = []
    for match in re.finditer(
        r"@(Post|Get|Put|Delete|Patch)Mapping\([\"']([^\"']+)[\"']\)",
        context_text
    ):
        method = match.group(1).upper()
        path = match.group(2)
        endpoints.append({"method": method, "path": path})

    for match in re.finditer(
        r"@(Post|Get|Put|Delete|Patch)Mapping",
        context_text
    ):
        pass

    return endpoints


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR: Configuração
# ═══════════════════════════════════════════════════════════════════════════════

def generate_config(ticket_dir, ticket_type, endpoints):
    """Gera config.json com variáveis globais."""
    project_context_dir = os.path.join(ticket_dir, "..", "..", "projects-context")
    headers = {}
    base_url = "http://localhost:8080"

    for ctx_file in Path(project_context_dir).glob("*.md"):
        if ctx_file.name.startswith("_"):
            continue
        ctx_text = read_file(str(ctx_file))
        if "@RequestMapping" in ctx_text:
            rm_match = re.search(r'@RequestMapping\(["\']([^"\']+)["\']\)', ctx_text)
            if rm_match:
                base_path = rm_match.group(1)
                base_url = f"http://localhost:8080{base_path}"
                break

    channel_match = None
    for ctx_file in Path(project_context_dir).glob("*.md"):
        if ctx_file.name.startswith("_"):
            continue
        ctx_text = read_file(str(ctx_file))
        ch_match = re.search(r"X_APPLICATION_CHANNELIDENTITY.*?['\"]([^'\"]+)['\"]", ctx_text)
        if ch_match:
            channel_match = ch_match.group(1)
            break

    if not channel_match:
        channel_match = "X-Application-Channelidentity"

    return {
        "baseUrl": "http://localhost:8080",
        "headers": {
            "Content-Type": "application/json",
            channel_match: "BIE",
            "X-Application-Scope": "Onboarding",
        },
        "timeouts": {
            "requestSeconds": 10,
            "pollIntervalSeconds": 2,
            "pollMaxAttempts": 15,
        },
        "variables": {
            "numeroDocumento": "999996953489167",
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR: Setup compartilhado
# ═══════════════════════════════════════════════════════════════════════════════

def make_setup_steps():
    """Gera os steps de setup compartilhados (iniciar → token → confirmar → datos)."""
    return [
        {
            "name": "Iniciar proceso",
            "request": {
                "method": "POST",
                "path": "/api/procesos/onboarding/iniciar",
                "body": {
                    "email": "test@banco.com",
                    "tipoDocumento": "CUIT",
                    "numeroDocumento": "{{numeroDocumento}}",
                    "contactoNombre": "TEST",
                    "contactoApellido": "USER",
                    "contactoTelefono": "1111111111",
                    "oficialCodigo": "OF001",
                    "sucursalCodigo": "SUC01",
                    "personaSubsegmento": "SOCIO_O_DIRECTOR_EMPRESA_CLIENTE",
                },
            },
            "extract": {"idSolicitud": "$.idSolicitud"},
            "assert": {"status": 200},
        },
        {
            "name": "Gerar token",
            "request": {
                "method": "POST",
                "path": "/api/procesos/onboarding/generarToken",
                "body": {"idSolicitud": "{{idSolicitud}}"},
            },
            "assert": {"status": 200},
        },
        {
            "name": "Obter token via Camunda",
            "request": {
                "method": "GET",
                "path": "/engine-rest/variable-instance?processInstanceBusinessKey={{idSolicitud}}&variableName=TokenEmailGenerado",
            },
            "extract": {"token": "$.value"},
            "assert": {"status": 200},
        },
        {
            "name": "Confirmar token",
            "request": {
                "method": "POST",
                "path": "/api/procesos/onboarding/confirmarToken",
                "body": {"idSolicitud": "{{idSolicitud}}", "token": "{{token}}"},
            },
            "assert": {"status": 200},
        },
        {
            "name": "Confirmar datos cliente",
            "request": {
                "method": "POST",
                "path": "/api/procesos/onboarding/{{idSolicitud}}/cliente",
                "body": {
                    "razonSocial": "EMPRESA TEST SA",
                    "nombreFantasia": "TEST FANTASIA",
                    "clienteNombre": "TEST",
                    "clienteApellido": "USER",
                    "actividad": "COMERCIO",
                    "facturacion": 1000000,
                    "domicilioCalle": "MAIPU",
                    "domicilioNumero": "123",
                    "domicilioCodigoPostal": "C1084ABA",
                    "domicilioProvincia": "BUENOS_AIRES",
                    "domicilioLocalidad": "CABA",
                    "iva": {"situacion": "RESPONSABLE_INSCRIPTO"},
                    "ganancias": {"situacion": "NO_RESPONSABLE"},
                    "sucursalCodigo": "SUC01",
                    "personaSubsegmento": "SOCIO_O_DIRECTOR_EMPRESA_CLIENTE",
                },
            },
            "assert": {"status": 200},
        },
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR: Cenários para BPMN (EDPCN-951 style)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_bpmn_scenarios(ticket_dir, description, refinamento, status_tasks):
    """Gera cenários para tickets BPMN/Processo."""
    scenarios = []

    ca_list = extract_acceptance_criteria(description)
    error_codes = extract_error_codes(refinamento)

    cuit_variables = {
        "cuitSucesso": "2242495243",
        "cuitDocInvalido": "2242495242",
        "cuitErrorTecnico": "30590714719",
        "cuitRestriccion": "38442640094",
    }

    poll_step = {
        "name": "Verificar resultado",
        "request": {
            "method": "GET",
            "path": "/api/procesos/onboarding/{{idSolicitud}}",
        },
        "poll": {"maxAttempts": 15, "intervalSeconds": 2},
        "assert": {"status": 200},
    }

    has_ca = len(ca_list) > 0

    if has_ca:
        for i, ca_text in enumerate(ca_list):
            ca_num = i + 1
            ca_lower = ca_text.lower()

            if any(kw in ca_lower for kw in ["sin errores", "habilitado", "avanza", "exito", "ok"]):
                cuit_var = "cuitSucesso"
                expected = {"$.integrantes[0].habilitado": True}
                nome = f"CA{ca_num} - Sucesso"
            elif any(kw in ca_lower for kw in ["error tecnico", "tecnico", "referencia", "40002"]):
                cuit_var = "cuitErrorTecnico"
                expected = {"$.integrantes[0].habilitado": False}
                nome = f"CA{ca_num} - Erro Tecnico"
            elif any(kw in ca_lower for kw in ["documento invalido", "invalido", "normalizacion", "999"]):
                cuit_var = "cuitDocInvalido"
                expected = {"$.integrantes[0].habilitado": False}
                nome = f"CA{ca_num} - Documento Invalido"
            elif any(kw in ca_lower for kw in ["mezcla", "mixed", "combinacion"]):
                cuit_var = None
                expected = {"$.integrantes[0].habilitado": False}
                nome = f"CA{ca_num} - Mistura Erros"
            elif any(kw in ca_lower for kw in ["concaten", "motivo", "restriccion"]):
                cuit_var = "cuitRestriccion"
                expected = {"$.integrantes[0].habilitado": False}
                nome = f"CA{ca_num} - Concatenacion"
            elif any(kw in ca_lower for kw in ["limpieza", "clear", "vacio"]):
                continue
            else:
                cuit_var = "cuitSucesso"
                expected = {}
                nome = f"CA{ca_num}"

            steps = make_setup_steps()

            if cuit_var:
                load_step = {
                    "name": f"Cargar integrantes (CA{ca_num})",
                    "request": {
                        "method": "POST",
                        "path": "/api/procesos/onboarding/integrantes",
                        "body": {
                            "idSolicitud": "{{idSolicitud}}",
                            "integrantes": [
                                {
                                    "numeroDocumento": "{{" + cuit_var + "}}",
                                    "tipoDocumento": "CUIT",
                                    "nombre": "TEST",
                                    "apellido": "USER",
                                    "porcentajeParticipacion": 50,
                                    "rol": "REPRESENTANTE_LEGAL_CON_FIRMA",
                                    "representanteLegal": True,
                                    "firmante": True,
                                    "email": "test@test.com",
                                    "pep": False,
                                    "fatca": False,
                                    "sujetoObligado": False,
                                }
                            ],
                        },
                    },
                    "assert": {"status": 200},
                }
            else:
                load_step = {
                    "name": f"Cargar integrantes (CA{ca_num} - mistura)",
                    "request": {
                        "method": "POST",
                        "path": "/api/procesos/onboarding/integrantes",
                        "body": {
                            "idSolicitud": "{{idSolicitud}}",
                            "integrantes": [
                                {
                                    "numeroDocumento": "{{cuitErrorTecnico}}",
                                    "tipoDocumento": "CUIT",
                                    "nombre": "ERROR",
                                    "apellido": "TECNICO",
                                    "porcentajeParticipacion": 30,
                                    "rol": "REPRESENTANTE_LEGAL_CON_FIRMA",
                                    "representanteLegal": True,
                                    "firmante": True,
                                    "email": "error@test.com",
                                    "pep": False,
                                    "fatca": False,
                                    "sujetoObligado": False,
                                },
                                {
                                    "numeroDocumento": "{{cuitDocInvalido}}",
                                    "tipoDocumento": "CUIT",
                                    "nombre": "DOC",
                                    "apellido": "INVALIDO",
                                    "porcentajeParticipacion": 70,
                                    "rol": "FIRMANTE_APODERADO",
                                    "representanteLegal": False,
                                    "firmante": True,
                                    "email": "doc@test.com",
                                    "pep": False,
                                    "fatca": False,
                                    "sujetoObligado": False,
                                },
                            ],
                        },
                    },
                    "assert": {"status": 200},
                }
            steps.append(load_step)

            verify_step = {**poll_step}
            if expected:
                verify_step = {**poll_step, "assert": {**poll_step["assert"], "jsonpath": expected}}
            steps.append(verify_step)

            scenarios.append({
                "nome": nome,
                "tipo": "bpmn",
                "fonte": f"description.md:CA{ca_num}",
                "variables": {k: v for k, v in cuit_variables.items()},
                "steps": steps,
            })

    if not scenarios:
        steps = make_setup_steps()
        steps.append({
            "name": "Cargar integrantes",
            "request": {
                "method": "POST",
                "path": "/api/procesos/onboarding/integrantes",
                "body": {
                    "idSolicitud": "{{idSolicitud}}",
                    "integrantes": [
                        {
                            "numeroDocumento": "{{cuitSucesso}}",
                            "tipoDocumento": "CUIT",
                            "nombre": "TEST",
                            "apellido": "USER",
                            "porcentajeParticipacion": 50,
                            "rol": "REPRESENTANTE_LEGAL_CON_FIRMA",
                            "representanteLegal": True,
                            "firmante": True,
                            "email": "test@test.com",
                            "pep": False,
                            "fatca": False,
                            "sujetoObligado": False,
                        }
                    ],
                },
            },
            "assert": {"status": 200},
        })
        steps.append({
            "name": "Verificar resultado",
            "request": {"method": "GET", "path": "/api/procesos/onboarding/{{idSolicitud}}"},
            "poll": {"maxAttempts": 15, "intervalSeconds": 2},
            "assert": {"status": 200},
        })
        scenarios.append({
            "nome": "Fluxo basico",
            "tipo": "bpmn",
            "fonte": "status-tasks.json",
            "variables": {k: v for k, v in cuit_variables.items()},
            "steps": steps,
        })

    return scenarios


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR: Cenários para API (openapi.yaml)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_api_scenarios(ticket_dir, openapi_text, status_tasks):
    """Gera cenários para tickets API baseado no openapi.yaml."""
    scenarios = []
    endpoints = extract_openapi_endpoints(openapi_text)

    for ep in endpoints:
        method = ep["method"]
        path = ep["path"]

        steps = [{
            "name": f"{method} {path} - sucesso",
            "request": {
                "method": method,
                "path": path,
            },
            "assert": {"status": 200},
        }]
        scenarios.append({
            "nome": f"{method} {path}",
            "tipo": "api",
            "fonte": "openapi.yaml",
            "steps": steps,
        })

    return scenarios


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR: Cenários de prioridade de erros
# ═══════════════════════════════════════════════════════════════════════════════

def generate_priority_scenario(cuit_variables):
    """Gera cenário de validação da prioridade de erros."""
    steps = make_setup_steps()

    steps.append({
        "name": "Cargar integrantes con doc invalido",
        "request": {
            "method": "POST",
            "path": "/api/procesos/onboarding/integrantes",
            "body": {
                "idSolicitud": "{{idSolicitud}}",
                "integrantes": [
                    {
                        "numeroDocumento": "{{cuitDocInvalido}}",
                        "tipoDocumento": "CUIT",
                        "nombre": "PRIORITY",
                        "apellido": "TEST",
                        "porcentajeParticipacion": 100,
                        "rol": "REPRESENTANTE_LEGAL_CON_FIRMA",
                        "representanteLegal": True,
                        "firmante": True,
                        "email": "priority@test.com",
                        "pep": False,
                        "fatca": False,
                        "sujetoObligado": False,
                    }
                ],
            },
        },
        "assert": {"status": 200},
    })

    steps.append({
        "name": "Verificar que ERROR_VALIDACION prevalece",
        "request": {
            "method": "GET",
            "path": "/api/procesos/onboarding/{{idSolicitud}}",
        },
        "poll": {"maxAttempts": 15, "intervalSeconds": 2},
        "assert": {
            "status": 200,
            "jsonpath": {"$.integrantes[0].habilitado": False},
        },
    })

    return {
        "nome": "Prioridad - ERROR_VALIDACION antes de ERROR_TECNICO",
        "tipo": "bpmn",
        "fonte": "status-tasks.json + refinamento-tecnico.md:L132-136",
        "variables": {k: v for k, v in cuit_variables.items()},
        "steps": steps,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 generate_functional_tests.py tickets/TICKET_ID/")
        sys.exit(1)

    ticket_dir = sys.argv[1].rstrip("/")
    if not os.path.isdir(ticket_dir):
        print(f"ERRO: Diretorio nao encontrado: {ticket_dir}", file=sys.stderr)
        sys.exit(1)

    description = read_file(os.path.join(ticket_dir, "description.md"))
    refinamento = read_file(os.path.join(ticket_dir, "refinamento-tecnico.md"))
    openapi_text = read_file(os.path.join(ticket_dir, "openapi.yaml"))
    status_tasks = load_json(os.path.join(ticket_dir, "status-tasks.json"))
    ticket_type = detect_ticket_type(ticket_dir)

    test_dir = os.path.join(ticket_dir, "testes-funcionais")
    cenarios_dir = os.path.join(test_dir, "cenarios")
    os.makedirs(cenarios_dir, exist_ok=True)

    print(f"  Ticket: {os.path.basename(ticket_dir)}")
    print(f"  Tipo: {ticket_type}")

    config = generate_config(ticket_dir, ticket_type, [])
    with open(os.path.join(test_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"  config.json gerado")

    if ticket_type == "bpmn":
        scenarios = generate_bpmn_scenarios(ticket_dir, description, refinamento, status_tasks)
        cuit_vars = {
            "cuitSucesso": "2242495243",
            "cuitDocInvalido": "2242495242",
            "cuitErrorTecnico": "30590714719",
            "cuitRestriccion": "38442640094",
        }
        scenarios.append(generate_priority_scenario(cuit_vars))
    elif ticket_type == "api" and openapi_text:
        scenarios = generate_api_scenarios(ticket_dir, openapi_text, status_tasks)
    else:
        scenarios = []

    for scenario in scenarios:
        slug = re.sub(r"[^a-z0-9]+", "_", scenario["nome"].lower()).strip("_")
        if len(slug) > 60:
            slug = slug[:60]
        filepath = os.path.join(cenarios_dir, f"{slug}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(scenario, f, indent=2, ensure_ascii=False)

    print(f"  {len(scenarios)} cenarios gerados em testes-funcionais/cenarios/")


if __name__ == "__main__":
    main()
