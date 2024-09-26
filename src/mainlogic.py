from src.convert import convert_to_wav
from src.assemblyTranscribe import assemblyDiaritization
from src.fileutils import save_transcription
from src.windowUtils import update_status
import os


def main_process(file_path, file_type, output_path,status_label):
    # Convert File

    # update_status(status_label,f"Processing {file_path}")
    # if file_path.startswith('{') and file_path.endswith('}'):
    #     file_path = file_path[1:-1]
    # if (file_type != 'wav'):
    #     wav_file = "temp_audio.wav"
    #     update_status(status_label,f"Converting {file_path} from {file_type} to WAV")
    #     convert_to_wav(file_path,file_type,wav_file)
    #     update_status(status_label,f"Converted {file_path}")
    # else:
    #     wav_file = file_path
    
    update_status(status_label,f"Transcribing...")
    transcription = assemblyDiaritization(file_path)
    
    update_status(status_label, f"Saving transcription to {output_path}...")
    save_transcription(transcription, output_path)
    update_status(status_label, f"Transcription saved to {output_path}.")

    