# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.
import time
import threading
import assemblyai as aai
import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('config.json')

# Replace with your API key
aai.settings.api_key = config['api_key']

# URL of the file to transcribe
#FILE_URL = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

def display_loading_message():
    print("Loading...", end='', flush=True)
    while loading:
        print(".", end='', flush=True)
        time.sleep(1)
    print("\n")

def ms_to_timestamp(ms):
    """Convert milliseconds to a timestamp in minutes:seconds format."""
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def assemblyTranscribe(file_path):

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return(transcript.error)
    else:
        return(transcript.text)


def assemblyDiaritization(file_path):
    global loading
    #loading = True

    # Start the loading message in a separate thread
    #loading_thread = threading.Thread(target=display_loading_message)
    #loading_thread.start()
    
    start_time = time.time()

    speaker_labels = config['transcription']['speaker_labels']
    language_code = config['transcription']['language_code']

    transcription_config = aai.TranscriptionConfig(speaker_labels=speaker_labels, language_code=language_code)

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
    file_path,
    config=transcription_config
    )

    # Stop the loading message
    #loading = False
    #loading_thread.join()  # Wait for the loading thread to finish

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print(f"Transcription completed in {elapsed_time:.2f} seconds.")

    lines = []
    for utterance in transcript.utterances:
        start_time = ms_to_timestamp(utterance.start)
        end_time = ms_to_timestamp(utterance.end)
        lines.append(f"[{start_time} - {end_time}] Speaker {utterance.speaker}: {utterance.text}")
        #lines.append(f"Speaker {utterance.speaker}: {utterance.text}")

    return '\n\n'.join(lines)