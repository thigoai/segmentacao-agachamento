import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from collections import deque
import csv

from processar_agachamento import (
    Fase,
    calcular_distancia_quadril_joelho,
    detectar_fase_agachamento,
)
from processar_video import inicializar_video, salvar_distancia_csv

def segmentar_agachamento(video_path):
    """
    Segmenta o vídeo de agachamento, salvando trechos em aquivos separados.
    """
    video, fps, width, height, mp_pose, pose_detec, draw = inicializar_video(video_path)

    contador = 0
    frames_buffer = deque(maxlen=int(fps * 3)) 
    ultimaDist = 1000
    fase = Fase.DESCIDA
    salvar = False
    saida = None
    frames_gravados = 0

    with open("dados_agachamento.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["frame", "dist_quadril_joelho", "fase", "serie"])

        frame_num = 0
        while True:
            success, img = video.read()
            if not success:
                break

            frame_limpo = img.copy()
            videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose_detec.process(videoRGB)
            points = results.pose_landmarks
            draw.draw_landmarks(img, points, mp_pose.POSE_CONNECTIONS)

            h, w, _ = img.shape

            if points:
                distQJ = calcular_distancia_quadril_joelho(points, h)
                fase_atual = detectar_fase_agachamento(distQJ, ultimaDist, fase)

                salvar_distancia_csv(writer, frame_num, distQJ, fase_atual, contador)
                frames_buffer.append(frame_limpo.copy())

                if fase == Fase.DESCIDA and fase_atual == Fase.SUBIDA:
                    contador += 1
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    saida = cv2.VideoWriter(f'trecho{contador}.mp4', fourcc, fps, (width, height))
                    salvar = True
                    frames_gravados = 0
                    for f in frames_buffer:
                        saida.write(f)

                if salvar and saida is not None:
                    saida.write(frame_limpo)
                    frames_gravados += 1
                    if fase_atual == Fase.DESCIDA and frames_gravados > fps:
                        saida.release()
                        saida = None
                        salvar = False

                fase = fase_atual
                ultimaDist = distQJ

                # texto para exibição
                texto = f'Fase: {fase.value} Serie: {contador}'
                cor = (0,255,0) if fase == Fase.SUBIDA else (0,0,255)
                cv2.putText(img, texto, (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, cor, 5)

            # retornamos o frame processado
            yield img

            frame_num += 1

    video.release()
    if saida is not None:
        saida.release()
