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
            file.write(bytes(encoded_postings[term_id]))

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
            term_id_byte = file.read(1)
            if not term_id_byte:
                break  # End of file reached
            term_id = ord(term_id_byte)

            postings_dict = {}
            last_doc_id = 0
            while True:
                # Read the gap
                gap_bytes = []
                while True:
                    byte = file.read(1)
                    if not byte:
                        break  # End of file or no more postings
                    byte_val = ord(byte)
                    gap_bytes.append(byte_val)
                    if byte_val < 128:
                        break

                if not byte:  # Check if end of file was reached
                    break
                gap = variable_byte_decode(gap_bytes)[0] if gap_bytes else 0

                # Read the frequency
                freq_bytes = []
                while True:
                    byte = file.read(1)
                    if not byte:
                        break  # End of file or no more postings
                    byte_val = ord(byte)
                    freq_bytes.append(byte_val)
                    if byte_val < 128:
                        break

                if not freq_bytes:
                    continue  # No frequency bytes, skip this posting

                freq = variable_byte_decode(freq_bytes)[0]

                # Calculate document ID from gap and update postings
                doc_id = last_doc_id + gap
                postings_dict[str(doc_id)] = freq
                last_doc_id = doc_id

            inverted_index[term_id] = postings_dict

    return inverted_index
