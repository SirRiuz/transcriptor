import pyaudio
import soundfile as sf
import numpy as np
import datetime
import wave
import audioop
import time
from pydub import AudioSegment
import socket
import speech_recognition as sr


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024
SILENCE_THRESHOLD = 1000  # Umbral de silencio (ajusta según tus necesidades)
SEGMENT_DURATION = 5  # Duración de los segmentos de audio guardados en segundos

# Inicializar PyAudio
audio = pyaudio.PyAudio()

# Variables de estado
audio_data = []
silence_counter = 0
filename_counter = 1


def enviar_segmento_audio(data):
    host = '127.0.0.1'  # Dirección IP del servidor
    port = 8000  # Puerto en el que el servidor está escuchando

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(data)

def guardar_segmento_audio(data):
    global filename_counter
    filename = f"out/audio_{filename_counter}.wav"
    filename_counter += 1

    # audio_segment = AudioSegment(
    #     data,
    #     sample_width=audio.get_sample_size(FORMAT),
    #     frame_rate=RATE,
    #     channels=CHANNELS)
    # audio_segment.export(filename, format="mp3")

    channels = 1  # Mono
    sample_width = 2  # 16 bits por muestra
    sample_rate = 44100  # Tasa de muestreo de 44.1 kHz

    # Crear objeto de archivo WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(data)


def callback(in_data, frame_count, time_info, flag):
    # Convertir los datos de audio a un array de NumPy
    global silence_counter, audio_data
    audio_np = np.frombuffer(in_data, dtype=np.int16)

    # Convertir los datos de audio a un array de NumPy
    audio_np = np.frombuffer(in_data, dtype=np.int16)

    # Calcular la energía del audio
    rms = audioop.rms(audio_np, 2)

    if rms >= 1050:
        TIME = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{TIME}] > Tracking audio - {len(audio_data)}")
        silence_counter = 0
    else:
        silence_counter += 1
        
    if silence_counter >= 15:
        if len(audio_data) > 5:
            print("[I] > Save audio tracking\n")
            #enviar_segmento_audio(b''.join(audio_data))
            guardar_segmento_audio(b''.join(audio_data))
            #print(b''.join(audio_data))

        audio_data = []

    #print(b''.join(audio_data))
    audio_data.append(in_data)

    return (in_data, pyaudio.paContinue)

# Abrir el stream de audio
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE,
                    stream_callback=callback)

stream.start_stream()
while stream.is_active():
    pass



stream.stop_stream()
stream.close()
audio.terminate()
client_socket.close()

