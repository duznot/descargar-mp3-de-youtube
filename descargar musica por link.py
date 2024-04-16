import tkinter as tk
from tkinter import filedialog
import pytube

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Descarga de música de YouTube")
ventana.geometry("500x500")

# Entrada de texto para el enlace o archivo
enlace_entrada = tk.Entry(ventana, width=50)
enlace_entrada.pack(pady=10)

# Botón para explorar la carpeta de destino
def seleccionar_carpeta():
    ruta_carpeta = filedialog.askdirectory()
    carpeta_entrada.set(ruta_carpeta)

boton_explorar = tk.Button(ventana, text="Explorar", command=seleccionar_carpeta)
boton_explorar.pack(pady=5)

# Entrada de texto para la carpeta de destino
carpeta_entrada = tk.StringVar()
carpeta_entrada_widget = tk.Entry(ventana, textvariable=carpeta_entrada, width=50)
carpeta_entrada_widget.pack(pady=5)

# Botón para iniciar la descarga
def descargar():
    enlace_youtube = enlace_entrada.get()
    carpeta_destino = carpeta_entrada.get()

    try:
        # Import os module
        import os

        # Descargar video de YouTube usando pytube
        video = pytube.YouTube(enlace_youtube)
        audio = video.streams.filter(only_audio=True).first()

        # Extraer audio y guardar en formato MP3
        titulo_video = video.title
        nombre_archivo = f"{titulo_video}.mp3"
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
        audio.download(filename=ruta_archivo)

        # Actualizar lista de descargas
        lista_descargas.insert(tk.END, f"Descarga completada: {titulo_video}")

    except Exception as error:
        lista_descargas.insert(tk.END, f"Error al descargar: {error}")


boton_descargar = tk.Button(ventana, text="Descargar", command=descargar)
boton_descargar.pack(pady=10)

# Lista de descargas
lista_descargas = tk.Listbox(ventana, width=50)
lista_descargas.pack(pady=10)

# Ejecución de la interfaz gráfica
ventana.mainloop()

