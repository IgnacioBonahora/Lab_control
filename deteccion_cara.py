import cv2
import face_recognition

# Inicia la captura de video desde la cámara (0 para la cámara principal)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    print("Cámara iniciada. Presiona 'q' para salir.")

while True:
    # Lee un cuadro de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el cuadro de la cámara.")
        break

    # Convierte el cuadro a RGB (face_recognition trabaja en RGB)
    rgb_frame = frame[:, :, ::-1]

    # Encuentra todas las ubicaciones de rostros en el cuadro
    face_locations = face_recognition.face_locations(rgb_frame)

    # Dibuja un cuadro alrededor de cada rostro detectado
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Muestra el cuadro en la ventana
    cv2.imshow("Detección de Rostros en Tiempo Real", frame)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
