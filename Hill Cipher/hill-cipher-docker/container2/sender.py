import socket
import time
from hill_cipher import HillCipher, KEY_MATRIX

class Sender:
    def __init__(self, receiver_host='receiver', receiver_port=5000):
        self.receiver_host = receiver_host
        self.receiver_port = receiver_port
        self.cipher = HillCipher(KEY_MATRIX)
        
    def send_messages(self):
        print("[Emissor] Tentando conectar ao receptor...")
        
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.receiver_host, self.receiver_port))
                print("[Emissor] Conectado ao receptor!")
                break
            except:
                print("[Emissor] Aguardando receptor...")
                time.sleep(2)
        
        messages = [
            "HELLO",
            "WORLD",
            "SECURITY",
            "INFORMATION",
            "HILLCIPHER"
        ]
        
        for msg in messages:
            print(f"\n[Emissor] Mensagem original: {msg}")
            
            # Criptografa
            encrypted = self.cipher.encrypt(msg)
            print(f"[Emissor] Mensagem criptografada: {encrypted}")
            
            # Envia
            sock.send(encrypted.encode())
            time.sleep(2)
        
        sock.close()

if __name__ == "__main__":
    sender = Sender()
    sender.send_messages()