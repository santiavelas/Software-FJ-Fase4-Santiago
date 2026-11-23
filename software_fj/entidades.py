"""Clases que representan entidades generales y clientes del sistema."""

from abc import ABC, abstractmethod

from .excepciones import DatoInvalidoError
from .logging_config import logger
from .validaciones import validar_correo, validar_telefono, validar_texto


class Entidad(ABC):
    """Clase abstracta con datos comunes a las entidades del sistema."""

    def __init__(self, identificador, nombre):
        # El guion bajo indica que los atributos se administran desde la clase.
        self._identificador = validar_texto(identificador, "identificador")
        self._nombre = validar_texto(nombre, "nombre")

    @property
    def identificador(self):
        """Entrega el identificador sin exponer una asignacion directa."""
        return self._identificador

    @property
    def nombre(self):
        """Entrega el nombre de la entidad."""
        return self._nombre

    @abstractmethod
    def describir(self):
        """Obliga a cada clase concreta a definir su propia descripcion."""
        raise NotImplementedError


class Cliente(Entidad):
    """Cliente con datos de contacto privados y reglas de validacion."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador, nombre)
        self._correo = validar_correo(correo)
        self._telefono = validar_telefono(telefono)
        self._activo = True

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    @property
    def activo(self):
        return self._activo

    def desactivar(self):
        """Desactiva al cliente y deja constancia del evento."""
        self._activo = False
        logger.info("Cliente %s desactivado.", self.identificador)

    def describir(self):
        """Devuelve una descripcion resumida del cliente."""
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente {self.identificador}: {self.nombre} | "
            f"Correo: {self.correo} | Estado: {estado}"
        )
