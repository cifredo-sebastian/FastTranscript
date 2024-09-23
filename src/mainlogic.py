from src.convert import convert_to_wav
from src.assemblyTranscribe import assemblyDiaritization
from src.fileutils import save_transcription
import os


def main_process(file_path, file_type, config, output_path):
    # Convert File

    print(f"Processing {file_path}")
    if file_path.startswith('{') and file_path.endswith('}'):
        file_path = file_path[1:-1]
    if (file_type != 'wav'):
        wav_file = "temp_audio.wav"
        convert_to_wav(file_path,file_type,wav_file)
    else:
        wav_file = file_path
    
    transcription = assemblyDiaritization(wav_file)
    
    save_transcription(transcription, output_path)


    