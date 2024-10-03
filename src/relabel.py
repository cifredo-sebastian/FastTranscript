import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import docx
import os
import sys

def relabel(file_path,filetype,status_label, file_destination):
    if file_destination:
        speaker_count, speaker_ids = count_speakers(file_path,filetype)
        if speaker_count == 0:
            messagebox.showinfo("Labels not found", f"No speaker labels found in {file_path}.")
        else:
            open_relabler(file_path,filetype,status_label,speaker_ids, speaker_count, file_destination)

def open_relabler(file_path,filetype,status_label,speaker_ids, speaker_count, file_destination):
    relabel_window = tk.Toplevel()
    relabel_window.title("Relabel")
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'public', 'fasttranscript.ico')
    else:
        icon_path = 'public/fasttranscript.ico'
    relabel_window.iconbitmap(icon_path)
    relabel_window.minsize(300, 300)

    entries = {}
    
    for speaker in speaker_ids:
        label = tk.Label(relabel_window, text=f'{speaker}: ')
        label.pack(anchor='w')
        entry = tk.Entry(relabel_window)
        entry.pack(fill='x')

        entries[speaker] = entry

    def save_data():
        speaker_data = {speaker: entries[speaker].get() for speaker in speaker_ids}
        speaker_relabel(file_path, filetype, speaker_data,file_destination)
        messagebox.showinfo("Relabel Saved", f"File relabeled and saved in {file_destination}.")
        relabel_window.destroy()

    tk.Button(relabel_window, text="Save", command=save_data).pack(padx=10, pady=10)

def speaker_relabel(file_path, filetype, speaker_data,file_destination):
    if filetype == 'docx':
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            lines = para.text.splitlines()
            updated_lines = []
            for line in lines:
                for old_speaker, new_speaker in speaker_data.items():
                    if old_speaker in line:
                        line = line.replace(old_speaker, new_speaker)
                updated_lines.append(line)

            para.text = "\n".join(updated_lines)
        doc.save(file_destination)

    else:
        with open(file_path, 'r') as file:
            file_content = file.read()

        for old_speaker, new_speaker in speaker_data.items():
            file_content = file_content.replace(old_speaker, new_speaker)

        with open(file_destination, 'w') as file:
            file.write(file_content)

    print(f"File saved to {file_destination}")


def count_speakers(file_path,filetype):
    speakers = set()

    if filetype == 'docx':
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            lines = para.text.splitlines()
            for line in lines:
                if 'Speaker' in line:
                    start = line.find('Speaker ') + len('Speaker ')
                    end = line.find(':', start)
                    speaker_id = "Speaker " + line[start:end].strip()
                    speakers.add(speaker_id)

    else:
        with open(file_path, 'r') as file:
            for line in file:
                if 'Speaker' in line:
                    start = line.find('Speaker ') + len('Speaker ')
                    end = line.find(':', start)
                    speaker_id = "Speaker " + line[start:end].strip()
                    speakers.add(speaker_id)

    return len(speakers), sorted(speakers)
