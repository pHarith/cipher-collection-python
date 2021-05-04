from typing import List, Any, Dict


# alphabet = 'abcdefghijklmnopqrstuvwxyz'
# index_to_letter = dict(zip(range(1, len(alphabet) + 1), alphabet))
# letter_to_index = dict(alphabet, zip(range(1, len(alphabet) + 1)))

alpha = [chr(i) for i in range(97, 123)]
alpha_reversed = [alpha[i] for i in range(len(alpha) - 1, -1, -1)]
index_to_letter = {k: v for k, v in enumerate(alpha)}
letter_to_index = {v: k for k,v in enumerate(alpha)}


class IncorrectModeError(Exception):
    pass

def baconian_cipher(s: str) -> str:
    """
    """
    encoded = ''
    baconian_dict = get_baconian_dict()
    for i in s:
        if i in alpha:
            encoded += baconian_dict[i]
        else:
            encoded += i
    return encoded

def caesar_cipher(s: str, key: int) -> str:
    """
    Cipher algorithm that encodes and decodes <s>, using a specific key to shift letters forward by
    <key>. To decode <s>, the <key> must be in form of 26 - <original_key>.

    >>> caesar_cipher('high ground', 66)
    'vwuv ufcibr'
    >>> caesar_cipher('birdy', 4)
    'fmvhc'
    >>> caesar_cipher('fmvhc', 22) # 26 - 4
    'birdy'
    """
    encoded = ''
    for i in range(len(s)):
        if s[i] in alpha:
            encoded += alpha[(alpha.index(s[i]) + key) % 26]
        else:
            encoded += s[i]
    return encoded

def atbash_cipher(s: str) -> str:
    """
    Cipher algorithm that encodes and decodes <s>, by substituting letters of <s> with 
    corresponding letters with the same index in the alphabet, counting in reverse. 
    For example, a -> z and z -> a, b -> y and y -> b and so forth.

    >>> atbash_cipher('hello there')
    'svool gsviv'
    >>> atbash_cipher('svool gsviv')
    'hello there'
    >>> atbash_cipher('tvmvizo pvmlyr')
    'general kenobi'
    """
    encoded = ''
    for i in range(len(s)):
        try:
            org = alpha.index(s[i])
            encoded += alpha_reversed[org]
        except ValueError:
            encoded += s[i]
    return encoded

def substitution_cipher(key: str) -> str:
    pass

def hill_cipher(key: str):
    return encoded

def keyword_cipher():
    return encoded

def playfair_cipher(s: str, key: str, mode: str) -> str:
    """
    Cipher algorithm that encodes <s>, by using a playfair cipher, requiring a
    string <key> and <mode> for either encoding or decoding a message.

    >>> playfair_cipher('secret message', 'keyword', 'encode')
    'nordkunkqzpcnd'
    >>> playfair_cipher('nordkunkqzpcnd', 'keyword', 'decode')
    'secretmessage'
    """
    if mode == 'encode':
        return playfair_encrypt(s, key)
    elif mode == 'decode':
        return playfair_decrypt(s, key)
    raise IncorrectModeError('Invalid mode parameter.')

def vignette_cipher(s: str, key: str, mode: str) -> str:
    """
    Cipher algorithm that encodes and decodes <s>, by using a vignette cipher algorithm, 
    requiring a string <key> and <mode> for either encoding or decoding.

    >>> vignette_cipher('batmanandrobin', 'joker', 'encode')
    'lpersxpyijyqts'
    >>> vignette_cipher('lpersxpyijyqts', 'joker', 'decode')
    'batmanandrobin'
    """
    ciphered = ''
    text = s.strip(' ')
    keystream = ''.join([key[: min(len(key), len(text) - i)] for i in range(0, len(text), len(key))])
    index_lst = [letter_to_index[c] for c in text]

    key_index_lst = [letter_to_index[k] for k in keystream]
    if mode == 'encode':
        cipher_index_lst = [(index_lst[i] + key_index_lst[i]) % 26 for i in range(len(index_lst))]
    elif mode == 'decode':
        cipher_index_lst = [(index_lst[i] - key_index_lst[i]) % 26 for i in range(len(index_lst))]
    else:
        raise IncorrectModeError('Invalid mode parameter.')
    return ''.join(index_to_letter[n] for n in cipher_index_lst)

def bifid_cipher():
    return encoded

def vernam_cipher():
    return encoded

def playfair_encrypt(s: str, key: str) -> str:
    """
    Cipher algorithm that encodes <s>, by using a playfair cipher, requiring a
    string <key> and <mode>.

    >>> playfair_encrypt('secret message', 'keyword')
    'nordkunkqzpcnd'
    """
    encoded = ''

    # Process of spliting up the original message
    s = s.replace(' ', '')
    for j in range(len(s) - 1) :
        if s[j] == s[j + 1]:
            s = s[:j + 1] + 'x' + s[j + 1:]
    if len(s) % 2 != 0:
        s = s + 'x'
    s_pairs = [s[i: i + 2] for i in range(0, len(s), 2)]
    
    # Forming the 5 x 5 matrix we need for our cipher
    cipher_matrix = get_cipher_matrix(key)

    # Encoding the Message
    for i in range(len(s_pairs)):
        encoded += encode_pair(s_pairs[i], cipher_matrix)

    # Return encoded message
    return encoded

def playfair_decrypt(s: str, key: str) -> str:
    """
    Cipher algorithm that decodes <s>, by using a playfair cipher, requiring a
    string <key>.

    >>> playfair_decrypt('nordkunkqzpcnd', 'keyword')
    'secretmessage'
    """
    decoded = ''
    cipher_matrix = get_cipher_matrix(key)
    s_pairs = [s[i: i + 2] for i in range(0, len(s), 2)]

    for i in range(len(s_pairs)):
        decoded += decode_pair(s_pairs[i], cipher_matrix)
    return remove_x(decoded)

# Helper Functions Here
def get_cipher_matrix(key: str) -> List[List[str]]:
    """
    Helper Function for playfair cipher. Produces a unique 5 x 5 matrix 
    (nested list of alphabets) for each input <key>.

    Algorithm Rules:
    1. List all alphabets, but remove j.
    2. Form a 5 x 5 matrix, and add the keywords to the top portion of matrix,
    left to right. 
    3. Fill in the rest of the matrix with remaining alphabets.

    Precondition: <key> must contain each letter no more than once.
    """
    cipher_matrix = []
    alpha_j = [a for a in alpha if a != 'j']
        
    i = 0
    while i < len(key):
        row = []
        while len(row) < 5 and i < len(key):
            row.append(key[i])
            alpha_j.remove(key[i])
            i += 1
        cipher_matrix.append(row)

    j = 0
    while j < len(alpha_j):
        if len(cipher_matrix[-1]) < 5:
            cipher_matrix[-1].append(alpha_j[j])
            j += 1
        else:
            row = []
            while len(row) < 5 and j < len(alpha_j):
                row.append(alpha_j[j])
                j += 1
            cipher_matrix.append(row)
    return cipher_matrix

def get_matrix_location(obj: Any, m: List[List[int]]) -> (int, int):
    """
    """
    row = 0
    while row < len(m):
        col = 0
        while col < len(m[0]):
            if m[row][col] == obj:
                return (row, col)
            col += 1
        row += 1
    return (-1, -1)

def get_smaller_matrix(loca1: (int, int), loca2: (int, int), m: List[str]):
    """
    """
    small_matrix = []
    row_start = min(loca1[0], loca2[0])
    row_stop = max(loca1[0], loca2[0])
    col_start = min(loca1[1], loca2[1])
    col_stop = max(loca1[1], loca2[1])
    for r in range(row_start, row_stop + 1):
        row = []
        for c in range(col_start, col_stop + 1):
            row.append(m[r][c])
        small_matrix.append(row)
    return small_matrix

def encode_pair(pair: (str, str), m: List[List[str]]) -> str:
    r1, c1 = get_matrix_location(pair[0], m)
    r2, c2 = get_matrix_location(pair[1], m)

    if r1 != r2 and c1 != c2:
        box = get_smaller_matrix((r1, c1), (r2, c2), m)
        b = len(box[0])
        loca1 = get_matrix_location(pair[0], box)
        loca2 = get_matrix_location(pair[1], box)
        return box[loca1[0]][b - loca1[1] - 1] + box[loca2[0]][b - loca2[1] - 1]
    elif r1 == r2:
        c1 = c1 + 1 if c1 < len(m) - 1 else 0
        c2 = c2 + 1 if c2 < len(m) - 1 else 0
    elif c1 == c2:
        r1 = r1 + 1 if r1 < len(m) - 1 else 0
        r2 = r2 + 1 if r2 < len(m) - 1 else 0
    return m[r1][c1] + m[r2][c2]


def decode_pair(pair: (str, str), m: List[List[str]]) -> str:
    r1, c1 = get_matrix_location(pair[0], m)
    r2, c2 = get_matrix_location(pair[1], m)

    if r1 != r2 and c1 != c2:
        box = get_smaller_matrix((r1, c1), (r2, c2), m)
        b = len(box[0])
        loca1 = get_matrix_location(pair[0], box)
        loca2 = get_matrix_location(pair[1], box)
        return box[loca1[0]][b - loca1[1] - 1] + box[loca2[0]][b - loca2[1] - 1]
    elif r1 == r2:
        c1 = c1 - 1
        c2 = c2 - 1
    elif c1 == c2:
        r1 = r1 - 1
        r2 = r2 -1
    return m[r1][c1] + m[r2][c2]

def remove_x(s: str) -> str:
    text = ''
    for i in range(len(s)):
        try:
            if not(s[i] == 'x' and s[i - 1] == s[i + 1]):
                text += s[i]
        except IndexError:
            text += s[i] 
    return text

def get_baconian_dict() -> Dict[str, str]:
    dictionary = {}
    for a in alpha:
        dictionary[a] = str(format(int(letter_to_index[a]), '05b')).replace('0', 'a').replace('1', 'b')
    return dictionary
