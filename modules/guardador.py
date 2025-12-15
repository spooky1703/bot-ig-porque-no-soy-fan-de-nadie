import json
from datetime import datetime
from pathlib import Path
from typing import List
from config import CARPETA_SALIDA
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


def _obtener_fecha() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def mostrar_en_pantalla(no_seguidores: List[dict], mostrar_detalles: bool = True):

    print("\n" + "=" * 60)
    print("REPORTE DE NO SEGUIDORES")
    print("=" * 60)
    print(f"Total de no seguidores: {len(no_seguidores)}")
    print("-" * 60)
    
    if not no_seguidores:
        print("Todos los que sigues te siguen de vuelta!")
        print("=" * 60 + "\n")
        return
    
    for i, usuario in enumerate(no_seguidores, 1):
        nombre_usuario = usuario['usuario']
        nombre_completo = usuario.get('nombre', '')
        verificado = "[V]" if usuario.get('es_verificado') else ""
        privado = "[P]" if usuario.get('es_privado') else ""
        
        if mostrar_detalles and nombre_completo:
            print(f"{i:3}. @{nombre_usuario} {verificado}{privado} ({nombre_completo})")
        else:
            print(f"{i:3}. @{nombre_usuario} {verificado}{privado}")
    
    print("=" * 60 + "\n")


def guardar_como_txt(no_seguidores: List[dict], nombre_archivo: str = None) -> Path:

    if nombre_archivo is None:
        nombre_archivo = f"no_seguidores_{_obtener_fecha()}.txt"
    
    ruta_archivo = CARPETA_SALIDA / nombre_archivo
    
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"# Reporte de No Seguidores\n")
        archivo.write(f"# Creado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        archivo.write(f"# Total: {len(no_seguidores)}\n")
        archivo.write("#" + "-" * 40 + "\n\n")
        
        for usuario in no_seguidores:
            archivo.write(f"@{usuario['usuario']}\n")
    
    registro.info(f"Guardado en TXT: {ruta_archivo}")
    return ruta_archivo


def guardar_como_json(
    no_seguidores: List[dict], 
    cantidad_siguiendo: int = 0,
    cantidad_seguidores: int = 0,
    nombre_archivo: str = None
) -> Path:

    if nombre_archivo is None:
        nombre_archivo = f"no_seguidores_{_obtener_fecha()}.json"
    
    ruta_archivo = CARPETA_SALIDA / nombre_archivo
    
    reporte = {
        'creado_el': datetime.now().isoformat(),
        'datos': {
            'cantidad_no_seguidores': len(no_seguidores),
            'cantidad_siguiendo': cantidad_siguiendo,
            'cantidad_seguidores': cantidad_seguidores,
        },
        'no_seguidores': no_seguidores,
    }
    
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(reporte, archivo, indent=2, ensure_ascii=False)
    
    registro.info(f"Guardado en JSON: {ruta_archivo}")
    return ruta_archivo


def guardar_todo(
    no_seguidores: List[dict],
    cantidad_siguiendo: int = 0,
    cantidad_seguidores: int = 0
) -> dict:

    fecha = _obtener_fecha()
    
    mostrar_en_pantalla(no_seguidores)
    
    # Guardar en archivos
    ruta_txt = guardar_como_txt(no_seguidores, f"no_seguidores_{fecha}.txt")
    ruta_json = guardar_como_json(
        no_seguidores, 
        cantidad_siguiendo, 
        cantidad_seguidores,
        f"no_seguidores_{fecha}.json"
    )
    
    return {
        'txt': ruta_txt,
        'json': ruta_json,
    }
