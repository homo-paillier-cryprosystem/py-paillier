"""Paillier encryption library for partially homomorphic encryption."""

from util import Euclid, PrimeDigit

DEFAULT_BIT_KEY_LENGTH = 256


# вспомогательная функция
def l_func(u, _n):
    return (u - 1) // _n


class PaillierPublicKey(object):

    def __init__(self, n):
        self.n = n
        self.g = self.generation_g(self.n)

    @staticmethod
    def generation_g(_n: int):
        g = PrimeDigit().generation_big_simple_digit_in_modulo(_n)
        return g

    def show_public_key(self):
        print(f"public_key: {self.n}, {self.g}")


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
        result_l_func = l_func((_g ** _lambdas) % (_n ** 2), _n)
        reverse_digit = Euclid().reverse_digit(result_l_func, _n)
        result = reverse_digit % _n
        return result

    def show_private_key(self):
        print(f"private_key: {self.lambdas}, {self.mu}")


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
