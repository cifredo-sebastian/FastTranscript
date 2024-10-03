from src.assemblyTranscribe import assemblyDiaritization, assemblyTranscribe
from src.fileutils import save_transcription
from tkinter import filedialog, messagebox, ttk
from src.windowUtils import update_status
from src.config_manager import load_config
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

    config = load_config()
    
    update_status(status_label, "Transcribing, please wait...")
    if config['transcription']['speaker_labels']:
        transcription, error = assemblyDiaritization(file_path, config)
    else:
        transcription, error = assemblyTranscribe(file_path, config)
    
    if error:
        update_status(status_label, f"Error found: {error}")
        if config['alert']:
            messagebox.showinfo("Transcription Incomplete", f"Transcription failed.")
    else:
        update_status(status_label, f"Saving transcription to {output_path}...")
        save_transcription(transcription, output_path)
        update_status(status_label, f"Transcription saved to {output_path}")
        if config['alert']:
            messagebox.showinfo("Transcription Complete", f"Transcription saved to {output_path}")

    