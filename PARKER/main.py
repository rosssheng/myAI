#msg = "Hello World"
from datetime import datetime
from chatgpt_wrapper import ChatGPT
import speech_recognition as sr 

import pyttsx3 #text 2 speech
import webbrowser 
import wikipedia 
import wolframalpha 

# Wolfram Alpha client 
APP_ID = 'T4AXLX-9YARUGHK32'
wolframClient = wolframalpha.Client(APP_ID)

# SPEECH ENGINE INITIALIZATION 
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0 -> male, 1 -> femals 
activationWord = 'parker' 

# Configure Browser 
# Set path for Chrome 
chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# USING TEXT TO SPEECH LIBRARY TO SPEAK TEXT
def speak(text, rate = 150): #rate of speech 
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

def searchWiki(query = ' '):
    searchResults = wikipedia.search(query)  # array of results
    if not searchResults:
        print('no wiki result')
        return 'No Result Recieved'
    
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var,list):
        return var[0]['plaintext']
    
    else:
        return var['plaintext']

def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)

    if response['@success'] == 'false':
        speak('I could not compute')
    
    else:
        result = ''

        #Question asked 
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]

        # pod0 has the highest confidence value 
        #  if its primary or has the title of result or definition then its the official result 
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = listOrDict(pod1['subpod'])

            return result.split('(')[0]
        
        else:
            question = listOrDict(pod0['subpod'])
            return question.split('(')[0] 

            speak('Calculation failed. Asking Wikipedia now')
            return searchWiki(question)
        

    # @success : query resolved 
    # @numpods : Number of results returned 
    # pod : List of results, can contain subpods 







#LIMITATIONS: Navigation: need to say .com after website navigation, MAIN: always listens for command - think about an end command 
# MAIN LOOP 
if __name__ == '__main__': 
    speak('I am ready to assist you Ross')

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
                    speak('Greetings Ross')

                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            # Navigation 
            if query[0] == 'go' and query[1] == 'to':
                query = ' '.join(query[2:])

                speak('going to' + query)
                webbrowser.get('chrome').open_new(query)


            # basic tasks with wolfram alpha 

            # computations with wolfram alpha 
            if query[0] == 'calculate':
                query = ' '.join(query[1:])
                speak('Calculating')
                try:
                    result = search_wolframAlpha(query)
                    speak(result)

                except:
                    speak('Unable to calculate')


            # morning rundown 
                # how many emails 
                # weather 
                # whats on my schedule - link with notion
                # important events - link with notion 

           # link with chat gpt for basic questions you need to search for https://github.com/mmabrouk/chatgpt-wrapper
           # TOO SLOW 


