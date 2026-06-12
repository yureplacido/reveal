# Contexto do Projeto — bpmemp-lib-commons

Contexto permanente da biblioteca compartilhada entre os processos BPM. Gerado a partir do codigo em `/home/placido/desarrollo/proyectos/bpmempresas/bpmemp-lib-commons` (branch `develop`).

## Stack

| Tecnologia | Versao |
|------------|--------|
| Linguagem | Java |
| Build | Gradle (multi-modulo) |
| Imutabilidade | Lombok `@Value`, `@Builder`, `@With` |
| Banco | Nao aplicavel (biblioteca, sem persistencia) |
| Mapeamento | Jackson via `@JsonProperty` nos DTOs de Feign |
| Testes | JUnit 5 + Mockito |
| Migracoes | Nao aplicavel |

Versao corrente do projeto: `0.44.0-SNAPSHOT`, declarada em `libs.versions.toml` na chave `project`. Consumidores declaram o mesmo catálogo em `libs.versions.toml` com a chave `commons`.

## Arquitetura

Biblioteca de contratos e contratos de integracao compartilhada. Nao possui controllers, endpoints, BPMN nem persistencia. Cada modulo e publicado como artefato independente e consumido por Spring Boot via Gradle.

A separacao de responsabilidades segue tres camadas:

1. `commons-domain` — modelo de dominio imutavel, compartilhado entre processos.
2. `commons-starter-feign-*` — DTOs JSON da API remota e conversores para o modelo de dominio.
3. `commons-starter-core` / `commons-enumeracion` / `commons-error` — suporte comum.

Um processo consumidor nunca deve duplicar classes do dominio compartilhado: ele usa o modelo e, quando precisa ler a resposta, usa o DTO de Feign.

## Estrutura de Pacotes

Pacote base: `ar.com.macro.plataformacomercial.bpm.domain`

```
commons-domain/src/main/java/ar/com/macro/plataformacomercial/bpm/domain/
  prestamo/oferta/      modelo de dominio do processo prestamo-oferta
  moneda/               enumeracao Moneda
  riesgo/enums/         RiesgoLineaTipo, RiesgoSublineaTipo

commons-starter-feign-bpmemp/src/main/java/ar/com/macro/bpmemp/commons/feign/bpmemp/domain/
  prestamo/oferta/      DTOs JSON + conversores do fluxo prestamo-oferta
```

## Convencoes de Nomenclatura

- Classes de dominio: `PrestamoOferta`, `PrestamoOfertaService`, `RiesgoLineaTipo`, `Moneda`.
- DTOs de Feign: `PrestamoOfertaIniciarEndpoint`, `PrestamoOfertaConsultaDetalleEndpoint`, `PrestamoOfertaDetalleResponse`, `PrestamoOfertaClient`.
- Sub-objetos aninhados: classes `static` internas com nome do conceito (`Condiciones`, `Cliente`, `Proveedor`, `Origen`).
- Campos JSON em portugues no dominio, espelhando o contrato do processo.

## Padroes de Models

Todas as classes de dominio usam Lombok, sem setters e sem construtores explicitos:

```java
@With
@Value
@Builder(toBuilder = true)
public static class Condiciones {

    private RiesgoLineaTipo riesgoLinea;
    private RiesgoSublineaTipo riesgoSublinea;
}
```

## Padroes de DTOs / Commands

DTOs de Feign declaram o JSON com `@JsonProperty` explicito e mantem o metodo `convert` estatico que traduz o modelo de dominio para o DTO:

```java
@FeignClient(...)
public interface PrestamoOfertaIniciarEndpoint {

    @PostMapping(...)
    ResponseEntity<...> iniciar(@RequestBody Request request);

    static Request convert(PrestamoOferta prestamoOferta) {
        return Request.builder()
            .condiciones(prestamoOferta.getCondiciones() == null ? null
                : Request.Condiciones.builder()
                    .riesgoLinea(prestamoOferta.getCondiciones().getRiesgoLinea())
                    .build())
            .build();
    }
}
```

Regra essencial: todo `convert` trata o objeto pai como possivelmente nulo e devolve `null` em vez de objeto vazio, para que campos ausentes nao aparecam no JSON.

## Tratamento de Erros

Excecoes padronizadas em `commons-error`. O consumidor deve preservar a cadeia existente de `IntegrationException` e `BpmnException` ao integrar novos campos.

## Modulos e Dependencias

| Modulo | Responsabilidade |
|--------|------------------|
| `commons-domain` | Modelos de dominio compartilhados |
| `commons-starter-feign-bpmemp` | Cliente Feign e DTOs dos processos BPM |
| `commons-starter-web` / `commons-starter-validation` | Suporte web e validacao |
| `commons-starter-camunda` / `commons-starter-camunda-jpa` | Integracao Camunda |
| `commons-starter-test` | Dependencias de teste compartilhadas |

Fluxo de uso do fluxo `prestamo-oferta`: `PrestamoOfertaService` (domain) monta o modelo, `PrestamoOfertaClient` chama `PrestamoOfertaIniciarEndpoint` (start) ou `PrestamoOfertaConsultaDetalleEndpoint` (detalhe), e `PrestamoOfertaDetalleResponse` volta convertido para o modelo.

## Classes de Referencia

| Tipo | Caminho |
|------|---------|
| Modelo de dominio | `commons-domain/src/main/java/ar/com/macro/plataformacomercial/bpm/domain/prestamo/oferta/PrestamoOferta.java` |
| Servico de dominio | `commons-domain/src/main/java/ar/com/macro/plataformacomercial/bpm/domain/prestamo/oferta/PrestamoOfertaService.java` |
| DTO de inicio (Feign) | `commons-starter-feign-bpmemp/src/main/java/ar/com/macro/bpmemp/commons/feign/bpmemp/domain/prestamo/oferta/PrestamoOfertaIniciarEndpoint.java` |
| DTO de detalhe (Feign) | `commons-starter-feign-bpmemp/src/main/java/ar/com/macro/bpmemp/commons/feign/bpmemp/domain/prestamo/oferta/PrestamoOfertaDetalleResponse.java` |
| Cliente Feign | `commons-starter-feign-bpmemp/src/main/java/ar/com/macro/bpmemp/commons/feign/bpmemp/domain/prestamo/oferta/PrestamoOfertaClient.java` |
| Enumeracao de moeda | `commons-domain/src/main/java/ar/com/macro/plataformacomercial/bpm/domain/moneda/Moneda.java` |

## Convencoes de Valores Monetarios

Valores monetarios usam `BigDecimal` com o tipo `Moneda` do dominio. Exemplos em `PrestamoOferta`: `CalificacionRiesgo.Endeudamiento.Valor.monto` (linha 63), `OfertasComerciales.PrestamoAmortizable.Monto.monto` (linha 192) e `Disponible` (linha 238). Nao usar `double` em contratos compartilhados.

## Precedente de Evisao de Contrato

O commit `94cc4fb` (EDPCN-675) mostra o padrao adotado quando um contrato compartilhado precisa de um novo campo:

1. Alterar a classe interna em `commons-domain`.
2. Alterar o DTO de inicio em `commons-starter-feign-bpmemp` e seu `convert`.
3. Alterar o DTO de detalhe em `commons-starter-feign-bpmemp` e seu `convert`.
4. Fechar a versao e publicar a nova versao do artifact.
5. No projeto consumidor, atualizar a chave `commons` em `libs.versions.toml` e consumir a versao nova.

Esse trabalho e feito no ticket da integracao (a ponte entre processos), e nao no ticket do processo consumidor.
