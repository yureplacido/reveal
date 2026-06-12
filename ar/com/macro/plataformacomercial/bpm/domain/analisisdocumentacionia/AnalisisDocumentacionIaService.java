package ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia;

import ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia.enums.AnalisisDocumentacionIaDocumentoTipo;
import lombok.NonNull;

public interface AnalisisDocumentacionIaService {

    @NonNull
    AnalisisDocumentacionIaResultado consultarResultado(@NonNull String gestionId,
                                                        @NonNull AnalisisDocumentacionIaDocumentoTipo analisisDocumentacionIaDocumentoTipo);

    @NonNull
    AnalisisDocumentacionIaGestion generarGestion(@NonNull AnalisisDocumentacionIaGestion gestion);

    @NonNull
    AnalisisDocumentacionIaPublicacionDocumento publicarDocumento(@NonNull AnalisisDocumentacionIaPublicacionDocumento analisisDocumentacionIAPublicacionDocumento);
}
