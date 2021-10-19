from py_paillier import py_paillier


if __name__ == '__main__':
    public_key, private_key = py_paillier.paillier_key_pair_generation(25)
    public_key.show_public_key()
    private_key.show_private_key()
