from typing import Dict, List
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


def encontrar_no_seguidores(
    seguidos: Dict[str, dict], 
    seguidores: Dict[str, dict]
) -> List[dict]:
    registro.info("Comparando seguidos contra seguidores...")
    
    ids_seguidos = set(seguidos.keys())
    ids_seguidores = set(seguidores.keys())
    
    ids_no_seguidores = ids_seguidos - ids_seguidores
    
    no_seguidores = []
    for id_usuario in ids_no_seguidores:
        info_usuario = seguidos[id_usuario]
        no_seguidores.append(info_usuario)
    
    no_seguidores.sort(key=lambda x: x['usuario'].lower())
    no_seguidores.sort(key=lambda x: x['usuario'].lower())
    
    registro.info(f"Encontrados {len(no_seguidores)} no seguidores")
    registro.info(f"Datos: {len(seguidos)} seguidos, {len(seguidores)} seguidores")
    
    return no_seguidores


def encontrar_fans(
    seguidos: Dict[str, dict], 
    seguidores: Dict[str, dict]
) -> List[dict]:
   
    ids_seguidos = set(seguidos.keys())
    ids_seguidores = set(seguidores.keys())
    
    ids_fans = ids_seguidores - ids_seguidos
    
    fans = []
    for id_usuario in ids_fans:
        info_usuario = seguidores[id_usuario]
        fans.append(info_usuario)
    
    fans.sort(key=lambda x: x['usuario'].lower())
    
    registro.info(f"Encontrados {len(fans)} fans (seguidores que no sigues)")
    
    return fans


def encontrar_mutuos(
    seguidos: Dict[str, dict], 
    seguidores: Dict[str, dict]
) -> List[dict]:

    ids_seguidos = set(seguidos.keys())
    ids_seguidores = set(seguidores.keys())
    
    ids_mutuos = ids_seguidos & ids_seguidores
    
    mutuos = []
    for id_usuario in ids_mutuos:
        info_usuario = seguidos[id_usuario]
        mutuos.append(info_usuario)
    
    mutuos.sort(key=lambda x: x['usuario'].lower())
    
    registro.info(f"Encontrados {len(mutuos)} mutuos")
    
    return mutuos
