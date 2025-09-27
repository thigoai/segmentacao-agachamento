import cv2
from segmentar_agachamento import segmentar_agachamento


def exibir_video(generator):
    cv2.namedWindow("Agachamento", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Agachamento", 800, 600)

    for frame in generator:
        cv2.imshow("Agachamento", frame)
        if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    generator = segmentar_agachamento("agachamento.mov")
    exibir_video(generator)