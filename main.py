import cv2
import sys
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
    if len(sys.argv) < 2:
        print("Uso: python main.py <nome_arquivo.mov>")
        sys.exit(1)

    arquivo = sys.argv[1]
    generator = segmentar_agachamento(arquivo)
    exibir_video(generator)
