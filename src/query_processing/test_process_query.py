import unittest
from process_query import process_query, tfidf, bm25, conjunctive_query, disjunctive_query

# Mock Inverted Index and Lexicon
mock_inverted_index = {
    1: {1: 3, 2: 2},  # Term 1 appears 3 times in doc 1, 2 times in doc 2
    2: {2: 1},        # Term 2 appears once in doc 2
}

mock_lexicon = {
    "term1": 1,
    "term2": 2,
}

total_docs = 2  # Total number of documents


class TestQueryProcessing(unittest.TestCase):
    
    def test_tfidf(self):
        # Test the TF-IDF function
        score = tfidf(mock_inverted_index, 1, 1, total_docs)
        self.assertTrue(isinstance(score, float))  # Check if score is a float

    def test_bm25(self):
        # Test the BM25 function
        avgdl = 100  # Assuming average document length is 100
        score = bm25(mock_inverted_index, 1, 1, total_docs, avgdl)
        self.assertTrue(isinstance(score, float))  # Check if score is a float

    def test_conjunctive_query(self):
        # Test the conjunctive query function
        results = conjunctive_query(["term1", "term2"], mock_inverted_index, mock_lexicon)
        self.assertIn(2, results)  # Document 2 should be in the results

    def test_disjunctive_query(self):
        # Test the disjunctive query function
        results = disjunctive_query(["term1", "term2"], mock_inverted_index, mock_lexicon)
        self.assertIn(1, results)  # Document 1 should be in the results
        self.assertIn(2, results)  # Document 2 should also be in the results

    def test_process_query(self):
        # Test the process_query function
        query = "term1 term2"
        results = process_query(query, mock_inverted_index, mock_lexicon, total_docs, ranking='tfidf', query_type='AND')
        self.assertTrue(len(results) > 0)  # Check if results are returned

# Additional tests can be added for edge cases and more complex scenarios

if __name__ == '__main__':
    unittest.main()
