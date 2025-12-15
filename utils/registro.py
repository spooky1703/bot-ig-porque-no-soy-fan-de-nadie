"""
Bot IG - Utilidad de Registro
Configura el registro con colores y niveles.
"""

import logging
import sys
from config import NIVEL_REGISTRO


class FormatoConColor(logging.Formatter):
    """Formato con colores para la terminal."""
    
    COLORES = {
        'DEBUG': '\033[36m',     # Azul claro
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Amarillo
        'ERROR': '\033[31m',     # Rojo
        'CRITICAL': '\033[35m',  # Morado
    }
    RESETEAR = '\033[0m'
    
    def format(self, registro):
        color = self.COLORES.get(registro.levelname, self.RESETEAR)
        registro.levelname = f"{color}{registro.levelname}{self.RESETEAR}"
        registro.msg = f"{color}{registro.msg}{self.RESETEAR}"
        return super().format(registro)


def obtener_registro(nombre: str) -> logging.Logger:
    """
    Obtiene un registro configurado.
    
    Parametros:
        nombre: Nombre del registro (usualmente __name__)
        
    Regresa:
        Registro configurado
    """
    registro = logging.getLogger(nombre)
    
    if not registro.handlers:
        manejador = logging.StreamHandler(sys.stdout)
        manejador.setFormatter(FormatoConColor(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        ))
        registro.addHandler(manejador)
        registro.setLevel(getattr(logging, NIVEL_REGISTRO.upper(), logging.INFO))
    
    return registro
