import pyttsx3


text_speech = pyttsx3.init()
text = "Virtual audio cable demo"
text_speech.say(text)
text_speech.runAndWait()

