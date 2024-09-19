# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "a062defa71084271b5dbe8d7e639a106"

# URL of the file to transcribe
#FILE_URL = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'


def assemblyTranscribe(file_path):

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return(transcript.error)
    else:
        return(transcript.text)


def assemblyDiaritization(file_path):
    config = aai.TranscriptionConfig(speaker_labels=True, language_code="es")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
    file_path,
    config=config
    )


    lines = []
    for utterance in transcript.utterances:
        lines.append(f"Speaker {utterance.speaker}: {utterance.text}")

    return '\n'.join(lines)