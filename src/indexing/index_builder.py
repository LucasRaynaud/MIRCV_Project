def parse_documents(documents):
    """
    Parses documents to extract document IDs and contents.

    Args:
    documents (list of str): List of documents where each document is a string.

    Returns:
    dict: A dictionary with document IDs as keys and document contents as values.
    """
    parsed_documents = {}
    for doc in documents:
        if '\t' in doc:  # Assuming the format is 'doc_id\tcontent'
            doc_id, content = doc.split('\t', 1)
            parsed_documents[doc_id] = content
    return parsed_documents

def create_lexicon(parsed_documents):
    """
    Create a lexicon mapping terms to unique IDs.

    Args:
    parsed_documents (dict): Parsed documents with document IDs as keys and contents as values.

    Returns:
    dict: A dictionary mapping terms to unique IDs.
    """
    lexicon = {}
    current_id = 0
    for content in parsed_documents.values():
        words = content.split()
        for word in words:
            if word not in lexicon:
                lexicon[word] = current_id
                current_id += 1
    return lexicon

def create_postings_lists(parsed_documents, lexicon):
    """
    Updated to use term IDs from the lexicon.
    """
    postings_lists = {}
    for doc_id, content in parsed_documents.items():
        words = content.split()
        for word in words:
            term_id = lexicon[word]
            if term_id not in postings_lists:
                postings_lists[term_id] = {}
            postings_lists[term_id].setdefault(doc_id, 0)
            postings_lists[term_id][doc_id] += 1
    return postings_lists

def sort_and_merge_postings(postings_lists):
    """
    Sort, merge, and apply gap compression to postings lists.

    Args:
    postings_lists (dict): Postings lists with term IDs as keys and dictionaries of document IDs and frequencies as values.

    Returns:
    dict: Gap-compressed, sorted, and merged postings lists.
    """
    for term_id, postings in postings_lists.items():
        # Sort postings by document ID
        sorted_postings = dict(sorted(postings.items()))

        # Apply gap compression
        last_doc_id = 0
        compressed_postings = {}
        for doc_id, freq in sorted_postings.items():
            gap = int(doc_id) - last_doc_id
            compressed_postings[gap] = freq
            last_doc_id = int(doc_id)

        postings_lists[term_id] = compressed_postings
    return postings_lists


def finalize_index(sorted_postings_lists):
    """
    Finalize the inverted index from sorted postings lists.

    Args:
    sorted_postings_lists (dict): Sorted and merged postings lists.

    Returns:
    dict: The final inverted index.
    """
    return sorted_postings_lists