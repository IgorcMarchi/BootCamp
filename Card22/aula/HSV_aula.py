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

    # cor azul
    low_blue = np.array([94, 80, 2]) # Limite inferior da cor azul
    high_blue = np.array([126, 255, 255]) # Limite superior da cor azul
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue) # Cria uma máscara para a cor azul
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask) # Aplica a máscara na imagem original

    # cor verde
    low_green = np.array([25,52, 72]) # Limite inferior da cor verde
    high_green = np.array([102, 255, 255]) # Limite superior
    green_mask = cv2.inRange(hsv_frame, low_green, high_green) # Cria uma máscara para a cor verde
    green = cv2.bitwise_and(frame, frame, mask=green_mask) # Aplica a máscara na imagem original

    # Todas as cores exceto o branco
    low = np.array([0, 42, 0]) # Limite inferior da cor branca
    high = np.array([179, 255, 255]) # Limite superior da cor branca
    mask = cv2.inRange(hsv_frame, low, high) # Cria uma máscara para todas as cores exceto o branco
    result = cv2.bitwise_and(frame, frame, mask=mask) # Aplica a mascara na imagem original

    cv2.imshow('Frame', frame) # Exibe a imagem original
    cv2.imshow('Result', result) # Exibe a imagem com todas as cores menos a  branca destacada

    key = cv2.waitKey(1) # Encerra a camera
    if key == 27:
        break