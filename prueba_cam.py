import cv2

def mostrar_video_camara_1():
    # Intenta acceder a la cámara con índice 1
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara 1.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el video.")
            break

        # Muestra el video en una ventana
        cv2.imshow("Cámara 1", frame)

        # Salir con la tecla "q"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la cámara y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mostrar_video_camara_1()
