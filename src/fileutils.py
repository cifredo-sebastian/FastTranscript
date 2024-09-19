def save_transcription(text, output_file):
    """
    Saves the transcribed text to a text file.
    :param text: The transcription text.
    :param output_file: The path of the output file.
    """
    try:
        with open(output_file, "w") as f:
            f.write(text)
        print(f"Saved transcription to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")
