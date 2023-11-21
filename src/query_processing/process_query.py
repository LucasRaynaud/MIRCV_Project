import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from data_preprocessing.data_preprocessing import preprocess_text

import math

def tfidf(inverted_index, doc_id, term_id, total_docs):
    """
    Calculate the TF-IDF score for a term in a specific document.

    Args:
    inverted_index (dict): The inverted index.
    doc_id (int): The document ID.
    term_id (int): The term ID.
    total_docs (int): The total number of documents in the corpus.

    Returns:
    float: The TF-IDF score.
    """
    # Calculate TF (Term Frequency)
    tf = inverted_index[term_id].get(doc_id, 0)

    # Calculate IDF (Inverse Document Frequency)
    doc_freq = len(inverted_index[term_id])
    idf = math.log(total_docs / doc_freq)

    return tf * idf

def bm25(inverted_index, doc_id, term_id, total_docs, avgdl,k1=1.5, b=0.75):
    """
    Calculate the BM25 score for a term in a specific document.

    Args:
    inverted_index (dict): The inverted index.
    doc_id (int): The document ID.
    term_id (int): The term ID.
    total_docs (int): The total number of documents in the corpus.
    avgdl (float): The average document length across the corpus.
    k1 (float): The BM25 parameter.
    b (float): The BM25 parameter.

    Returns:
    float: The BM25 score.
    """
    # Calculate IDF (Inverse Document Frequency)
    doc_freq = len(inverted_index[term_id])
    idf = math.log((total_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

    # Calculate term frequency in the document
    tf = inverted_index[term_id].get(doc_id, 0)

    # Calculate the document length
    doc_length = sum(inverted_index[term].get(doc_id, 0) for term in inverted_index)

    # Calculate BM25
    score = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avgdl))))
    return score


def average_document_length(inverted_index):
    total_length = 0
    doc_count = 0
    for term_id in inverted_index:
        postings = inverted_index[term_id]
        total_length += sum(postings.values())
        doc_count += len(postings)
    return total_length / doc_count if doc_count > 0 else 0

def compute_scores(query_terms, inverted_index, lexicon, total_docs, ranking_func):
    scores = {}
    avgdl = average_document_length(inverted_index) if ranking_func == bm25 else 0

    for term in query_terms:
        term_id = lexicon.get(term)
        if term_id is not None and term_id in inverted_index:
            postings = inverted_index[term_id]
            for doc_id in postings:
                if doc_id not in scores:
                    scores[doc_id] = 0
                if ranking_func == tfidf:
                    score = ranking_func(inverted_index, doc_id, term_id, total_docs)
                elif ranking_func == bm25:
                    score = ranking_func(inverted_index, doc_id, term_id, total_docs, avgdl=avgdl)
                scores[doc_id] += score

    return scores

def process_query(query, inverted_index, lexicon, total_docs, ranking='tfidf', query_type='AND'):
    """
    Process the query, compute ranking scores and return relevant documents ordered by relevance.

    Args:
    query (str): The user's query.
    inverted_index (dict): The inverted index.
    lexicon (dict): The lexicon mapping terms to term IDs.
    total_docs (int): The total number of documents in the corpus.
    ranking (str): The ranking method ('tfidf' or 'bm25').
    query_type (str): The type of query ('AND' or 'OR').

    Returns:
    list: A list of tuples (doc_id, score) ordered by score.
    """
    processed_query = preprocess_text(query)
    query_terms = processed_query.split()

    # Select relevant documents based on query type
    if query_type == 'AND':
        relevant_docs = conjunctive_query(query_terms, inverted_index, lexicon)
    else:  # 'OR' query type
        relevant_docs = disjunctive_query(query_terms, inverted_index, lexicon)

    # Compute scores only for relevant documents
    ranking_func = bm25 if ranking == 'bm25' else tfidf
    scores = {}
    avgdl = average_document_length(inverted_index) if ranking_func == bm25 else 0

    for doc_id in relevant_docs:
        scores[doc_id] = 0
        for term in query_terms:
            if term in lexicon:
                term_id = lexicon[term]
                if ranking_func == tfidf:
                    score = ranking_func(inverted_index, doc_id, term_id, total_docs)
                elif ranking_func == bm25:
                    score = ranking_func(inverted_index, doc_id, term_id, total_docs, avgdl=avgdl)
                scores[doc_id] += score

    # Sort documents by their scores in descending order
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs

def conjunctive_query(preprocessed_query, inverted_index, lexicon):
    posting_lists = [inverted_index[lexicon[term]] for term in preprocessed_query if term in lexicon]
    
    if not posting_lists:
        return []

    # Find intersection of posting lists
    common_documents = set.intersection(*map(set, posting_lists))
    return list(common_documents)

def disjunctive_query(preprocessed_query, inverted_index, lexicon):
    all_documents = set()

    for term in preprocessed_query:
        if term in lexicon:
            all_documents.update(inverted_index[lexicon[term]])

    return list(all_documents)
