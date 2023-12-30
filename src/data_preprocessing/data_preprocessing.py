def preprocess_text(text,stemmer,stop_words,punctuation_translator,spell):
    """Preprocesses the input text by removing stopwords and applying stemming."""
    # Remove punctuation and check if word exists
    words = (word.translate(punctuation_translator) for word in text if word not in stop_words and spell.known([word]))

    # Stemming
    processed_words = [stemmer.stem(word) for word in words]

    return processed_words
    
def normalize_text(text,compiled_re):
    """Normalizes the given text by lowercasing and removing non-alphanumeric characters."""
    return (compiled_re.sub('', word.lower()) for word in text)

def tokenize(text):
    """Tokenizes the given text into words."""
    return text.split()

def preprocess_tokenize(document,compiled_re,stemmer,stop_words,punctuation_translator,spell):
    return preprocess_text(
        normalize_text(tokenize(document), compiled_re),
        stemmer, stop_words, punctuation_translator,spell)