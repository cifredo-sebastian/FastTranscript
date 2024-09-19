import os
from src.convert import convert_m4a_to_wav
from src.transcribe import transcribe_audio
from src.fileutils import save_transcription

def main(input_m4a,output_txt):
    #wav_file = "temp_audio.wav"
    #convert_m4a_to_wav(input_m4a,wav_file)

    transcription = transcribe_audio("temp_audio.wav")

    save_transcription(transcription, output_txt)



if __name__ == "__main__":
    input_m4a = "videoplayback.m4a"
    output_txt = "transcription.txt"
    main (input_m4a,output_txt)