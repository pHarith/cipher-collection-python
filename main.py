"""
Sample Application to put Cipher Algorithms to Use.
"""

from cipher import *

choice_to_functions = {'a': caesar_cipher, 'b': sub_cipher, 'c': playfair_cipher, 'd': vignette_cipher}

class ApplicationError(Exception):
    pass

if __name__ == "__main__":
    print('='*20, ' Welcome to the Cipher Program. ', '='*20)
    text = input('Input text to be ciphered/deciphered: ')

    choice = input('Which algorithm do you wish to use?\na) Caesar Cipher\t\tb) Substitution Cipher'
            + '\nc) Playfair Cipher \t\td) Vignette Cipher\n')

    if choice in ['a', 'c', 'd']:
        key = input('Input Secret Key: ')
        mode = input('Choose Mode to use:\na) Encrypt\t\tb) Decipher\n')
        if choice == 'a':
            int_key = int(key) if mode == 'a' else abs(26 - int(key))
            try:
                result = choice_to_functions[choice](text, int_key)
            except:
                raise ApplicationError
        result = choice_to_functions[choice](text, str(key), mode)
    elif choice == 'b':
        result = choice_to_functions[choice](text)
    print('Here is the result: ', result)