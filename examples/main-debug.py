from py_paillier import py_paillier


if __name__ == '__main__':
    public_key, private_key = py_paillier.paillier_key_pair_generation(16)
    public_key.show_public_key()
    private_key.show_private_key()

    plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore " \
                "et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut " \
                "aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse " \
                "cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, " \
                "sunt in culpa qui officia deserunt mollit anim id est laborum."

    plaintext_as_digits_list = []
    for symbol in plaintext:
        plaintext_as_digits_list.append(ord(symbol))

    encrypt_text_as_digits_list = public_key.encryption(plaintext_as_digits_list)
    print(encrypt_text_as_digits_list)

    decrypt_text_as_digits_list = private_key.decryption(encrypt_text_as_digits_list)

    decrypt_text = ""
    for d in decrypt_text_as_digits_list:
        decrypt_text += chr(d)

    print(plaintext)
    print(decrypt_text)
    print(f"Compare plaintext & decrypt_text {plaintext == decrypt_text}")
