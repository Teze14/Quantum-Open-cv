# Se importan las librerías
import cv2   # Open cv para tener la visón por computadora en tiempo real y poder detectar a los ArUcos
import numpy as np    # Numpy para introducir matrices y determinar si cumplen con la condición (linea 25)
import math          # Math para usar raices cuadradas

parametros = cv2.aruco.DetectorParameters()    # Se configuran los parametros para detectar ArUcos
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)    # Se establece el tipo de ArUco que se utilizará (5x5_250)

camara = cv2.VideoCapture(0)   # Se establece a la camara 0 como la camara a utilizar

# Se pone como constante el tamaño físico del marcador ArUco en centímetros
marcador_cm = 20.0

# Loop para detectar cada fotograma 
while True:
    ret, frame = camara.read() # ret indica si hay captura de fotogramas y frame se encarga de utilizar cada fotograma y capturarlos de la camara 

    if not ret:   # Condicional por si no hay fotogramas, se pueda dar el mensaje del problema
        print("No se pudo capturar el fotograma.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Se cambian las tonalidades de los fotogramas a escalas de gris para que haya una mejor captura.

    esquinas, ids, _ = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros) # Se detectan los ARucos y se devuelven sus esquinas y su id

    # Condicional para determinar si hay un ArUco en cámara
    if np.all(ids is not None):
        # Loop que recorre todas las esquinas detectadas del ArUco
        for i, esquina in enumerate(esquinas):
            id_marcador = ids[i][0]
            x, y = map(int, esquina[0][0])  # Convertir a enteros
            cv2.putText(frame, str(id_marcador), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Se imprime en el frame el id del ArUco

            # Calcular el tamaño del marcador en píxeles
            marcador_pixeles = max(esquina[0][0]) - min(esquina[0][0])

            # Calcular la distancia aproximada en centímetros
            distancia_aprox_cm = (marcador_cm * 100) / marcador_pixeles

            # Calcular el centro del ArUco para saber comparar con los puntos de la izquierda y derecha
            centro_x = int((esquina[0][0][0] + esquina[0][2][0]) / 2)
            centro_y = int((esquina[0][0][1] + esquina[0][2][1]) / 2)

            # Calcular los puntos más a la izquierda y a la derecha para comparar con punto central
            punto_izquierda = (int(esquina[0][0][0]), centro_y)
            punto_derecha = (int(esquina[0][2][0]), centro_y)

            # Calcular la distancia entre el punto central y los puntos izquierda y derecha para saber hacia donde se debe de mover el robot
            distancia_centro_izquierda = math.sqrt((centro_x - punto_izquierda[0]) ** 2 + (centro_y - punto_izquierda[1]) ** 2)
            distancia_centro_derecha = math.sqrt((centro_x - punto_derecha[0]) ** 2 + (centro_y - punto_derecha[1]) ** 2) # Se utilizó la fórmula de distancia euclidiana entre dos puntos en un plano 

            # Mostrar en el frame la distancia, el centro y los puntos izquierda y derecha 
            cv2.putText(frame, f'Distancia: {distancia_aprox_cm:.2f} cm', (x, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #cv2.FONT_HERSHEY_SIMPLEX se utilizó para poner formato al texto
            cv2.circle(frame, (centro_x, centro_y), 4, (0, 0, 255), -1)
            cv2.circle(frame, punto_izquierda, 4, (255, 0, 0), -1)
            cv2.circle(frame, punto_derecha, 4, (255, 0, 0), -1)

            # Condicionales que indican en el frame hacia dónde se debe de mover el robot
            if distancia_centro_izquierda < distancia_centro_derecha:
                cv2.putText(frame, f'Ve a la izquierda', (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif distancia_centro_derecha < distancia_centro_izquierda:
                cv2.putText(frame, f'Ve a la derecha', (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                cv2.putText(frame, f'Estas centrado', (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Mostrar las distancias en el fotograma del centro hacia la izquierda y hacia la derecha
            cv2.putText(frame, f'Distancia Centro a Izquierda: {distancia_centro_izquierda:.2f} px', (x, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f'Distancia Centro a Derecha: {distancia_centro_derecha:.2f} px', (x, y + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar únicamente el fotograma si no se detecta ningún ArUco
    cv2.imshow("Frame", frame)

    # Sirve para terminar el programa utilizando la tecla (esc) que tiene relación con el 27
    k = cv2.waitKey(1)
    if k == 27:
        break

camara.release() # Se libera la cámara
cv2.destroyAllWindows() # Se cierran todas las ventanas
