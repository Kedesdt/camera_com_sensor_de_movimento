import numpy as np
import cv2 as cv
import time, os

def  main():
    FPS = 30.0
    LIMITE = FPS * 60 * 1
    TEMPO_PERSISTENCIA = 1 # Segundos
    rodando = True
    TIME_LAPSE = 20 # Segundos

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    frameold = None
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    #fourcc = cv.VideoWriter_fourcc('M','J','P','G')
    #print(fourcc)
    #fourcc = -1


    while rodando:

        print("""
        Iniciando.....
        Os arquivos são alvos em videos de 3 minutos,
        para salvar o vídeo atual altes dos 3 minutos
        pressione "s"
        para terminar pressione "q"
    
            """)

        frames = 0
        f = 0
        ret, frame = cap.read()
        largura = frame.shape[1]
        altura = frame.shape[0]
        out = cv.VideoWriter(".." + os.sep + "arquivos" + os.sep + "videos_sensor_de_movimento" + os.sep + time.strftime("%Y%m%d%H%M%S.avi", time.localtime()), fourcc, FPS, (largura,  altura))

        persistencia = 0
        while rodando:
            hora = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            # Capture frame-by-frame
            ret, frame = cap.read()
            f += 1
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

            frameold = frame.copy()

            if maximo > 100:
                persistencia = TEMPO_PERSISTENCIA * FPS

            if persistencia > 0 or f % (TIME_LAPSE * FPS) == 0:
                persistencia -= 1
                cv.circle(frame, (20, 20), 5, (0, 0, 255), -1)
                cv.imshow('Imagem', frame)
                cv.putText(frame, hora, (30, 30), cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255))

                out.write(frame)
                frames += 1
                f = 0
                if frames >= LIMITE:
                    out.release()
                    break
            else:
                cv.imshow('Imagem', frame)
            key = cv.waitKey(30)

            if key == ord('q'):
                rodando = False
                break
            elif key == ord("s"):
                break
    # When everything done, release the capture
    out.release()
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()