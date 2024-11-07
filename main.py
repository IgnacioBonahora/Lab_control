import cv2
import face_recognition
import tkinter as tk
from tkinter import messagebox
import os

IMAGENES_DIR = "./imagenes_alumnos/"
ADMIN_PASSWORD_FILE = "admin_password.txt"


def cargar_imagen_alumno(nro_alumno):
    """
    Carga la imagen de un alumno específico y obtiene su encoding facial.
    """
    try:
        imagen_path = os.path.join(IMAGENES_DIR, f"{nro_alumno}.jpg")
        imagen_alumno = face_recognition.load_image_file(imagen_path)
        encoding = face_recognition.face_encodings(imagen_alumno)
        if encoding:
            return encoding[0]
        else:
            print(f"No se encontraron rostros en la imagen del alumno {nro_alumno}")
            return None
    except Exception as e:
        print(f"Error al cargar imagen para el alumno {nro_alumno}: {e}")
        return None


def comparar_imagen_con_captura(encoding_alumno):
    """
    Captura una imagen en vivo y la compara con la imagen de referencia del alumno.
    """
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: No se pudo capturar la imagen.")
        return

    # Codificar la imagen capturada en tiempo real
    desconocida_encoding = face_recognition.face_encodings(frame)

    if len(desconocida_encoding) == 0:
        print("No se detectó ninguna cara.")
        return

    # Comparar las dos imágenes
    resultado = face_recognition.compare_faces([encoding_alumno], desconocida_encoding[0])

    if resultado[0]:
        print("¡Las caras coinciden! Acceso concedido.")
        cv2.putText(frame, "Acceso concedido", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        print("Las caras no coinciden. Acceso denegado.")
        cv2.putText(frame, "Acceso denegado", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Mostrar el resultado
    cv2.imshow("Verificación de acceso en tiempo real", frame)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()


def verificar_acceso(nro_alumno):
    """
    Verifica el acceso de un alumno comparando su foto registrada con una foto en tiempo real.
    """
    encoding_alumno = cargar_imagen_alumno(nro_alumno)
    if encoding_alumno is None:
        print("Error: No se pudo cargar el encoding del alumno.")
        return

    comparar_imagen_con_captura(encoding_alumno)


def registrar_alumno(nro_alumno):
    """
    Registra un nuevo alumno tomando una foto y guardándola con su número de identificación.
    """
    if os.path.exists(os.path.join(IMAGENES_DIR, f"{nro_alumno}.jpg")):
        messagebox.showerror("Error", "Número de alumno ya registrado.")
        return

    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    cap.release()

    if ret:
        imagen_path = os.path.join(IMAGENES_DIR, f"{nro_alumno}.jpg")
        cv2.imwrite(imagen_path, frame)
        messagebox.showinfo("Éxito", "Alumno registrado exitosamente.")
    else:
        messagebox.showerror("Error", "Error al capturar imagen.")


def solicitar_registro():
    """
    Solicita la contraseña de administrador y el número de alumno para registrar una nueva imagen.
    """

    def registrar():
        password = entry_password.get()
        if verificar_password(password):
            nro_alumno = entry_alumno.get()
            if nro_alumno:
                registrar_alumno(nro_alumno)
                ventana_registro.destroy()
            else:
                messagebox.showerror("Error", "Número de alumno no proporcionado.")
        else:
            messagebox.showerror("Error", "Contraseña de administrador incorrecta.")

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Alumno")
    ventana_registro.geometry("400x200")

    tk.Label(ventana_registro, text="Número de Alumno:").pack(pady=10)
    entry_alumno = tk.Entry(ventana_registro)
    entry_alumno.pack()

    tk.Label(ventana_registro, text="Contraseña de Administrador:").pack(pady=10)
    entry_password = tk.Entry(ventana_registro, show="*")
    entry_password.pack()

    tk.Button(ventana_registro, text="Registrar", command=registrar).pack(pady=20)


def verificar_password(password):
    """
    Verifica si la contraseña proporcionada es correcta.
    """
    with open(ADMIN_PASSWORD_FILE, "r") as f:
        return f.read().strip() == password


def iniciar_interfaz():
    """
    Inicia la interfaz gráfica del sistema.
    """
    ventana = tk.Tk()
    ventana.title("Sistema de Acceso")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Número de Alumno:", font=("Arial", 14)).pack(pady=20)
    entry_nro_alumno = tk.Entry(ventana, font=("Arial", 12))
    entry_nro_alumno.pack(pady=10)

    def verificar():
        nro_alumno = entry_nro_alumno.get()
        if nro_alumno:
            verificar_acceso(nro_alumno)

    tk.Button(ventana, text="Verificar Acceso", command=verificar, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana, text="Registrar Alumno", command=solicitar_registro, font=("Arial", 12)).pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    if not os.path.exists(ADMIN_PASSWORD_FILE):
        with open(ADMIN_PASSWORD_FILE, "w") as f:
            f.write("admin123")

    if not os.path.exists(IMAGENES_DIR):
        os.makedirs(IMAGENES_DIR)

    iniciar_interfaz()
