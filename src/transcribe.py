import speech_recognition as sr

def transcribe_audio(wav_path):
    """
    Transcribes the audio from a WAV file to text using Google's Web Speech API.
    :param wav_path: Path to the WAV file.
    :return: Transcribed text.
    """
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)

    try:
        #print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
