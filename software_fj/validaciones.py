"""Funciones compartidas para validar entradas antes de procesarlas."""

import math
import re

from .excepciones import DatoInvalidoError


def validar_texto(valor, nombre_campo):
    """Exige una cadena de texto que contenga al menos un caracter util."""
    if not isinstance(valor, str) or not valor.strip():
        raise DatoInvalidoError(f"El campo '{nombre_campo}' es obligatorio.")
    return valor.strip()


def validar_numero_positivo(valor, nombre_campo):
    """Convierte a float y valida que el numero sea finito y mayor que cero."""
    try:
        numero = float(valor)
    except (TypeError, ValueError) as error:
        # 'from error' conserva la excepcion original como causa del nuevo error.
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser un numero valido."
        ) from error

    if not math.isfinite(numero) or numero <= 0:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser mayor que cero."
        )
    return numero


def validar_entero_positivo(valor, nombre_campo):
    """Acepta un entero positivo y rechaza booleanos y otros tipos."""
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser un entero mayor que cero."
        )
    return valor


def validar_porcentaje(valor, nombre_campo):
    """Valida un porcentaje decimal entre 0.0 y 1.0."""
    try:
        porcentaje = float(valor)
    except (TypeError, ValueError) as error:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser numerico."
        ) from error

    if not math.isfinite(porcentaje) or not 0 <= porcentaje <= 1:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe estar entre 0 y 1."
        )
    return porcentaje


def validar_correo(correo):
    """Aplica una validacion basica de estructura para correo electronico."""
    correo_limpio = validar_texto(correo, "correo").lower()
    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if re.fullmatch(patron, correo_limpio) is None:
        raise DatoInvalidoError("El correo electronico no tiene un formato valido.")
    return correo_limpio


def validar_telefono(telefono):
    """Permite telefonos con entre siete y quince digitos."""
    telefono_limpio = validar_texto(str(telefono), "telefono")
    digitos = re.sub(r"\D", "", telefono_limpio)
    if not 7 <= len(digitos) <= 15:
        raise DatoInvalidoError(
            "El telefono debe contener entre 7 y 15 digitos."
        )
    return digitos
