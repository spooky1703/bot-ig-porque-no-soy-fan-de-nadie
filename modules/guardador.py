"""
Bot IG - Módulo de Guardado y Reportes
Genera reportes en pantalla, TXT y JSON con datos completos.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config import CARPETA_SALIDA
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


def _obtener_fecha() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def mostrar_dashboard(estadisticas: dict):
    """Muestra un dashboard visual con las estadísticas de la cuenta."""
    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  📊  RESUMEN DE TU CUENTA{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

    total_seg = estadisticas["total_seguidos"]
    total_segr = estadisticas["total_seguidores"]
    ratio = estadisticas["ratio_seguidores"]
    recip = estadisticas["porcentaje_reciprocidad"]

    # Stats principales
    print(f"  Seguidos      {CYAN}{total_seg:>6}{RESET}")
    print(f"  Seguidores    {CYAN}{total_segr:>6}{RESET}")
    print(f"  {'─' * 25}")
    print(f"  Mutuos        {VERDE}{estadisticas['total_mutuos']:>6}{RESET}")
    print(f"  No te siguen  {ROJO}{estadisticas['total_no_seguidores']:>6}{RESET}")
    print(f"  Fans          {AMARILLO}{estadisticas['total_fans']:>6}{RESET}")
    print()
    print(f"  Ratio         {CYAN}{ratio}{RESET}")
    print(f"  Reciprocidad  {CYAN}{recip}%{RESET}")
    print(f"\n{'─' * 60}\n")


def mostrar_lista(usuarios: List[dict], titulo: str, color: str = RESET, limite: int = 0):
    """Muestra una lista de usuarios con formato."""
    total = len(usuarios)

    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"  {color}{BOLD}{titulo}{RESET}")
    print(f"  {GRIS}Total: {total}{RESET}")
    print(f"{'═' * 60}")

    if not usuarios:
        print(f"\n  {VERDE}  ¡Lista vacía!{RESET}\n")
        print(f"{'═' * 60}\n")
        return

    mostrar = usuarios[:limite] if limite > 0 else usuarios

    for i, usuario in enumerate(mostrar, 1):
        nombre_usuario = usuario["usuario"]
        nombre_completo = usuario.get("nombre", "")
        verificado = f" {CYAN}✓{RESET}" if usuario.get("es_verificado") else ""
        privado = f" {AMARILLO}🔒{RESET}" if usuario.get("es_privado") else ""

        linea = f"  {GRIS}{i:3}.{RESET} @{nombre_usuario}{verificado}{privado}"
        if nombre_completo:
            linea += f" {GRIS}({nombre_completo}){RESET}"
        print(linea)

    if limite > 0 and total > limite:
        print(f"\n  {GRIS}... y {total - limite} más (ver archivo completo){RESET}")

    print(f"{'═' * 60}\n")


def guardar_como_txt(
    no_seguidores: List[dict],
    fans: List[dict] = None,
    mutuos: List[dict] = None,
    nombre_archivo: str = None,
) -> Path:
    """Guarda el reporte en formato TXT con links directos."""
    if nombre_archivo is None:
        nombre_archivo = f"reporte_{_obtener_fecha()}.txt"

    ruta = CARPETA_SALIDA / nombre_archivo
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"# Reporte de Instagram\n")
        f.write(f"# Fecha: {ahora}\n")
        f.write(f"{'#' + '─' * 50}\n\n")

        # No seguidores
        f.write(f"## NO TE SIGUEN ({len(no_seguidores)})\n\n")
        for u in no_seguidores:
            f.write(f"  @{u['usuario']}  →  instagram.com/{u['usuario']}\n")

        # Fans
        if fans:
            f.write(f"\n## FANS - Te siguen pero no los sigues ({len(fans)})\n\n")
            for u in fans:
                f.write(f"  @{u['usuario']}  →  instagram.com/{u['usuario']}\n")

        # Mutuos
        if mutuos:
            f.write(f"\n## MUTUOS ({len(mutuos)})\n\n")
            for u in mutuos:
                f.write(f"  @{u['usuario']}\n")

    registro.info(f"Guardado TXT: {ruta}")
    return ruta


def guardar_como_json(
    no_seguidores: List[dict],
    fans: List[dict] = None,
    mutuos: List[dict] = None,
    estadisticas: dict = None,
    nombre_archivo: str = None,
) -> Path:
    """Guarda el reporte completo en formato JSON."""
    if nombre_archivo is None:
        nombre_archivo = f"reporte_{_obtener_fecha()}.json"

    ruta = CARPETA_SALIDA / nombre_archivo

    reporte = {
        "creado_el": datetime.now().isoformat(),
        "estadisticas": estadisticas or {},
        "no_seguidores": no_seguidores,
        "fans": fans or [],
        "mutuos": mutuos or [],
    }

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    registro.info(f"Guardado JSON: {ruta}")
    return ruta


def guardar_todo(
    no_seguidores: List[dict],
    fans: List[dict],
    mutuos: List[dict],
    estadisticas: dict,
) -> dict:
    """Guarda los reportes en archivos TXT y JSON."""
    fecha = _obtener_fecha()

    ruta_txt = guardar_como_txt(
        no_seguidores, fans, mutuos,
        f"reporte_{fecha}.txt"
    )
    ruta_json = guardar_como_json(
        no_seguidores, fans, mutuos, estadisticas,
        f"reporte_{fecha}.json"
    )

    return {"txt": ruta_txt, "json": ruta_json}
