# Table of Contents
1. [Introduction](#Introduction)
2. [Installation](#Installation)
3. [Features](#Features)
4. [Usage](#Usage)
5. [Configuration](#Configuration)

# Introduction

Welcome to [FastTranscript](https://github.com/cifredo-sebastian/FastTranscript)! This program allows users to easily transcribe audio files with speaker diarization, enabling you to distinguish between different speakers in your recordings and have them transcribed into a text file.

# Installation
1. **Prerequisites**: 
	- [FastTranscript](https://github.com/cifredo-sebastian/FastTranscript/releases) (currently only compatible on Windows devices.) 
	- An active [AssemblyAI](https://www.assemblyai.com/) account and Key is required for use.
	- An internet connection for the transcription process.
2. **Creating an AssemblyAI Account**:
	- Visit the [AssemblyAI website](https://www.assemblyai.com/).
	- Click on the "Sign Up" button.
	- Fill in the required information to create your account.
	- After signing up, navigate to your [account dashboard](https://www.assemblyai.com/app).
	- Locate your API key in the Home section, to the right. Copy this key for use in the application.
    
   
# Features
- **Drag-and-Drop Interface**: Simply drag your audio files into the program window for transcription, or manually open a file.
- **Speaker Diarization**: Automatically identifies and labels different speakers in the transcription.
- **Speaker Labeling**: Relabel your text files to add manual speaker labels.
- **Configuration Options**: Customize settings such as language selection, timestamp formats and output text file type.

# Usage

1. **Launching the Application**:
    - Download FastTranscript from the GitHub <a href="https://github.com/cifredo-sebastian/FastTranscript/releases">Releases</a> page and open it by double-clicking on `FastTranscript.exe`.

1. **Transcribing Audio**:
    - Drag and drop your audio file into the designated area of the program, or open it manually by clicking on `open`.
    - Click the “Start” button to begin transcription.
    - A "clear" link appears in the window that clears the file from the program.
    - Note: An internet connection and an API key is REQUIRED to connect to AssemblyAI and transcribe audio.
2. **Saving Transcriptions**:
    - Before transcription is started, you will be prompted to select a save location and filename for the output `.txt` or `.docx` file.
3. **Viewing Results**:
    - When the transcription is complete, the program will let you know where the transcription has been saved. 
    - Note: The transcription may have errors in transcribing, grammar, labeling, etc. Do not assume it is a perfect result.
    - The transcription will include speaker labels and timestamps, formatted for easy readability, per your configuration.
4. **Relabeling**:
	- Optionally, you can drop or open a `.txt` or `.docx` file that FastTranscript produces to change the labels into custom ones of your choosing. The "Start" button will change into a "Relabel" button when you drop or open a `.txt` or `.docx` file. A "Relabel" window will appear when you press the button for you to manually input your desired labels. 
	- Note: Relabeling does not require an internet connection or an AssemblyAI API key.
# Configuration

1. **Accessing Configuration Settings**:
    - Click on the "Preferences" button to open the configuration window.
2. **Available Settings**:
    - **API Key**: Enter your API key for the speech-to-text service (displayed as a password field). This is REQUIRED for connection to the AssemblyAI API. The program WILL NOT WORK without it. Click the eye icon next to the entry field to toggle between showing or hiding the API key.
    - **Speaker Labels**: Check the box to enable speaker labels (speech diarization) for transcription.
    - **Language Selection**: Choose the language of the audio from the dropdown menu.
    - **Timestamp Format**: Select the desired timestamp format from the options available. "None" turns off timestamps, "Start" when that speaker first speaks in the audio file, and "Start-End" displays both when the speaker starts speaking and when they stop. The format is in minutes:seconds.
    - **Default Output Filetype**: Set the preferred filetype for the transcription text file between `.txt` and `.docx`. Note: you can always manually specify by using the drop down menu in Window's file saving menu.
    - **Display configuration settings on main window**: Check the box to display your current saved settings under the `Settings` button on the main window. The format is as follows: `Speaker Labels, Language, Timestamp, Output type`.
    - **Alert message on completion of transcription**: Check the box to have FastTranscript alert you when the transcription process finishes.


# Developer

`pip install -r requirements.txt`