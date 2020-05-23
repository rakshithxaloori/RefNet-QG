import string

from nltk.tokenize import wordpunct_tokenize, word_tokenize
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def remove_non_language(sentence, language_code):
    """ Removes the non-language words from a sentence. """
    for word in word_tokenize(sentence):
        # Ignoring punctuations
        if word in string.punctuation or word in string.digits:
            continue
        
        # Punctuations throw an exception
        try:
            if detect(word) != language_code:
                sentence = sentence.replace(word, '')
        except LangDetectException:
            # Probably, a punctuation is detected
            pass
    return sentence