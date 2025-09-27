import mediapipe as mp
from enum import Enum

class Fase(Enum):
    SUBIDA = "subida"
    DESCIDA = "descida"


def calcular_distancia_quadril_joelho(points, h):
    """
    Calcula a distância vertical entre o ponto médio do quadril e o ponto médio do joelho.
    """
    # quadril direito/esquerdo
    qdy = int(points.landmark[mp.solutions.pose.PoseLandmark.RIGHT_HIP].y * h)
    qey = int(points.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP].y * h)

    # joelho direito/esquerdo
    jdy = int(points.landmark[mp.solutions.pose.PoseLandmark.RIGHT_KNEE].y * h)
    jey = int(points.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE].y * h)

    # ponto médio do quadril e joelho
    qmy = (qdy + qey) / 2
    jmy = (jdy + jey) / 2

    return jmy - qmy  # distância vertical

def detectar_fase_agachamento(distQJ, ultimaDist, fase, limiar=3):
    """
    Detecta a fase do agachamento com base na distância entre o quadril e o joelho.
    """
    fase_atual = fase
    if distQJ < ultimaDist - limiar:
        fase_atual = Fase.DESCIDA
    elif distQJ > ultimaDist + limiar:
        fase_atual = Fase.SUBIDA
    return fase_atual