from input_output.index_io import load_inverted_index_binary, load_lexicon

# Assuming process_query.py is in the same directory or its path is in sys.path
from query_processing.process_query import process_query

def main():
    # Load inverted index and lexicon
    print("Loading the inverted index")
    inverted_index = load_inverted_index_binary('data/inverted_index.bin')
    print("Inverted index loaded")
    print("Loading lexicon")
    lexicon = load_lexicon('data/lexicon.txt')
    print("Lexicon loaded")
    total_docs = len(inverted_index)  # Adjust this if needed

    # User input for query and number of documents
    user_query = input("Enter your query: ")
    num_docs = int(input("Enter the number of documents you want to retrieve: "))

    # Process query (adjust 'tfidf' to 'bm25' if desired)
    results_tfidf = process_query(user_query, inverted_index, lexicon, total_docs, ranking='tfidf')
    results_bm25 = process_query(user_query, inverted_index, lexicon, total_docs, ranking='bm25')

    # Display top N results
    top_results_tfidf = results_tfidf[:num_docs]
    top_results_bm25 = results_bm25[:num_docs]
    print(f"Top {num_docs} relevant documents TFIDF:")
    for doc_id, score in top_results_tfidf:
        print(f"Document ID: {doc_id}, Score: {score}")

    print(f"Top {num_docs} relevant documents BM25:")
    for doc_id, score in top_results_bm25:
        print(f"Document ID: {doc_id}, Score: {score}")

if __name__ == "__main__":
    main()
