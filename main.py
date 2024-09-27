import os
from src.windowGUI import create_window

def main():
    #wav_file = "temp_audio.wav"
    #convert_to_wav(input_m4a,wav_file)

    #transcription = assemblyDiaritization(input_m4a)

    #save_transcription(transcription, output_txt)

    create_window()



if __name__ == "__main__":
    input_m4a = "Interrogatorio padre de Rey Oquendo.mp3"
    output_txt = "transcription.txt"
    #main (input_m4a,output_txt)
    main()