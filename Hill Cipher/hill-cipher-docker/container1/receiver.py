import socket
import time
from hill_cipher import HillCipher, KEY_MATRIX

class Receiver:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.cipher = HillCipher(KEY_MATRIX)
        
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(1)
        
        print(f"[Receptor] Aguardando conexão na porta {self.port}...")
        
        conn, addr = server.accept()
        print(f"[Receptor] Conectado por {addr}")
        
        while True:
            # Recebe a mensagem criptografada
            encrypted_msg = conn.recv(1024).decode()
            if not encrypted_msg:
                break
            
            print(f"\n[Receptor] Mensagem criptografada: {encrypted_msg}")
            
            # Descriptografa
            decrypted_msg = self.cipher.decrypt(encrypted_msg)
            print(f"[Receptor] Mensagem descriptografada: {decrypted_msg}")
        
        conn.close()

if __name__ == "__main__":
    receiver = Receiver()
    receiver.start_server()