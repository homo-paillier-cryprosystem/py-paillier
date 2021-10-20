import random
import time


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

    # Функция проверки простоты по малой теореме Ферма
    @staticmethod
    def fermat_s_little_theorem(n: int):
        if pow(2, n - 1, n) == 1:
            return True
        else:
            return False

    # генерация большого простого числа для p и q
    @staticmethod
    def generation_big_simple_digit(n: int):
        x = 4
        # while not PrimeDigit().is_prime(x):
        while not PrimeDigit().fermat_s_little_theorem(x):
            x = random.SystemRandom().randrange(
                2 ** (n - 1),
                2 ** n
            )
        return x

    # генерация большого простого числа по модулю n
    @staticmethod
    def generation_big_simple_digit_in_modulo(n: int):
        x = 4
        while not PrimeDigit().fermat_s_little_theorem(x):
            x = random.SystemRandom().randrange(n // 2, n)
            # print('\r%d' % x, end='', flush=True)
        # print()
        return x

    # решето Эратосфена
    @staticmethod
    def sieve_of_eratosthenes(n: int):
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


# функция расчета приведенной системы вычетов по модулю n
def calc_reduced_system_deductions(n: int):
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


# функция проверки текста на возможность шифрования
def check_plaintext(plaintext_as_digits_list: [int], n: int):
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
