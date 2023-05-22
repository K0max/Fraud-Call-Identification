import random
from Crypto.Util import number
import threading

class Paillier:
    def __init__(self, key_length=1024, num_threads=4):
        self.key_length = key_length
        self.public_key, self.private_key = self.generate_key_pair()
        self.num_threads = num_threads

    '''
    公钥是一个元组(n, g)，其中n是模数，g是生成器。模数n是两个大质数p和q的乘积，而g等于n + 1。生成器g用于加密明文，而模数n用于加密和解密密文。

    私钥是一个元组(lam, mu)，其中lam是n的Carmichael函数，mu是lam在模n下的模反元素。Carmichael函数lam是p-1和q-1
    '''
    
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

    def encrypt_parallel(self, plaintexts):
        n, g = self.public_key
        r = [random.randint(1, n - 1) for _ in range(len(plaintexts))]
        plaintexts_int = [int(p * 10 ** 6) for p in plaintexts]
        ciphertexts = [0] * len(plaintexts)
        threads = []
        chunk_size = (len(plaintexts) + self.num_threads - 1) // self.num_threads
        for i in range(self.num_threads):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(plaintexts))
            thread = threading.Thread(target=self.encrypt_chunk, args=(plaintexts_int[start:end], r[start:end], ciphertexts, n))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return ciphertexts

    def encrypt_chunk(self, plaintexts, r, ciphertexts, n):
        for i, plaintext_int in enumerate(plaintexts):
            ciphertexts[i] = self.mod_pow(self.public_key[1], plaintext_int, n ** 2) * self.mod_pow(r[i], n, n ** 2) % (n ** 2)

    def decrypt_parallel(self, ciphertexts):
        n, g = self.public_key
        lam, mu = self.private_key
        plaintexts_int = [0] * len(ciphertexts)
        threads = []
        chunk_size = (len(ciphertexts) + self.num_threads - 1) // self.num_threads
        for i in range(self.num_threads):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(ciphertexts))
            thread = threading.Thread(target=self.decrypt_chunk, args=(ciphertexts[start:end], plaintexts_int, lam, mu, n))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        plaintexts = [p_int / 10 ** 6 for p_int in plaintexts_int]
        return plaintexts

    def decrypt_chunk(self, ciphertexts, plaintexts_int, lam, mu, n):
        for i, ciphertext in enumerate(ciphertexts):
            plaintexts_int[i] = (self.mod_pow(ciphertext, lam, n ** 2) - 1) // n * mu % n