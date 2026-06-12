# Plano de Correção — EDPCN-886 (Webhook lectura documentos IA)

Ticket: `EDPCN-886` — Fazer os cenários E2E do webhook passarem (hoje NPE → 500).
Branch: `feature/EDPCN-886`. EDPCN-978 (anterior, `e618d587c`) já é ancestral e ajustou campos no converter/DTO/domain.

## Diagnóstico definitivo

### Causa 1 — NPE (500 em 2.1/2.2/2.6–2.14)
`ArtaxApiConverter.paraDominio` retorna `base` quando `datosExtraidos == null`
(linhas 26-28) e mapeia `documentacionValida`/`errores` apenas dentro do branch
`datosExtraidos` (linhas 161-171). Nenhum body 2.x envia `datosExtraidos`, então:
- `documentacionValida = null`
- `OnboardingAnalisisDocumentacionIaResultadoStrategy.isDocumentacionValida("isTrue(null)") = false`
- DMN regra `?.EstatutoSocietario.DocumentacionValida = false` dispara
- `Mensaje = string join(for item in Errores return item.Mensaje, " / ")` = `""` (Errores vazio)
- NPE em `ProcesoValidacionDelegate:36` — "El valor de la columna 'Mensaje' del DMN de validación es obligatório"

**Correção (Fix 1):** em `ArtaxApiConverter.paraDominio`, mapear
`documentacionValida` e `errores` SEMPRE no builder `base`, fora do branch
`datosExtraidos`. Campos vêm do DTO top-level `validacionesResultado`.
Não quebra testes 978 (fixture `-sin-datos-extraidos-request.json` não possui
`validacionesResultado` → seguem null).

Após o fix:
- 2.1 (valido=true) → documentacionValida=true → DMN aprobado → 200 RESGUARDADO
- 2.2 (valido=false + errores SECCION_INCOMPLETA) → mensaje não vazio → ValidationException → NO_VALIDO → 200 RESGUARDADO

### Causa 2 — evento ignorado (2.3 retorna código errado)
`OnboardingService.guardarDatosAnalisisDocumentacionIaResultado` (linha ~1131)
só checa `estado != COMPLETADO`. `evento` existe no request → domain
`ArtaxResultadoLecturaDocumentosIA` mas é dropado; constante
`ANALISIS_DOCUMENTACION_IA_DOCUMENTO_COMPLETADO = "document.completed"` (linha 156)
nunca é usada.

- 2.3: estado=processing, evento=processing → hoje ESTADO_NO_FINAL (errado; esperado ANALISIS_INCOMPLETO)
- 2.4: estado=processing, evento=completed → ESTADO_NO_FINAL (correto)

Ordem de checagem (segundo roteiro): evento ANTES do estado.

**Correção (Fix 2):**
1. Adicionar campo `evento` (String) em `OnboardingAnalisisDocumentacionIaResultado` (domain).
2. `ArtaxService`: propagar `.evento(resultadoLecturaDocumentosIA.getEvento())`.
3. `OnboardingService` guardar: se `evento != "document.completed"` → resolucao `ANALISIS_INCOMPLETO`; senão se `estado != COMPLETADO` → `ESTADO_NO_FINAL`.
4. Strict (decisão do usuário): exigir `document.completed`. Atualizar builders de teste
   que criam `OnboardingAnalisisDocumentacionIaResultado` para setar `.evento("document.completed")`
   — ex.: `OnboardingAnalisisDocumentacionIaConsultarResultadoFixture.buildValido()/buildNoValido()`.

### Causa 3 — collection 2.7–2.14 não produzem o descarte esperado
O código casa o documento APENAS por `grupoId` (`OnboardingService` ~1142,
`Objects.equals(AnalisisDocumentacionIaGrupoId, grupoId)`), ignorando o
`documentoTipo` do payload. Como 2.7–2.14 enviam `{{grupoId}} = GRP-1005`
(publicado para doc 77/estatuto), o app acha o doc 77 → hoje NPE; após Fix 1
resguardaria como ESTATUTO, nunca descartaria com `DESCARTADO_ID_DOCUMENTO_INCORRECTO`.

**Correção (Fix 3):** nos bodies 2.7–2.14 usar `idDocuLecturaDocumentosIA` com um
grupo NÃO publicado. Criar env var nova `grupoIdNoPublicado` (ex.: `GRP-9999`) no
environment da collection e usar `{{grupoIdNoPublicado}}`. Assim → resolucao
`GRUPO_ID_INCORRECTO` → `DESCARTADO_ID_DOCUMENTO_INCORRECTO`.

### Decisão — cenário 2.6 (reenvio duplicado)
Collection 2.6 esperava `RESGUARDADO`. Após 2.1 resguardar+consolidar doc 77, o
reenvio vira `RESULTADO_YA_RECIBIDO` → `DESCARTADO_RESULTADO_YA_RECIBIDO`.
**Decisão do usuário:** alinhar ao roteiro → atualizar assertion 2.6 para
`DESCARTADO_RESULTADO_YA_RECIBIDO`.

## Arquivos a alterar

| Arquivo | Mudança |
|---------|---------|
| `src/main/java/.../api/webhook/artax/ArtaxApiConverter.java` | Mover `.documentacionValida(...)` e `.errores(...)` para o builder `base` (Fix 1); remover do `toBuilder` |
| `src/main/java/.../core/proceso/onb/OnboardingAnalisisDocumentacionIaResultado.java` | Adicionar campo `evento` (Fix 2) |
| `src/main/java/.../core/webhook/artax/ArtaxService.java` | `.evento(...)` no build do resultado (Fix 2) |
| `src/main/java/.../core/proceso/onb/OnboardingService.java` | Checagem `evento` antes de `estado` (Fix 2) |
| `src/test/java/.../data/apigee/analisisdocumentacionia/OnboardingAnalisisDocumentacionIaConsultarResultadoFixture.java` | `.evento("document.completed")` nos builders (Fix 2) |
| `.../ArtaxControllerTest.java` | (opcional/necessário) teste para converter com validacionesResultado sem datosExtraidos |
| Collection Postman `EDPCN-886/demo-artifacts/postman-collection.json` | Bodies 2.7–2.14 → `{{grupoIdNoPublicado}}`; assertion 2.6 → DESCARTADO_RESULTADO_YA_RECIBIDO (Fix 3) |
| Environment Postman | Adicionar `grupoIdNoPublicado` |

## Verificação

1. `./gradlew test` — 41+ testes verdes (incluindo 978 e os novos).
2. E2E Newman folder 2 com `--delay-request 7000`:
   - 2.1 → RESGUARDADO
   - 2.2 → RESGUARDADO
   - 2.3 → DESCARTADO_ANALISIS_INCOMPLETO
   - 2.4 → DESCARTADO_ESTADO_NO_FINAL
   - 2.5 → DESCARTADO_ID_LECTURAIA_INCORRECTO
   - 2.6 → DESCARTADO_RESULTADO_YA_RECIBIDO
   - 2.7–2.14 → DESCARTADO_ID_DOCUMENTO_INCORRECTO
3. Novo fluxo: re-executar 1.1–1.5 + 2.1 para confirmar 200 RESGUARDADO sem NPE.
4. Conferir persistência: v1 listar documento 77 → analisisDocumentacionIaEstadoDocumento VALIDO, observações populadas.

## Observações de consistência (AGENTS.md)
- Atualizar `contexto-implementacao.md`/`status-tasks.json` se a task 0001 do ticket for concluída.
- Verificar `projects-context/` existe para credenciais dos serviços (Jira/Bitbucket).