import numpy as np
import string

class HillCipher:
    def __init__(self, key_matrix):
        self.key_matrix = np.array(key_matrix)
        self.mod = 26
        self.char_to_num = {chr(i+65): i for i in range(26)}
        self.num_to_char = {i: chr(i+65) for i in range(26)}
    
    def encrypt(self, plaintext):
        """Criptografa uma mensagem usando a cifra de Hill"""
        plaintext = plaintext.upper().replace(" ", "")
        
        # Adiciona padding se necessário
        n = len(self.key_matrix)
        if len(plaintext) % n != 0:
            pad = n - (len(plaintext) % n)
            plaintext += 'X' * pad
        
        ciphertext = ""
        for i in range(0, len(plaintext), n):
            block = plaintext[i:i+n]
            vector = np.array([self.char_to_num[char] for char in block])
            
            # Multiplica pela matriz chave
            encrypted = np.dot(self.key_matrix, vector) % self.mod
            ciphertext += ''.join([self.num_to_char[num] for num in encrypted])
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        """Descriptografa uma mensagem usando a cifra de Hill"""
        ciphertext = ciphertext.upper().replace(" ", "")
        n = len(self.key_matrix)
        
        # Calcula a matriz inversa
        det = int(round(np.linalg.det(self.key_matrix)))
        det_mod = det % self.mod
        
        # Calcula o inverso modular
        det_inv = pow(det_mod, -1, self.mod)
        
        # Matriz adjunta
        adj = np.round(det * np.linalg.inv(self.key_matrix)).astype(int) % self.mod
        
        # Matriz inversa
        inv_key = (det_inv * adj) % self.mod
        
        plaintext = ""
        for i in range(0, len(ciphertext), n):
            block = ciphertext[i:i+n]
            vector = np.array([self.char_to_num[char] for char in block])
            
            decrypted = np.dot(inv_key, vector) % self.mod
            plaintext += ''.join([self.num_to_char[num] for num in decrypted])
        
        return plaintext

# Matriz chave exemplo (2x2)
# [[3, 3],
#  [2, 5]]
# Esta matriz é invertível módulo 26
KEY_MATRIX = [[3, 3], [2, 5]]