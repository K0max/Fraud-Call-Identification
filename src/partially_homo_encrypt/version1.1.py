'''
1.使用位运算代替乘法和除法：在计算大整数的时候，乘法和除法的性能通常比较低。用位运算来代替乘法和除法

2.使用快速模幂算法：在加密和解密过程中，需要进行大量的幂运算。为了提高性能.用快速模幂算法来代替普通的幂运算
'''
import random
from Crypto.Util import number

class Pallier:
    def __init__(self, key_length=1024):
        self.key_length = key_length
        self.public_key, self.private_key = self.generate_key_pair()

    def generate_key_pair(self):
        p = number.getPrime(self.key_length // 2)
        q = number.getPrime(self.key_length // 2)
        n = p * q
        g = pow(n + 1, 2, n ** 2)
        return (n, g), (p, q)

    def encrypt(self, plaintext):
        n, g = self.public_key
        r = random.randint(1, n - 1)
        ciphertext = self.mod_pow(g, plaintext, n ** 2) * self.mod_pow(r, n, n ** 2) % (n ** 2)
        return ciphertext

    def decrypt(self, ciphertext):
        n, g = self.public_key
        p, q = self.private_key
        lam = self.lcm(p - 1, q - 1)
        mu = self.mod_pow(pow(g, lam, n ** 2), -1, n)
        plaintext = (self.mod_pow(ciphertext, lam, n ** 2) - 1) // n * mu % n
        return plaintext

    def mod_pow(self, base, exponent, modulus):
        result = 1
        while exponent > 0:
            if exponent & 1:
                result = result * base % modulus
            exponent >>= 1
            base = base * base % modulus
        return result

    def lcm(self, a, b):
        return a * b // number.GCD(a, b)