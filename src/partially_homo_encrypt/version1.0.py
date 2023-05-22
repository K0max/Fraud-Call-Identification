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
        g = pow(n + 1, 2, n ** 2)
        return (n, g), (p, q)

    def encrypt(self, plaintext):
        n, g = self.public_key
        r = random.randint(1, n - 1)
        ciphertext = pow(g, plaintext, n ** 2) * pow(r, n, n ** 2) % (n ** 2)
        return ciphertext

    def decrypt(self, ciphertext):
        n, g = self.public_key
        p, q = self.private_key
        lam = (p - 1) * (q - 1) // number.GCD(p - 1, q - 1)
        mu = pow(pow(g, lam, n ** 2), -1, n)
        plaintext = (pow(ciphertext, lam, n ** 2) - 1) // n * mu % n
        return plaintext
