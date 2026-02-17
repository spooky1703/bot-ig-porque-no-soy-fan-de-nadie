"""
Bot IG - Módulo de Búsqueda
Obtiene listas de seguidos y seguidores con reintentos y progreso.
"""

import time
from typing import Dict, Tuple
from instagrapi import Client
from instagrapi.exceptions import ClientError
from config import MAX_REINTENTOS
from utils.registro import obtener_registro
from utils.control_tiempo import control_tiempo

registro = obtener_registro(__name__)

CYAN = "\033[36m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
RESET = "\033[0m"


class BuscadorInstagram:
    """Busca datos de seguidos y seguidores."""

    def __init__(self, cliente: Client, id_usuario: str):
        self.cliente = cliente
        self.id_usuario = id_usuario

    def _obtener_con_reintentos(self, funcion, nombre: str) -> dict:
        """
        Ejecuta una función de búsqueda con reintentos automáticos.
        Si falla por rate limit o error de red, espera y reintenta.
        """
        for intento in range(1, MAX_REINTENTOS + 1):
            try:
                print(f"  {CYAN}↓{RESET} Descargando {nombre}...", end="", flush=True)
                resultado = funcion(self.id_usuario, amount=0)
                print(f" {VERDE}✓ {len(resultado)}{RESET}")
                return resultado

            except ClientError as error:
                error_str = str(error)
                print(f" {AMARILLO}✗{RESET}")

                if "429" in error_str or "rate" in error_str.lower():
                    espera = 60 * intento
                    registro.warning(f"Rate limit alcanzado. Esperando {espera}s...")
                    time.sleep(espera)
                elif intento < MAX_REINTENTOS:
                    espera = 5 * intento
                    registro.warning(f"Error al buscar {nombre}: {error}")
                    registro.info(f"Reintentando en {espera}s... ({intento}/{MAX_REINTENTOS})")
                    time.sleep(espera)
                else:
                    registro.error(f"No se pudo obtener {nombre} después de {MAX_REINTENTOS} intentos")
                    return {}

            except Exception as error:
                print(f" {AMARILLO}✗{RESET}")
                registro.error(f"Error inesperado al buscar {nombre}: {error}")
                if intento < MAX_REINTENTOS:
                    espera = 5 * intento
                    registro.info(f"Reintentando en {espera}s...")
                    time.sleep(espera)
                else:
                    return {}

        return {}

    def _convertir_usuarios(self, datos: dict) -> Dict[str, dict]:
        """Convierte datos crudos de instagrapi a formato simple."""
        resultado = {}
        for id_usuario, info in datos.items():
            resultado[str(id_usuario)] = {
                "id_usuario": str(id_usuario),
                "usuario": info.username,
                "nombre": getattr(info, "full_name", "") or "",
                "es_privado": getattr(info, "is_private", False),
                "es_verificado": getattr(info, "is_verified", False),
            }
        return resultado

    def obtener_seguidos(self) -> Dict[str, dict]:
        """Obtiene la lista completa de cuentas que sigues."""
        registro.info("Buscando seguidos...")
        datos = self._obtener_con_reintentos(
            self.cliente.user_following, "seguidos"
        )

        if not datos:
            return {}

        resultado = self._convertir_usuarios(datos)
        control_tiempo.espera_larga(razon="después de buscar seguidos")
        return resultado

    def obtener_seguidores(self) -> Dict[str, dict]:
        """Obtiene la lista completa de seguidores."""
        registro.info("Buscando seguidores...")
        datos = self._obtener_con_reintentos(
            self.cliente.user_followers, "seguidores"
        )

        if not datos:
            return {}

        resultado = self._convertir_usuarios(datos)
        control_tiempo.espera_larga(razon="después de buscar seguidores")
        return resultado

    def obtener_todos_los_datos(self) -> Tuple[Dict[str, dict], Dict[str, dict]]:
        """Obtiene seguidos y seguidores con pausa entre peticiones."""
        print()
        seguidos = self.obtener_seguidos()
        control_tiempo.esperar(razon="entre peticiones")
        seguidores = self.obtener_seguidores()
        print()
        return seguidos, seguidores
