"""
Bot IG - Módulo de Entrada
Maneja la autenticación con Instagram, incluyendo:
- Login con sesión guardada
- Verificación de dos pasos (2FA)
- Resolución de challenges de seguridad
- Reintentos con backoff exponencial
"""

import time
import traceback
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    TwoFactorRequired,
    ChallengeRequired,
    BadPassword,
    UserNotFound,
    ClientError,
    ClientNotFoundError,
)
from config import (
    USUARIO_INSTAGRAM,
    CONTRASENA_INSTAGRAM,
    ARCHIVO_SESION,
    MAX_REINTENTOS,
    ESPERA_MINIMA,
    ESPERA_MAXIMA,
)
from utils.registro import obtener_registro

registro = obtener_registro(__name__)

# Colores para mensajes directos
VERDE = "\033[32m"
AMARILLO = "\033[33m"
ROJO = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"


class EntradaInstagram:
    """Manejador de autenticación con Instagram."""

    def __init__(self):
        self.cliente = Client()
        self.id_usuario = None
        self._preparar_cliente()

    def _preparar_cliente(self):
        """Prepara el cliente para que parezca un dispositivo real."""
        self.cliente.set_device({
            "app_version": "302.1.0.36.111",
            "android_version": 33,
            "android_release": "13.0",
            "dpi": "480dpi",
            "resolution": "1080x2400",
            "manufacturer": "Samsung",
            "device": "dm3q",
            "model": "SM-S9110",
            "cpu": "qcom",
            "version_code": "570924886",
        })
        self.cliente.delay_range = [ESPERA_MINIMA, ESPERA_MAXIMA]

    def _cargar_sesion(self) -> bool:
        """Intenta cargar una sesión guardada previamente."""
        ruta_sesion = Path(ARCHIVO_SESION)
        if not ruta_sesion.exists():
            registro.debug("No hay sesión guardada")
            return False

        try:
            registro.info("Cargando sesión guardada...")
            self.cliente.load_settings(ruta_sesion)
            self.cliente.login(USUARIO_INSTAGRAM, CONTRASENA_INSTAGRAM)

            # Verificar que la sesión es válida
            try:
                self.cliente.get_timeline_feed()
            except LoginRequired:
                registro.warning("Sesión expirada, eliminando...")
                ruta_sesion.unlink(missing_ok=True)
                return False

            self.id_usuario = self.cliente.user_id
            registro.info("Sesión cargada correctamente")
            return True

        except (LoginRequired, ChallengeRequired):
            registro.warning("Sesión inválida, se necesita login nuevo")
            ruta_sesion.unlink(missing_ok=True)
            return False
        except Exception as error:
            registro.warning(f"No se pudo cargar la sesión: {error}")
            ruta_sesion.unlink(missing_ok=True)
            return False

    def _guardar_sesion(self):
        """Guarda la sesión actual para reutilizarla después."""
        try:
            self.cliente.dump_settings(Path(ARCHIVO_SESION))
            registro.debug("Sesión guardada")
        except Exception as error:
            registro.warning(f"No se pudo guardar la sesión: {error}")

    def _manejar_challenge(self) -> bool:
        """
        Maneja un challenge de seguridad de Instagram.
        Instagram puede pedir verificación por email o SMS.
        """
        try:
            print(f"\n{AMARILLO}╔{'═' * 58}╗")
            print(f"║  ⚠  Instagram requiere verificación de seguridad         ║")
            print(f"╚{'═' * 58}╝{RESET}\n")

            # Intentar resolver el challenge
            try:
                self.cliente.challenge_resolve(self.cliente.last_json)
            except (ClientNotFoundError, Exception) as e:
                # Instagram usa /auth_platform/ que instagrapi no soporta
                if "Not Found" in str(e) or "404" in str(e):
                    print(f"{AMARILLO}  Instagram está usando un método nuevo de verificación.{RESET}")
                    print(f"{AMARILLO}  Necesitas verificar tu cuenta manualmente:{RESET}\n")
                    print(f"  {CYAN}1.{RESET} Abre Instagram en tu celular o navegador")
                    print(f"  {CYAN}2.{RESET} Completa cualquier verificación que te pida")
                    print(f"  {CYAN}3.{RESET} Espera unos minutos")
                    print(f"  {CYAN}4.{RESET} Vuelve a correr este bot\n")
                    return False

            # Si llegamos aquí, instagrapi puede manejar el challenge
            print(f"  Instagram mandó un código de verificación.")
            print(f"  Revisa tu {CYAN}email{RESET} o {CYAN}SMS{RESET}.\n")

            codigo = input(f"  {CYAN}→{RESET} Escribe el código: ").strip()

            if not codigo:
                registro.error("No se proporcionó código")
                return False

            self.cliente.challenge_code_handler = lambda username, choice: codigo
            self.cliente.login(USUARIO_INSTAGRAM, CONTRASENA_INSTAGRAM)
            self.id_usuario = self.cliente.user_id
            self._guardar_sesion()
            registro.info("¡Verificación exitosa!")
            return True

        except Exception as error:
            registro.error(f"No se pudo resolver la verificación: {error}")
            print(f"\n{AMARILLO}  Intenta verificar tu cuenta desde la app de Instagram")
            print(f"  y luego vuelve a correr este bot.{RESET}\n")
            return False

    def _manejar_dos_pasos(self) -> bool:
        """Maneja la autenticación de dos factores (2FA)."""
        try:
            print(f"\n{CYAN}╔{'═' * 58}╗")
            print(f"║  🔐  Se necesita código de verificación (2FA)             ║")
            print(f"╚{'═' * 58}╝{RESET}\n")
            print(f"  Revisa tu app de autenticación (Google Auth, etc.)\n")

            codigo = input(f"  {CYAN}→{RESET} Escribe el código de 2FA: ").strip()

            if not codigo:
                registro.error("No se proporcionó código")
                return False

            self.cliente.two_factor_login(codigo)
            self.id_usuario = self.cliente.user_id
            self._guardar_sesion()
            registro.info("¡Verificación de dos pasos exitosa!")
            return True

        except Exception as error:
            registro.error(f"Falló la verificación de dos pasos: {error}")
            return False

    def entrar(self) -> bool:
        """
        Proceso principal de autenticación.
        Intenta: sesión guardada → login nuevo → manejo de challenges.
        """
        if not USUARIO_INSTAGRAM or not CONTRASENA_INSTAGRAM:
            registro.error("No hay datos de Instagram configurados")
            print(f"\n  {ROJO}Copia .env.example a .env y llena tus datos{RESET}\n")
            return False

        # Intentar con sesión guardada
        if self._cargar_sesion():
            return True

        # Login nuevo con reintentos
        for intento in range(1, MAX_REINTENTOS + 1):
            registro.info(f"Entrando como {USUARIO_INSTAGRAM}... (intento {intento}/{MAX_REINTENTOS})")

            try:
                self.cliente.login(USUARIO_INSTAGRAM, CONTRASENA_INSTAGRAM)
                self.id_usuario = self.cliente.user_id
                self._guardar_sesion()
                registro.info("¡Entrada exitosa!")
                return True

            except BadPassword:
                registro.error("Contraseña incorrecta")
                print(f"\n  {ROJO}Revisa INSTAGRAM_PASSWORD en tu archivo .env{RESET}\n")
                return False

            except UserNotFound:
                registro.error(f"Usuario '{USUARIO_INSTAGRAM}' no encontrado")
                print(f"\n  {ROJO}Revisa INSTAGRAM_USERNAME en tu archivo .env{RESET}\n")
                return False

            except TwoFactorRequired:
                return self._manejar_dos_pasos()

            except ChallengeRequired:
                registro.warning("Instagram requiere verificación de seguridad")
                return self._manejar_challenge()

            except ClientNotFoundError:
                # Nuevo tipo de challenge con /auth_platform/
                registro.warning("Instagram requiere verificación (método nuevo)")
                return self._manejar_challenge()

            except LoginRequired:
                registro.error("Sesión expirada")
                Path(ARCHIVO_SESION).unlink(missing_ok=True)
                if intento < MAX_REINTENTOS:
                    espera = 2 ** intento
                    registro.info(f"Reintentando en {espera}s...")
                    time.sleep(espera)
                continue

            except Exception as error:
                error_str = str(error)

                # JSONDecodeError = respuesta vacía de Instagram (challenge silencioso)
                if "Expecting value" in error_str or "JSONDecodeError" in error_str:
                    registro.warning("Instagram respondió con datos inválidos (posible bloqueo)")
                    if intento < MAX_REINTENTOS:
                        espera = 5 * intento
                        registro.info(f"Esperando {espera}s antes de reintentar...")
                        time.sleep(espera)
                        # Recrear cliente limpio
                        self.cliente = Client()
                        self._preparar_cliente()
                        continue
                    else:
                        print(f"\n{AMARILLO}  Instagram está bloqueando los intentos de login.")
                        print(f"  Esto puede pasar por:")
                        print(f"    • Muchos intentos seguidos")
                        print(f"    • Tu cuenta necesita verificación")
                        print(f"    • Instagram detectó actividad inusual\n")
                        print(f"  {CYAN}Solución:{RESET}")
                        print(f"    1. Abre Instagram en tu celular")
                        print(f"    2. Verifica tu cuenta si te lo pide")
                        print(f"    3. Espera 15-30 minutos")
                        print(f"    4. Vuelve a correr este bot{RESET}\n")
                        return False
                else:
                    registro.error(f"Error inesperado: {error}")
                    registro.debug(f"Tipo: {type(error).__name__}")
                    registro.debug(f"Traceback:\n{traceback.format_exc()}")
                    if intento < MAX_REINTENTOS:
                        espera = 2 ** intento
                        registro.info(f"Reintentando en {espera}s...")
                        time.sleep(espera)
                    continue

        registro.error("Se agotaron los intentos de login")
        return False

    def salir(self):
        """Cierra la sesión de Instagram."""
        try:
            self.cliente.logout()
            registro.info("Sesión cerrada")
        except Exception:
            pass

    def esta_dentro(self) -> bool:
        """Verifica si hay una sesión activa."""
        return self.id_usuario is not None

    def obtener_cliente(self) -> Client:
        """Retorna el cliente de instagrapi."""
        return self.cliente
