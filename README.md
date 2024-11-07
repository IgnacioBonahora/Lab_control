# Sistema de Acceso Basado en Reconocimiento Facial

desarollo de un sistema de acceso para un laboratorio que utiliza reconocimiento facial para verificar la identidad de los usuarios en tiempo real. Está desarrollado en Python y utiliza las librerías `face_recognition`, `OpenCV` (`cv2`) y `Tkinter` para crear una interfaz gráfica simple y amigable para la administración de registros y el control de acceso. El sistema permite registrar y verificar a los usuarios mediante sus fotos, brindando acceso solo a los individuos registrados.

## Características

- **Registro de Usuarios**: Permite registrar nuevos usuarios tomando una foto en tiempo real y guardándola como imagen de referencia.
- **Verificación en Tiempo Real**: Compara la imagen de referencia del usuario con una imagen capturada en tiempo real para conceder o denegar acceso.
- **Interfaz Gráfica (GUI)**: Incluye una interfaz gráfica para facilitar el uso del sistema.
- **Protección de Registro**: Solo permite el registro de nuevos usuarios si se introduce una contraseña de administrador correcta.
- **Registro en CSV**: Almacena registros de cada intento de acceso y cada nuevo registro de usuario en archivos CSV.

## Requisitos

- Python 3.x
- Librerías de Python:
  - `face_recognition`
  - `opencv-python`
  - `tkinter` (generalmente incluida con Python en sistemas operativos de escritorio)
  - `csv` (nativa de Python)
  
Puedes instalar `face_recognition` y `opencv-python` ejecutando:
```bash
pip install face_recognition opencv-python
