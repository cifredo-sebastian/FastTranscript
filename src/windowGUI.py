import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from src.mainlogic import main_process
from src.windowUtils import update_status
from src.relabel import relabel
from src.config_manager import load_config, save_config
import tkinter.font as tkFont
import webbrowser
import os
import threading
import sys
import json

VALID_FILETYPES = {'3ga', '8svx', 'aac', 'ac3', 'aif', 'aiff', 'alac', 'amr', 'ape', 'au', 'dss', 'flac', 'flv', 'm4a', 'm4b', 'm4p', 
                   'm4r', 'mp3', 'mpga', 'ogg', 'oga', 'mogg', 'opus', 'qcp', 'tta', 'voc', 'wav', 'wma', 'wv', 'm2ts', 'mov', 'mp2', 'mp4', 'm4p', 'm4v', 'mxf', 'webm',
                   'txt','docx'}



file_uploaded = False
file_valid = False
processing = False
output_file_path = ""

language_codes = {
        "Global English": "en",
        "Australian English": "en_au",
        "British English": "en_uk",
        "US English": "en_us",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Dutch": "nl",
        "Hindi": "hi",
        "Japanese": "ja",
        "Chinese": "zh",
        "Finnish": "fi",
        "Korean": "ko",
        "Polish": "pl",
        "Russian": "ru",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Vietnamese": "vi"
    }

# def update_status(status_label, message):
#     status_label.config(text=message)

def process_file(file_path, filetype, status_label, buttons, clear_link):
    global processing
    if file_uploaded:
        if file_valid:
            config = load_config()
            if filetype == 'txt' or filetype == 'docx':
                output_file_path = filedialog.asksaveasfilename(
                    defaultextension=f".{filetype}",
                    initialfile=f"{os.path.splitext(os.path.basename(file_path))[0]}_relabel",
                    filetypes=[("All files", "*.*"), ("Text files", "*.txt"), ("Word Document", "*.docx")]
                )
                relabel(file_path,filetype,status_label,output_file_path)
            elif config["api_key"]:
                output_file_path = filedialog.asksaveasfilename(
                    defaultextension=config.get("output-filetype", ".txt"),
                    initialfile=os.path.splitext(os.path.basename(file_path))[0],
                    filetypes=[("All files", "*.*"), ("Text files", "*.txt"), ("Word Document", "*.docx")]
                )
                if output_file_path:
                    print(f"{file_path}")
                    processing = True
                    toggle_buttons(buttons)
                    thread = threading.Thread(target=process_in_thread, args=(file_path, filetype, output_file_path, status_label, buttons, clear_link))
                    thread.start()
            else:
                messagebox.showinfo("API Key","Missing API key for transcription. Go to Preferences to enter your AssemblyAI API key.")
        else:
            messagebox.showinfo("File Valid", "File not valid for processing")
    else:
        messagebox.showinfo("File not uploaded", "File not uploaded for processing.")
    

def process_in_thread(file_path, filetype,output_file_path, status_label, buttons, clear_link):
    global processing, file_uploaded, file_valid
    clear_link.place_forget()
    main_process(file_path,filetype,output_file_path,status_label)
    processing = False
    file_uploaded = False
    file_valid = False
    toggle_buttons(buttons)
    config = load_config()
    # if config['alert']:
    #     messagebox.showinfo("Transcription Complete", f"Transcription saved to {output_file_path}")

def open_dropdown(event):
    event.widget.event_generate('<Down>')

def show_context_menu(event, entry):
    # Create the context menu
    context_menu = tk.Menu(entry, tearoff=0)
    
    # Add context menu commands
    # context_menu.add_command(label="Undo", command=lambda: entry.event_generate("<<Undo>>"))
    # context_menu.add_command(label="Redo", command=lambda: entry.event_generate("<<Redo>>"))
    context_menu.add_command(label="Cut", command=lambda: entry.event_generate("<<Cut>>"))
    context_menu.add_command(label="Copy", command=lambda: entry.event_generate("<<Copy>>"))
    context_menu.add_command(label="Paste", command=lambda: entry.event_generate("<<Paste>>"))
    context_menu.add_command(label="Delete", command=lambda: entry.delete(0, 'end'))
    context_menu.add_separator()
    context_menu.add_command(label="Select All", command=lambda: entry.select_range(0, 'end'))

    
    # Show the context menu at the mouse position
    context_menu.tk_popup(event.x_root, event.y_root)


def open_config(config_label):
    config_window = tk.Toplevel()
    config_window.title("Preferences")
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'public', 'fasttranscript.ico')
    else:
        icon_path = 'public/fasttranscript.ico'
    config_window.iconbitmap(icon_path)
    config_window.minsize(300, 300)  # Set minimum window size (width, height)

    config = load_config()

    label_frame = tk.Frame(config_window)
    label_frame.pack(anchor="w", padx=10, pady=5)

    #tk.Label(config_window, text="API Key").pack(anchor="w", padx=10, pady=5)

    tk.Label(label_frame, text="API Key").pack(side="left", padx=(0, 5))

    def open_api_key_website(event):
        webbrowser.open("https://www.assemblyai.com/app")

    link = tk.Label(label_frame, text="Get your API Key here", fg="blue", cursor="hand2", font=(tkFont.nametofont("TkDefaultFont"),9))
    link.pack(side="left", padx=(0))
    link.bind("<Button-1>", open_api_key_website)

    entry_frame = tk.Frame(config_window)
    entry_frame.pack(anchor="w", padx=10, pady=5)

    # API Key
    api_key_var = tk.StringVar(value=config["api_key"])
    api_key_entry = tk.Entry(entry_frame, textvariable=api_key_var, show="*")
    api_key_entry.pack(side="left", padx=(0, 5))

    # api_key_entry.config(undo=True)
    api_key_entry.bind("<Button-3>", lambda event: show_context_menu(event, api_key_entry))

    def toggle_api_key_visibility():
        if api_key_entry.cget('show') == '*':
            api_key_entry.config(show='')
        else:
            api_key_entry.config(show='*')

    toggle_button = tk.Button(entry_frame, text="👁", command=toggle_api_key_visibility)
    toggle_button.pack(side="left")



    # Checkbutton for speaker labels
    tk.Label(config_window, text="Speaker Labels").pack(anchor="w", padx=10, pady=5)
    speaker_labels_var = tk.BooleanVar(value=config["transcription"]["speaker_labels"])
    check1 = tk.Checkbutton(config_window, text="Enable Speaker Labels", variable=speaker_labels_var)
    check1.pack(anchor="w", padx=10, pady=5)

    # Language Dropdown   
    tk.Label(config_window, text="Choose Language").pack(anchor="w", padx=10, pady=5)
    language_var = tk.StringVar()
    dropdown = ttk.Combobox(config_window, textvariable=language_var, state="readonly")
    dropdown['values'] = ("Global English", "Australian English", "British English", "US English", "Spanish", "French", "German", "Italian", "Portuguese", 
                          "Dutch", "Hindi", "Japanese", "Chinese", "Finnish", "Korean", "Polish", "Russian", "Turkish", "Ukrainian", "Vietnamese")

    dropdown.bind('<Button-1>', open_dropdown)




    # Set the dropdown to the current saved language code
    current_language = [key for key, value in language_codes.items() if value == config["transcription"]["language_code"]][0]
    language_var.set(current_language)
    dropdown.pack(anchor="w", padx=10, pady=5)

    # Timestamp Format Dropdown   
    tk.Label(config_window, text="Timestamp Format").pack(anchor="w", padx=10, pady=5)
    timestamp_var = tk.StringVar()
    dropdown_ts = ttk.Combobox(config_window, textvariable=timestamp_var, state="readonly")
    dropdown_ts['values'] = ("None", "[Start]", "[Start-End]")
    dropdown_ts.bind('<Button-1>', open_dropdown)

    timestamp_codes = {
        "None": "",
        "[Start]": "start",
        "[Start-End]": "start-end"
    }

    # Set the dropdown to the current saved format
    current_timestamp = [key for key, value in timestamp_codes.items() if value == config["transcription"]["timestamp_format"]][0]
    timestamp_var.set(current_timestamp)
    dropdown_ts.pack(anchor="w", padx=10, pady=5)

    # Output Filetype Dropdown   
    tk.Label(config_window, text="Default Output Filetype").pack(anchor="w", padx=10, pady=5)
    filetype_var = tk.StringVar()
    dropdown_ts = ttk.Combobox(config_window, textvariable=filetype_var, state="readonly")
    dropdown_ts['values'] = (".txt", ".docx")
    dropdown_ts.bind('<Button-1>', open_dropdown)

    timestamp_codes = {
        "None": "",
        "[Start]": "start",
        "[Start-End]": "start-end"
    }

    # Set the dropdown to the current saved filetype
    filetype_var.set(config["output-filetype"])
    dropdown_ts.pack(anchor="w", padx=10, pady=5)

    # Checkbutton for config on main window
    config_show_var = tk.BooleanVar(value=config["config-show"])
    check1 = tk.Checkbutton(config_window, text="Display configuration settings on main window", variable=config_show_var)
    check1.pack(anchor="w", padx=10, pady=5)

    # Checkbutton for alert on transcript complete
    alert_var = tk.BooleanVar(value=config["alert"])
    check2 = tk.Checkbutton(config_window, text="Alert message on completion of transcription", variable=alert_var)
    check2.pack(anchor="w", padx=10, pady=5)

    # Save button
    def save_new_config():
        new_config = {
            "api_key": api_key_var.get(),
            "transcription": {
                "speaker_labels": speaker_labels_var.get(),
                "language_code": language_codes[language_var.get()],
                "timestamp_format": timestamp_codes[timestamp_var.get()]
            },
            "output-filetype": filetype_var.get(),
            "config-show": config_show_var.get(),
            "alert": alert_var.get()
        }
        save_config(new_config)
        config_window.destroy()
        #Update the config label
        update_config_display(config_label)

    tk.Button(config_window, text="Save", command=save_new_config).pack(padx=10, pady=10)


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

def on_file_drop(event, file_path, status_label,clear_link, start_button):
    global file_uploaded, file_valid

    file_path.set(clean_file_path(event.data))

    # Extract file extension
    file_extension = get_extension(event.data)

    # Check if the file type is valid
    if (file_extension in VALID_FILETYPES):
        status = f"{os.path.splitext(os.path.basename(event.data))[0]}"
        file_uploaded = True
        file_valid = True
        clear_link.place(x=148, y=185)
        if file_extension == 'txt' or file_extension == 'docx':
            start_button.config(text="Relabel")
        else:
            start_button.config(text="Start")
    else:
        file_valid = False
        clear_file(file_path,status_label, start_button)
        messagebox.showinfo("Invalid Filetype","Invalid filetype for transcription.")
        

    # Update the status label with the current state
    update_status(status_label,status)


def open_file_dialog(file_path, status_label,clear_link, start_button):
    global file_uploaded, file_valid

    file = filedialog.askopenfilename()
    if file:
        file_path.set(clean_file_path(file))
        
        # Extract file extension
        file_extension = get_extension(file)

        # Check if the file type is valid
        if file_extension in VALID_FILETYPES:
            status = f"{os.path.basename(file)}"
            file_uploaded = True
            file_valid = True
            clear_link.place(x=148, y=185)
            if file_extension == 'txt' or file_extension == 'docx':
                start_button.config(text="Relabel")
            else:
                start_button.config(text="Start")
        else:
            file_valid = False
            clear_file(file_path,status_label, start_button)
            messagebox.showinfo("Invalid Filetype","Invalid filetype for transcription.")

        # Update the status label
        update_status(status_label,status)



def create_window():
    root = TkinterDnD.Tk()
    root.title("FastTranscript")

    file_path = tk.StringVar()

    drop_label = tk.Label(root, text="Drag or           a file here", relief="sunken", width=40, height=10)
    drop_label.pack(padx=20, pady=20)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', lambda event: on_file_drop(event, file_path, status_label, clear_link, start_button))

    # Open Link
    open_link = tk.Label(drop_label, text="open", fg="blue", cursor="hand2")
    open_link.place(x=118, y=65) 
    open_link.bind("<Button-1>", lambda event: open_file_dialog(file_path, status_label, clear_link, start_button))

    # Clear Link (initially hidden)
    clear_link = tk.Label(root, text="Clear", fg="blue", cursor="hand2")
    clear_link.place(x=180, y=225)
    clear_link.bind("<Button-1>", lambda event: clear_file_and_link(file_path, status_label, clear_link, start_button))
    clear_link.place_forget()  # Hide initially

    # Status Label text
    status_label = tk.Message(root, text="No file selected", width=300, justify='center', anchor='center')
    status_label.pack(pady=10)

    # Start Button
    start_button = tk.Button(root, text="Start", command=lambda: process_file(file_path.get(), get_extension(file_path.get()), status_label, buttons, clear_link))
    start_button.pack(pady=10)

    # Config Button
    config_label = None
    config_button = tk.Button(root, text="Preferences", command=lambda: open_config(config_label))
    config_button.pack(pady=10)

    # Config status text
    config_label = tk.Message(root, text="", width=300, justify='center', anchor='center')
    update_config_display(config_label)
    config_label.pack(pady=10)

    buttons = [start_button, config_button]

    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'public', 'fasttranscript.ico')
    else:
        icon_path = 'public/fasttranscript.ico'

    root.iconbitmap(icon_path)
    root.mainloop()



def toggle_buttons(buttons):
    state = "disabled" if processing else "normal"
    for button in buttons:
        button.config(state=state)


def clear_file(file_path, status_label, start_button):
    global file_uploaded, file_valid
    file_path.set("")
    status_label.config(text="No file selected")
    file_uploaded = False
    file_valid = False
    start_button.config(text="Start")

def clear_file_and_link(file_path, status_label, clear_link, start_button):
    clear_file(file_path,status_label,start_button)
    clear_link.place_forget()



def update_config_display(config_label):
    reversed_language_codes = {v: k for k, v in language_codes.items()}
    config = load_config()
    if config['config-show']:
        # Convert True/False to Enabled/Disabled
        speaker_status = "Enabled" if config['transcription']['speaker_labels'] else "Disabled"
        
        # Get the language name from the reversed_language_codes dictionary
        language_name = reversed_language_codes.get(config['transcription']['language_code'], config['transcription']['language_code'])
        
        # Create the config text with newlines for display
        config_text = (
            f"Speaker Labels: {speaker_status}\n"
            f"Language: {language_name}\n"
            f"Timestamp Format: {config['transcription']['timestamp_format']}\n"
            f"Filetype: {config['output-filetype']}"
        )
        config_label.config(text=config_text)
    else:
        config_label.config(text="")