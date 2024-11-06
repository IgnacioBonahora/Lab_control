import cv2
import face_recognition
import tkinter as tk
from tkinter import messagebox
import os

IMAGENES_DIR = "./imagenes_alumnos/"
ADMIN_PASSWORD_FILE = "admin_password.txt"

def cargar_imagen_alumno(nro_alumno):
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

def verificar_acceso(nro_alumno):
    print("Cargando imagen del alumno...")
    encoding_alumno = cargar_imagen_alumno(nro_alumno)
    print(encoding_alumno)
    if encoding_alumno is None:
        messagebox.showerror("Error", "Alumno no registrado o imagen inválida.")
        return

    cap = cv2.VideoCapture(1)
    acceso_concedido = False

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    print("Iniciando verificación de acceso...")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el cuadro de la cámara.")
            break

        rgb_frame = frame[:, :, ::-1]

        # Procesar cada 10 cuadros para reducir carga
        if frame_count % 10 == 0:
            try:
                face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=1)
                print(f"Rostros detectados: {len(face_locations)}")

                if face_locations:
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    for face_encoding, face_location in zip(face_encodings, face_locations):
                        resultado = face_recognition.compare_faces([encoding_alumno], face_encoding)
                        top, right, bottom, left = face_location

                        if resultado[0]:
                            color = (0, 255, 0)  # Verde si coincide
                            cv2.putText(frame, "Acceso concedido", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                        color, 2)
                            acceso_concedido = True
                            print("Acceso concedido")
                        else:
                            color = (0, 0, 255)  # Rojo si no coincide
                            cv2.putText(frame, "Acceso denegado", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                        color, 2)
                            print("Acceso denegado")

                        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                else:
                    print("No se detectaron rostros en este cuadro.")
            except Exception as e:
                print(f"Error durante la verificación del rostro: {e}")

        cv2.imshow("Verificación de acceso en tiempo real", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord("q") or acceso_concedido:
            print("Saliendo de la verificación de acceso.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Cámara liberada y ventanas cerradas.")

def registrar_alumno(nro_alumno):
    if os.path.exists(os.path.join(IMAGENES_DIR, f"{nro_alumno}.jpg")):
        messagebox.showerror("Error", "Número de alumno ya registrado.")
        return

    cap = cv2.VideoCapture(1)  # Índice 0 para usar la cámara principal
    ret, frame = cap.read()
    cap.release()

    if ret:
        imagen_path = os.path.join(IMAGENES_DIR, f"{nro_alumno}.jpg")
        cv2.imwrite(imagen_path, frame)
        messagebox.showinfo("Éxito", "Alumno registrado exitosamente.")
    else:
        messagebox.showerror("Error", "Error al capturar imagen.")

def solicitar_registro():
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
    with open(ADMIN_PASSWORD_FILE, "r") as f:
        return f.read().strip() == password

def iniciar_interfaz():
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
