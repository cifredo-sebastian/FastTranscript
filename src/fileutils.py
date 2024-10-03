import docx

def save_transcription(text, output_file):
    try:
        if output_file.endswith('.docx'):
            doc = docx.Document()
            doc.add_paragraph(text)
            doc.save(output_file)
            print(f"Saved transcription as a Word document to {output_file}")
        else:
            with open(output_file, "w") as f:
                f.write(text)
            print(f"Saved transcription to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")
