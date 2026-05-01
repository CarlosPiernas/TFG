import subprocess
import os

def extraer_frames(ruta_mp4, nombre_carpeta):
    carpeta = f'assets/fondos/{nombre_carpeta}'
    os.makedirs(carpeta, exist_ok=True)
    
    subprocess.run([
        r'C:\ffmpeg\bin\ffmpeg.exe',
        '-i', ruta_mp4,
        f'{carpeta}/frame_%02d.png'
    ], check=True)
    
    print(f"Frames extraídos en {carpeta}")

# Uso:
extraer_frames('fondo_gacha_anomalia.mp4', 'fondo_gacha_anomalia')
extraer_frames('fondo_gacha_guardianes.mp4', 'fondo_gacha_guardianes')