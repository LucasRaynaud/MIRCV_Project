import tarfile

def parse_documents(tar_path):
    """
    Parses documents to extract document IDs and contents.

    Args:
    documents (list of str): List of documents where each document is a string.

    Returns:
    dict: A dictionary with document IDs as keys and document contents as values.
    """
    documents = {}
    with tarfile.open(tar_path, "r:gz") as tar:
        tsv_file = tar.extractfile('collection.tsv')
        if tsv_file:
            content = tsv_file.read().decode('utf-8')
            lines = content.split('\n')
            for line in lines:
                if '\t' in line:
                    doc_id, doc_content = line.split('\t', 1)
                    documents[doc_id] = doc_content
    return documents


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

def variable_byte_encode(number):
    """Encodes a number using variable byte encoding.

    Args:
    number (int): The number to encode.

    Returns:
    list: A list of integers, each representing an encoded byte.
    """
    if number == 0:
        return [0]

    bytes_list = []
    while number > 0:
        # Extract the last 7 bits
        byte = number & 0b01111111
        # Shift to prepare for the next iteration
        number >>= 7
        # Add to the list
        bytes_list.append(byte)
    
    # Reverse the list and add the continuation bits
    bytes_list = bytes_list[::-1]
    for i in range(len(bytes_list)):
        # Add continuation bit (1 for all but the last byte)
        bytes_list[i] |= 0b10000000 if i < len(bytes_list) - 1 else 0

    return bytes_list


def sort_and_merge_postings(postings_lists):
    """ Apply gap compression with variable-byte encoding. """
    for term_id, postings in postings_lists.items():
        postings = {int(doc_id): freq for doc_id, freq in postings.items()}
        sorted_postings = dict(sorted(postings.items()))
        last_doc_id = 0
        final_postings = []
        for doc_id, freq in sorted_postings.items():
            print(doc_id)
            print(freq)
            gap = doc_id - last_doc_id
            final_postings[gap] = freq
            last_doc_id = doc_id
        postings_lists[term_id] = final_postings
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