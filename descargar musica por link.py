import tkinter as tk
import pytube
import os
import re
from youtubesearchpython import VideosSearch

# Configuration of the main window
ventana = tk.Tk()
ventana.title("Descarga de música de YouTube")
ventana.geometry("600x500")

# Function to add to the download list and start download
def agregar_a_lista():
    global lista_de_descargas, lista_links_validos

    # Get the YouTube link
    enlace_youtube = enlace_entrada.get()

    

    # Validate the link
    if validar_enlace(enlace_youtube):
        print(f"Enlace válido: {enlace_youtube}")
        lista_links_validos.append(enlace_youtube)
        try:
            video = pytube.YouTube(enlace_youtube)
            titulo_video = video.title
            artista = extraer_artista(titulo_video, video.description)
            
            descargar_musica(enlace_youtube, titulo_video, artista)

            # Clear the entry field
            enlace_entrada.delete(0, tk.END)

        except pytube.exceptions.VideoUnavailable as error:
            print(f"Error al validar el enlace: {error}")
            print(f"Enlace no se pudo validar: {enlace_youtube}")
    else:
        print(f"Enlace no válido: {enlace_youtube}")

# Function to validate YouTube link
def validar_enlace(enlace):
    return 'youtube.com' in enlace or 'youtu.be' in enlace

# Function to download music
def descargar_musica(enlace_youtube, titulo_video, artista):
    carpeta_musica = os.path.join(os.getcwd(), 'musica')  # Folder for music
    if not os.path.exists(carpeta_musica):
        os.mkdir(carpeta_musica)  # Create the folder if it doesn't exist

    

    # Remove invalid characters from the filename
    nombre_limpio = re.sub(r'[\\/*?:"<>|]', '', f"{artista} - {titulo_video}")
    
    # Rename with artist-song format
    nombre_archivo = f"{nombre_limpio}.mp3"

    # Download and save the audio file
    ruta_archivo = os.path.join(carpeta_musica, nombre_archivo)
    video = pytube.YouTube(enlace_youtube)
    audio = video.streams.filter(only_audio=True).first()
    
    if audio:
        
        audio.download(filename=nombre_archivo, output_path=carpeta_musica)
        

        if variable_renombrar.get():
            lista_descargas.insert(tk.END, f"{nombre_limpio} (Descargado)")
        else:
            lista_descargas.insert(tk.END, f"{titulo_video} (Descargado)")
        
        lista_descargas.itemconfig(tk.END, {'fg': 'green'})
    else:
       
        lista_descargas.insert(tk.END, f"{titulo_video} (Artista: {artista}) (No disponible)")

# Function to extract artist name
def extraer_artista(titulo_video, descripcion):
    if descripcion:
        # Using regular expression to extract artist from the description
        matches = re.search(r'Artista: (.+?)(?=\n|$)', descripcion)
        if matches:
            return matches.group(1)
    
    # Using youtubesearchpython to get artist name
    videosSearch = VideosSearch(titulo_video, limit=1)
    video = videosSearch.result()['result'][0]
    return video['channel']['name'] if video['channel']['name'] else "Artista desconocido"

# Panel for the YouTube link
panel_enlace = tk.Frame(ventana)
panel_enlace.pack(pady=10)

# Entry field for the YouTube link
enlace_entrada = tk.Entry(panel_enlace, width=70)
enlace_entrada.pack(side=tk.LEFT)

# Button "Añadir a la lista" (Add to List)
boton_agregar = tk.Button(panel_enlace, text="Añadir a la lista", command=agregar_a_lista)
boton_agregar.pack(side=tk.LEFT)

# Panel for the download list
panel_lista = tk.Frame(ventana)
panel_lista.pack(pady=10)

# Download list
lista_descargas = tk.Listbox(panel_lista, width=70)
lista_descargas.pack(side=tk.LEFT)

# Checkbox for artist-song renaming
variable_renombrar = tk.BooleanVar()
casilla_renombrar = tk.Checkbutton(ventana, text="Renombrar con formato (Artista) - (Canción)",
                                 variable=variable_renombrar)
casilla_renombrar.pack(pady=5)

# Global variables
lista_links_validos = []

# Run the graphical user interface
ventana.mainloop()

