import time,cProfile
from input_output.index_io import load_document_index, load_inverted_index_binary, load_lexicon
from query_processing.process_query import process_query

def main():
    # Load inverted index and lexicon
    inverted_index_start = time.time()
    print("Loading the inverted index")
    inverted_index = load_inverted_index_binary('data/inverted_index_100000.bin')
    print(f"Inverted index loaded in {time.time() - inverted_index_start} s")
    total_docs = len(inverted_index)  # Adjust this if needed

    lexicon_start = time.time()
    print("Loading lexicon")
    lexicon = load_lexicon('data/lexicon.txt')
    print(f"Lexicon loaded in {time.time() - lexicon_start} s")

    document_index_start = time.time()
    print("Loading document index")
    document_index = load_document_index("data/document_index.txt")
    print(f"Document index loaded in {time.time() - document_index_start} s")

    # User input for query and number of documents
    while True:
        user_query = input("Enter your query: ")
        num_docs = int(input("Enter the number of documents you want to retrieve: "))

        query_start = time.time()
        # Process query (adjust 'tfidf' to 'bm25' if desired)
        results_tfidf = process_query(user_query, inverted_index, lexicon, document_index, total_docs, ranking='tfidf')
        top_results_tfidf = results_tfidf[:num_docs]
        print(f"Top {num_docs} relevant documents TFIDF:")
        for doc_id, score in top_results_tfidf:
            print(f"Document ID: {doc_id}, Score: {score}")
        print(f"TFIDF processed in {time.time() - query_start} s")

        query_start = time.time()
        results_bm25 = process_query(user_query, inverted_index, lexicon,document_index, total_docs, ranking='bm25')
        top_results_bm25 = results_bm25[:num_docs]
        print(f"Top {num_docs} relevant documents BM25:")
        for doc_id, score in top_results_bm25:
            print(f"Document ID: {doc_id}, Score: {score}")
        print(f"BM25 processed in {time.time() - query_start} s")

if __name__ == "__main__":
    cProfile.run('main()', 'output.prof')
