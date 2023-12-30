def save_document_index(document_index,filename):
    """
    Saves the document index to a text file.

    Args:
    document_index (dict): A dictionary mapping document id to the length of the document
    filename (str): The filename to save the document_index.
    """
    with open(filename, 'w') as file:
        for docid, doclen in document_index.items():
            file.write(f"{docid}\t{doclen}\n")

def load_document_index(filename):
    """
    Loads the docmuent_index from a text file.

    Args:
    filename (str): The filename of the document_index file.

    Returns:
    dict: A dictionary mapping docid to doc length.
    """
    document_index = {}
    with open(filename, 'r',encoding="utf-8") as file:
        for line in file:
            docid, doc_len = line.strip().split('\t')
            document_index[docid] = int(doc_len)
    return document_index

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
    with open(filename, 'r',encoding="utf-8") as file:
        for line in file:
            term, term_id = line.strip().split('\t')
            lexicon[term] = int(term_id)
    return lexicon

def save_inverted_index(inverted_index, filename):
    with open(filename, 'wb') as file:
        for term_id, encoded_postings in inverted_index.items():
            # Apply variable byte encoding to the term ID
            file.write(bytes(variable_byte_encode(term_id)))

            # Write the length of the encoded postings list (variable byte encoded)
            postings_length_encoded = variable_byte_encode(len(encoded_postings))
            file.write(bytes(postings_length_encoded))

            # Write the encoded postings list
            file.write(bytes(encoded_postings))

def variable_byte_decode(encoded_bytes):
    """Decodes a sequence of bytes using variable byte encoding.

    Args:
    encoded_bytes (list of int): The encoded bytes.

    Returns:
    list of int: The decoded integers.
    """
    decoded_numbers = []
    current_number = 0
    for byte in encoded_bytes:
        # Add the 7 least significant bits of the byte to the current number
        current_number = (current_number << 7) | (byte & 0x7F)
        # Check if this is the last byte in the number
        if (byte & 0x80) == 0:  # If the most significant bit is not set
            decoded_numbers.append(current_number)
            current_number = 0  # Reset for the next number
    return decoded_numbers

def variable_byte_encode(number):
    """Encodes a number using variable byte encoding."""
    if number == 0:
        return [0]

    bytes_list = []
    while number > 0:
        bytes_list.insert(0, number % 128)
        number >>= 7

    # Set the most significant bit to 1 for all but the last byte
    for i in range(len(bytes_list) - 1):
        bytes_list[i] |= 0x80
    bytes_list[-1] |= 0x00  # Ensure the last byte is in the range 0-127

    return bytes_list

def load_inverted_index_binary(filename):
    """Loads the inverted index from a binary file with specified structure."""
    inverted_index = {}
    with open(filename, 'rb') as file:
        while True:
            # Read the term ID (with variable byte encoding)
            term_id_bytes = []
            while True:
                byte = file.read(1)
                if not byte:
                    break  # End of file reached or no more term IDs
                byte_val = ord(byte)
                term_id_bytes.append(byte_val)
                if byte_val < 128:  # End of the variable byte encoded term ID
                    break

            if not term_id_bytes:  # Check if end of file was reached
                break

            term_id = variable_byte_decode(term_id_bytes)[0]

            # Read the length of the bytes of the posting list
            postings_length_bytes = []
            while True:
                byte = file.read(1)
                byte_val = ord(byte)
                postings_length_bytes.append(byte_val)
                if byte_val < 128:  # End of the variable byte encoded length
                    break

            postings_length = variable_byte_decode(postings_length_bytes)[0]

            # Read the posting list bytes based on the obtained length
            postings_bytes = file.read(postings_length)

            # Decode the posting list (considering document IDs are stored as gaps)
            decoded_postings = variable_byte_decode(postings_bytes)
            postings_dict = {}
            last_doc_id = 0
            for i in range(0, len(decoded_postings), 2):
                gap = decoded_postings[i]
                freq = decoded_postings[i + 1]
                doc_id = last_doc_id + gap
                postings_dict[str(doc_id)] = freq
                last_doc_id = doc_id

            inverted_index[term_id] = postings_dict

    return inverted_index