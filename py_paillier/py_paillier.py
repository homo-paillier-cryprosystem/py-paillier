"""Paillier encryption library for partially homomorphic encryption."""

from util import Euclid, PrimeDigit, calc_reduced_system_deductions, check_plaintext
import random


DEFAULT_BIT_KEY_LENGTH = 256


def l_func(u: int, _n: int):
    """ Helper function L takes an integer number of occurrences (u - 1) in n.
    Examples:
        13 / 4 = 3 * (1 / 4) -> result will be 3                  \n
        25 / 5 = 5 * (0 / 5) -> result will be 5                  \n
        67 / 11 = 6 * (1 / 11) -> result will be 6                \n
    :param u: int as dividend
    :param _n: int as divisor
    :return: int as quotient
    """
    return (u - 1) // _n


class PaillierPublicKey(object):
    """Contains a public key and associated encryption method.

    Args:
        public's:
            n (int): part of public key - see [1] \n
            g (int): part of public key - see [1] \n
        private's:
            __n_square (int): (n ** 2), stored for calculations \n
            __multiplicative_group_mod_n (list[int]): the list used to encrypt the text by this public key - see [2] \n
            __len_multiplicative_group_mod_n (int): length of __multiplicative_group_mod_n \n

    Links:
        [1] - https://en.wikipedia.org/wiki/Paillier_cryptosystem#Key_generation
        [2] - https://en.wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n
    """
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
        """Function for generating g as part of a public key.

        :param _n: int as modulo
        :return: g (int) as large prime
        """
        g = PrimeDigit().generating_a_large_prime_modulo(_n ** 2)
        return g

    def show_public_key(self):
        """Public key display function

        :return: None
        """
        print(f"public_key: {self.n}, {self.g}")

    def encryption(self, plaintext_as_digits_list: [int]):
        """Encryption function of plain text presented as a list of unencrypted numbers.

        :param plaintext_as_digits_list: (list[int]) - list of unencrypted numbers
        :return: empty list [] or non-empty list including encrypted digits
        """
        plaintext_is_current: bool = check_plaintext(
            plaintext_as_digits_list, self.n
        )
        if plaintext_is_current:
            if not self.__multiplicative_group_mod_n:
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
    """Contains a private key and associated decryption method.

    Args:
        public's:
            lambdas (int): part of private key - see [1] \n
            mu (int): part of private key - see [1] \n
        private's:
            __public_key (object): object of class PaillierPublicKey
            __p (int): large prime
            __q (int): large prime

    Links:
        [1] - https://en.wikipedia.org/wiki/Paillier_cryptosystem#Key_generation
    """

    def __init__(self, public_key, p, q):
        self.__public_key = public_key
        self.__p = p
        self.__q = q
        self.lambdas = self.generation_lambdas(self.__p, self.__q)
        self.mu = self.generation_mu(self.__public_key.g, self.__public_key.n, self.lambdas)

    @staticmethod
    def generation_lambdas(p: int, q: int):
        """Function for generating lambdas as part of a private key.

        :param p: (int) large prime
        :param q: (int) large prime
        :return: (int) _lambdas as least common multiple of (p - 1) and (q - 1)
        """
        _lambdas = Euclid().least_common_multiple(p - 1, q - 1)
        return _lambdas

    @staticmethod
    def generation_mu(_g: int, _n: int, _lambdas: int):
        """Function for generating mu as part of a private key.

        :param _g: (int) part of public key
        :param _n: (int) part of public key
        :param _lambdas: (int) _lambdas as least common multiple of (p - 1) and (q - 1)
        :return: (int) mu as reverse digit modulo _n
        """
        result_l_func = l_func(pow(_g, _lambdas, _n ** 2), _n)
        reverse_digit = Euclid().reverse_digit(result_l_func, _n)
        mu = reverse_digit % _n
        return mu

    def show_private_key(self):
        """Private key display function

        :return: None
        """
        print(f"private_key: {self.lambdas}, {self.mu}")

    def decryption(self, encryption_digits_list: [int]):
        """Function for decrypting a list of encrypted numbers.

        :param encryption_digits_list: list [int] - list of encrypted numbers
        :return: list [int] - list of decrypted numbers
        """
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
    """Function for generating public and private keys based on the bit length of the key.

    :param bit_key_length: (int) key length in bits (optional)
    :return: object's of classes PaillierPublicKey and PaillierPrivateKey
    """
    def p_q_generating(half_bit_key_length: int):
        """Helper function.
        Generates _p and _q as large primes by certain condition.

        :param half_bit_key_length: (int) half of key length in bits
        :return: (int) _p and (int) _q as large primes
        """

        _p = 3
        _q = 2

        while Euclid().greatest_common_divisor(_p * _q, (_p - 1) * (_q - 1)) != 1:
            _p = PrimeDigit().generation_a_large_prime(half_bit_key_length)
            _q = PrimeDigit().generation_a_large_prime(half_bit_key_length)
            while _q == _p:
                _q = PrimeDigit().generation_a_large_prime(half_bit_key_length)

        return _p, _q

    p, q = p_q_generating(bit_key_length // 2)

    n = p * q

    public_key = PaillierPublicKey(n)
    private_key = PaillierPrivateKey(public_key, p, q)

    return public_key, private_key
