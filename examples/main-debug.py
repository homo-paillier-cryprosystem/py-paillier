from py_paillier import py_paillier


if __name__ == '__main__':
    public_key, private_key = py_paillier.paillier_key_pair_generation(25)
    print(f"public_key: {public_key.n}, {public_key.g}")
    print(f"public_key: {private_key.lambdas}, {private_key.mu}")
