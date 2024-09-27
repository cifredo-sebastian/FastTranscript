import tkinter as tk

def update_status(status_label, message):
    # max_length = 50
    # if len(message) > max_length:
    #     message = message[:max_length] + '...'
    status_label.config(text=message)

