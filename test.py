import speech_recognition as sr

# Crear un objeto de reconocimiento de voz
r = sr.Recognizer()

# Especificar la ruta del archivo de audio
archivo_audio = "out/audio_4.wav"

# Abrir el archivo de audio
with sr.AudioFile(archivo_audio) as source:
    # Cargar el audio en memoria
    audio = r.record(source)

    try:
        # Utilizar el reconocimiento de voz para convertir el audio a texto
        texto = r.recognize_google(audio, language='es')

        # Imprimir el texto obtenido
        print("Texto reconocido:")
        print(texto)

    except sr.UnknownValueError:
        print("No se pudo reconocer el audio")

    except sr.RequestError as e:
        print("Error al enviar la solicitud al servicio de reconocimiento de voz; {0}".format(e))