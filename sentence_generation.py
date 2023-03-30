from keytotext import pipeline
# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration


class sentenceGeneration:

    def __init__(self):
        # self.nlp = pipeline("k2t")
        # self.model = T5ForConditionalGeneration.from_pretrained("t5-base")

        # self.model.save_pretrained("/t5base", from_pt=True)

        self.model = T5ForConditionalGeneration.from_pretrained("C:\\Users\\kshit\\Documents\\Final Year Project\\application\\models\\sentence_generation_model")
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')




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
        # self.model.eval()
        keywords_joined="WebNLG:"+" | ".join(keywords)+ " </s>"
        input_ids = self.tokenizer.encode(keywords_joined, return_tensors="pt")  # Batch size 1
        outputs = self.model.generate(input_ids)
        ans=self.tokenizer.decode(outputs[0])       
        # print(self.nlp(keywords))
        ans=ans.replace('<pad>','')
        ans=ans.replace('</s>','')
        print(ans)
        self.convertToMP3(ans)
        return ans

        

    
if __name__ == "__main__":    
    keywords=['high','blood pressure', 'doctor','emergency']
    a=sentenceGeneration()
    a.generateSentence(keywords)
