"""
Uso:
    1. Copia .env.example a .env y llena tus datos
    2. Instala lo necesario: pip install -r requirements.txt
    3. Corre: python main.py

git: https://github.com/spooky1703
"""

import sys
from modules.entrada import EntradaInstagram
from modules.buscador import BuscadorInstagram
from modules.comparador import encontrar_no_seguidores
from modules.guardador import guardar_todo
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


def mostrar_titulo():
    titulo = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    Detector de falsos reales                              ║
    ║   ─────────────────────────────────────                   ║
    ║   Encuentra cuentas que no te siguen de vuelta            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(titulo)


def principal():
    mostrar_titulo()
    
    # Paso 1: Entrar a la cuenta
    registro.info("Iniciando entrada a la cuenta...")
    entrada = EntradaInstagram()
    
    if not entrada.entrar():
        registro.error("No se pudo entrar. Revisa tus datos.")
        sys.exit(1)
    
    try:
        # Paso 2: Buscar datos
        registro.info("Buscando datos...")
        buscador = BuscadorInstagram(entrada.obtener_cliente(), entrada.id_usuario)
        siguiendo, seguidores = buscador.obtener_todos_los_datos()
        
        if not siguiendo:
            registro.warning("No se pudo obtener la lista de seguidos")
            sys.exit(1)
        
        if not seguidores:
            registro.warning("No se pudo obtener la lista de seguidores")
            sys.exit(1)
        
        # Paso 3: Comparar
        registro.info("Comparando datos...")
        no_seguidores = encontrar_no_seguidores(siguiendo, seguidores)
        
        # Paso 4: Guardar resultados
        registro.info("Guardando resultados...")
        archivos = guardar_todo(
            no_seguidores,
            cantidad_siguiendo=len(siguiendo),
            cantidad_seguidores=len(seguidores)
        )
        
        print("\nArchivos creados:")
        print(f"   - TXT: {archivos['txt']}")
        print(f"   - JSON: {archivos['json']}")
        print("\nListo!")
        
    except KeyboardInterrupt:
        registro.info("\nCancelado por el usuario")
        sys.exit(0)
    except Exception as error:
        registro.error(f"Ocurrio un error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    principal()
