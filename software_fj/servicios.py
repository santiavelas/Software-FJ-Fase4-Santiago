"""Servicios abstractos y sus tres implementaciones especializadas."""

from abc import ABC, abstractmethod

from .entidades import Entidad
from .excepciones import DatoInvalidoError, RecursoNoDisponibleError, ServicioNoDisponibleError
from .logging_config import logger
from .validaciones import (
    validar_entero_positivo,
    validar_numero_positivo,
    validar_porcentaje,
    validar_texto,
)


class Servicio(Entidad, ABC):
    """Define las operaciones compartidas por los servicios de Software FJ."""

    def __init__(self, identificador, nombre, tarifa_base):
        super().__init__(identificador, nombre)
        self._tarifa_base = validar_numero_positivo(tarifa_base, "tarifa_base")
        self._disponible = True

    @property
    def disponible(self):
        return self._disponible

    @property
    def tarifa_base(self):
        return self._tarifa_base

    def cambiar_disponibilidad(self, disponible):
        """Habilita o inhabilita el servicio con un valor booleano."""
        if not isinstance(disponible, bool):
            raise DatoInvalidoError("La disponibilidad debe ser True o False.")
        self._disponible = disponible
        logger.info(
            "Servicio %s: disponibilidad cambiada a %s.",
            self.identificador,
            self._disponible,
        )

    @staticmethod
    def calcular_total_con_cargos(subtotal, impuesto=0.0, descuento=0.0):
        """Aplica descuento e impuesto; ambos porcentajes son opcionales."""
        tasa_impuesto = validar_porcentaje(impuesto, "impuesto")
        tasa_descuento = validar_porcentaje(descuento, "descuento")
        subtotal_ajustado = subtotal * (1 - tasa_descuento)
        return round(subtotal_ajustado * (1 + tasa_impuesto), 2)

    def validar_duracion(self, duracion):
        return validar_numero_positivo(duracion, "duracion")

    @abstractmethod
    def validar_parametros(self, duracion, parametros):
        """Cada servicio valida los datos adicionales que necesita."""
        raise NotImplementedError

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, parametros=None):
        """Calcula el precio con variantes mediante parametros opcionales."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    def apartar_recursos(self, duracion, parametros):
        """Verifica disponibilidad y reserva los recursos necesarios."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no esta disponible actualmente."
            )
        self.validar_parametros(duracion, parametros)
        self._actualizar_recursos_al_apartar(parametros)
        logger.info("Recursos apartados para el servicio %s.", self.identificador)

    def liberar_recursos(self, parametros):
        """Libera recursos cuando se cancela o procesa una reserva."""
        self._actualizar_recursos_al_liberar(parametros)
        logger.info("Recursos liberados para el servicio %s.", self.identificador)

    def _actualizar_recursos_al_apartar(self, parametros):
        """Metodo de extension para servicios sin inventario fisico."""
        return None

    def _actualizar_recursos_al_liberar(self, parametros):
        """Metodo de extension para servicios sin inventario fisico."""
        return None


class ServicioSala(Servicio):
    """Alquiler de sala con control de capacidad maxima."""

    def __init__(self, identificador, tarifa_hora, capacidad):
        super().__init__(identificador, "Reserva de sala", tarifa_hora)
        self._capacidad = validar_entero_positivo(capacidad, "capacidad")

    def validar_parametros(self, duracion, parametros):
        self.validar_duracion(duracion)
        datos = parametros or {}
        asistentes = validar_entero_positivo(datos.get("personas"), "personas")
        if asistentes > self._capacidad:
            raise DatoInvalidoError(
                f"La sala admite maximo {self._capacidad} personas."
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, parametros=None):
        """Calcula el alquiler por hora, con impuesto y descuento opcionales."""
        datos = parametros if parametros is not None else {"personas": 1}
        self.validar_parametros(duracion, datos)
        subtotal = self._tarifa_base * self.validar_duracion(duracion)
        return self.calcular_total_con_cargos(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Reserva de sala | Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Capacidad: {self._capacidad} personas"
        )


class ServicioEquipo(Servicio):
    """Alquiler por hora de equipos que tienen existencias limitadas."""

    def __init__(self, identificador, nombre_equipo, tarifa_hora, existencias):
        super().__init__(identificador, nombre_equipo, tarifa_hora)
        self._existencias_disponibles = validar_entero_positivo(
            existencias, "existencias"
        )

    @property
    def existencias_disponibles(self):
        return self._existencias_disponibles

    def validar_parametros(self, duracion, parametros):
        self.validar_duracion(duracion)
        datos = parametros or {}
        cantidad = validar_entero_positivo(datos.get("cantidad"), "cantidad")
        if cantidad > self._existencias_disponibles:
            raise RecursoNoDisponibleError(
                f"Solo hay {self._existencias_disponibles} unidades de "
                f"'{self.nombre}' disponibles."
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, parametros=None):
        """Calcula el costo por hora y por unidad de equipo solicitada."""
        datos = parametros if parametros is not None else {"cantidad": 1}
        cantidad = validar_entero_positivo(datos.get("cantidad"), "cantidad")
        subtotal = self._tarifa_base * self.validar_duracion(duracion) * cantidad
        return self.calcular_total_con_cargos(subtotal, impuesto, descuento)

    def _actualizar_recursos_al_apartar(self, parametros):
        cantidad = validar_entero_positivo(parametros.get("cantidad"), "cantidad")
        if cantidad > self._existencias_disponibles:
            raise RecursoNoDisponibleError(
                f"No hay suficientes unidades de '{self.nombre}'."
            )
        self._existencias_disponibles -= cantidad

    def _actualizar_recursos_al_liberar(self, parametros):
        self._existencias_disponibles += validar_entero_positivo(
            parametros.get("cantidad"), "cantidad"
        )

    def describir(self):
        return (
            f"Alquiler de {self.nombre} | Tarifa por hora y unidad: "
            f"${self.tarifa_base:,.2f} | Existencias: {self.existencias_disponibles}"
        )


class ServicioAsesoria(Servicio):
    """Asesoria especializada cuyo tema se especifica en cada reserva."""

    def __init__(self, identificador, area, tarifa_hora):
        area_validada = validar_texto(area, "area")
        super().__init__(identificador, f"Asesoria en {area_validada}", tarifa_hora)
        self._area = area_validada

    def validar_parametros(self, duracion, parametros):
        self.validar_duracion(duracion)
        datos = parametros or {}
        validar_texto(datos.get("tema"), "tema")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, parametros=None):
        """Calcula el costo de asesoria por hora."""
        datos = parametros if parametros is not None else {"tema": self._area}
        self.validar_parametros(duracion, datos)
        subtotal = self._tarifa_base * self.validar_duracion(duracion)
        return self.calcular_total_con_cargos(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoria en {self._area} | Tarifa por hora: "
            f"${self.tarifa_base:,.2f}"
        )
