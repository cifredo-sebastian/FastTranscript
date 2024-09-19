# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.
import time
import threading
import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "a062defa71084271b5dbe8d7e639a106"

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

def assemblyTranscribe(file_path):

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return(transcript.error)
    else:
        return(transcript.text)


def assemblyDiaritization(file_path):
    global loading
    loading = True

    # Start the loading message in a separate thread
    loading_thread = threading.Thread(target=display_loading_message)
    loading_thread.start()
    
    start_time = time.time()

    config = aai.TranscriptionConfig(speaker_labels=True, language_code="es")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
    file_path,
    config=config
    )

    # Stop the loading message
    loading = False
    loading_thread.join()  # Wait for the loading thread to finish

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print(f"Transcription completed in {elapsed_time:.2f} seconds.")

    lines = []
    for utterance in transcript.utterances:
        lines.append(f"Speaker {utterance.speaker}: {utterance.text}")

    return '\n'.join(lines)