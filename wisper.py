import whisper
import os
from pathlib import Path



model = whisper.load_model("base")
data = model.transcribe("out/audio_1.mp3")
print(data)



# FILE_LIST = sorted(
#     Path(BASE_DIR).iterdir(),
#     key=os.path.getmtime)

# for file in FILE_LIST:
#     audio = whisper.load_audio(file)
#     audio = whisper.pad_or_trim(audio)
#     result = model.transcribe(audio)
#     mel = whisper.log_mel_spectrogram(audio).to(model.device)
#     _, probs = model.detect_language(mel)
#     open("out.txt", "a").write(f"\n{file} - {result['text']}")

# def hello():


#     # Load audio
#     audio = whisper.load_audio("out/audio_5.wav")
#     audio = whisper.pad_or_trim(audio)

#     result = model.transcribe(audio)
#     mel = whisper.log_mel_spectrogram(audio).to(model.device)
#     _, probs = model.detect_language(mel)


#     print(f"\n\nDetected language: {max(probs, key=probs.get)}")
#     print(result["text"])

#     # model = whisper.load_model("base")
#     # audio = whisper.load_audio("/home/riuz/Descargas/test-audio.mp3")
#     # audio = whisper.pad_or_trim(audio)

#     # mel = whisper.log_mel_spectrogram(audio).to(model.device)
#     # _, probs = model.detect_language(mel)
#     # options = whisper.DecodingOptions()
#     # result = whisper.decode(model, mel, options)
#     # print(f"Detected language: {max(probs, key=probs.get)}")

