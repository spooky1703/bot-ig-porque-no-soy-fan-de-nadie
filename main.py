"""
Detector de Falsos Reales
Encuentra cuentas de Instagram que no te siguen de vuelta,
tus fans, y tus mutuos.

Uso:
    1. Copia .env.example a .env y llena tus datos
    2. Instala: pip install -r requirements.txt
    3. Corre: python main.py

git: https://github.com/spooky1703
"""

import sys
import signal
from config import validar_configuracion
from modules.entrada import EntradaInstagram
from modules.buscador import BuscadorInstagram
from modules.comparador import (
    encontrar_no_seguidores,
    encontrar_fans,
    encontrar_mutuos,
    generar_estadisticas,
)
from modules.guardador import guardar_todo, mostrar_lista, mostrar_dashboard
from utils.registro import obtener_registro

registro = obtener_registro(__name__)

# Colores
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CYAN = "\033[36m"
GRIS = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _salir_limpio(sig, frame):
    """Maneja Ctrl+C limpiamente."""
    print(f"\n\n  {GRIS}Cancelado.{RESET}\n")
    sys.exit(0)


signal.signal(signal.SIGINT, _salir_limpio)


def mostrar_titulo():
    titulo = f"""
{BOLD}    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    Detector de falsos reales                              ║
    ║   ─────────────────────────────────────                   ║
    ║   Encuentra cuentas que no te siguen de vuelta            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝{RESET}
    """
    print(titulo)


def mostrar_menu():
    """Muestra el menú de opciones después del análisis."""
    print(f"  {BOLD}¿Qué quieres ver?{RESET}\n")
    print(f"    {CYAN}1.{RESET} No seguidores (quién no te sigue de vuelta)")
    print(f"    {CYAN}2.{RESET} Fans (te siguen pero no los sigues)")
    print(f"    {CYAN}3.{RESET} Mutuos")
    print(f"    {CYAN}4.{RESET} Todo (dashboard + listas)")
    print(f"    {CYAN}5.{RESET} Solo guardar archivos (sin mostrar listas)")
    print(f"    {CYAN}0.{RESET} Salir\n")


def principal():
    mostrar_titulo()

    # Validar configuración
    validar_configuracion()

    # Paso 1: Login
    registro.info("Iniciando entrada a la cuenta...")
    entrada = EntradaInstagram()

    if not entrada.entrar():
        registro.error("No se pudo entrar. Revisa tus datos.")
        sys.exit(1)

    try:
        # Paso 2: Buscar datos
        registro.info("Buscando datos de tu cuenta...")
        buscador = BuscadorInstagram(entrada.obtener_cliente(), entrada.id_usuario)
        seguidos, seguidores = buscador.obtener_todos_los_datos()

        if not seguidos:
            registro.warning("No se pudo obtener la lista de seguidos")
            sys.exit(1)

        if not seguidores:
            registro.warning("No se pudo obtener la lista de seguidores")
            sys.exit(1)

        # Paso 3: Analizar
        registro.info("Analizando datos...")
        no_seguidores = encontrar_no_seguidores(seguidos, seguidores)
        fans = encontrar_fans(seguidos, seguidores)
        mutuos_lista = encontrar_mutuos(seguidos, seguidores)
        estadisticas = generar_estadisticas(
            seguidos, seguidores, no_seguidores, fans, mutuos_lista
        )

        # Mostrar dashboard siempre
        mostrar_dashboard(estadisticas)

        # Menú interactivo
        while True:
            mostrar_menu()
            opcion = input(f"  {CYAN}→{RESET} Elige una opción: ").strip()

            if opcion == "1":
                mostrar_lista(no_seguidores, "NO TE SIGUEN DE VUELTA", ROJO)
            elif opcion == "2":
                mostrar_lista(fans, "FANS (te siguen, no los sigues)", AMARILLO)
            elif opcion == "3":
                mostrar_lista(mutuos_lista, "MUTUOS", VERDE)
            elif opcion == "4":
                mostrar_lista(no_seguidores, "NO TE SIGUEN DE VUELTA", ROJO)
                mostrar_lista(fans, "FANS (te siguen, no los sigues)", AMARILLO)
                mostrar_lista(mutuos_lista, "MUTUOS", VERDE)
            elif opcion == "5":
                pass  # Solo guardar abajo
            elif opcion == "0":
                print(f"\n  {GRIS}Saliendo...{RESET}\n")
                sys.exit(0)
            else:
                print(f"\n  {AMARILLO}Opción no válida{RESET}\n")
                continue

            # Guardar archivos
            if opcion in ("1", "2", "3", "4", "5"):
                registro.info("Guardando reportes...")
                archivos = guardar_todo(
                    no_seguidores, fans, mutuos_lista, estadisticas
                )

                print(f"  {VERDE}Archivos guardados:{RESET}")
                print(f"    → TXT:  {archivos['txt']}")
                print(f"    → JSON: {archivos['json']}")
                print(f"\n  {BOLD}¡Listo!{RESET}\n")
                break

    except KeyboardInterrupt:
        print(f"\n\n  {GRIS}Cancelado.{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    principal()
