from pydub import AudioSegment

def convert_m4a_to_wav(m4a_path, wav_path):
    """
    Converts an M4A file to WAV format using pydub.
    :param m4a_path: Path to input M4A file.
    :param wav_path: Path to output WAV file.
    """
    try:
        audio = AudioSegment.from_file(m4a_path, format="m4a")
        audio.export(wav_path, format="wav")
        print(f"Converted {m4a_path} to {wav_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
