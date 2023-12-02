from indexing.index_builder import variable_byte_encode


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
            encoded_term_id = variable_byte_encode(term_id)
            file.write(bytes(encoded_term_id))

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

def load_inverted_index_binary(filename):
    """
    Loads the inverted index from a binary file.

    Args:
    filename (str): The filename of the inverted index file.

    Returns:
    dict: The inverted index.
    """
    inverted_index = {}
    with open(filename, 'rb') as file:
        while True:
            # Read and decode the term ID
            term_id_bytes = []
            while True:
                byte = file.read(1)
                if not byte:
                    return inverted_index  # End of file reached
                byte_val = ord(byte)
                term_id_bytes.append(byte_val)
                if byte_val < 128:
                    break
            term_id = variable_byte_decode(term_id_bytes)

            # Read and decode the length of postings list
            length_bytes = []
            for _ in range(4):  # Assuming length is encoded in 4 bytes
                byte = file.read(1)
                if not byte:
                    return inverted_index  # End of file or error
                length_bytes.append(ord(byte))
            postings_length = variable_byte_decode(length_bytes)

            # Read and decode the postings list
            encoded_postings = []
            print(postings_length)
            for _ in range(len(postings_length)):
                postings_byte = file.read(1)
                if not postings_byte:
                    break  # End of file or error
                encoded_postings.append(ord(postings_byte))

            # Decode postings list
            decoded_postings = []
            postings_bytes_iter = iter(encoded_postings)
            for byte in postings_bytes_iter:
                number_bytes = [byte]
                while byte & 0x80:  # While the continuation bit is set
                    byte = next(postings_bytes_iter, None)
                    if byte is None:
                        break  # End of file or error
                    number_bytes.append(byte)
                decoded_number = variable_byte_decode(number_bytes)
                decoded_postings.append(decoded_number)

            inverted_index[term_id] = decoded_postings

    return inverted_index