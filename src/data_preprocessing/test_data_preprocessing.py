import unittest
from data_preprocessing import read_data_from_tar_gz, normalize_text, tokenize

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

# Run the tests
if __name__ == '__main__':
    unittest.main()