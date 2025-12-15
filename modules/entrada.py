from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    TwoFactorRequired,
    ChallengeRequired,
    BadPassword,
    UserNotFound,
    ClientError,
)
from config import USUARIO_INSTAGRAM, CONTRASENA_INSTAGRAM, ARCHIVO_SESION
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


class EntradaInstagram:

    def __init__(self):
        """manejador de entrada."""
        self.cliente = Client()
        self.id_usuario = None
        self._preparar_cliente()
    
    def _preparar_cliente(self):
        """Prepara el cliente para que parezca un celular real."""
        self.cliente.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "OnePlus",
            "device": "devitron",
            "model": "6T Dev",
            "cpu": "qcom",
            "version_code": "314665256",
        })
        # Tiempo entre peticiones
        self.cliente.delay_range = [1, 3]
    
    def _cargar_sesion(self) -> bool:

        ruta_sesion = Path(ARCHIVO_SESION)
        if not ruta_sesion.exists():
            registro.debug("No hay sesion guardada")
            return False
        
        try:
            self.cliente.load_settings(ruta_sesion)
            self.cliente.login(USUARIO_INSTAGRAM, CONTRASENA_INSTAGRAM)
            self.id_usuario = self.cliente.user_id
            registro.info("Sesion cargada correctamente")
            return True
        except Exception as error:
            registro.warning(f"No se pudo cargar la sesion: {error}")
            ruta_sesion.unlink(missing_ok=True)
            return False
    
    def _guardar_sesion(self):
        try:
            self.cliente.dump_settings(Path(ARCHIVO_SESION))
            registro.debug("Sesion guardada")
        except Exception as error:
            registro.warning(f"No se pudo guardar la sesion: {error}")
    
    def entrar(self) -> bool:

        if not USUARIO_INSTAGRAM or not CONTRASENA_INSTAGRAM:
            registro.error("No hay datos de Instagram configurados!")
            registro.error("Copia .env.example a .env y llena tus datos")
            return False
        
        # Intentar cargar sesion guardada
        if self._cargar_sesion():
            return True
        
        # Entrada nueva
        registro.info(f"Entrando como {USUARIO_INSTAGRAM}...")
        
        try:
            self.cliente.login(USUARIO_INSTAGRAM, CONTRASENA_INSTAGRAM)
            self.id_usuario = self.cliente.user_id
            self._guardar_sesion()
            registro.info("Entrada exitosa!")
            return True
            
        except BadPassword:
            registro.error("Contrasena incorrecta")
            return False
            
        except UserNotFound:
            registro.error("Usuario no encontrado")
            return False
            
        except TwoFactorRequired:
            registro.warning("Se necesita codigo de dos pasos")
            return self._manejar_dos_pasos()
            
        except ChallengeRequired:
            registro.error("Instagram detecto entrada sospechosa")
            registro.error("Entra desde la app para verificar tu cuenta")
            return False
            
        except LoginRequired:
            registro.error("Se necesita entrar de nuevo - la sesion expiro")
            return False
            
        except Exception as error:
            registro.error(f"No se pudo entrar: {error}")
            return False
    
    def _manejar_dos_pasos(self) -> bool:

        try:
            codigo = input("Escribe el codigo de verificacion: ").strip()
            self.cliente.two_factor_login(codigo)
            self.id_usuario = self.cliente.user_id
            self._guardar_sesion()
            registro.info("Verificacion exitosa!")
            return True
        except Exception as error:
            registro.error(f"Fallo la verificacion: {error}")
            return False
    
    def salir(self):
        """Cierra la sesion de Instagram."""
        try:
            self.cliente.logout()
            registro.info("Sesion cerrada")
        except Exception as error:
            registro.warning(f"Error al salir: {error}")
    
    def esta_dentro(self) -> bool:

        return self.id_usuario is not None
    
    def obtener_cliente(self) -> Client:

        return self.cliente
