# Voice-Activated Chatbot Using Google Generative AI

## Overview

This program implements a voice-activated chatbot using Google's Generative AI and integrates it with speech recognition and text-to-speech capabilities. It listens for user input via a microphone, processes the input using Google’s speech recognition API, and generates responses based on system information and user queries.

## Requirements

- Python 3.x
- Required libraries:
  - `google-generativeai`
  - `speech_recognition`
  - `pyttsx3`
- A valid API key for Google Generative AI services
- Access to a microphone for voice input

## Installation

You can install the required libraries using pip:

```bash
pip install google-generativeai speech_recognition pyttsx3
```

## Usage

1. **Setup API Key**: Replace the placeholder API key in the code with your valid Google Generative AI API key.
2. **Run the Program**: Execute the Python script. Ensure your microphone is working and you have permission to access it.
3. **Interaction**:
   - Speak your questions clearly into the microphone.
   - The chatbot will respond vocally using the configured text-to-speech engine.
   - To exit the program, say "exit" or "quit".
   - To clear the chat history, say "clear".

## Code Explanation

### Imports

```python
import google.generativeai as genai
import subprocess
import speech_recognition as sr
import pyttsx3
```

- **google.generativeai**: For generating responses using Google's Generative AI.
- **subprocess**: To execute shell commands and retrieve system information.
- **speech_recognition**: To convert spoken language into text.
- **pyttsx3**: To convert text responses back to speech.

### Initializing Components

```python
recognizer = sr.Recognizer()
engine = pyttsx3.init()
```

- Initializes the speech recognizer and text-to-speech engine.

### Configure Voice Properties

```python
engine.setProperty('rate', 140) 
engine.setProperty('volume', 1) 
voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', voice_id)
```

- Sets the speech rate, volume, and voice ID for the text-to-speech engine.

### Retrieving OS Information

```python
command = '''systeminfo | findstr /B /C:"OS Name:" /C:"OS Version:"'''
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

- Uses a shell command to gather OS data, which is included in the chatbot's initial context.

### Chat Session Initialization

```python
chat = model.start_chat(history=[...])
```

- Starts the chat session with an initial context based on the retrieved OS information.

### Main Loop

```python
while True:
    ...
```

- Continuously listens for user input and processes commands until the user opts to exit.

### Error Handling

- Catches exceptions during speech recognition and OS data retrieval, providing user feedback in case of errors.

### User Commands

- **Exit**: Ends the program when the user says "exit" or "quit".
- **Clear**: Resets the chat session when the user says "clear".

### Response Handling

```python
response = chat.send_message(user_input, stream=True)
```

- Sends the user's input to the generative model and processes the response, outputting it both to the console and as speech.

## Conclusion

This program allows users to interact with a chatbot using voice commands, making it a convenient tool for hands-free assistance. The integration of system information adds context to the responses provided by the generative AI model.
