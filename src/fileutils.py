import docx

def save_transcription(text, output_file):
    """
    Saves the transcribed text to a file. Supports both .txt and .docx formats.
    :param text: The transcription text.
    :param output_file: The path of the output file.
    """
    try:
        # Check if the output file is a .docx file
        if output_file.endswith('.docx'):
            # Create a new Word document
            doc = docx.Document()
            # Add the transcription text to the document
            doc.add_paragraph(text)
            # Save the document as a .docx file
            doc.save(output_file)
            print(f"Saved transcription as a Word document to {output_file}")
        else:
            # Default to saving as plain text (.txt or other extensions)
            with open(output_file, "w") as f:
                f.write(text)
            print(f"Saved transcription to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")
