import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import datetime
from threading import Thread
import queue
import wave
import hashlib



chunk_size = 1024  # número de frames por buffer
sample_rate = 44100  # tasa de muestreo en Hz
record_seconds = 5  # duración de la grabación en segundos

# Configura los parámetros del espectrograma
NFFT = 1024  # longitud de la ventana de transformada de Fourier
Fs = 44100  # tasa de muestreo en Hz
noverlap = NFFT // 2  # superposición de ventanas
audio_detect_lumbral = 300

chunk_size = 1024  # número de frames por buffer
sample_rate = 44100  # tasa de muestreo en Hz
record_seconds = 5  # duración de la grabación en segundos




def audio_stream(cola: queue.Queue):
    frames = []
    no_track_counter = 0
    frame_list = []
    # Inicializa PyAudio
    p = pyaudio.PyAudio()


    # Abre el stream de audio para capturar datos del micrófono
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate,
                    input=True, frames_per_buffer=chunk_size)

    print("* Capturando audio...")
    # Lee los datos del stream de audio en tiempo real y los guarda en un buffer


    while True:
        data = stream.read(chunk_size)
        #frames.append(data)
        data_np = np.frombuffer(data, dtype=np.int16) / 32768.0  # convierte los datos a un array numpy de punto flotante
        spectrum = np.abs(np.fft.fft(data_np))[:chunk_size // 2]  # calcula la magnitud del espectro
        frequency = np.argmax(spectrum) * sample_rate / chunk_size  # calcula la frecuencia correspondiente al índice del máximo del espectro

        if frequency > audio_detect_lumbral:
            print("CAPTURE AUDIO")
            frame_list.append(data)
            no_track_counter = 0

        if no_track_counter > 30 and len(frame_list) > 10:
            print(len(frame_list))
            print("\n\n")
            cola.put({
                "frequency": frequency,
                "data": frame_list})
            frame_list = []
            no_track_counter = 0
            stream.stop_stream()
            stream.close()
            p.terminate()
            return

        no_track_counter = no_track_counter + 1


def proceess(cola:queue.Queue):
    a = pyaudio.PyAudio()
    while True:
        data:list = cola.get().get("data")
        file_name = hashlib.sha256(data.__str__().encode()).hexdigest()
        #print("Capture ->", f"{file_name}.wav")
        wf = wave.open(f"out/{file_name}.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(a.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(data))
        wf.close()

cola = queue.Queue()
Thread(target=audio_stream, args=(cola,)).start()
Thread(target=proceess, args=(cola,)).start()
