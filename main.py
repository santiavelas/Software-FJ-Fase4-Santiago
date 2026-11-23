"""Punto de entrada: demuestra 23 operaciones y el manejo de errores."""

from datetime import datetime

from software_fj import (
    Cliente,
    ErrorSistemaFJ,
    ServicioAsesoria,
    ServicioEquipo,
    ServicioSala,
    SistemaFJ,
)
from software_fj.logging_config import ARCHIVO_LOG, RAIZ_PROYECTO, logger


def ejecutar_operacion(numero, descripcion, accion, resultados):
    """Ejecuta una operacion aislada y permite continuar ante un error."""
    print(f"\nOPERACION {numero}: {descripcion}")
    try:
        resultado = accion()
    except ErrorSistemaFJ as error:
        # Los errores esperados se muestran y se almacenan en el log.
        resultados["fallidas"] += 1
        logger.error("Operacion %s fallida: %s", numero, error, exc_info=True)
        print(f"[ERROR CONTROLADO] {error}")
    except Exception as error:
        # Este bloque protege la demostracion ante errores no previstos.
        resultados["fallidas"] += 1
        logger.exception("Error inesperado en la operacion %s.", numero)
        print(f"[ERROR INESPERADO] {error}")
    else:
        # Solo se ejecuta cuando la accion termina sin levantar excepciones.
        resultados["exitosas"] += 1
        logger.info("Operacion %s completada correctamente.", numero)
        print(f"[OK] {resultado}" if resultado is not None else "[OK] Completada.")
    finally:
        # El contador y el mensaje se actualizan incluso cuando hubo un fallo.
        resultados["total"] += 1
        print("Fin de la operacion.")


def ejecutar_demostracion():
    """Construye datos de prueba y simula flujos validos e invalidos."""
    sistema = SistemaFJ()
    resultados = {"total": 0, "exitosas": 0, "fallidas": 0}

    print("=" * 76)
    print("SOFTWARE FJ | GESTION DE CLIENTES, SERVICIOS Y RESERVAS")
    print("Componente practico: POO y manejo avanzado de excepciones")
    print("Ejecucion:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("Tarifas ilustrativas para pruebas academicas; no son precios oficiales.")
    print("=" * 76)

    ejecutar_operacion(1, "Registrar cliente con datos correctos", lambda: sistema.registrar_cliente(
        Cliente("CLI-001", "Laura Gomez", "laura@example.com", "3001234567")
    ).describir(), resultados)

    ejecutar_operacion(2, "Rechazar correo electronico con formato incorrecto", lambda: sistema.registrar_cliente(
        Cliente("CLI-002", "Carlos Ruiz", "correo-invalido", "3019876543")
    ), resultados)

    ejecutar_operacion(3, "Registrar segundo cliente con correo valido", lambda: sistema.registrar_cliente(
        Cliente("CLI-002", "Carlos Ruiz", "carlos@example.com", "3019876543")
    ).describir(), resultados)

    ejecutar_operacion(4, "Detectar identificador de cliente duplicado", lambda: sistema.registrar_cliente(
        Cliente("CLI-001", "Laura Gomez Dos", "laura2@example.com", "3021112233")
    ), resultados)

    ejecutar_operacion(5, "Registrar servicio de alquiler de sala", lambda: sistema.registrar_servicio(
        ServicioSala("SAL-001", 80000, 12)
    ).describir(), resultados)

    ejecutar_operacion(6, "Registrar servicio de alquiler de proyectores", lambda: sistema.registrar_servicio(
        ServicioEquipo("EQ-001", "Proyector", 25000, 2)
    ).describir(), resultados)

    ejecutar_operacion(7, "Registrar servicio de asesoria especializada", lambda: sistema.registrar_servicio(
        ServicioAsesoria("ASE-001", "desarrollo de software", 120000)
    ).describir(), resultados)

    ejecutar_operacion(8, "Rechazar servicio con tarifa no numerica", lambda: sistema.registrar_servicio(
        ServicioSala("SAL-ERR", "tarifa", 10)
    ), resultados)

    ejecutar_operacion(9, "Crear reserva valida de sala", lambda: sistema.crear_reserva(
        "RES-001", "CLI-001", "SAL-001", 2, {"personas": 5}
    ).describir(), resultados)

    ejecutar_operacion(10, "Confirmar reserva de sala", lambda: sistema.confirmar_reserva("RES-001").value, resultados)

    ejecutar_operacion(11, "Calcular total con impuesto y descuento", lambda: (
        f"Total RES-001: ${sistema.buscar_reserva('RES-001').calcular_total(0.19, 0.10):,.2f}"
    ), resultados)

    ejecutar_operacion(12, "Procesar reserva confirmada", lambda: (
        f"Total procesado: ${sistema.procesar_reserva('RES-001', 0.19, 0.10):,.2f}"
    ), resultados)

    ejecutar_operacion(13, "Impedir segundo procesamiento de la misma reserva", lambda: sistema.procesar_reserva("RES-001"), resultados)

    ejecutar_operacion(14, "Rechazar reserva de equipos superior al inventario", lambda: sistema.crear_reserva(
        "RES-002", "CLI-002", "EQ-001", 3, {"cantidad": 5}
    ), resultados)

    ejecutar_operacion(15, "Crear reserva de un proyector disponible", lambda: sistema.crear_reserva(
        "RES-003", "CLI-002", "EQ-001", 4, {"cantidad": 1}
    ).describir(), resultados)

    ejecutar_operacion(16, "Confirmar reserva de proyector y descontar inventario", lambda: sistema.confirmar_reserva("RES-003").value, resultados)

    ejecutar_operacion(17, "Cancelar reserva y devolver unidad al inventario", lambda: sistema.cancelar_reserva("RES-003").value, resultados)

    ejecutar_operacion(18, "Crear reserva de asesoria especializada", lambda: sistema.crear_reserva(
        "RES-004", "CLI-001", "ASE-001", 1.5,
        {"tema": "revision de arquitectura de software"}
    ).describir(), resultados)

    ejecutar_operacion(19, "Confirmar reserva de asesoria", lambda: sistema.confirmar_reserva("RES-004").value, resultados)

    ejecutar_operacion(20, "Procesar asesoria con impuesto y descuento", lambda: (
        f"Total de asesoria: ${sistema.procesar_reserva('RES-004', 0.19, 0.05):,.2f}"
    ), resultados)

    # Se inhabilita el servicio para demostrar una confirmacion no permitida.
    sala = sistema.buscar_servicio("SAL-001")
    sala.cambiar_disponibilidad(False)
    reserva_temporal = sistema.crear_reserva(
        "RES-005", "CLI-002", "SAL-001", 1, {"personas": 3}
    )
    ejecutar_operacion(21, "Impedir confirmacion de un servicio inhabilitado", lambda: reserva_temporal.confirmar(), resultados)
    sala.cambiar_disponibilidad(True)

    ejecutar_operacion(22, "Rechazar reserva con cliente inexistente", lambda: sistema.crear_reserva(
        "RES-006", "CLI-999", "SAL-001", 1, {"personas": 2}
    ), resultados)

    ejecutar_operacion(23, "Rechazar reserva con duracion igual a cero", lambda: sistema.crear_reserva(
        "RES-007", "CLI-001", "ASE-001", 0, {"tema": "prueba"}
    ), resultados)

    sistema.mostrar_resumen()
    print("\nBALANCE DE LA DEMOSTRACION")
    print("-" * 76)
    print(f"Operaciones ejecutadas: {resultados['total']}")
    print(f"Operaciones exitosas: {resultados['exitosas']}")
    print(f"Errores controlados: {resultados['fallidas']}")
    print(f"Archivo de registro: {ARCHIVO_LOG.relative_to(RAIZ_PROYECTO)}")
    print("La ejecucion continuo despues de capturar cada error simulado.")

    logger.info(
        "Demostracion finalizada. Total=%s; exitosas=%s; fallidas=%s.",
        resultados["total"], resultados["exitosas"], resultados["fallidas"]
    )
    return sistema, resultados


def main():
    """Controla la ejecucion general y registra tambien los cierres anormales."""
    try:
        ejecutar_demostracion()
    except KeyboardInterrupt:
        logger.warning("La demostracion fue interrumpida manualmente.")
        print("\nEjecucion interrumpida por el usuario.")
    except Exception as error:
        logger.exception("Fallo no controlado en el punto de entrada.")
        print(f"Error general: {error}")
    finally:
        # Este bloque queda garantizado aunque la demostracion sea interrumpida.
        logger.info("Fin de la ejecucion de Software FJ.")
        print(f"\nEventos y errores registrados en: {ARCHIVO_LOG.relative_to(RAIZ_PROYECTO)}")


if __name__ == "__main__":
    main()
