# test_index_builder.py

import unittest
from index_builder import parse_documents, create_lexicon, create_postings_lists, sort_and_merge_postings, finalize_index

class TestIndexBuilder(unittest.TestCase):

    def test_parse_documents(self):
        input_documents = ["1\tDocument one content", "2\tDocument two content"]
        expected_output = {"1": "Document one content", "2": "Document two content"}
        self.assertEqual(parse_documents(input_documents), expected_output)

    def test_create_lexicon(self):
        parsed_documents = {"1": "Document one", "2": "Document two one"}
        lexicon = create_lexicon(parsed_documents)
        self.assertTrue(isinstance(lexicon, dict))
        self.assertTrue("Document" in lexicon)
        self.assertTrue("one" in lexicon)
        self.assertTrue("two" in lexicon)

    def test_create_postings_lists(self):
        parsed_documents = {"1": "Document one", "2": "Document two one"}
        lexicon = {"Document": 0, "one": 1, "two": 2}
        postings_lists = create_postings_lists(parsed_documents, lexicon)
        expected_output = {
            0: {"1": 1, "2": 1},
            1: {"1": 1, "2": 1},
            2: {"2": 1}
        }
        self.assertEqual(postings_lists, expected_output)

    def test_sort_and_merge_postings(self):
        lexicon = {"Document": 0, "one": 1, "two": 2}
        postings_lists = {
            0: {"2": 1, "1": 1},
            1: {"2": 1, "1": 1},
            2: {"2": 1}
        }
        compressed_postings = sort_and_merge_postings(postings_lists)
        expected_output = {
            0: {1: 1, 1: 1},
            1: {1: 1, 1: 1},
            2: {2: 1}
        }
        self.assertEqual(compressed_postings, expected_output)

    def test_finalize_index(self):
        compressed_postings_lists = {
            0: {1: 1, 1: 1},
            1: {1: 1, 1: 1},
            2: {2: 1}
        }
        # The final index should be the same as compressed postings lists in this simple implementation
        self.assertEqual(finalize_index(compressed_postings_lists), compressed_postings_lists)

if __name__ == '__main__':
    unittest.main()