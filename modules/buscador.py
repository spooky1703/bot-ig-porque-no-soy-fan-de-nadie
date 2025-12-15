from typing import Dict, List
from instagrapi import Client
from utils.registro import obtener_registro
from utils.control_tiempo import control_tiempo

registro = obtener_registro(__name__)


class BuscadorInstagram:

    
    def __init__(self, cliente: Client, id_usuario: str):

        self.cliente = cliente
        self.id_usuario = id_usuario
    
    def obtener_seguidos(self) -> Dict[str, dict]:

        registro.info("Buscando lista de seguidos...")
        
        try:
            seguidos = self.cliente.user_following(self.id_usuario)
            registro.info(f"Encontrados {len(seguidos)} seguidos")
            
            # Convertir a formato simple
            resultado = {}
            for id_usuario, info_usuario in seguidos.items():
                resultado[str(id_usuario)] = {
                    'id_usuario': str(id_usuario),
                    'usuario': info_usuario.username,
                    'nombre': getattr(info_usuario, 'full_name', '') or '',
                    'es_privado': getattr(info_usuario, 'is_private', False),
                    'es_verificado': getattr(info_usuario, 'is_verified', False),
                }
            
            control_tiempo.espera_larga(razon="despues de buscar seguidos")
            return resultado
            
        except Exception as error:
            registro.error(f"Error al buscar seguidos: {error}")
            return {}
    
    def obtener_seguidores(self) -> Dict[str, dict]:
        registro.info("Buscando lista de seguidores...")
        
        try:
            seguidores = self.cliente.user_followers(self.id_usuario)
            registro.info(f"Encontrados {len(seguidores)} seguidores")
            
            # Convertir a formato simple
            resultado = {}
            for id_usuario, info_usuario in seguidores.items():
                resultado[str(id_usuario)] = {
                    'id_usuario': str(id_usuario),
                    'usuario': info_usuario.username,
                    'nombre': getattr(info_usuario, 'full_name', '') or '',
                    'es_privado': getattr(info_usuario, 'is_private', False),
                    'es_verificado': getattr(info_usuario, 'is_verified', False),
                }
            
            control_tiempo.espera_larga(razon="despues de buscar seguidores")
            return resultado
            
        except Exception as error:
            registro.error(f"Error al buscar seguidores: {error}")
            return {}
    
    def obtener_todos_los_datos(self) -> tuple:
        seguidos = self.obtener_seguidos()
        control_tiempo.esperar(razon="entre peticiones")
        seguidores = self.obtener_seguidores()
        
        return seguidos, seguidores
