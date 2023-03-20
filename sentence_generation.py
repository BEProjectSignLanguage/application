from keytotext import pipeline



class sentenceGeneration:
    
    def generateSentence(self,keywords):
        nlp = pipeline("k2t")
        return print(nlp(keywords))
keywords=['high','blood pressure', 'doctor','emergency']
a=sentenceGeneration()
a.generateSentence(keywords)