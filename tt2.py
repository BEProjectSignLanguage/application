


# The text that you want to convert to audio

    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text, lang=language, slow=True)

    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("word.mp3")


        
