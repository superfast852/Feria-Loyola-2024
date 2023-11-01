from itertools import groupby
from operator import itemgetter

# All the navigation algorithms go here.


class Map:
    pass


class SLAM:
    pass


class RRT:
    pass


def detectar_obstaculo(mapa, limites_angulo=(0, 180), limites_distancia=300):
    for angulo in range(limites_angulo[0], limites_angulo[1]+1):
        distancia = mapa[angulo]
        if distancia > limites_distancia:
            pass
        else:
            return True
    return False


def encontrar_espacios(mapa, limites_angulo=(0, 180), limites_distancia=300, min_len=2):
    l_clear = []
    r_clear = []

    punto_medio = sum(limites_angulo)/2

    for angulo, distancia in enumerate(mapa[0:punto_medio]):
        if distancia > limites_distancia:
            l_clear.append(angulo)

    for angulo, distancia in enumerate(mapa[punto_medio:]):
        if distancia > limites_distancia:
            angulo += punto_medio
            r_clear.append(angulo)

    espacios_izq = _extract_sequence(l_clear, min_len)
    espacios_der = _extract_sequence(r_clear, min_len)

    esp_final_izq = max(espacios_izq, key=len) if len(espacios_izq) > 0 else None
    esp_final_der = max(espacios_der, key=len) if len(espacios_der) > 0 else None

    if esp_final_izq is None and esp_final_der is None:
        return -1
    elif esp_final_izq is None:
        return "der"
    elif esp_final_der is None:
        return "izq"

    if len(esp_final_izq) > len(esp_final_der):
        return "izq"
    else:
        return "der"


def _extract_sequence(array, min_length=2):
    sequences = []
    for k, g in groupby(enumerate(array), lambda x: x[0] - x[1]):
        seq = list(map(itemgetter(1), g))
        sequences.append(seq) if len(seq) > min_length else None
    return sequences


def auto_manejo(mapa, limites_angulo=(0, 180), limites_distancia=300, min_len=2):
    if detectar_obstaculo(mapa, limites_angulo, limites_distancia):
        lado = encontrar_espacios(mapa, limites_angulo, limites_distancia, min_len)
        if lado == -1:
            return "bwd"
        else:
            return lado
    else:
        return "fwd"