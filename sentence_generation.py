from keytotext import pipeline

class sentenceGeneration:

    def __init__(self):
        self.nlp = pipeline("k2t")
    
    def generateSentence(self,keywords):        
        print(self.nlp(keywords))
        return self.nlp(keywords)
    
if __name__ == "__main__":    
    keywords=['high','blood pressure', 'doctor','emergency']
    a=sentenceGeneration()
    a.generateSentence(keywords)