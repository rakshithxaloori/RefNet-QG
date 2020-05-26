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


def remove_numbers(sentence):
    """ Removes the [number] substring from sentence. """
    while True:
        index = sentence.find("[")
        if index == -1:
            break
        # Remove a set of [number]
        sentence.replace(sentence[index+2], '')
        sentence.replace(sentence[index+1], '')
        sentence.replace(sentence[index], '')

    return sentence
