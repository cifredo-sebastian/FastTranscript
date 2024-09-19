import os
from src.convert import convert_m4a_to_wav
from src.transcribe import transcribe_audio
from src.fileutils import save_transcription
from src.assemblyTranscribe import assemblyTranscribe, assemblyDiaritization

def main(input_m4a,output_txt):
    #wav_file = "temp_audio.wav"
    #convert_m4a_to_wav(input_m4a,wav_file)

    transcription = assemblyDiaritization("temp_audio.wav")

    save_transcription(transcription, output_txt)



if __name__ == "__main__":
    input_m4a = "R6 Veronica Rivera.m4a"
    output_txt = "transcription.txt"
    main (input_m4a,output_txt)