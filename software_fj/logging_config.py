"""Configuracion centralizada del registro de eventos y errores."""

import logging
from pathlib import Path

# La carpeta logs queda en la raiz del proyecto, fuera del paquete de codigo.
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_LOGS = RAIZ_PROYECTO / "logs"
CARPETA_LOGS.mkdir(parents=True, exist_ok=True)
ARCHIVO_LOG = CARPETA_LOGS / "software_fj.log"

# Se usa un solo logger compartido por todos los modulos del sistema.
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)
logger.propagate = False

# Evita agregar manejadores duplicados cuando se importan varios modulos.
if not logger.handlers:
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
