import random
from Crypto.Util import number

class Paillier:
    def __init__(self, key_length=1024):
        self.key_length = key_length
        self.public_key, self.private_key = self.generate_key_pair()

    def generate_key_pair(self):
        p = number.getPrime(self.key_length // 2)
        q = number.getPrime(self.key_length // 2)
        n = p * q
        g = n + 1
        lam = number.lcm(p - 1, q - 1)
        mu = number.inverse(lam, n)
        return (n, g), (lam, mu)

    def encrypt(self, plaintext):
        n, g = self.public_key
        r = random.randint(1, n - 1)
        plaintext_int = int(plaintext * 10 ** 6)
        ciphertext = self.mod_pow(g, plaintext_int, n ** 2) * self.mod_pow(r, n, n ** 2) % (n ** 2)
        return ciphertext

    def decrypt(self, ciphertext):
        n, g = self.public_key
        lam, mu = self.private_key
        plaintext_int = (self.mod_pow(ciphertext, lam, n ** 2) - 1) // n * mu % n
        plaintext = plaintext_int / 10 ** 6
        return plaintext

    def mod_pow(self, base, exponent, modulus):
        result = 1
        while exponent > 0:
            if exponent & 1:
                result = result * base % modulus
            exponent >>= 1
            base = base * base % modulus
        return result