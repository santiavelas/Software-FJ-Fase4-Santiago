"""Excepciones propias para identificar fallos del sistema Software FJ."""


class ErrorSistemaFJ(Exception):
    """Clase base para las excepciones controladas de la aplicacion."""


class DatoInvalidoError(ErrorSistemaFJ):
    """Se genera cuando un dato no cumple una regla de validacion."""


class ClienteDuplicadoError(ErrorSistemaFJ):
    """Se genera cuando el identificador o correo de un cliente ya existe."""


class ServicioDuplicadoError(ErrorSistemaFJ):
    """Se genera cuando el identificador de un servicio esta repetido."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se genera cuando se intenta confirmar un servicio inhabilitado."""


class RecursoNoDisponibleError(ErrorSistemaFJ):
    """Se genera cuando no hay suficientes equipos para una reserva."""


class EntidadNoEncontradaError(ErrorSistemaFJ):
    """Se genera cuando no se encuentra un cliente, servicio o reserva."""


class EstadoReservaError(ErrorSistemaFJ):
    """Se genera cuando una reserva recibe una accion no permitida."""
