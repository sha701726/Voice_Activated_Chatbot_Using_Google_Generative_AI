import google.generativeai as genai
import subprocess
import speech_recognition as sr
import pyttsx3

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 140) 
engine.setProperty('volume', 1) 
voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', voice_id)

# Configure the API key for the Generative AI service
genai.configure(api_key="AIzaSyAxFa_ZyjIrZ8vdVOHTLb6BYwjQLJpPYJs")

# Get OS data using a shell command
try:
    command = '''systeminfo | findstr /B /C:"OS Name:" /C:"OS Version:"'''
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    os_data = result.stdout
except Exception as e:
    print(f"Error retrieving OS data: {e}")
    os_data = "Unknown OS data"

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-flash')

# Start the initial chat session with valid roles
chat = model.start_chat(
    history=[
        {"role": "user", "parts": f"Here is some system data: {os_data}. Please ensure answers are precise and accurate, holding a minimum number of lines."},
        {"role": "model", "parts": "Understood. I'm ready to help with your problems or doubts."}
    ]
)

# Loop to interact with the chat session
while True:
    with sr.Microphone() as source:
        print("Please ask something...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")  # Print user input for confirmation
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            continue
    
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting the chat.")
        break  # Use break instead of exit() for a cleaner exit

    if user_input.lower() == 'clear':
        # Reinitialize the chat session to clear history
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Please ensure answers are precise and accurate."},
                {"role": "model", "parts": "Understood. I'm ready to help with your questions."}
            ]
        )
        print("Chat history cleared.")
        continue
    
    # Send the user's question to the chat session and get the response
    response = chat.send_message(user_input, stream=True)
    for chunk in response:
        print(chunk.text, end="")
        engine.say(chunk.text)
        engine.runAndWait()
