"""
Bot IG - Módulo de Comparación
Compara seguidos vs seguidores para encontrar:
- No seguidores: gente que sigues pero no te sigue
- Fans: gente que te sigue pero no sigues
- Mutuos: se siguen mutuamente
"""

from typing import Dict, List
from utils.registro import obtener_registro

registro = obtener_registro(__name__)


def encontrar_no_seguidores(
    seguidos: Dict[str, dict],
    seguidores: Dict[str, dict],
) -> List[dict]:
    """Encuentra cuentas que sigues pero no te siguen de vuelta."""
    ids_no_seguidores = set(seguidos.keys()) - set(seguidores.keys())

    no_seguidores = [seguidos[uid] for uid in ids_no_seguidores]
    no_seguidores.sort(key=lambda x: x["usuario"].lower())

    registro.info(f"Encontrados {len(no_seguidores)} no seguidores")
    return no_seguidores


def encontrar_fans(
    seguidos: Dict[str, dict],
    seguidores: Dict[str, dict],
) -> List[dict]:
    """Encuentra cuentas que te siguen pero tú no sigues."""
    ids_fans = set(seguidores.keys()) - set(seguidos.keys())

    fans = [seguidores[uid] for uid in ids_fans]
    fans.sort(key=lambda x: x["usuario"].lower())

    registro.info(f"Encontrados {len(fans)} fans")
    return fans


def encontrar_mutuos(
    seguidos: Dict[str, dict],
    seguidores: Dict[str, dict],
) -> List[dict]:
    """Encuentra cuentas con seguimiento mutuo."""
    ids_mutuos = set(seguidos.keys()) & set(seguidores.keys())

    mutuos = [seguidos[uid] for uid in ids_mutuos]
    mutuos.sort(key=lambda x: x["usuario"].lower())

    registro.info(f"Encontrados {len(mutuos)} mutuos")
    return mutuos


def generar_estadisticas(
    seguidos: Dict[str, dict],
    seguidores: Dict[str, dict],
    no_seguidores: List[dict],
    fans: List[dict],
    mutuos: List[dict],
) -> dict:
    """Calcula estadísticas de la cuenta."""
    total_seguidos = len(seguidos)
    total_seguidores = len(seguidores)

    ratio = total_seguidores / total_seguidos if total_seguidos > 0 else 0
    reciprocidad = len(mutuos) / total_seguidos * 100 if total_seguidos > 0 else 0

    return {
        "total_seguidos": total_seguidos,
        "total_seguidores": total_seguidores,
        "total_no_seguidores": len(no_seguidores),
        "total_fans": len(fans),
        "total_mutuos": len(mutuos),
        "ratio_seguidores": round(ratio, 2),
        "porcentaje_reciprocidad": round(reciprocidad, 1),
    }
