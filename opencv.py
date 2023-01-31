import numpy as np
import cv2 as cv
import time, os

LIMITE = 20 * 60 * 5
rodando = True

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

frameold = None
fourcc = cv.VideoWriter_fourcc(*'XVID')


while rodando:

    print("""
    Iniciando.....
    Os arquivos são alvos em videos de 5 minutos,
    para salvar o vídeo atual altes dos 5 minutos
    pressione "s"
    para terminar pressione "q"

        """)

    frames = 0
    out = cv.VideoWriter(".." + os.sep + "arquivos" + os.sep + "videos_sensor_de_movimento" + os.sep + time.strftime("%Y%m%d%H%M%S.avi", time.localtime()), fourcc, 30.0, (640,  480))
    while rodando:
        hora = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        # Capture frame-by-frame
        ret, frame = cap.read()
        #print(frame.shape)
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if frameold is None:
            frameold = frame
            continue
        # Our operations on the frame come here
        grayold = cv.cvtColor(frameold, cv.COLOR_BGR2GRAY)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        d = cv.absdiff(gray, grayold)
        maximo = np.max(d)

        # Display the resulting frame
        cv.imshow('frame', d)
        frameold = frame.copy()

        if maximo > 100:
            cv.putText(frame, hora, (10,30), cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255))
            out.write(frame)
            frames += 1
            if frames >= LIMITE:
                out.release()
                break
        key = cv.waitKey(1)
        if key == ord('q'):
            rodando = False
            break
        elif key == ord("s"):
            break
# When everything done, release the capture
out.release()
cap.release()
cv.destroyAllWindows()
