package ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia;

import lombok.Builder;
import lombok.Value;
import lombok.With;

import ar.com.macro.plataformacomercial.bpm.domain.documento.Documento;
import ar.com.macro.plataformacomercial.bpm.domain.documento.DocumentoTipo;

@With
@Value
@Builder(toBuilder = true)
public class AnalisisDocumentacionIaGestion {

    // REQUISICION

    private String contactoTelefono;
    private String email;
    private String idSolicitud;
    private String razonSocial;
    private String urlRetornoResultadoGestion;

    private Documento<DocumentoTipo.Tributario> documentoTributario;

    // RESPUESTA

    private String gestionId;

}
