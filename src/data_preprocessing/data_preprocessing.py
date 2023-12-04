import re
import string

def preprocess_text(text,stemmer,stop_words,punctuation_translator):
    """
    Preprocesses the input text by removing stopwords and applying stemming.

    Args:
    text (dict(str)): The input text to preprocess.

    Returns:
    dict(str): The preprocessed text.
    """
    # Remove punctuation
    words = {word.translate(punctuation_translator) for word in text}

    processed_words = [stemmer.stem(word) for word in words if word not in stop_words]

    return processed_words
    
def normalize_text(text,compiled_re):
    """
    Normalizes the given text by lowercasing and removing non-alphanumeric characters.

    Args:
    text (dict(str)): The text to be normalized.

    Returns:
    dict(str): The normalized text.
    """
    return {compiled_re.sub('', word.lower()) for word in text}

def tokenize(text):
    """
    Tokenizes the given text into words.

    Args:
    text (str): The text to be tokenized.

    Returns:
    list of str: A list of words (tokens) from the text.
    """
    return text.split()

def preprocess_tokenize(document,compiled_re,stemmer,stop_words,punctuation_translator):
    tokenized_document = tokenize(document)
    normalized_text = normalize_text(tokenized_document,compiled_re)
    return preprocess_text(normalized_text,stemmer,stop_words,punctuation_translator)
