package ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia;

import ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia.enums.AnalisisDocumentacionIaDocumentoTipo;
import lombok.Builder;
import lombok.Value;
import lombok.With;

@With
@Value
@Builder(toBuilder = true)
public class AnalisisDocumentacionIaPublicacionDocumento {

    //REQUISICION

    private String archivoBase64;
    private String gestionId;
    private MetaDatos metaDatos;

    //RESPUESTA

    private String grupoId;

    @Value
    @Builder
    public static class MetaDatos {

        private AnalisisDocumentacionIaDocumentoTipo analisisDocumentacionIaDocumentoTipo;
        private Integer numeroParte;
        private Integer cantidadTotalPartes;
    }
}
