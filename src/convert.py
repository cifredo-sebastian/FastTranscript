from pydub import AudioSegment

def convert_to_wav(file_path, file_type, wav_path):
    """
    Converts a audio file to WAV format using pydub.
    :param file_path: Path to input audio file.
    :param file_type: Imported audio file type
    :param wav_path: Path to output WAV file.
    """
    try:
        #print(f"Converting {file_path} from {file_type} to WAV")
        audio = AudioSegment.from_file(file_path, format=file_type)
        audio.export(wav_path, format="wav")
        #print(f"Converted {file_path} to {wav_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
