#IMPORTAR PAQUETES
from pytube import YouTube
import os

#INPUT URL
yt = YouTube(str(input("Introduce el url del video: \n>>")))

#Extraer audio
video = yt.streams.filter(only_audio = True).first()

#Verificar el destino para guardar el archivo
print("Introduce el destino (deja en blanco el directorio actual)")
destination = str(input(">> ")) or '.'

#Descargar archivo
out_file = video.download(output_path = destination)

#Guardar archivo
base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)

#Resulado
print(yt.title + "ha sido descargado exitosamente en formato mp3")
