"""
Bot IG - Utilidad de Control de Tiempo
Controla los tiempos entre peticiones para evitar bloqueos.
"""

import random
import time
from config import ESPERA_MINIMA, ESPERA_MAXIMA
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


class ControlTiempo:
    """
    Controla tiempos de espera con pausas aleatorias.
    """
    
    def __init__(self, espera_minima: float = None, espera_maxima: float = None):
        """
        Prepara el control de tiempo.
        
        Parametros:
            espera_minima: Tiempo minimo de espera en segundos
            espera_maxima: Tiempo maximo de espera en segundos
        """
        self.espera_minima = espera_minima or ESPERA_MINIMA
        self.espera_maxima = espera_maxima or ESPERA_MAXIMA
        self.ultima_peticion = 0
    
    def esperar(self, razon: str = "control de tiempo"):
        """
        Espera un tiempo aleatorio entre peticiones.
        
        Parametros:
            razon: Porque estamos esperando (para el registro)
        """
        tiempo = random.uniform(self.espera_minima, self.espera_maxima)
        registro.debug(f"Esperando {tiempo:.2f}s ({razon})")
        time.sleep(tiempo)
        self.ultima_peticion = time.time()
    
    def espera_larga(self, multiplicador: float = 3.0, razon: str = "pausa larga"):
        """
        Espera un tiempo mas largo (util despues de operaciones grandes).
        
        Parametros:
            multiplicador: Cuanto mas largo que lo normal
            razon: Porque estamos esperando
        """
        tiempo = random.uniform(
            self.espera_minima * multiplicador, 
            self.espera_maxima * multiplicador
        )
        registro.info(f"Espera larga: {tiempo:.2f}s ({razon})")
        time.sleep(tiempo)
        self.ultima_peticion = time.time()


# Control de tiempo global
control_tiempo = ControlTiempo()
