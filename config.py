
import os
from pathlib import Path
from dotenv import load_dotenv

# Carga .env
load_dotenv()

CARPETA_BASE = Path(__file__).parent
CARPETA_SALIDA = CARPETA_BASE / "output"
ARCHIVO_SESION = CARPETA_BASE / os.getenv("SESSION_FILE", "session.json")

USUARIO_INSTAGRAM = os.getenv("INSTAGRAM_USERNAME", "")
CONTRASENA_INSTAGRAM = os.getenv("INSTAGRAM_PASSWORD", "")

ESPERA_MINIMA = float(os.getenv("MIN_DELAY", "1.0"))
ESPERA_MAXIMA = float(os.getenv("MAX_DELAY", "3.0"))

NIVEL_REGISTRO = os.getenv("LOG_LEVEL", "INFO")

CARPETA_SALIDA.mkdir(exist_ok=True)
