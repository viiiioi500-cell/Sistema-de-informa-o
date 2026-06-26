#!/usr/bin/env python3
import socket
import struct
import datetime
import time
import threading
import os
import sys
from hill_cipher import HillCipher, KEY_MATRIX

class NetworkSniffer:
    def __init__(self):
        self.captured_messages = []
        self.running = True
        self.log_file = "/shared/captured.txt"
        self.cipher = HillCipher(KEY_MATRIX)
        
        # Cria diretório shared se não existir
        os.makedirs("/shared", exist_ok=True)
        
    def parse_tcp_packet(self, data):
        """Extrai dados TCP de um pacote"""
        try:
            # Cabeçalho IP (20 bytes)
            ip_header = data[:20]
            iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
            
            # Versão e tamanho do header IP
            version_ihl = iph[0]
            ihl = (version_ihl & 0xF) * 4
            
            # Protocolo
            protocol = iph[6]
            
            # Endereços IP
            src_ip = socket.inet_ntoa(iph[8])
            dst_ip = socket.inet_ntoa(iph[9])
            
            # Se for TCP (protocolo 6)
            if protocol == 6:
                # Cabeçalho TCP (20 bytes)
                tcp_header_start = ihl
                tcp_header = data[tcp_header_start:tcp_header_start+20]
                tcph = struct.unpack('!HHLLBBHHH', tcp_header)
                
                src_port = tcph[0]
                dst_port = tcph[1]
                
                # Tamanho do header TCP
                tcp_header_len = (tcph[4] >> 4) * 4
                
                # Dados (payload)
                tcp_data_start = tcp_header_start + tcp_header_len
                payload = data[tcp_data_start:]
                
                return {
                    'src_ip': src_ip,
                    'dst_ip': dst_ip,
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'payload': payload
                }
        except Exception as e:
            pass
        return None
    
    def process_payload(self, packet_info):
        """Processa o payload capturado"""
        try:
            payload = packet_info['payload']
            
            # Tenta decodificar como texto
            try:
                message = payload.decode('utf-8', errors='ignore')
                
                # Filtra apenas mensagens com letras maiúsculas (Hill Cipher)
                # e com tamanho entre 4 e 50 caracteres
                cleaned = ''.join(c for c in message if c.isalpha()).upper()
                
                if len(cleaned) >= 4 and len(cleaned) <= 50 and cleaned.isupper():
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    print(f"\n{'='*70}")
                    print(f"[SNIFFER] 🕵️  PACOTE CAPTURADO!")
                    print(f"[SNIFFER] 📅 {timestamp}")
                    print(f"[SNIFFER] 📡 Origem: {packet_info['src_ip']}:{packet_info['src_port']}")
                    print(f"[SNIFFER] 📡 Destino: {packet_info['dst_ip']}:{packet_info['dst_port']}")
                    print(f"[SNIFFER] 🔒 Mensagem Criptografada: {cleaned}")
                    
                    # Tenta descriptografar
                    try:
                        decrypted = self.cipher.decrypt(cleaned)
                        print(f"[SNIFFER] 🔓 MENSAGEM DESCRIPTOGRAFADA: {decrypted}")
                        print(f"[SNIFFER] ✅ ATAQUE DE SNIFFING BEM SUCEDIDO!")
                        
                        # Salva no log
                        with open(self.log_file, "a") as f:
                            f.write(f"{timestamp} - Capturado: {cleaned}\n")
                            f.write(f"{timestamp} - Decriptado: {decrypted}\n")
                            f.write(f"{'='*70}\n")
                        
                        self.captured_messages.append({
                            'timestamp': timestamp,
                            'encrypted': cleaned,
                            'decrypted': decrypted,
                            'src': f"{packet_info['src_ip']}:{packet_info['src_port']}",
                            'dst': f"{packet_info['dst_ip']}:{packet_info['dst_port']}"
                        })
                        
                    except Exception as e:
                        print(f"[SNIFFER] ⚠️  Não foi possível descriptografar: {e}")
                        
                    print(f"{'='*70}")
                    
            except UnicodeDecodeError:
                pass
                
        except Exception as e:
            print(f"Erro ao processar payload: {e}")
    
    def sniff_packets(self):
        """Método principal de sniffing usando socket raw"""
        try:
            # Cria socket raw para capturar todos os pacotes TCP
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
            sock.settimeout(1)
            
            print("[SNIFFER] 🚀 Iniciando captura de pacotes...")
            print("[SNIFFER] 🔍 Monitorando porta 5000")
            print(f"[SNIFFER] 📁 Logs salvos em: {self.log_file}")
            print("[SNIFFER] ⏹️  Pressione Ctrl+C para parar\n")
            
            while self.running:
                try:
                    # Recebe pacote
                    packet, addr = sock.recvfrom(65535)
                    
                    # Analisa o pacote
                    packet_info = self.parse_tcp_packet(packet)
                    
                    if packet_info:
                        # Filtra apenas tráfego na porta 5000
                        if packet_info['src_port'] == 5000 or packet_info['dst_port'] == 5000:
                            self.process_payload(packet_info)
                            
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Erro ao capturar pacote: {e}")
                    
        except PermissionError:
            print("[SNIFFER] ❌ Erro: Permissão negada!")
            print("[SNIFFER] Execute o container com --privileged ou como root")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"[SNIFFER] ❌ Erro ao iniciar sniffing: {e}")
        finally:
            sock.close()
    
    def show_summary(self):
        """Mostra resumo das capturas"""
        print(f"\n{'='*70}")
        print("[SNIFFER] 📊 RESUMO DA CAPTURA")
        print(f"{'='*70}")
        print(f"Total de mensagens capturadas: {len(self.captured_messages)}")
        
        for i, msg in enumerate(self.captured_messages, 1):
            print(f"\n{i}. {msg['timestamp']}")
            print(f"   Origem: {msg['src']} -> Destino: {msg['dst']}")
            print(f"   🔒 Encriptado: {msg['encrypted']}")
            print(f"   🔓 Decriptado: {msg['decrypted']}")
        
        if self.captured_messages:
            print(f"\n✅ Sniffing realizado com sucesso!")
            print(f"📁 Logs salvos em: {self.log_file}")
    
    def start(self):
        """Inicia o sniffer"""
        try:
            self.sniff_packets()
        except KeyboardInterrupt:
            print("\n[SNIFFER] ⏹️  Captura interrompida pelo usuário")
        finally:
            self.running = False
            self.show_summary()

if __name__ == "__main__":
    # Verifica se está rodando como root
    if os.geteuid() != 0:
        print("[SNIFFER] ⚠️  Aviso: Executando sem privilégios root")
        print("[SNIFFER] Algumas funcionalidades podem ser limitadas")
    
    sniffer = NetworkSniffer()
    sniffer.start()