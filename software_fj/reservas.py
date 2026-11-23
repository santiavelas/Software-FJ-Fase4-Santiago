"""Estados y operaciones de las reservas creadas por los clientes."""

from enum import Enum

from .entidades import Cliente
from .excepciones import DatoInvalidoError, EstadoReservaError
from .logging_config import logger
from .servicios import Servicio
from .validaciones import validar_numero_positivo, validar_texto


class EstadoReserva(Enum):
    """Estados permitidos para controlar el ciclo de vida de una reserva."""

    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva:
    """Relaciona un cliente con un servicio, una duracion y un estado."""

    def __init__(self, identificador, cliente, servicio, duracion, parametros):
        self._identificador = validar_texto(identificador, "identificador_reserva")

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere un objeto Cliente valido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere un objeto Servicio valido.")
        if not cliente.activo:
            raise DatoInvalidoError("No se puede reservar para un cliente inactivo.")
        if not isinstance(parametros, dict):
            raise DatoInvalidoError("Los parametros deben entregarse en un diccionario.")

        self._duracion = validar_numero_positivo(duracion, "duracion")
        self._cliente = cliente
        self._servicio = servicio
        self._parametros = dict(parametros)
        self._estado = EstadoReserva.PENDIENTE
        self._recursos_apartados = False

        # Se validan los parametros antes de guardar la reserva en el sistema.
        self._servicio.validar_parametros(self._duracion, self._parametros)

    @property
    def identificador(self):
        return self._identificador

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    def calcular_total(self, impuesto=0.0, descuento=0.0):
        """Calcula el valor con cero, uno o dos parametros adicionales."""
        return self._servicio.calcular_costo(
            self._duracion,
            impuesto=impuesto,
            descuento=descuento,
            parametros=self._parametros,
        )

    def confirmar(self):
        """Pasa una reserva pendiente a confirmada y aparta sus recursos."""
        if self._estado is not EstadoReserva.PENDIENTE:
            raise EstadoReservaError(
                "Solo se pueden confirmar reservas que esten pendientes."
            )
        self._servicio.apartar_recursos(self._duracion, self._parametros)
        self._recursos_apartados = True
        self._estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva %s confirmada.", self.identificador)
        return self._estado

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada y libera recursos."""
        if self._estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise EstadoReservaError(
                "No se puede cancelar una reserva cancelada o procesada."
            )
        if self._recursos_apartados:
            self._servicio.liberar_recursos(self._parametros)
            self._recursos_apartados = False
        self._estado = EstadoReserva.CANCELADA
        logger.info("Reserva %s cancelada.", self.identificador)
        return self._estado

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Procesa una reserva confirmada y devuelve el valor final."""
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise EstadoReservaError(
                "Solo se pueden procesar reservas que esten confirmadas."
            )
        total = self.calcular_total(impuesto, descuento)
        if self._recursos_apartados:
            self._servicio.liberar_recursos(self._parametros)
            self._recursos_apartados = False
        self._estado = EstadoReserva.PROCESADA
        logger.info("Reserva %s procesada. Total: $%.2f.", self.identificador, total)
        return total

    def describir(self):
        return (
            f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duracion: {self._duracion} | "
            f"Estado: {self.estado.value}"
        )
