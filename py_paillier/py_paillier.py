"""Paillier encryption library for partially homomorphic encryption."""

from util import Euclid, PrimeDigit, calc_reduced_system_deductions, check_plaintext
import random


DEFAULT_BIT_KEY_LENGTH = 256


# вспомогательная функция
def l_func(u, _n):
    return (u - 1) // _n


class PaillierPublicKey(object):

    def __init__(self, n):
        # public key
        self.n = n
        self.g = self.generation_g(self.n)

        # parameters for calculations
        self.__n_square = n ** 2
        self.__multiplicative_group_mod_n = []
        self.__len_multiplicative_group_mod_n = 0

    @staticmethod
    def generation_g(_n: int):
        g = PrimeDigit().generation_big_simple_digit_in_modulo(_n ** 2)
        return g

    def show_public_key(self):
        print(f"public_key: {self.n}, {self.g}")

    def encryption(self, plaintext_as_digits_list: [int]):
        plaintext_is_current: bool = check_plaintext(
            plaintext_as_digits_list, self.n
        )
        if plaintext_is_current:
            self.__multiplicative_group_mod_n = calc_reduced_system_deductions(self.n)
            self.__len_multiplicative_group_mod_n = len(
                self.__multiplicative_group_mod_n
            )

            encrypt_text = []
            for digit in plaintext_as_digits_list:
                r = self.__multiplicative_group_mod_n[random.randint(0, self.__len_multiplicative_group_mod_n - 1)]
                encrypt_text.append(
                    ((self.g ** digit) * (r ** self.n)) % self.__n_square
                )

            return encrypt_text
        else:
            return []


class PaillierPrivateKey(object):

    def __init__(self, public_key, p, q):
        self.__public_key = public_key
        self.__p = p
        self.__q = q
        self.lambdas = self.generation_lambdas(self.__p, self.__q)
        self.mu = self.generation_mu(self.__public_key.g, self.__public_key.n, self.lambdas)

    @staticmethod
    def generation_lambdas(p: int, q: int):
        _lambdas = Euclid().least_common_multiple(p - 1, q - 1)
        return _lambdas

    @staticmethod
    def generation_mu(_g: int, _n: int, _lambdas: int):
        result_l_func = l_func(pow(_g, _lambdas, _n ** 2), _n)
        reverse_digit = Euclid().reverse_digit(result_l_func, _n)
        mu = reverse_digit % _n
        return mu

    def show_private_key(self):
        print(f"private_key: {self.lambdas}, {self.mu}")

    def decryption(self, encryption_digits_list: [int]):
        decrypt_text = []
        for encrypt_digit in encryption_digits_list:
            decrypt_digit = (
                    (l_func(
                        (encrypt_digit ** self.lambdas) % (self.__public_key.n ** 2),
                        self.__public_key.n
                    ) * self.mu) % self.__public_key.n
            )
            decrypt_text.append(decrypt_digit)

        return decrypt_text


def paillier_key_pair_generation(bit_key_length: int = DEFAULT_BIT_KEY_LENGTH):

    def p_q_generating(half_bit_key_length: int):
        _p = 3
        _q = 2

        while Euclid().greatest_common_divisor(_p * _q, (_p - 1) * (_q - 1)) != 1:
            _p = PrimeDigit().generation_big_simple_digit(half_bit_key_length)
            _q = PrimeDigit().generation_big_simple_digit(half_bit_key_length)
            while _q == _p:
                _q = PrimeDigit().generation_big_simple_digit(half_bit_key_length)

        return _p, _q

    p, q = p_q_generating(bit_key_length // 2)

    n = p * q

    public_key = PaillierPublicKey(n)
    private_key = PaillierPrivateKey(public_key, p, q)

    return public_key, private_key
