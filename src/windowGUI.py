import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os

VALID_FILETYPES ={'m4a', 'mp4', 'wav', 'mp3'}

file_uploaded = False
file_valid = False

def process_file(file_path, filetype, config_params):
    if file_uploaded:
        if file_valid:
            print(f"Processing file: {file_path}")
            print(f"Filetype: {filetype}")
            print(f"Using config: {config_params}")
        else:
            messagebox.showinfo("File Valid", "File not valid for processing")
    else:
        messagebox.showinfo("File not uploaded", "File not uploaded for processing.")
    

def open_config():
    config_window = tk.Toplevel()
    config_window.title("Configuration")

    tk.Label(config_window, text="Option 1").pack(anchor="w")
    check1 = tk.Checkbutton(config_window, text="Enable Feature X")
    check1.pack(anchor="w")

    tk.Label(config_window, text="Choose Language").pack(anchor="w")
    language_var = tk.StringVar()
    dropdown = ttk.Combobox(config_window, textvariable=language_var)
    dropdown['values'] = ("English", "Spanish", "French")
    dropdown.current(0)
    dropdown.pack(anchor="w")

    def save_config():
        config = {
            "enable_feature_x": check1.instate(['selected']),
            "language": language_var.get()
        }
        print(f"Saved config: {config}")
        config_window.destroy()

    tk.Button(config_window, text="Save", command=save_config).pack()

def get_extension(file_path):
    # Extract the file extension and strip unwanted characters
    _, file_extension = os.path.splitext(file_path)
    return file_extension.strip('}').strip('.')

def on_file_drop(event, file_path, status_label):
    global file_uploaded, file_valid

    file_path.set(event.data)
    file_uploaded = True

    # Extract file extension
    file_extension = get_extension(event.data)

    # Check if the file type is valid
    if (file_extension in VALID_FILETYPES):
        status = f"{os.path.splitext(os.path.basename(event.data))[0]}, valid filetype"
        file_valid = True
    else:
        status = f"{os.path.splitext(os.path.basename(event.data))[0]}, invalid filetype"
        file_valid = False

    # Update the status label with the current state
    status_label.config(text=status)


def open_file_dialog(file_path, status_label):
    global file_uploaded, file_valid

    file = filedialog.askopenfilename()
    if file:
        file_path.set(file)
        file_uploaded = True

        # Extract file extension
        file_extension = get_extension(file)

        # Check if the file type is valid
        if file_extension in VALID_FILETYPES:
            status = f"{os.path.basename(file)}, valid filetype"
            file_valid = True
        else:
            status = f"{os.path.basename(file)}, invalid filetype"
            file_valid = False

        # Update the status label
        status_label.config(text=status)

def create_window():
    root = TkinterDnD.Tk()
    root.title("Drag and Drop GUI")

    # Status label to display the current state
    

    file_path = tk.StringVar()

    drop_label = tk.Label(root, text="Drag a file here", relief="sunken", width=40, height=10)
    drop_label.pack(pady=20)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', lambda event: on_file_drop(event, file_path, status_label))

    #tk.Label(root, textvariable=file_path).pack()

    status_label = tk.Label(root, text="No file selected")
    status_label.pack(pady=10)

    tk.Button(root, text="Open File", command=lambda: open_file_dialog(file_path, status_label)).pack(pady=10)

    tk.Button(root, text="Start", command=lambda: process_file(file_path.get(), get_extension(file_path.get()), {"config": "example"})).pack(pady=10)

    tk.Button(root, text="Config", command=open_config).pack(pady=10)

    root.mainloop()
