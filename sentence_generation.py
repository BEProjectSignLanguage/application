from keytotext import pipeline
# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

class sentenceGeneration:

    def __init__(self):
        self.nlp = pipeline("k2t")

    def convertToMP3(self,text):
    # The text that you want to convert to audio

        # Language in which you want to convert
        language = 'en'

        # Passing the text and language to the engine,
        # here we have marked slow=False. Which tells
        # the module that the converted audio should
        # have a high speed
        myobj = gTTS(text, lang=language,tld="co.in", slow=True)

        # Saving the converted audio in a mp3 file named
        # welcome
        os.remove('word.mp3')
        myobj.save("word.mp3")

    
    def generateSentence(self,keywords):        
        print(self.nlp(keywords))
        self.convertToMP3(self.nlp(keywords))
        return self.nlp(keywords)
    
    

    

        

    
if __name__ == "__main__":    
    keywords=['high','blood pressure', 'doctor','emergency']
    a=sentenceGeneration()
    a.generateSentence(keywords)