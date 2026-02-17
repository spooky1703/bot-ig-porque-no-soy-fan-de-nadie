"""
Bot IG - Control de Tiempo
Controla tiempos entre peticiones con pausas adaptativas.
"""

import random
import time
from config import ESPERA_MINIMA, ESPERA_MAXIMA
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


class ControlTiempo:
    """Controla tiempos de espera con pausas aleatorias y adaptativas."""

    def __init__(self, espera_minima: float = None, espera_maxima: float = None):
        self.espera_minima = espera_minima or ESPERA_MINIMA
        self.espera_maxima = espera_maxima or ESPERA_MAXIMA
        self.ultima_peticion = 0
        self._factor_adaptativo = 1.0

    def ajustar_velocidad(self, mas_lento: bool = True):
        """
        Ajusta la velocidad automáticamente.
        Si Instagram responde lento o con errores, hace todo más lento.
        """
        if mas_lento:
            self._factor_adaptativo = min(self._factor_adaptativo * 1.5, 5.0)
            registro.debug(f"Velocidad reducida (factor: {self._factor_adaptativo:.1f}x)")
        else:
            self._factor_adaptativo = max(self._factor_adaptativo * 0.8, 1.0)

    def esperar(self, razon: str = "control de tiempo"):
        """Espera un tiempo aleatorio entre peticiones."""
        tiempo = random.uniform(
            self.espera_minima * self._factor_adaptativo,
            self.espera_maxima * self._factor_adaptativo,
        )
        registro.debug(f"Esperando {tiempo:.1f}s ({razon})")
        time.sleep(tiempo)
        self.ultima_peticion = time.time()

    def espera_larga(self, multiplicador: float = 3.0, razon: str = "pausa larga"):
        """Espera un tiempo más largo (después de operaciones grandes)."""
        tiempo = random.uniform(
            self.espera_minima * multiplicador * self._factor_adaptativo,
            self.espera_maxima * multiplicador * self._factor_adaptativo,
        )
        registro.info(f"Pausa: {tiempo:.1f}s ({razon})")
        time.sleep(tiempo)
        self.ultima_peticion = time.time()


# Instancia global
control_tiempo = ControlTiempo()
