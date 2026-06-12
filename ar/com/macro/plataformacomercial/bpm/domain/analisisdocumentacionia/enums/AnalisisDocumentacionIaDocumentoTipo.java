package ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia.enums;

import ar.com.macro.plataformacomercial.bpm.util.enumeracion.Enumeracion;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

public interface AnalisisDocumentacionIaDocumentoTipo extends Enumeracion<AnalisisDocumentacionIaDocumentoTipo.Values> {

    @Getter
    @RequiredArgsConstructor
    enum Values implements AnalisisDocumentacionIaDocumentoTipo {

        ESTATUTO_SOCIETARIO("estatuto", "Estatuto Societario"),
        ACTAS_DIRECTORIO("acta_asamblea", "Actas Directorio"),
        PODER_OTORGADO("poder_legal", "Poder Otorgado"),
        IDENTIDAD_PERSONA("dni_autoridades", "Identidad Persona"),
        IDENTIDAD_PERSONA_JURIDICA("inscripcion_arca", "Identidad Persona Juridica"),
        BALANCES_MANIFESTACION_BIENES("balance", "Balances/Manifestación de Bienes"),
        LIQUIDACION_EXPENSA("expensa", "Liquidacion de Expensa"),
        INSCRIPCION_IGJ("inscripcion_igj", "Inscripción IGJ"),
        REGLAMENTO_COPROPIEDAD("consorcio", "Reglamento de Copropiedad")

        ;

        private final String codigo;
        private final String descripcion;
    }
}
