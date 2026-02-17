"""
Bot IG - Configuración
Carga variables de entorno y define constantes.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carga .env
load_dotenv()

# Rutas
CARPETA_BASE = Path(__file__).parent
CARPETA_SALIDA = CARPETA_BASE / "output"
ARCHIVO_SESION = CARPETA_BASE / os.getenv("SESSION_FILE", "session.json")

# Credenciales
USUARIO_INSTAGRAM = os.getenv("INSTAGRAM_USERNAME", "").strip()
CONTRASENA_INSTAGRAM = os.getenv("INSTAGRAM_PASSWORD", "").strip()

# Tiempos de espera
ESPERA_MINIMA = float(os.getenv("MIN_DELAY", "2.0"))
ESPERA_MAXIMA = float(os.getenv("MAX_DELAY", "5.0"))

# Reintentos
MAX_REINTENTOS = int(os.getenv("MAX_REINTENTOS", "3"))

# Logging
NIVEL_REGISTRO = os.getenv("LOG_LEVEL", "INFO")

# Crear carpeta de salida
CARPETA_SALIDA.mkdir(exist_ok=True)


def validar_configuracion():
    """Valida que la configuración mínima esté lista."""
    errores = []

    if not USUARIO_INSTAGRAM:
        errores.append("INSTAGRAM_USERNAME no está configurado en .env")
    if not CONTRASENA_INSTAGRAM:
        errores.append("INSTAGRAM_PASSWORD no está configurado en .env")
    if ESPERA_MINIMA > ESPERA_MAXIMA:
        errores.append("MIN_DELAY no puede ser mayor que MAX_DELAY")
    if ESPERA_MINIMA < 0.5:
        errores.append("MIN_DELAY muy bajo, riesgo de bloqueo (mínimo 0.5)")

    if errores:
        print("\n\033[31m✗ Errores de configuración:\033[0m")
        for error in errores:
            print(f"  → {error}")
        print("\n  Copia .env.example a .env y llena tus datos\n")
        sys.exit(1)
