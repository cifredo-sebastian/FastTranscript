import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from src.mainlogic import main_process
from src.windowUtils import update_status
from src.config_manager import load_config, save_config
import os
import threading
import json

VALID_FILETYPES = {'3ga', '8svx', 'aac', 'ac3', 'aif', 'aiff', 'alac', 'amr', 'ape', 'au', 'dss', 'flac', 'flv', 'm4a', 'm4b', 'm4p', 
                   'm4r', 'mp3', 'mpga', 'ogg', 'oga', 'mogg', 'opus', 'qcp', 'tta', 'voc', 'wav', 'wma', 'wv', 'm2ts', 'mov', 'mp2', 'mp4', 'm4p', 'm4v', 'mxf', 'webm'}



file_uploaded = False
file_valid = False
output_file_path = ""

# def update_status(status_label, message):
#     status_label.config(text=message)

def process_file(file_path, filetype, status_label):
    if file_uploaded:
        if file_valid:
            # print(f"Processing file: {file_path}")
            # print(f"Filetype: {filetype}")
            output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])            
            if output_file_path:
                #print(f"Output will be saved to: {output_file_path}")
                print(f"{file_path}")
                thread = threading.Thread(target=process_in_thread, args=(file_path, filetype, output_file_path, status_label))
                thread.start()
            else:
                messagebox.showinfo("Save Transcription","Save operation was cancelled.")
        else:
            messagebox.showinfo("File Valid", "File not valid for processing")
    else:
        messagebox.showinfo("File not uploaded", "File not uploaded for processing.")
    

def process_in_thread(file_path, filetype,output_file_path, status_label):
    #update_status(status_label, "Transcription started, please wait...")
    main_process(file_path,filetype,output_file_path,status_label)
    #update_status(status_label, "Transcription complete.")

def open_config():
    config_window = tk.Toplevel()
    config_window.title("Configuration")

    config = load_config()

    # Service Dropdown
    # tk.Label(config_window, text="Choose Transcriber").pack(anchor="w")
    # service_var = tk.StringVar()
    # dropdown = ttk.Combobox(config_window, textvariable=service_var)
    # dropdown['values'] = ("Google", "AssemblyAI")

    # service_codes = {
    #     "Google Cloud Speech-to-Text": "google",
    #     "AssemblyAI": "assemblyai"
    # }

    # API Key
    tk.Label(config_window, text="API Key").pack(anchor="w")
    api_key_var = tk.StringVar(value=config["api_key"])
    api_key_entry = tk.Entry(config_window, textvariable=api_key_var, show="*")
    api_key_entry.pack(anchor="w")

    # Checkbutton for speaker labels
    tk.Label(config_window, text="Speaker Labels").pack(anchor="w")
    speaker_labels_var = tk.BooleanVar(value=config["transcription"]["speaker_labels"])
    check1 = tk.Checkbutton(config_window, text="Enable Speaker Labels", variable=speaker_labels_var)
    check1.pack(anchor="w")

    # Language Dropdown   
    tk.Label(config_window, text="Choose Language").pack(anchor="w")
    language_var = tk.StringVar()
    dropdown = ttk.Combobox(config_window, textvariable=language_var)
    dropdown['values'] = ("English", "Spanish", "French")

    language_codes = {
        "English": "en",
        "Spanish": "es",
        "French": "fr"
    }

    # Set the dropdown to the current saved language code
    current_language = [key for key, value in language_codes.items() if value == config["transcription"]["language_code"]][0]
    language_var.set(current_language)
    dropdown.pack(anchor="w")

    # Timestamp Format Dropdown   
    tk.Label(config_window, text="Timestamp Format").pack(anchor="w")
    timestamp_var = tk.StringVar()
    dropdown = ttk.Combobox(config_window, textvariable=timestamp_var)
    dropdown['values'] = ("None", "[Start]", "[Start-End]")

    timestamp_codes = {
        "None": "",
        "[Start]": "start",
        "[Start-End]": "start-end"
    }

    # Set the dropdown to the current saved format
    current_timestamp = [key for key, value in timestamp_codes.items() if value == config["transcription"]["timestamp_format"]][0]
    timestamp_var.set(current_timestamp)
    dropdown.pack(anchor="w")

    def save_new_config():
        new_config = {
            "api_key": api_key_var.get(),
            "transcription": {
                "speaker_labels": speaker_labels_var.get(),
                "language_code": language_codes[language_var.get()],
                "timestamp_format": timestamp_codes[timestamp_var.get()]
            }
        }
        save_config(new_config)
        config_window.destroy()

    tk.Button(config_window, text="Save", command=save_new_config).pack()

def clean_file_path(file_path):
    # Check if file_path starts and ends with curly braces
    if file_path.startswith("{") and file_path.endswith("}"):
        # Remove the curly braces
        file_path = file_path[1:-1]
    return file_path

def get_extension(file_path):
    # Extract the file extension and strip unwanted characters
    _, file_extension = os.path.splitext(file_path)
    return file_extension.strip('}').strip('.').lower()

def on_file_drop(event, file_path, status_label):
    global file_uploaded, file_valid

    file_path.set(clean_file_path(event.data))
    file_uploaded = True

    # Extract file extension
    file_extension = get_extension(event.data)

    # Check if the file type is valid
    if (file_extension in VALID_FILETYPES):
        #status = f"{os.path.splitext(os.path.basename(event.data))[0]}, valid filetype"
        status = f"{os.path.splitext(os.path.basename(event.data))[0]}"
        file_valid = True
    else:
        status = f"{os.path.splitext(os.path.basename(event.data))[0]}, invalid filetype"
        messagebox.showinfo("Invalid Filetype","Invalid filetype for transcription.")
        file_valid = False

    # Update the status label with the current state
    update_status(status_label,status)


def open_file_dialog(file_path, status_label):
    global file_uploaded, file_valid

    file = filedialog.askopenfilename()
    if file:
        file_path.set(clean_file_path(file))
        file_uploaded = True

        # Extract file extension
        file_extension = get_extension(file)

        # Check if the file type is valid
        if file_extension in VALID_FILETYPES:
            #status = f"{os.path.basename(file)}, valid filetype"
            status = f"{os.path.basename(file)}"
            file_valid = True
        else:
            status = f"{os.path.basename(file)}, invalid filetype"
            messagebox.showinfo("Invalid Filetype","Invalid filetype for transcription.")
            file_valid = False

        # Update the status label
        update_status(status_label,status)

def create_window():
    root = TkinterDnD.Tk()
    root.title("Drag and Drop GUI")

    file_path = tk.StringVar()

    drop_label = tk.Label(root, text="Drag a file here", relief="sunken", width=40, height=10)
    drop_label.pack(pady=20)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', lambda event: on_file_drop(event, file_path, status_label))

    #tk.Label(root, textvariable=file_path).pack()

    status_label = tk.Label(root, text="No file selected")
    status_label.pack(pady=10)

    tk.Button(root, text="Open File", command=lambda: open_file_dialog(file_path, status_label)).pack(pady=10)

    tk.Button(root, text="Start", command=lambda: process_file(file_path.get(), get_extension(file_path.get()), status_label)).pack(pady=10)

    tk.Button(root, text="Config", command=open_config).pack(pady=10)

    root.mainloop()
