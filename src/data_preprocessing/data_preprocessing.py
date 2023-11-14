import re
import string
import tarfile
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess_text(text):
    """
    Preprocesses the input text by removing stopwords and applying stemming.

    Args:
    text (str): The input text to preprocess.

    Returns:
    str: The preprocessed text.
    """
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()
    processed_words = [stemmer.stem(word) for word in words if word.lower() not in stop_words]

    processed_text = ' '.join(processed_words)
    return processed_text


def read_data_from_tar_gz(file_path):
    """
    Reads data from a .tar.gz file without extracting it.

    Args:
    file_path (str): The path to the .tar.gz file containing the data.

    Returns:
    generator of str: A generator where each element is a line from the files in the archive.
    """
    with tarfile.open(file_path, "r:gz") as tar:
        for member in tar.getmembers():
            # Assuming each member (file) in the tar is a text file
            f = tar.extractfile(member)
            if f is not None:
                # This will yield lines from each file in the tar
                for line in f:
                    yield line.decode('utf-8')  # Decoding from bytes to string

    
def normalize_text(text):
    """
    Normalizes the given text by lowercasing and removing non-alphanumeric characters.

    Args:
    text (str): The text to be normalized.

    Returns:
    str: The normalized text.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters (keeping spaces)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def tokenize(text):
    """
    Tokenizes the given text into words.

    Args:
    text (str): The text to be tokenized.

    Returns:
    list of str: A list of words (tokens) from the text.
    """
    return text.split()