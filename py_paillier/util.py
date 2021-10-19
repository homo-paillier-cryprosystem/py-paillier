import random


# алгоритмы Евклида
class Euclid(object):

    # алгоритм для расчета наибольшего общего делителя
    @staticmethod
    def greatest_common_divisor(a: int, b: int):

        def gcd(_a: int, _b: int):
            q = _a // _b
            r = _a - _b * q
            if r == 0:
                return _b
            else:
                return gcd(_b, r)
            pass

        if a < b:
            a, b = b, a

        return gcd(a, b)

    # алгоритм для расчета наименьшее общего кратного
    @staticmethod
    def least_common_multiple(a: int, b: int):
        gsd_result = Euclid().greatest_common_divisor(a, b)
        return int((a * b) / gsd_result)

    # алгоритм для расчета обратного числа
    @staticmethod
    def reverse_digit(a: int, n: int):
        x, xx, y, yy = 1, 0, 0, 1
        _max = max(a, n)
        while n:
            q = a // n
            r = a % n
            a, n = n, r
            if r == 0:
                return xx
            else:
                x, xx = xx % _max, (x + xx * (_max - q)) % _max
                y, yy = yy % _max, (y + yy * (_max - q)) % _max


# класс для работы с простыми числами
class PrimeDigit(object):

    # функция проверяющая простоту
    @staticmethod
    def is_prime(n: int):
        i = 2
        j = 0
        while i ** 2 <= n and j != 1:
            if n % i == 0:
                j += 1
            i += 1
        if j == 1:
            return False
        else:
            return True

    # генерация большого простого числа для p и q
    @staticmethod
    def generation_big_simple_digit(n: int):
        x = 4
        while not PrimeDigit().is_prime(x):
            # x = random.randint(10000, 100000)
            # x = random.randint(100, 1000)
            # x = random.randint(50, 100)
            # x = random.randint(3, 20)
            x = random.SystemRandom().randrange(
                2 ** (n - 1),
                2 ** n
            )
        return x

    # генерация большого простого числа по модулю n
    @staticmethod
    def generation_big_simple_digit_in_modulo(n: int):
        x = 4
        while not PrimeDigit().is_prime(x):
            x = random.SystemRandom().randrange(1, n)
        return x
