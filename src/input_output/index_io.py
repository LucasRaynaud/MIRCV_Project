def save_lexicon(lexicon, filename):
    """
    Saves the lexicon to a text file.

    Args:
    lexicon (dict): A dictionary mapping terms to unique IDs.
    filename (str): The filename to save the lexicon.
    """
    with open(filename, 'w') as file:
        for term, term_id in lexicon.items():
            file.write(f"{term}\t{term_id}\n")

def load_lexicon(filename):
    """
    Loads the lexicon from a text file.

    Args:
    filename (str): The filename of the lexicon file.

    Returns:
    dict: A dictionary mapping terms to unique IDs.
    """
    lexicon = {}
    with open(filename, 'r') as file:
        for line in file:
            term, term_id = line.strip().split('\t')
            lexicon[term] = int(term_id)
    return lexicon


def save_inverted_index(inverted_index, filename):
    """
    Saves the inverted index to a text file.

    Args:
    inverted_index (dict): The inverted index to save.
    filename (str): The filename to save the inverted index.
    """
    with open(filename, 'w') as file:
        for term_id, postings in inverted_index.items():
            postings_str = ','.join([f"{doc_id}:{freq}" for doc_id, freq in postings.items()])
            file.write(f"{term_id}\t{postings_str}\n")

def load_inverted_index(filename):
    """
    Loads the inverted index from a text file.

    Args:
    filename (str): The filename of the inverted index file.

    Returns:
    dict: The inverted index.
    """
    inverted_index = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                term_id, postings_str = parts
                postings = {}
                for posting in postings_str.split(','):
                    doc_id, freq = posting.split(':')
                    postings[int(doc_id)] = int(freq)
                inverted_index[int(term_id)] = postings
    return inverted_index
