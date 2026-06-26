FROM python:3.9-slim

# Instala ferramentas básicas de rede
RUN apt-get update && apt-get install -y \
    tcpdump \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia os arquivos
COPY requirements.txt .
COPY sniffer.py .
COPY hill_cipher.py .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# REMOVIDO: setcap - não é mais necessário
# O privilégio será dado pelo docker-compose.yml

CMD ["python", "sniffer.py"]