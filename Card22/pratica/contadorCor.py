import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Abre a câmera

while True:
    _, frame = cap.read() # Captura um frame da câmera
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Converte de BGR para HSV

    # cor vermelha
    low_red = np.array([161, 155, 84]) # Limite inferior da cor vermelha
    high_red = np.array([179, 255, 255]) # Limite superior da cor vermelha
    red_mask = cv2.inRange(hsv_frame, low_red, high_red) # Cria uma máscara para a cor vermelha
    red = cv2.bitwise_and(frame, frame, mask=red_mask) # Aplica a máscara na imagem original

    # Cor amarela
    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # cor verde
    low_green = np.array([25,52, 72]) # Limite inferior da cor verde
    high_green = np.array([102, 255, 255]) # Limite superior
    green_mask = cv2.inRange(hsv_frame, low_green, high_green) # Cria uma máscara para a cor verde
    green = cv2.bitwise_and(frame, frame, mask=green_mask) # Aplica a máscara na imagem original

    # cor azul
    low_blue = np.array([94, 80, 2]) # Limite inferior da cor azul
    high_blue = np.array([126, 255, 255]) # Limite superior da cor azul
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue) # Cria uma máscara para a cor azul
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask) # Aplica a máscara na imagem original

    # conta os pixels de cada cor
    vermelho = cv2.countNonZero(red_mask)
    verde = cv2.countNonZero(green_mask)
    amarelo = cv2.countNonZero(yellow_mask)
    azul = cv2.countNonZero(blue_mask)

    # exibe a quantidade de pixels de cada cor na tela
    mensagemVerm = f"Vermelho: {vermelho}"
    mensagemVerd = f"Verde: {verde}"
    mensagemAmel = f"Amarelo: {amarelo}"
    mensagemAzul = f"Azul: {azul}"
    # Descobre o maior valor
    maior = max(vermelho, verde, amarelo, azul)

    # Branco por padrão
    corVermelho = (255, 255, 255)
    corVerde = (255, 255, 255)
    corAmarelo = (255, 255, 255)
    corAzul = (255, 255, 255)

    # Muda a cor do texto que tiver o maior valor
    if vermelho == maior:
        corVermelho = (0, 0, 255)

    elif verde == maior:
        corVerde = (0, 255, 0)

    elif amarelo == maior:
        corAmarelo = (0, 255, 255)

    elif azul == maior:
        corAzul = (255, 0, 0)

    # exibe a quantidade de pixels de cada cor na tela
    cv2.putText(frame,mensagemVerm,(30, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(corVermelho),2)
    cv2.putText(frame,mensagemVerd,(30, 100),cv2.FONT_HERSHEY_SIMPLEX,1,(corVerde),2)
    cv2.putText(frame,mensagemAmel,(30, 150),cv2.FONT_HERSHEY_SIMPLEX,1,(corAmarelo),2)
    cv2.putText(frame,mensagemAzul,(30, 200),cv2.FONT_HERSHEY_SIMPLEX,1,(corAzul),2)


    cv2.imshow("Contador", frame) # Exibe a imagem original

    key = cv2.waitKey(1) # Encerra a camera
    if key == 27:
        break