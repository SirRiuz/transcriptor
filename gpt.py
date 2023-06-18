import pyaudio
import wave

# Configura los parámetros de grabación de audio
chunk_size = 1024  # número de frames por buffer
sample_rate = 44100  # tasa de muestreo en Hz
record_seconds = 5  # duración de la grabación en segundos

# Inicializa PyAudio
p = pyaudio.PyAudio()

# Abre el stream de audio para capturar datos del micrófono
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate,
                input=True, frames_per_buffer=chunk_size)

print("* Capturando audio...")

# Lee los datos del stream de audio en tiempo real y los guarda en un buffer
frames = []
for i in range(0, int(sample_rate / chunk_size * record_seconds)):
    data = stream.read(chunk_size)
    frames.append(data)

print("* Grabación terminada")

# Detiene y cierra el stream de audio
stream.stop_stream()
stream.close()
p.terminate()

# Guarda los datos de audio en un archivo WAV
wf = wave.open("audio.wav", "wb")
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(sample_rate)
wf.writeframes(b"".join(frames))
wf.close()