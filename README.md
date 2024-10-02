# Voice-Activated Chatbot Using Google Generative AI

## Overview

This program implements a voice-activated chatbot utilizing Google's Generative AI, speech recognition, and text-to-speech capabilities. Users can ask questions vocally, and the chatbot will respond with generated answers, incorporating system information for context. This document provides an overview, setup instructions, and detailed explanations of the code components.

## Requirements

To run this program, you need:

- **Python 3.x**: Ensure you have Python installed on your machine.
- **Required Libraries**:
  - `google-generativeai`: For generating responses based on user input.
  - `speech_recognition`: For converting spoken language into text.
  - `pyttsx3`: For converting text responses into speech.

You can install the required libraries using pip:

```bash
pip install google-generativeai speech_recognition pyttsx3
```

- **API Key**: A valid API key for Google Generative AI services.
- **Microphone**: A working microphone for voice input.

## Usage Instructions

1. **Setup the API Key**: Replace the placeholder API key in the code with your valid Google Generative AI API key.
2. **Run the Program**: Execute the Python script. Ensure that your microphone is functioning and that the program has permission to access it.
3. **Interaction**:
   - Speak your questions clearly into the microphone.
   - The chatbot will respond vocally using the configured text-to-speech engine.
   - To exit the program, say "exit" or "quit".
   - To clear the chat history, say "clear".

## Code Explanation

### Import Statements

```python
import google.generativeai as genai
import subprocess
import speech_recognition as sr
import pyttsx3
```

- **google.generativeai**: This module is used to access Google’s Generative AI services, allowing the chatbot to generate responses based on user queries.
- **subprocess**: This module allows the execution of shell commands from within Python, which is used to retrieve system information.
- **speech_recognition**: This library provides functionality to recognize speech input from the user.
- **pyttsx3**: This library is used to convert text to speech, enabling the chatbot to respond vocally.

### Initializing Components

```python
recognizer = sr.Recognizer()
engine = pyttsx3.init()
```

- **Recognizer**: Initializes the speech recognition engine.
- **Engine**: Initializes the text-to-speech engine, which will be used to vocalize responses.

### Configure Voice Properties

```python
engine.setProperty('rate', 140) 
engine.setProperty('volume', 1) 
voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', voice_id)
```

- **Rate**: Sets the speed at which the speech is delivered. A rate of 140 words per minute is typically clear and understandable.
- **Volume**: Sets the volume level for the speech output, where `1` is the maximum volume.
- **Voice ID**: Configures the specific voice for the text-to-speech engine. The voice ID provided targets Microsoft’s Zira voice on Windows systems.

### Retrieving OS Information

```python
try:
    command = '''systeminfo | findstr /B /C:"OS Name:" /C:"OS Version:"'''
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    os_data = result.stdout
except Exception as e:
    print(f"Error retrieving OS data: {e}")
    os_data = "Unknown OS data"
```

- **Command Execution**: The `subprocess.run()` function executes a shell command to retrieve the operating system's name and version.
- **Error Handling**: If there’s an issue retrieving the information, the error is caught, and a fallback message is set for `os_data`.

### Initializing the Generative Model

```python
model = genai.GenerativeModel('gemini-1.5-flash')
```

- **Model Initialization**: This line initializes the generative model that will be used to generate responses to user queries.

### Starting the Chat Session

```python
chat = model.start_chat(
    history=[
        {"role": "user", "parts": f"Here is some system data: {os_data}. Please ensure answers are precise and accurate, holding a minimum number of lines."},
        {"role": "model", "parts": "Understood. I'm ready to help with your problems or doubts."}
    ]
)
```

- **Chat Initialization**: This starts the chat session, providing initial context based on the system information. The `history` parameter contains predefined messages from both the user and the model.

### Main Interaction Loop

```python
while True:
    with sr.Microphone() as source:
        print("Please ask something...")
        audio = recognizer.listen(source)
        ...
```

- **Listening for Input**: The program continuously listens for user input. The microphone captures audio, which is then processed to recognize speech.

### Error Handling for Speech Recognition

```python
try:
    user_input = recognizer.recognize_google(audio)
    print(f"You said: {user_input}")
except sr.UnknownValueError:
    print("Could not understand audio. Please try again.")
    continue
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
    continue
```

- **Recognition**: Attempts to convert the audio input into text using Google’s speech recognition service.
- **Error Handling**: Catches exceptions if the speech cannot be understood or if there’s a problem with the recognition service, prompting the user to try again.

### Handling User Commands

```python
if user_input.lower() in ['exit', 'quit']:
    print("Exiting the chat.")
    break
```

- **Exit Commands**: The program checks if the user wants to exit the chat session and breaks the loop if the command is recognized.

### Clearing Chat History

```python
if user_input.lower() == 'clear':
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Please ensure answers are precise and accurate."},
            {"role": "model", "parts": "Understood. I'm ready to help with your questions."}
        ]
    )
    print("Chat history cleared.")
    continue
```

- **Clear Command**: If the user says "clear", the chat session is reinitialized, effectively clearing previous interactions.

### Sending User Input to the Model

```python
response = chat.send_message(user_input, stream=True)
for chunk in response:
    print(chunk.text, end="")
    engine.say(chunk.text)
    engine.runAndWait()
```

- **Message Sending**: The user’s input is sent to the generative model to get a response.
- **Response Handling**: The response is printed to the console and converted to speech using the text-to-speech engine, enabling vocal replies.

## Conclusion

This voice-activated chatbot allows for interactive conversation through vocal commands, enhancing user experience by providing hands-free assistance. The integration of system information and generative AI models ensures responses are contextual and informative.
