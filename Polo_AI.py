import speech_recognition as sr
import os
import webbrowser
import datetime
import pywhatkit
import pyttsx3
import sys
import pyautogui
import ollama
import time

# def ai_response(prompt: str) -> str:
#     try:
#         response = ollama.chat(
#             model="phi3",   
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response["message"]["content"]
#     except Exception as e:
#         return f"Error talking to Ollama: {e}"

def ai_response(prompt: str) -> str:
    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )
        # Handle both formats: single "message" or list of "messages"
        if "message" in response and "content" in response["message"]:
            return response["message"]["content"]
        elif "messages" in response and isinstance(response["messages"], list):
            return response["messages"][-1].get("content", "")
        else:
            return str(response)
    except Exception as e:
        return f"Error talking to Ollama: {e}"
    
    
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[7].id)  

def say(text , voice = "Fred"):
    if not text:
        return
    print("Speaking:", text[:80], "..." if len(text) > 80 else "")
    engine.say(text)
    engine.runAndWait()

def say_AI(text, voice="Fred"):
    if not text:
        return
    print("Speaking:", text[:80], "..." if len(text) > 80 else "")
    os.system(f'say -v "{voice}" "{text}"')


# def say(text):
#     engine.say(text)
#     engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")

        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query

        except sr.WaitTimeoutError:
            print("No audio detected from source")
            return ""

        except sr.UnknownValueError:
            print("Sorry, could not understand your speech")
            return ""

        except sr.RequestError:
            print("Speech recognition service unavailable")
            return ""


def processCommand(text):
    if "date" in text.lower():
        date = datetime.date.today()
        say(f"The date today is {date}")

    elif "time" in text.lower():
        now = datetime.datetime.now()
        hour = now.strftime("%I").lstrip("0")
        minute = now.strftime("%M")
        ampm = now.strftime("%p")

        if minute == "00":
            say(f"The time right now is {hour} o'clock {ampm}")
        else:
            say(f"The time right now is {hour}:{minute} {ampm}")

    elif "open calculator" in text.lower():
        os.system("open /System/Applications/Calculator.app")

    elif text.lower().startswith("play"):
        song = text.lower().replace("play", "").strip()
        pywhatkit.playonyt(song)
        say("Playing " + song)
    else:
        return False  
    return True  


# def stop():
#     engine.say("Goodbye, shutting down.")
#     engine.runAndWait()   # ensure speech completes
#     time.sleep(0.3)       # let audio driver flush
#     sys.exit(0)

def stop():
    os.system('say "Goodbye, shutting down."')  # macOS system TTS
    sys.exit(0)



if __name__ == '__main__':
    say("Hello, I am Polo. How may I help you?")

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["whatsapp", "https://web.whatsapp.com/"],
        ["google", "https://www.google.com"],
        ["github", "https://www.github.com"],
        ["stackoverflow", "https://stackoverflow.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["reddit", "https://www.reddit.com"],
        ["twitter", "https://twitter.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["amazon", "https://www.amazon.com"],
        ["netflix", "https://www.netflix.com"],
        ["gemini", "https://gemini.google.com"],
        ["chatgpt", "https://chat.openai.com"],
        ["instagram", "https://www.instagram.com"],
        ["facebook", "https://www.facebook.com"],
        ["spotify", "https://www.spotify.com"],
        ["news", "https://news.google.com"],
        ["gmail", "https://mail.google.com"],
        ["maps", "https://maps.google.com"]
    ]

    apps = [
        ["calculator", "open /System/Applications/Calculator.app"],
        ["safari", "open /Applications/Safari.app"],
        ["notes", "open /System/Applications/Notes.app"],
        ["calendar", "open /System/Applications/Calendar.app"],
        ["music", "open /System/Applications/Music.app"],
        ["messages", "open /System/Applications/Messages.app"],
        ["facetime", "open /System/Applications/FaceTime.app"]
    ]

    while True:
        query = take_command()

        if not query:
            continue

        if "stop" in query.lower() and "polo" in query.lower():
            stop()

        handled = False

        if "open" in query.lower():
            for site in sites:
                if f"open {site[0]}" in query.lower():
                    say(f"Opening {site[0]}")
                    webbrowser.open(site[1])
                    handled = True
                    break

        if not handled and "open" in query.lower():
            for app in apps:
                if f"open {app[0]}" in query.lower():
                    say(f"Opening {app[0]}")
                    os.system(app[1])
                    handled = True
                    break

        if not handled:
            handled = processCommand(query)

        if not handled:
            reply = ai_response(query)
            print("AI Response:", reply)
            say_AI(reply)

