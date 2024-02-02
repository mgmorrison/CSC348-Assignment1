def caesar_cipher(message, shift, encrypt):

    # initialize en/decoded message
    new_message = ''

    # loops through characters in message
    for ch in message:

        # shift characters up by shift places to encrypt
        if encrypt:
            new_message += chr((ord(ch)+shift-32)%95+32)

        # shift characters down by shift places to decrypt
        else:
            new_message += chr((ord(ch)-shift-32)%95+32)

    return new_message


def vignere_cipher(message, keyword, encrypt):

    # initialize en/decoded message
    new_message = ''

    # call caesar_cipher method for each character in message with corresponding keyword character
    for i in range(len(message)):
        new_message += caesar_cipher(message[i], ord(keyword[i % len(keyword)]) - 32, encrypt)

    return new_message


if __name__ == '__main__':

    # test caesar cipher by encoding then decoding
    enc_message = caesar_cipher('I love cybersecurity!', 5, True)
    print('Encrypted message: '+enc_message)
    print('Decrypted message: '+caesar_cipher(enc_message, 5, False))

    # test vignere cipher by encoding then decoding
    v_enc_message = vignere_cipher('I love cybersecurity!', 'abc', True)
    print('Encrypted message: ' + v_enc_message)
    print('Decrypted message: ' + vignere_cipher(v_enc_message, 'abc', False))
