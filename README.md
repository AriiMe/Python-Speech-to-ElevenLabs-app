# Sigma Recorder

Sigma Recorder is a voice recognition and text-to-speech synthesis application developed in Python using the Elevenlabs API. It allows you to record voice, transcribe it into text, and then convert the text into speech using a chosen voice from the Elevenlabs API.

This README provides instructions on how to install and run Sigma Recorder.

## Requirements

* Python 3.6 or higher
* Pip (Python Package Installer)
* This project uses the Elevenlabs API for text-to-speech synthesis. A paid subscription is needed for custom models

## Installation

First, clone this repository to your local machine using git clone.

Next, navigate to the cloned repository's directory in your terminal.

To install the necessary Python libraries, use the following commands:

```bash
pip install tkinter
pip install speechrecognition
pip install requests
pip install threading
pip install os
pip install pygame
pip install json
```

## Usage

Before running the application, make sure you have the voices.json file and an API key from Elevenlabs in the api_key.txt file in your project directory.

To run the application, use the following command in your terminal:

```bash
python main.py
```

The GUI of the application will appear. Here, you can:

* Select a voice from the dropdown menu
* Record your voice
* Generate audio from the recognized text
* Play the generated audio
* Stop the audio

## Build

To build the app run the following command:
```bash
pyinstaller --onefile --noconsole app.py
```

## License

This project is licensed under the MIT License.