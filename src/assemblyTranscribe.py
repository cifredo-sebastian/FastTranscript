# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.
import time
import threading
import assemblyai as aai
import json
from src.config_manager import load_config

#config = load_config()

# Replace with your API key
#aai.settings.api_key = config['api_key']

# URL of the file to transcribe
#FILE_URL = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

# def display_loading_message():
#     print("Loading...", end='', flush=True)
#     while loading:
#         print(".", end='', flush=True)
#         time.sleep(1)
#     print("\n")

def ms_to_timestamp(ms):
    """Convert milliseconds to a timestamp in minutes:seconds format."""
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def assemblyTranscribe(file_path, config):
    #config = load_config()

    # Replace with your API key
    aai.settings.api_key = config['api_key']

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return(transcript.error)
    else:
        return(transcript.text)


def assemblyDiaritization(file_path, config):
    global loading
    #config = load_config()

    # Replace with your API key
    aai.settings.api_key = config['api_key']

    #loading = True

    # Start the loading message in a separate thread
    #loading_thread = threading.Thread(target=display_loading_message)
    #loading_thread.start()

    print('Loading...')
    
    start_time = time.time()

    speaker_labels = config['transcription']['speaker_labels']
    language_code = config['transcription']['language_code']
    timestamp_format = config['transcription']['timestamp_format']

    transcription_config = aai.TranscriptionConfig(speaker_labels=speaker_labels, language_code=language_code)

    try:
        print("Transcription started.")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(
        file_path,
        config=transcription_config
        )
        
    except Exception as e:
        print("Found error")
        return None, str(e)

    # Stop the loading message
    #loading = False
    #loading_thread.join()  # Wait for the loading thread to finish

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print(f"Transcription completed in {elapsed_time:.2f} seconds.")

    lines = []
    try:
        for utterance in transcript.utterances:
            start_time = ms_to_timestamp(utterance.start)
            end_time = ms_to_timestamp(utterance.end)
            timestamp = (
                f"[{start_time} - {end_time}]" if timestamp_format == "start-end" 
                else f"[{start_time}]" if timestamp_format == "start" 
                else f""
            )
            lines.append(f"{timestamp} Speaker {utterance.speaker}: {utterance.text}")
    except Exception as e:
        print("Error in transcription")
        return None, str(e)

    return '\n\n'.join(lines), None