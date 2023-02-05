#msg = "Hello World"
from datetime import datetime

import speech_recognition as sr 

import pyttsx3 #text 2 speech
import webbrowser 
import wikipedia 
import wolframalpha 

print(sr.__version__)


# SPEECH ENGINE INITIALIZATION 
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0 -> male, 1 -> femals 
activationWord = 'parker' 

# USING TEXT TO SPEECH LIBRARY TO SPEAK TEXT
def speak(text, rate = 120): #rate of speech 
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


# LISTENER, UNDERSTANDING MICROPHONE INPUT 
def parseCommand():
    listener = sr.Recognizer() # parse voice to text
    print('Listening for a command')

    with sr.Microphone() as source:
        listener.pause_threshold = 2 #cutoff 
        input_speech = listener.listen(source) # google api of speech recognition, limit of 30 sec at a time 
        #input_speech is whatever that was received from the microphone 

    try:
        print('Recognizing Speech')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not catch that')
        speak('I did not catch that')
        print(exception)
        return 'None'
    
    return query

# MAIN LOOP 
if __name__ == '__main__': 
    speak('Initializing my Brain')

    while True: # Listen for commands until False 
        # Parse Command as list
        # First word expect to hear is the activation keyword, Parker 
        query = parseCommand().lower().split()

        # if first word is activation word 
        if query[0] == activationWord:
            query.pop(0)


            # List Commands 
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, Ross')

                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)




            # morning rundown 
                # how many emails 
                # weather 
                # whats on my schedule 
                # important events 

