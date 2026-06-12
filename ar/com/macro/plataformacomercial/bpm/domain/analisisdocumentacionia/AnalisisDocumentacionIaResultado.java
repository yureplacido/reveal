package ar.com.macro.plataformacomercial.bpm.domain.analisisdocumentacionia;

import java.time.LocalDate;
import java.util.List;
import lombok.Builder;
import lombok.Value;

@Value
@Builder(toBuilder = true)
public class AnalisisDocumentacionIaResultado {

    private DatosExtraidos datosExtraidos;
    private ValidacionResultado validacionResultado;

    @Value
    @Builder(toBuilder = true)
    public static class DatosExtraidos {

        private InscripcionIgj inscripcionIgj;
        private DatosEncuentro datosEncuentro;
        private Otorgante otorgante;
        private LegalizacionApostilla legalizacionApostilla;
        private DatosInscripcion datosInscripcion;

        private List<Apoderado> apoderado;
        private List<DatosPersonales> datosPersonales;

        @Value
        @Builder(toBuilder = true)
        public static class Apoderado {

            private String apellido;
            private String nombre;
            private String cuit;
            private String numeroDocumento;

        }

        @Value
        @Builder(toBuilder = true)
        public static class DatosEncuentro {

            private String entidad;
        }

        @Value
        @Builder(toBuilder = true)
        public static class DatosInscripcion {

            private String cuit;
        }

        @Value
        @Builder(toBuilder = true)
        public static class DatosPersonales {

            private String documentoPersonalNumero;
            private LocalDate fechaNacimiento;
            private LocalDate fechaVencimiento;

        }

        @Value
        @Builder(toBuilder = true)
        public static class InscripcionIgj {
            private String cuit;
        }

        @Value
        @Builder(toBuilder = true)
        public static class LegalizacionApostilla {

            private String numeroProtocolo;
            private Boolean sello;
        }

        @Value
        @Builder(toBuilder = true)
        public static class Otorgante {

            private String cuitSociedad;

        }

    }

    @Value
    @Builder(toBuilder = true)
    public static class ValidacionResultado {

        private Boolean valido;
        private List<Error> errores;

        @Value
        @Builder(toBuilder = true)
        public static class Error {

            private String codigo;
            private String mensaje;
        }
    }
}
