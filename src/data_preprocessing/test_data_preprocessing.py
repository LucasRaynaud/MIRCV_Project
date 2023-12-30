import unittest
import string
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from spellchecker import SpellChecker
from data_preprocessing import preprocess_text, normalize_text, tokenize, preprocess_tokenize

class TestPreprocessingFunctions(unittest.TestCase):

    def setUp(self):
        # Mocking the external dependencies like stemmer, stop_words, etc.
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.compiled_re = re.compile(r'[^a-z0-9\\s]')
        self.punctuation_translator = str.maketrans('', '', string.punctuation)
        self.spell = SpellChecker()

    def test_normalize_text(self):
        text =  ["HeLLo", "WoRLd!123"]
        expected_output = ['hello', 'world123']
        result = normalize_text(text, self.compiled_re)
        self.assertEqual(list(result), expected_output)

    def test_tokenize(self):
        text = "hello world"
        expected_output = ['hello', 'world']
        result = tokenize(text)
        self.assertEqual(result, expected_output)

    def test_preprocess_tokenize(self):
        document = "This is a sample document."
        expected_output = ['sampl', 'document']
        result = preprocess_tokenize(document, self.compiled_re, self.stemmer, self.stop_words, self.punctuation_translator, self.spell)
        self.assertEqual(list(result), expected_output)

if __name__ == '__main__':
    unittest.main()
