import os
from src.convert import convert_to_wav
from src.transcribe import transcribe_audio
from src.fileutils import save_transcription
from src.windowGUI import create_window
from src.assemblyTranscribe import assemblyTranscribe, assemblyDiaritization

def main():
    #wav_file = "temp_audio.wav"
    #convert_to_wav(input_m4a,wav_file)

    #transcription = assemblyDiaritization("temp_audio.wav")

    #save_transcription(transcription, output_txt)

    create_window()



if __name__ == "__main__":
    #input_m4a = "ME PERDI EN EL MAR CON MI VECINO!.m4a"
    #output_txt = "transcription.txt"
    #main (input_m4a,output_txt)
    main()