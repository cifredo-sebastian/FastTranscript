from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
import io

def transcribe_with_diarization(audio_file_path):
    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file('skilful-earth-436119-q3-675a22d52306.json')

    # Initialize the speech client with credentials
    client = speech.SpeechClient(credentials=credentials)

    # Load the audio file
    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    # Configure the audio and diarization settings
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming WAV file
        sample_rate_hertz=16000,  # Adjust according to your audio sample rate
        language_code="en-US",  # Adjust to the appropriate language
        enable_speaker_diarization=True,
        diarization_speaker_count=2  # Adjust based on the expected number of speakers
    )

    # Perform the transcription
    #response = client.recognize(config=config, audio=audio)

    # Perform asynchronous (long-running) transcription
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=3600)  # Wait for up to an hour for the operation to complete


    return response

    # Parse and display the results
    #for result in response.results:
    #    print("Transcript: {}".format(result.alternatives[0].transcript))
    #    for word in result.alternatives[0].words:
    #        print(f"Word: {word.word}, Speaker Tag: {word.speaker_tag}")
