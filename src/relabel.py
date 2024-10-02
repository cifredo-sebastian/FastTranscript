import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from src.windowUtils import update_status
from src.config_manager import load_config, save_config
import os
import threading
import json

def relabel(file_path,filetype,status_label):
    speaker_count, speaker_ids = count_speakers(file_path)
    open_relabler(file_path,filetype,status_label,speaker_ids)

def open_relabler(file_path,filetype,status_label,speaker_ids):
    relabel_window = tk.Toplevel()
    relabel_window.title("Relabel")
    relabel_window.iconbitmap("public\\fasttranscript.ico")
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
        speaker_relabel(file_path, filetype, speaker_data)

    tk.Button(relabel_window, text="Save", command=save_data).pack(padx=10, pady=10)

def speaker_relabel(file_path, file_extension, speaker_data):
    print(speaker_data)


def count_speakers(file_path):
    speakers = set()

    # Read the text file
    with open(file_path, 'r') as file:
        for line in file:
            if 'Speaker' in line:
                start = line.find('Speaker ') + len('Speaker ')
                end = line.find(':', start)
                speaker_id = "Speaker" + line[start:end].strip()
                speakers.add(speaker_id)
    return len(speakers), sorted(speakers)
