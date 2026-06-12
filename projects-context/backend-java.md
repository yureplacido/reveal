# Contexto do Projeto — backend-java

Gerado automaticamente em 2026-07-17 10:01:23

---

## Stack

| Tecnologia | Versao |
|------------|--------|
| Linguagem | Java |
| Build | gradle |

> Consulte o `AGENTS.md` do projeto para versoes exatas (Spring Boot, Java, etc.).

## Arquitetura

Package-by-Feature com padrao de modularizacao por funcionalidade.
Cada feature contem seus proprios controller, service, domain, repository.

> Consulte o `AGENTS.md` do projeto para detalhes arquiteturais especificos.

## Pacote Base

`ar.com.macro.plataformacomercial`

## Estrutura de Diretorios

```
java/
ar/
  com/
    macro/
      plataformacomercial/
        bpm/
          Application.java
          ApplicationConfiguration.java
```

## Padroes de Controllers

### Anotacoes de Classe

- `Deprecated(since = "1.27")`
- `RequestMapping("/api/altaAcuerdoCtaCte")`
- `RequestMapping("/api/altaComercio")`
- `RequestMapping("/api/desbordeOnboarding")`
- `RequestMapping("/api/desbordePrestamo")`
- `RequestMapping("/api/prestamoAgro")`
- `RequestMapping("/api/procesos")`
- `RequestMapping("/api/procesos/onboarding")`
- `RequestMapping("/api/v0/procesos/bandejas")`
- `RequestMapping("/api/v0/procesos/cliente-situacion")`
- `RequestMapping("/api/v0/procesos/fianza")`
- `RequestMapping("/api/v0/procesos/firma-tyc-omnicanal")`
- `RequestMapping("/api/v0/procesos/orquestador-comercial")`
- `RequestMapping("/api/v0/procesos/prestamo-amortizable")`
- `RequestMapping("/api/v0/procesos/prestamo-indirecto")`
- `RequestMapping("/api/v0/procesos/prestamo-oferta")`
- `RequestMapping("/api/v1/procesos/alta-de-comercio")`
- `RequestMapping("/api/v1/procesos/desborde-onboarding")`
- `RequestMapping("/api/v1/procesos/desborde-prestamo")`
- `RequestMapping("/api/webhooks/artax")`
- `RequestMapping(LogController.BASE_PATH)`
- `RequestMapping(ParametroNegocioController.BASE_PATH)`
- `RequiredArgsConstructor`
- `RestController`
- `Slf4j`
- `Tag(name = "Logs - V1", description = LogController.BASE_PATH)`
- `Tag(name = "Parametros Negocio - V1", description = ParametroNegocioController.BASE_PATH)`
- `Tag(name = "Procesos - Alta Acuerdo Cuenta Corriente - V0", description = "/api/altaAcuerdoCtaCte")`
- `Tag(name = "Procesos - Alta Comercio - V0", description = "/api/altaComercio")`
- `Tag(name = "Procesos - Alta Comercio - V1", description = "/api/v1/procesos/alta-de-comercio")`
- `Tag(name = "Procesos - Cliente Situacion - V0", description = "/api/v0/procesos/cliente-situacion")`
- `Tag(name = "Procesos - Desborde Onboarding - V0", description = "/api/desbordeOnboarding")`
- `Tag(name = "Procesos - Desborde Onboarding - V1", description = "/api/v1/procesos/desborde-onboarding")`
- `Tag(name = "Procesos - Desborde Prestamo - V0", description = "/api/desbordePrestamo")`
- `Tag(name = "Procesos - Desborde Prestamo - V1", description = "/api/v1/procesos/desborde-prestamo")`
- `Tag(name = "Procesos - Fianza Digital - V0", description = "/api/v0/procesos/fianza")`
- `Tag(name = "Procesos - Firma TYC Ominicanal - V0", description = "/api/v0/procesos/firma-tyc-omnicanal")`
- `Tag(name = "Procesos - Onboarding - V0", description = "/api/procesos/onboarding")`
- `Tag(name = "Procesos - Orquestador Comercial - V0", description = "/api/v0/procesos/orquestador-comercial")`
- `Tag(name = "Procesos - Prestamo Agro - V0", description = "/api/prestamoAgro")`
- `Tag(name = "Procesos - Prestamo Amortizable - V0", description = "/api/v0/procesos/prestamo-amortizable")`
- `Tag(name = "Procesos - Prestamo Indirecto - V0", description = "/api/v0/procesos/prestamo-indirecto")`
- `Tag(name = "Procesos - Prestamo Oferta - V0", description = "/api/v0/procesos/prestamo-oferta")`
- `Tag(name = "Procesos - V0", description = "/api/procesos")`
- `Tag(name = "Procesos Bandejas - V0", description = "/api/procesos/bandejas")`
- `Tag(name = "Webhooks Artax", description = "/api/webhooks/artax")`
- `Validated`

### Anotacoes de Metodo

- `@GetMapping`
- `@NonNull`
- `@Nullable`
- `@PatchMapping`
- `@PostMapping`
- `@PutMapping`
- `@ResponseStatus`

### Endpoints Encontrados

| Anotacao | Path |
|----------|------|
| @RequestMapping | /api/altaAcuerdoCtaCte |
| @RequestMapping | /api/altaComercio |
| @RequestMapping | /api/desbordeOnboarding |
| @RequestMapping | /api/desbordePrestamo |
| @RequestMapping | /api/prestamoAgro |
| @RequestMapping | /api/procesos |
| @RequestMapping | /api/procesos/onboarding |
| @RequestMapping | /api/v0/procesos/bandejas |
| @RequestMapping | /api/v0/procesos/cliente-situacion |
| @RequestMapping | /api/v0/procesos/fianza |
| @RequestMapping | /api/v0/procesos/firma-tyc-omnicanal |
| @RequestMapping | /api/v0/procesos/orquestador-comercial |
| @RequestMapping | /api/v0/procesos/prestamo-amortizable |
| @RequestMapping | /api/v0/procesos/prestamo-indirecto |
| @RequestMapping | /api/v0/procesos/prestamo-oferta |
| @RequestMapping | /api/v1/procesos/alta-de-comercio |
| @RequestMapping | /api/v1/procesos/desborde-onboarding |
| @RequestMapping | /api/v1/procesos/desborde-prestamo |
| @RequestMapping | /api/webhooks/artax |
| GetMapping | /condiciones |
| GetMapping | /condicionesAcuerdoCC/{canal}/{idProducto} |
| GetMapping | /condicionesProductos |
| GetMapping | /consultaDetalle |
| GetMapping | /consultaTycs/idSolicitud/{idSolicitud} |
| GetMapping | /documentacion/archivos/{idArchivo} |
| GetMapping | /estados-internos |
| GetMapping | /estados-operativos |
| GetMapping | /lineasAcuerdo |
| GetMapping | /metricas |
| GetMapping | /operaciones |
| GetMapping | /tipos |
| GetMapping | /tycs |
| GetMapping | /{idSolicitud} |
| GetMapping | /{idSolicitud}/cancelacion |
| GetMapping | /{idSolicitud}/dictamen/archivo |
| GetMapping | /{idSolicitud}/documentacion |
| GetMapping | /{idSolicitud}/documentacion/archivos |
| GetMapping | /{idSolicitud}/firma |
| GetMapping | /{idSolicitud}/liquidaciones/prestamos-amortizables/{idLiquidacionPrestamoAmortizable} |
| GetMapping | /{idSolicitud}/simulaciones/prestamos-amortizables/{idSolicitudPrestamoAmortizable} |
| GetMapping | /{idSolicitud}/tyc/{idTyc} |
| GetMapping | /{idSolicitud}/tycs |
| GetMapping | /{idSolicitud}/tycs/{idTyc} |
| GetMapping | /{nombre} |
| PatchMapping | /{idSolicitud} |
| PatchMapping | /{idSolicitud}/tycs/{idTyc} |
| PostMapping | /activos/exportacion/datalake |
| PostMapping | /actualizarEstadoLead |
| PostMapping | /autorizar |
| PostMapping | /cancelacion |
| PostMapping | /confirmarToken |
| PostMapping | /exportacion |
| PostMapping | /finalizados/exportacion/datalake |
| PostMapping | /firmaRealizada |
| PostMapping | /generarAltaCobis |
| PostMapping | /generarToken |
| PostMapping | /iniciar |
| PostMapping | /integrantes |
| PostMapping | /simular |
| PostMapping | /tycs |
| PostMapping | /{idSolicitud}/cancelacion |
| PostMapping | /{idSolicitud}/cliente |
| PostMapping | /{idSolicitud}/dictamen |
| PostMapping | /{idSolicitud}/documento/{idDocumento} |
| PostMapping | /{idSolicitud}/integrantes/biometrias |
| PostMapping | /{idSolicitud}/liquidaciones |
| PostMapping | /{idSolicitud}/simulaciones |
| PostMapping | /{idSolicitud}/tycs/firmas |
| PostMapping | /{idSolicitud}/tycs/{idTyc}/firmas |
| PostMapping | resultado-lectura-documentos-ia |
| PutMapping | /{idSolicitud}/cancelacion |
| PutMapping | /{idSolicitud}/documento/{idDocumento}/archivos/{idArchivo} |
| PutMapping | /{idSolicitud}/firma |
| PutMapping | /{idSolicitud}/lead |
| PutMapping | /{idSolicitud}/tycs/{idTyc} |
| PutMapping | /{nombre} |
| RequestMapping | /api/altaAcuerdoCtaCte |
| RequestMapping | /api/altaComercio |
| RequestMapping | /api/desbordeOnboarding |
| RequestMapping | /api/desbordePrestamo |
| RequestMapping | /api/prestamoAgro |
| RequestMapping | /api/procesos |
| RequestMapping | /api/procesos/onboarding |
| RequestMapping | /api/v0/procesos/bandejas |
| RequestMapping | /api/v0/procesos/cliente-situacion |
| RequestMapping | /api/v0/procesos/fianza |
| RequestMapping | /api/v0/procesos/firma-tyc-omnicanal |
| RequestMapping | /api/v0/procesos/orquestador-comercial |
| RequestMapping | /api/v0/procesos/prestamo-amortizable |
| RequestMapping | /api/v0/procesos/prestamo-indirecto |
| RequestMapping | /api/v0/procesos/prestamo-oferta |
| RequestMapping | /api/v1/procesos/alta-de-comercio |
| RequestMapping | /api/v1/procesos/desborde-onboarding |
| RequestMapping | /api/v1/procesos/desborde-prestamo |
| RequestMapping | /api/webhooks/artax |

### Exemplos

- `ar.com.macro.plataformacomercial.bpm.api.proceso.ProcesoController`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/api/proceso/ProcesoController.java`
- `ar.com.macro.plataformacomercial.bpm.api.proceso.acom.v0.AltaComercioController`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/api/proceso/acom/v0/AltaComercioController.java`
- `ar.com.macro.plataformacomercial.bpm.api.proceso.acom.v1.AltaComercioControllerV1`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/api/proceso/acom/v1/AltaComercioControllerV1.java`
- `ar.com.macro.plataformacomercial.bpm.api.proceso.prestamo.indirecto.PrestamoIndirectoController`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/api/proceso/prestamo/indirecto/PrestamoIndirectoController.java`
- `ar.com.macro.plataformacomercial.bpm.api.proceso.prestamo.oferta.PrestamoOfertaController`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/api/proceso/prestamo/oferta/PrestamoOfertaController.java`

## Padroes de Services

### Anotacoes

- `Component`
- `Component("ACCCalcularTasas")`
- `Component("ACCClientesConsultaDetalleCuentasCorriente")`
- `Component("ACCClientesConsultaGeneral")`
- `Component("ACCConsolidaValidaciones")`
- `Component("ACCConsultaAcopiador")`
- `Component("ACCConsultaCalculoDisponible")`
- `Component("ACCConsultaDiaHabil")`
- `Component("ACCConsultaLineaCredito")`
- `Component("ACCConsultaTycs")`
- `Component("ACCDeletarTyc")`
- `Component("ACCDenegarCancelacion")`
- `Component("ACCIntegracionDocumento")`
- `Component("ACCParametrosCondiciones")`
- `Component("ACCPasivasConsultaDetalleCuenta")`
- `Component("ACCPasivasGeneraAcuerdo")`
- `Component("ACCPreparaValidaciones")`
- `Component("ACCRecibirTycFirmado")`
- `Component("ACCRegistrarYFirmarTyc")`
- `Component("ACCSituacionEndeudamientoCC")`
- `Component("ACCVerificarDisponible")`
- `Component("AComClientesConsultaCuentasV2")`
- `Component("AComConsultaEstadoSolicitudEnSmo")`
- `Component("AComEnriquecerFirmanteV2")`
- `Component("AComEnriquecerTitularResponsableV2")`
- `Component("AComPasivasConsultaDetalleCuentaV2")`
- `Component("AComTarjetasGeneraComercioV2")`
- `Component("AComVerificarFirmanteV2")`
- `Component("CreacionLeadDelegate")`
- `Component("DEPRECATED-CalculoCft")`
- `Component("DEPRECATED-CalculoTea")`
- `Component("DEPRECATED-CalculoTir")`
- `Component("DEPRECATED-CalculoVpl")`
- `Component("DEPRECATED-FuncionLimite")`
- `Component("FianzaCancelacionFirmaTyc")`
- `Component("FianzaConsolidarValidacion")`
- `Component("FianzaConsolidarValidacionEndeudamiento")`
- `Component("FianzaConsultaCalificacionCliente")`
- `Component("FianzaConsultaEndeudamientoCliente")`
- `Component("FianzaConsultaGeneralClienteFiador")`
- `Component("FianzaConsultaMailClienteAfianzado")`
- `Component("FianzaConsultaSucursal")`
- `Component("FianzaConsultaTycProcesoCliente")`
- `Component("FianzaDeterminacionResultadoFirmasTyc")`
- `Component("FianzaEnriquecerDatosTycDinamico")`
- `Component("FianzaFormatearClienteNombreLargo")`
- `Component("FianzaGeneracionTycsDinamicos")`
- `Component("FianzaGenerarPrestamoGarantia")`
- `Component("FianzaIniciarFirmaTyc")`
- `Component("FianzaMailCancelacion")`
- `Component("FianzaMailCancelacionSolicitud")`
- `Component("FianzaNotificacionClienteFianzaDisponible")`
- `Component("FianzaNotificarFiadoresNecesidadFirma")`
- `Component("FianzaReintento")`
- `Component("FianzaSolicitarResguardoTyc")`
- `Component("FianzaValidacionFiadoresInformados")`
- `Component("FianzaValidarDatosProductos")`
- `Component("FirmaTycBorrarArchivosTemporales")`
- `Component("FirmaTycBuscarRequisitosDocumentos")`
- `Component("FirmaTycBusquedaFacultades")`
- `Component("FirmaTycBusquedaTycs")`
- `Component("FirmaTycCompletarDatosFirmantes")`
- `Component("FirmaTycEnriquecerDatosDelCliente")`
- `Component("FirmaTycGeneraTycsEstaticos")`
- `Component("FirmaTycGenerarTycDinamico")`
- `Component("FirmaTycIntegracionApidoc")`
- `Component("FirmaTycIntegracionApidocClienteSolicitante")`
- `Component("FirmaTycMailNecesidadDeFirma")`
- `Component("FirmaTycMailTycsAceptados")`
- `Component("FirmaTycMailTycsRechazados")`
- `Component("FirmaTycPublicarCancelacionFirma")`
- `Component("FirmaTycPublicarFinalizacionFirma")`
- `Component("FirmaTycValidacionDatosComplementarios")`
- `Component("OnbAgregarTitularIntegrantes")`
- `Component("OnbAsignarValorValido")`
- `Component("OnbAutorizaSolicitudCalificacion")`
- `Component("OnbBorrarArchivosTemporales")`
- `Component("OnbBorrarDatosAnalisisDocumentacionIa")`
- `Component("OnbBuscaDocumentacionRequerida")`
- `Component("OnbBuscaDocumentacionRequeridaV2")`
- `Component("OnbBuscarPaqueteCliente")`
- `Component("OnbCalificacionConsultaDetalle")`
- `Component("OnbConsolidacionErrorTecnicoFiltrosIniciales")`
- `Component("OnbConsolidarDatosAnalisisDocumentacionIa")`
- `Component("OnbConsolidarRestricciones")`
- `Component("OnbConsultaConsolidadoLegales")`
- `Component("OnbConsultaCuentaCreada")`
- `Component("OnbConsultaEmailOficialDelCliente")`
- `Component("OnbConsultaListaDeCuentasCreadas")`
- `Component("OnbConsultaTycs")`
- `Component("OnbConsultarCondicionImpositivaDelProspecto")`
- `Component("OnbConsultarResultadoAnalisisDocumentacionIa")`
- `Component("OnbConsultarSituacionDictamen")`
- `Component("OnbConsultarSituacionGestionLegales")`
- `Component("OnbConsultarSituacionIntegrantes")`
- `Component("OnbDesbordarCrmDocumentacionaNoValida")`
- `Component("OnbDesbordeOnboarding")`
- `Component("OnbDeterminarActividadCliente")`
- `Component("OnbDeterminarAnalisisIaHabilitado")`
- `Component("OnbDeterminarCantidadIntentosConsultaDictamen")`
- `Component("OnbDeterminarCodigoCiudadYProvinciaBancoMacro")`
- `Component("OnbDeterminarConsolidadoFacultadesAperturaCuenta")`
- `Component("OnbDeterminarConsolidadoFacultadesFirmaCuenta")`
- `Component("OnbDeterminarEstadoTycPersonaFisica")`
- `Component("OnbDeterminarEstadoTycPersonaJuridica")`
- `Component("OnbDeterminarFirmantesAperturaCuenta")`
- `Component("OnbDeterminarTipoDeEnvioDeResumen")`
- `Component("OnbDeterminarUsoFirma")`
- `Component("OnbDeterminarValores")`
- `Component("OnbEnriquecerDatosAnalisisIaListaDocumentacion")`
- `Component("OnbEnriquecerDatosLegalesListaDocumentacion")`
- `Component("OnbEnriquecerDatosListaDocumentacion")`
- `Component("OnbEnviaEmailToken")`
- `Component("OnbGeneraAltaHomeBanking")`
- `Component("OnbGeneraAltaSolicitudBuzonDictamenDevuelto")`
- `Component("OnbGenerarAltaClientePersonaFisica")`
- `Component("OnbGenerarAltaClientePersonaFisicaV2")`
- `Component("OnbGenerarAltaClientePersonaJuridica")`
- `Component("OnbGenerarAltaClientePersonaJuridicaV2")`
- `Component("OnbGenerarAltaIntegrantes")`
- `Component("OnbGenerarAltaIntegrantesV2")`
- `Component("OnbGenerarAltaPaquete")`
- `Component("OnbGenerarGestionAnalisisDocumentacionIa")`
- `Component("OnbGenerarGestionLegales")`
- `Component("OnbGenerarSolicitudCalificacion")`
- `Component("OnbGenerarTycs")`
- `Component("OnbInformarOficialCancelacionPorInconsistencia")`
- `Component("OnbInformarProspectoCancelacionPorInconsitencia")`
- `Component("OnbInformarProspectoConFirmaConjuntaAltaProductos")`
- `Component("OnbInformarProspectoConFirmaConjuntaDocumentacionAprobada")`
- `Component("OnbInformarProspectoDocumentacionNoValida")`
- `Component("OnbInformarProspectoDocumentacionRechazada")`
- `Component("OnbIntegracionDocumento")`
- `Component("OnbMailAvisoAperturaCuenta")`
- `Component("OnbMailAvisoAperturaCuentaConSeleccionProductos")`
- `Component("OnbMailAvisoBienvenida")`
- `Component("OnbMailAvisoBiometriaIntegrantes")`
- `Component("OnbMailAvisoDictamenDesfavorable")`
- `Component("OnbMailAvisoDictamenDevuelto")`
- `Component("OnbMailAvisoDocumentacionEnValidacion")`
- `Component("OnbMailAvisoDocumentacionRechazada")`
- `Component("OnbMailAvisoFallaAltaCobis")`
- `Component("OnbMailAvisoOficialDictamenDevuelto")`
- `Component("OnbMailAvisoRecordatorioDictaminarEstatuto")`
- `Component("OnbMailRecordatorioFalloAltaPaquete")`
- `Component("OnbMailRecordatorioSolicitudValidarRoles")`
- `Component("OnbMailRecordatorioSolicitudVerificarDocumentacion")`
- `Component("OnbMailRecordatorioSolicitudVerificarDocumentacionLSPlus")`
- `Component("OnbModificaVariablesDelScopeDictamenDevuelto")`
- `Component("OnbNotificarOficialAguardandoBiometriaCliente")`
- `Component("OnbNotificarOficialAltaExitosa")`
- `Component("OnbNotificarPendenciaSubidaDocumentacion")`
- `Component("OnbPublicarDocumentacionAnalisisIa")`
- `Component("OnbPublicarDocumentacionGestionLegales")`
- `Component("OnbReintento")`
- `Component("OnbReintentoConsultaGestionLegales")`
- `Component("OnbReintentoPorCantidadIntentos")`
- `Component("OnbValidaDatosCliente")`
- `Component("OnbValidaDireccion")`
- `Component("OnbValidaDuracionToken")`
- `Component("OnbValidaEstadoDelEnvioToken")`
- `Component("OnbValidaIntegrantes")`
- `Component("OnbValidaTelefonoContacto")`
- `Component("OnbValidaToken")`
- `Component("OnbValidacionConsistenciaOficial")`
- `Component("OnbValidacionPorcentajeAccionarioIntegrantes")`
- `Component("OnbValidarTodosDocumentosRecebidosAnalisadosIa")`
- `Component("OnbValidarYEnriquecerGruposIntegrantes")`
- `Component("OnbVerificaSolicitudDuplicada")`
- `Component("OrquestadorComercialConsultaClienteSituacion")`
- `Component("OrquestadorComercialConsultaProveedorSituacion")`
- `Component("OrquestadorComercialIniciarPrestamoOfertaDelegate")`
- `Component("OrquestadorComercialLiquidacionInicializacionPrestamoIndirecto")`
- `Component("OrquestadorComercialNoficarClienteLiquidacion")`
- `Component("OrquestadorComercialNoficarProveedorLiquidacion")`
- `Component("OrquestadorComercialReintento")`
- `Component("OrquestadorComercialSimulacionInicializacionPrestamoIndirecto")`
- `Component("OrquestadorComercialValidacionLiquidacionesPrestamosAmortizables")`
- `Component("OrquestadorComercialValidacionSimulacionesPrestamosAmortizables")`
- `Component("OrquestadorComercialValidarDetallePrestamoOferta")`
- `Component("OrquestadorComercialValidarSegmentacionCliente")`
- `Component("PersonalizacionTarea")`
- `Component("PresAgroAcreditacionAutomaticaFondos")`
- `Component("PresAgroAltaDefinitiva")`
- `Component("PresAgroAltaTemporal")`
- `Component("PresAgroBloqueoDeFondos")`
- `Component("PresAgroBorrarTycs")`
- `Component("PresAgroCalcularMontoPesificadoSinDescuentos")`
- `Component("PresAgroConsolidaValidaciones")`
- `Component("PresAgroConsultaClientes")`
- `Component("PresAgroConsultaCuentas")`
- `Component("PresAgroConsultaSucursal")`
- `Component("PresAgroConsultaTycsCliente")`
- `Component("PresAgroEnviaEmailAcreditacionMontoConvertido")`
- `Component("PresAgroEnviaEmailBandejaDeBloqueo")`
- `Component("PresAgroEnviaEmailConversionMoneda")`
- `Component("PresAgroEnviaEmailErrorAltaDefinitiva")`
- `Component("PresAgroEnviaEmailErrorDeBloqueo")`
- `Component("PresAgroEnvioDocumentosCalificacionCrediticia")`
- `Component("PresAgroGenerarTycs")`
- `Component("PresAgroTransferirFondosInsumera")`
- `Component("PrestamoAmortizableGeneraAltaDefinitiva")`
- `Component("PrestamoAmortizableGeneraAltaTemporal")`
- `Component("PrestamoAmortizableIndirectoConsultaEstadoCuentaCliente")`
- `Component("PrestamoAmortizableIndirectoEnriquecerDatosClienteTyc")`
- `Component("PrestamoAmortizableIndirectoIniciaFirmaTyc")`
- `Component("PrestamoAmortizableNotificacionAreaCentralizadaFalloAltaDefinitiva")`
- `Component("PrestamoAmortizablePublicacionCambioEstado")`
- `Component("PrestamoAmortizableSimulacionGeneraAltaTemporal")`
- `Component("PrestamoAmortizableSimulacionPrestamo")`
- `Component("PrestamoIndirectoBloqueoFondos")`
- `Component("PrestamoIndirectoCancelacionFirmaTyc")`
- `Component("PrestamoIndirectoConsultaCalificacionEndeudamientoCliente")`
- `Component("PrestamoIndirectoConsultaEstadoCuentaProveedor")`
- `Component("PrestamoIndirectoConsultaPrestamoAmortizableAltaDefinitiva")`
- `Component("PrestamoIndirectoConsultaPrestamoAmortizableAltaTemporal")`
- `Component("PrestamoIndirectoConsultaSituacionEndeudamientoCliente")`
- `Component("PrestamoIndirectoConsultaSucursal")`
- `Component("PrestamoIndirectoEnriquecerDatosProveedor")`
- `Component("PrestamoIndirectoEnriquecerDatosTycDinamico")`
- `Component("PrestamoIndirectoEnriquecimientoDatosTransferenciaCausales")`
- `Component("PrestamoIndirectoGeneracionTransferenciaProveedor")`
- `Component("PrestamoIndirectoGenerarTycsDinamicos")`
- `Component("PrestamoIndirectoIniciarPrestamoAmortizable")`
- `Component("PrestamoIndirectoNotificacionAreaCentralizadaBloqueoDeFondos")`
- `Component("PrestamoIndirectoNotificacionAreaCentralizadaBloqueoDeFondosConError")`
- `Component("PrestamoIndirectoNotificacionAreaCentralizadaEstadoPrestamo")`
- `Component("PrestamoIndirectoPublicacionCambioEstado")`
- `Component("PrestamoIndirectoReintento")`
- `Component("PrestamoIndirectoSolicitacionDescarteResguardoFirmaTyc")`
- `Component("PrestamoIndirectoSolicitacionLiquidacion")`
- `Component("PrestamoIndirectoSolicitarResguardoTyc")`
- `Component("PrestamoIndirectoValidacionCuentasClienteYProveedor")`
- `Component("PrestamoIndirectoValidacionResultadoDisponiblesRiesgo")`
- `Component("PrestamoOfertaCalificacionCalculaMontoDisponible")`
- `Component("PrestamoOfertaConsultaDetalleCalificacionRiesgo")`
- `Component("PrestamoOfertaConsultaEndeudamientoCliente")`
- `Component("PrestamoOfertaConsultarParametrosPrestamos")`
- `Component("PrestamoOfertaGeneraCalificacionCreditoSimple")`
- `Component("PrestamoOfertaManejoTopesMonto")`
- `Component("PrestamoOfertaPublicacionCambioEstado")`
- `Component("SpvcConsultaCliente")`
- `Component("SpvcConsultaConstanciaInscripcionAFIP")`
- `Component("SpvcConsultaCuentasActivas")`
- `Component("SpvcConsultaInformacionCrediticia")`
- `Component("SpvcConsultaNormalizacionIndividuos")`
- `Component("SpvcConsultaRefereciasExternas")`
- `Component("SpvcConsultaReferenciasNormativas")`
- `Component("SpvcDeterminarAfipAmbientesBajos")`
- `Component("SpvcManejaVariablesAFIP")`
- `Component("ValidacionEstadoInterno")`
- `Deprecated`
- `Deprecated(forRemoval = true)`
- `Deprecated(forRemoval = true, since = "1.80")`
- `Deprecated(forRemoval = true, since = "1.81")`
- `Deprecated(since = "1.32", forRemoval = true)`
- `Deprecated(since = "1.33", forRemoval = true)`
- `Deprecated(since = "1.54")`
- `Deprecated(since = "1.55")`
- `Deprecated(since = "1.78", forRemoval = true)`
- `Deprecated(since="1.44", forRemoval=true)`
- `EnableConfigurationProperties(FeatureToggleProperties.class)`
- `EnableConfigurationProperties(IncidentProperties.class)`
- `EnableSchedulerLock(defaultLockAtMostFor = "PT30M")`
- `EnableScheduling`
- `Qualifier("ACCPreparaValidaciones")`
- `RequiredArgsConstructor`
- `Service`
- `Slf4j`

### Exemplos

- `ar.com.macro.plataformacomercial.bpm.msg.in.webhook.macrosoluciones.MacroSolucionesFinalizacionFirmaTycListener`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/webhook/macrosoluciones/MacroSolucionesFinalizacionFirmaTycListener.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.prestamo.amortizable.PrestamoAmortizableConsultaDetalleListenerConverter`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/prestamo/amortizable/PrestamoAmortizableConsultaDetalleListenerConverter.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.prestamo.amortizable.PrestamoAmortizableConsultaDetalleListener`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/prestamo/amortizable/PrestamoAmortizableConsultaDetalleListener.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.cancelacion.PrestamoIndirectoCancelacionFirmaListener`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/cancelacion/PrestamoIndirectoCancelacionFirmaListener.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.finalizacion.PrestamoIndirectoFinalizacionFirmaListener`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/finalizacion/PrestamoIndirectoFinalizacionFirmaListener.java`

## Padroes de Entities

### Anotacoes

- `AllArgsConstructor`
- `Builder`
- `Data`
- `Entity`
- `FieldNameConstants`
- `NoArgsConstructor`
- `Table(schema = "fianza", name = "datos_productos")`
- `Table(schema = "fianza", name = "mapeo_datos_tycs")`
- `Table(schema = "fianza", name = "tyc_proceso")`
- `Table(schema = "firmatyc", name = "archivos")`
- `Table(schema = "logging_schema", name = "archivo_temporal")`
- `Table(schema = "logging_schema", name = "feriados")`
- `Table(schema = "logging_schema", name = "localidad")`
- `Table(schema = "logging_schema", name = "logging")`
- `Table(schema = "paquete_schema", name = "paquetes")`
- `Table(schema = "procesos", name = "alta_acuerdo_cta_cte")`
- `Table(schema = "procesos", name = "alta_comercio")`
- `Table(schema = "procesos", name = "bandejas")`
- `Table(schema = "procesos", name = "cliente_situacion")`
- `Table(schema = "procesos", name = "desborde_onboarding")`
- `Table(schema = "procesos", name = "desborde_prestamo")`
- `Table(schema = "procesos", name = "fianza")`
- `Table(schema = "procesos", name = "firma_tyc")`
- `Table(schema = "procesos", name = "onboarding")`
- `Table(schema = "procesos", name = "orquestador_comercial")`
- `Table(schema = "procesos", name = "prestamo_agro")`
- `Table(schema = "procesos", name = "prestamo_amortizable")`
- `Table(schema = "procesos", name = "prestamo_amortizable_indirecto")`
- `Table(schema = "procesos", name = "prestamo_oferta")`
- `Table(schema = "procesos", name = "validacion_cliente")`
- `Table(schema = "rubro_schema", name = "condiciones")`
- `Table(schema = "rubro_schema", name = "rubro_interno")`
- `Table(schema = "rubro_schema", name = "rubro_marca")`
- `Table(schema = "rubro_schema", name = "rubro_ramo")`

### Exemplos

- `ar.com.macro.plataformacomercial.bpm.data.proceso.acom.AltaComercioJpaEntity`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/data/proceso/acom/AltaComercioJpaEntity.java`
- `ar.com.macro.plataformacomercial.bpm.data.proceso.spvc.ValidacionClienteJpaEntity`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/data/proceso/spvc/ValidacionClienteJpaEntity.java`
- `ar.com.macro.plataformacomercial.bpm.data.proceso.prestamo.indirecto.PrestamoAmortizableIndirectoJpaEntity`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/data/proceso/prestamo/indirecto/PrestamoAmortizableIndirectoJpaEntity.java`

## Padroes de DTOs

### Anotacoes

- `AllArgsConstructor`
- `Builder`
- `Builder(toBuilder = true)`
- `Data`
- `Deprecated(since = "1.27")`
- `FieldNameConstants`
- `Getter`
- `Jacksonized`
- `JsonInclude(JsonInclude.Include.NON_EMPTY)`
- `NoArgsConstructor`
- `NoArgsConstructor(access = AccessLevel.PACKAGE)`
- `ProcessDefinition(code = "ACC", key = "AltaAcuerdoCtaCte", name = "Alta Acuerdo Cuenta Corriente")`
- `ProcessDefinition(code = "ACOM", key = "AltaComercioV3", name = "Alta de Comercio")`
- `ProcessDefinition(code = "ACOM", key = "AltaDeComercio", name = "Alta de Comercio")`
- `ProcessDefinition(code = "CLIENTESIT", key = "cliente-situacion", name = "Cliente Situacion")`
- `ProcessDefinition(code = "DESONB", key = "DesbordeOnboarding", name = "Desborde Onboarding")`
- `ProcessDefinition(code = "DESPRE", key = "DesbordePrestamo", name = "Desborde de Prestamo")`
- `ProcessDefinition(code = "FIANZA", key = "fianza", name = "fianza")`
- `ProcessDefinition(code = "FIRMATYC", key = "FirmaTycOmnicanal", name = "Firma Tyc Omnicanal")`
- `ProcessDefinition(code = "ONB", key = "Onboarding", name = "Onboarding")`
- `ProcessDefinition(code = "ORQUECOM", key = "orquestador-comercial", name = "Orquestador Comercial")`
- `ProcessDefinition(code = "PRESAGRO", key = "PrestamoAgro", name = "PrestamoAgro")`
- `ProcessDefinition(code = "PRESAMORT", key = "prestamo-amortizable", name = "Resultado Amortizable")`
- `ProcessDefinition(code = "PRESAMORTIND", key = "prestamo-indirecto", name = "Prestamo Amortizable Indirecto")`
- `ProcessDefinition(code = "PRESOFERTA", key = "prestamo-oferta", name = "Prestamo Oferta")`
- `ProcessDefinition(code = "SPVC", key = "ValidacionCliente", name = "ValidacionCliente")`
- `SharedDataTransferObject`
- `Slf4j`
- `Value`
- `With`

### Exemplos

- `ar.com.macro.plataformacomercial.bpm.msg.in.webhook.macrosoluciones.MacroSolucionesFinalizacionFirmaTycListenerDto`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/webhook/macrosoluciones/MacroSolucionesFinalizacionFirmaTycListenerDto.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.prestamo.amortizable.PrestamoAmortizableConsultaDetalleListenerDto`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/prestamo/amortizable/PrestamoAmortizableConsultaDetalleListenerDto.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.cancelacion.PrestamoIndirectoCancelacionFirmaListenerDto`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/cancelacion/PrestamoIndirectoCancelacionFirmaListenerDto.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.prestamo.indirecto.finalizacion.PrestamoIndirectoFinalizacionFirmaListenerDto`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/prestamo/indirecto/finalizacion/PrestamoIndirectoFinalizacionFirmaListenerDto.java`
- `ar.com.macro.plataformacomercial.bpm.msg.in.firmatyc.rojosoft.RojosoftFinalizacionFirmaTycListenerDto`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/msg/in/firmatyc/rojosoft/RojosoftFinalizacionFirmaTycListenerDto.java`

## Padroes de Repositories

### Anotacoes

- `Deprecated(forRemoval = true, since = "1.81")`
- `Repository`
- `RequiredArgsConstructor`

### Exemplos

- `ar.com.macro.plataformacomercial.bpm.data.proceso.ProcesoRepository`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/data/proceso/ProcesoRepository.java`
- `ar.com.macro.plataformacomercial.bpm.data.proceso.acom.AltaComercioRepository`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/data/proceso/acom/AltaComercioRepository.java`
- `ar.com.macro.plataformacomercial.bpm.data.proceso.acom.AltaComercioRepositoryV3`  — `src/main/java/ar/com/macro/plataformacomercial/bpm/data/proceso/acom/AltaComercioRepositoryV3.java`

## Pacotes Encontrados

```
Total de classes analisadas: ~14 pacotes
- ar.com.macro.plataformacomercial.bpm
```

---

*Contexto gerado em 2026-07-17 10:01:23*
*Regenerar com: `./generate-project-context.sh {name}`*