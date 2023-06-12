import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import requests
import threading
import os
import pygame
import json

# Global Variables
output_count = 1
selected_voice_id = None
output_file_name = None
api_key_file = 'api_key.txt'

# Check if api_key.txt exists
if not os.path.isfile(api_key_file):
    root = tk.Tk()
    root.title("API Key Required")

    # Prompt user to enter the API key
    label = tk.Label(root, text="Enter Elevenlabs API Key:")
    label.pack(pady=10)

    api_key_entry = tk.Entry(root)
    api_key_entry.pack(pady=10)

    # Save the API key to the file
    def save_api_key():
        with open(api_key_file, 'w') as f:
            f.write(api_key_entry.get())
        root.destroy()

    submit_button = tk.Button(root, text="Submit", command=save_api_key)
    submit_button.pack(pady=10)

    root.mainloop()

# Loading the API key
with open(api_key_file, 'r') as f:
    api_key = f.read().strip()

# Loading voices.json
with open("voices.json") as f:
    voices = json.load(f)

# Recording Audio


def record_audio():
    def _record_audio():
        global recognized_text
        r = sr.Recognizer()
        with sr.Microphone() as source:
            recognized_text_entry.delete("1.0", tk.END)
            recognized_text_entry.insert(tk.END, "Listening...")
            audio = r.listen(source)
            recognized_text_entry.delete("1.0", tk.END)
            recognized_text_entry.insert(tk.END, "Processing...")
        try:
            recognized_text = r.recognize_google(audio)
            recognized_text_entry.delete("1.0", tk.END)
            recognized_text_entry.insert(tk.END, recognized_text)
        except sr.UnknownValueError:
            recognized_text_entry.delete("1.0", tk.END)
            recognized_text_entry.insert(tk.END, "Unable to recognize speech")
        except sr.RequestError as e:
            recognized_text_entry.delete("1.0", tk.END)
            recognized_text_entry.insert(tk.END, "Error: " + str(e))

    threading.Thread(target=_record_audio).start()

# Generating Audio from Text


def generate_audio():
    def _generate_audio():
        global recognized_text, output_count, selected_voice_id, output_file_name
        text = recognized_text_entry.get("1.0", tk.END).strip()
        if text and selected_voice_id:
            CHUNK_SIZE = 1024
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}/stream"

            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }

            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.77
                }
            }

            response = requests.post(
                url, json=data, headers=headers, stream=True)

            if response.status_code == 200:
                output_file_name = f"output{output_count}.mp3"
                with open(output_file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                recognized_text_entry.delete("1.0", tk.END)
                recognized_text_entry.insert(
                    tk.END, "Audio file generated successfully.")
                output_count += 1
            else:
                recognized_text_entry.delete("1.0", tk.END)
                recognized_text_entry.insert(
                    tk.END, "Error: " + str(response.status_code))
        else:
            recognized_text_entry.delete("1.0", tk.END)
            recognized_text_entry.insert(
                tk.END, "No recognized text or voice selected for audio generation.")

    threading.Thread(target=_generate_audio).start()

# Playing Audio


def play_audio():
    global output_file_name
    if output_file_name:
        pygame.mixer.music.load(output_file_name)
        pygame.mixer.music.play()

# Stopping Audio Playback


def stop_audio():
    pygame.mixer.music.stop()

# GUI Setup


window = tk.Tk()
window.title("Sigma Recorder")

# Dropdown Voice selection

voice_names = list(voices.keys())
selected_voice_name = tk.StringVar(window)
selected_voice_name.set(voice_names[0])  # default choice
voice_dropdown = ttk.OptionMenu(window, selected_voice_name, *voice_names)
voice_dropdown.pack(pady=5)

record_button = tk.Button(window, text="Record", command=record_audio)
record_button.pack(pady=10)

generate_button = tk.Button(
    window, text="Generate Audio", command=generate_audio)
generate_button.pack(pady=10)

play_button = tk.Button(window, text="Play", command=play_audio)
play_button.pack(pady=10)

stop_button = tk.Button(window, text="Stop", command=stop_audio)
stop_button.pack(pady=10)

recognized_text_entry = tk.Text(window, height=5, width=50)
recognized_text_entry.pack(pady=10)

# When a voice is selected from the dropdown, get the corresponding voice_id


def update_selected_voice_id(*args):
    global selected_voice_id
    selected_voice_id = voices[selected_voice_name.get()]["voice_id"]


selected_voice_name.trace("w", update_selected_voice_id)

# Global variable to store the recognized text

recognized_text = ""

# Initialize the audio player

pygame.mixer.init()

window.mainloop()
