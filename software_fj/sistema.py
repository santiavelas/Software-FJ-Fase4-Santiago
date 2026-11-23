"""Coordinador principal: mantiene las listas internas y conecta los objetos."""

from .entidades import Cliente
from .excepciones import (
    ClienteDuplicadoError,
    DatoInvalidoError,
    EntidadNoEncontradaError,
    ServicioDuplicadoError,
)
from .logging_config import logger
from .reservas import Reserva
from .servicios import Servicio


class SistemaFJ:
    """Administra clientes, servicios y reservas sin utilizar bases de datos."""

    def __init__(self):
        # La informacion vive en memoria mientras el programa esta abierto.
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def registrar_cliente(self, cliente):
        """Valida duplicados y agrega el objeto Cliente a la lista."""
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Solo se pueden registrar objetos Cliente.")
        identificador_repetido = any(
            actual.identificador.casefold() == cliente.identificador.casefold()
            for actual in self._clientes
        )
        correo_repetido = any(
            actual.correo == cliente.correo for actual in self._clientes
        )
        if identificador_repetido or correo_repetido:
            raise ClienteDuplicadoError(
                "El identificador o el correo del cliente ya se encuentra registrado."
            )
        self._clientes.append(cliente)
        logger.info("Cliente %s registrado.", cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio):
        """Registra una instancia de cualquier subclase de Servicio."""
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El elemento no pertenece a una clase Servicio.")
        if any(
            actual.identificador.casefold() == servicio.identificador.casefold()
            for actual in self._servicios
        ):
            raise ServicioDuplicadoError(
                f"Ya existe un servicio con identificador {servicio.identificador}."
            )
        self._servicios.append(servicio)
        logger.info("Servicio %s registrado.", servicio.identificador)
        return servicio

    def buscar_cliente(self, identificador):
        """Busca un cliente por identificador, sin exponer la lista interna."""
        clave = str(identificador).casefold()
        for cliente in self._clientes:
            if cliente.identificador.casefold() == clave:
                return cliente
        raise EntidadNoEncontradaError(f"No se encontro el cliente {identificador}.")

    def buscar_servicio(self, identificador):
        """Busca cualquier servicio especializado por su identificador."""
        clave = str(identificador).casefold()
        for servicio in self._servicios:
            if servicio.identificador.casefold() == clave:
                return servicio
        raise EntidadNoEncontradaError(f"No se encontro el servicio {identificador}.")

    def buscar_reserva(self, identificador):
        """Busca una reserva por identificador."""
        clave = str(identificador).casefold()
        for reserva in self._reservas:
            if reserva.identificador.casefold() == clave:
                return reserva
        raise EntidadNoEncontradaError(f"No se encontro la reserva {identificador}.")

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion, parametros):
        """Crea la reserva y la agrega solo cuando sus datos iniciales son validos."""
        if any(
            reserva.identificador.casefold() == str(identificador).casefold()
            for reserva in self._reservas
        ):
            raise DatoInvalidoError(
                f"Ya existe una reserva con identificador {identificador}."
            )
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        reserva = Reserva(identificador, cliente, servicio, duracion, parametros)
        self._reservas.append(reserva)
        logger.info(
            "Reserva %s creada para el cliente %s.", identificador, id_cliente
        )
        return reserva

    def confirmar_reserva(self, identificador):
        return self.buscar_reserva(identificador).confirmar()

    def cancelar_reserva(self, identificador):
        return self.buscar_reserva(identificador).cancelar()

    def procesar_reserva(self, identificador, impuesto=0.0, descuento=0.0):
        return self.buscar_reserva(identificador).procesar(impuesto, descuento)

    def mostrar_resumen(self):
        """Imprime un resumen polimorfico de reservas y servicios."""
        print("\nRESUMEN DEL SISTEMA SOFTWARE FJ")
        print("-" * 72)
        print(f"Clientes registrados: {len(self._clientes)}")
        print(f"Servicios registrados: {len(self._servicios)}")
        print(f"Reservas registradas: {len(self._reservas)}")
        print("\nRESERVAS:")
        for reserva in self._reservas:
            print(" -", reserva.describir())
        print("\nSERVICIOS:")
        for servicio in self._servicios:
            # El mismo metodo produce una descripcion distinta por cada servicio.
            print(" -", servicio.describir())
