import socket
import datetime
import threading
import time

class SimpleSniffer:
    def __init__(self):
        self.running = True
        self.captured = []
        
    def start_sniffing(self):
        """Sniffer simples usando socket"""
        print("[SNIFFER] Iniciando captura na porta 5000...")
        
        # Cria socket para sniffing
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.bind(('0.0.0.0', 0))
        
        while self.running:
            try:
                # Recebe pacote
                packet, addr = sock.recvfrom(65535)
                
                # Extrai dados (implementação simplificada)
                # Na prática, precisaria parsear o cabeçalho TCP
                # Esta é uma versão simplificada
                
                # Procura por padrões de texto (mensagens em maiúsculo)
                try:
                    data = packet.decode('utf-8', errors='ignore')
                    # Filtra mensagens com letras maiúsculas e números
                    import re
                    patterns = re.findall(r'[A-Z]{4,}', data)
                    for pattern in patterns:
                        if len(pattern) >= 4:
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"\n[SNIFFER] {timestamp} - Capturado: {pattern}")
                            self.captured.append(pattern)
                except:
                    pass
                    
            except Exception as e:
                print(f"Erro: {e}")
                
        sock.close()
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    sniffer = SimpleSniffer()
    try:
        sniffer.start_sniffing()
    except KeyboardInterrupt:
        print("\n[SNIFFER] Parando captura...")
        sniffer.stop()
        print(f"[SNIFFER] Total capturado: {len(sniffer.captured)}")
        print(f"[SNIFFER] Mensagens: {sniffer.captured}")