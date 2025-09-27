import cv2
import mediapipe as mp


def inicializar_video(filename):
    """
    Inicializa o vídeo para processamento.
    """
    video = cv2.VideoCapture(filename)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    mp_pose = mp.solutions.pose
    pose_detec = mp_pose.Pose(
        min_tracking_confidence=0.5,
        min_detection_confidence=0.5
    )
    draw = mp.solutions.drawing_utils

    return video, fps, width, height, mp_pose, pose_detec, draw

def salvar_distancia_csv(writer, frame_num, distQJ, fase_atual, contador):
    """ 
    Salva os dados de distância e fase em um arquivo CSV.
    """
    writer.writerow([frame_num, distQJ, fase_atual.value, contador])