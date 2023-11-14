import unittest
from data_preprocessing import read_data_from_tar_gz, normalize_text, tokenize, preprocess_text

class TestDataPreprocessing(unittest.TestCase):

    def test_read_data_from_tar_gz(self):
        # Test reading data from a .tar.gz file
        data_gen = read_data_from_tar_gz('data/msmarco/sub_collection.tar.gz')
        first_line = next(data_gen)
        self.assertTrue(len(first_line) > 0)  # Check if the first line is not empty

    def test_normalize_text(self):
        # Test text normalization
        original_text = "Hello, World! 123"
        expected_normalized_text = "hello world 123"
        self.assertEqual(normalize_text(original_text), expected_normalized_text)

    def test_tokenize(self):
        # Test tokenization
        text = "hello world"
        expected_tokens = ["hello", "world"]
        self.assertEqual(tokenize(text), expected_tokens)

    def test_preprocess_text(self):
        # Test case with a mix of stopwords and regular words
        input_text = "This is a test of the preprocessing function."
        expected_output = "test preprocess function"
        self.assertEqual(preprocess_text(input_text), expected_output)

        # Test case with all stopwords
        input_text = "This is and of the"
        expected_output = ""
        self.assertEqual(preprocess_text(input_text), expected_output)

        # Test case with no stopwords
        input_text = "Unique words only"
        expected_output = "uniqu word"
        self.assertEqual(preprocess_text(input_text), expected_output)

        # Test case with punctuation (assuming basic split on space)
        input_text = "Testing, with punctuation!"
        expected_output = "test punctuat"
        self.assertEqual(preprocess_text(input_text), expected_output)

        # Test case with case sensitivity
        input_text = "The Preprocessing Function Works Well"
        expected_output = "preprocess function work well"
        self.assertEqual(preprocess_text(input_text), expected_output)

# Run the tests
if __name__ == '__main__':
    unittest.main()