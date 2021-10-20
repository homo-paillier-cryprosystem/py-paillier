import random
import time


class Euclid(object):
    """Euclid's algorithms"""

    @staticmethod
    def greatest_common_divisor(a: int, b: int):
        """Function wrapper for function gcd.
        :param a: (int)
        :param b: (int)
        :return: (int) greatest common divisor
        """
        def gcd(_a: int, _b: int):
            """The function of calculating the greatest common divisor.

            :param _a: (int)
            :param _b: (int)
            :return: (int) greatest common divisor
            """
            q = _a // _b
            r = _a - _b * q
            if r == 0:
                return _b
            else:
                return gcd(_b, r)

        if a < b:
            a, b = b, a

        return gcd(a, b)

    @staticmethod
    def least_common_multiple(a: int, b: int):
        """The function of calculating the least common multiple.

        :param a: (int)
        :param b: (int)
        :return: (int) least common multiple
        """
        gsd_result = Euclid().greatest_common_divisor(a, b)
        return int((a * b) / gsd_result)

    @staticmethod
    def reverse_digit(a: int, n: int):
        """The function of calculating the reverse digit (Unit [see [1]]) modulo n.

        :param a: (int)
        :param n: (int) as modulo
        :return: (int) reverse digit (Unit)

        Links:
            [1] - https://en.wikipedia.org/wiki/Unit_(ring_theory)
        """

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


class PrimeDigit(object):

    @staticmethod
    def is_prime(n: int):
        """Function testing simplicity.

        :param n: (int) digit for test
        :return: (bool) prime number (True) or not a prime number (False)
        """
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

    @staticmethod
    def fermat_s_little_theorem(n: int):
        """Function for checking simplicity by Fermat's little theorem - see [1].

        :param n: (int) digit for test
        :return: (bool) prime number (True) or not a prime number (False)

        Links:
            [1] - https://en.wikipedia.org/wiki/Fermat%27s_little_theorem
        """
        if pow(2, n - 1, n) == 1:
            return True
        else:
            return False

    @staticmethod
    def generation_a_large_prime(n: int):
        """Large prime generation function for p and q.

        :param n: (int) key length in bits
        :return: (int) large prime
        """
        x = 4
        while not PrimeDigit().fermat_s_little_theorem(x):
            x = random.SystemRandom().randrange(
                2 ** (n - 1),
                2 ** n
            )
        return x

    @staticmethod
    def generating_a_large_prime_modulo(n: int):
        """Large prime generation function for g in modulo n.

        :param n: (int) as modulo
        :return: (int) large prime
        """
        x = 4
        while not PrimeDigit().fermat_s_little_theorem(x):
            x = random.SystemRandom().randrange(n // 2, n)
        return x

    @staticmethod
    def sieve_of_eratosthenes(n: int):
        """Function of finding all primes up to some integer n.

        :param n: (int) as limit
        :return: (_list[int]) list of primes up to n

        Links:
            [1] - https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
        """
        a = list(range(n + 1))
        a[1] = 0
        _list = []
        i = 2
        while i <= n:
            if a[i] != 0:
                _list.append(a[i])
                for j in range(i, n + 1, i):
                    a[j] = 0
            i += 1
        return _list


def calc_reduced_system_deductions(n: int):
    """Function for calculating the reduced system of residues modulo n.

    :param n: (int) as modulo
    :return: (list[int]) list of numbers of the reduced system of residues modulo n
    """
    multiplicative_group = []

    # variable 1
    # for number in range(1, n):
    #     if Euclid().greatest_common_divisor(n, number) == 1:
    #         multiplicative_group.append(number)

    # variable 2
    # multiplicative_group = PrimeDigit().sieve_of_eratosthenes(n)

    # variable 3
    prime_numbers = PrimeDigit().sieve_of_eratosthenes(n)
    for number in prime_numbers:
        if Euclid().greatest_common_divisor(n, number) == 1:
            multiplicative_group.append(number)

    return multiplicative_group


def check_plaintext(plaintext_as_digits_list: [int], n: int):
    """Function of checking the text for the possibility of encryption.

    :param plaintext_as_digits_list: (list[int]) - list of unencrypted numbers
    :param n: (int) as limit
    :return: (bool) suitable text (True) or not (False)
    """
    currently = True
    print(f"Идет проверка принадлежности символов множеству Z_{n}.\n"
          f"Пожалуйста подождите.")

    unique_digits = list(set(plaintext_as_digits_list))
    percent = 100 / len(unique_digits)
    digits_not_in_n = []

    for digit in unique_digits:
        if digit not in range(n):
            digits_not_in_n.append(digit)
            currently = False
        progress = percent * (unique_digits.index(digit) + 1)
        print('\rПроверка завершена на %3d%%' % progress, end='', flush=True)
        time.sleep(0.01)

    if not currently:
        print(f"\nДанные числа {digits_not_in_n} не принадлежат множеству Z_{n}")
        print("Сформируйте ключи повторно для большего количества бит.")
        return False
    else:
        print("\nВведенный текст успешно проверен.")
        return True
