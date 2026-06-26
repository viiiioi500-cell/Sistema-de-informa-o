# corrigir_sniffer.ps1
Write-Host "Corrigindo o Container 3 (Sniffer)..." -ForegroundColor Green

# 1. Atualiza o Dockerfile
@"
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
"@ | Out-File -FilePath "container3/Dockerfile" -Encoding utf8

Write-Host "✅ Dockerfile atualizado" -ForegroundColor Green

# 2. Cria requirements.txt
@"
numpy
scapy
"@ | Out-File -FilePath "container3/requirements.txt" -Encoding utf8

Write-Host "✅ requirements.txt criado" -ForegroundColor Green

# 3. Copia hill_cipher.py
if (Test-Path "hill_cipher.py") {
    Copy-Item "hill_cipher.py" -Destination "container3/" -Force
    Write-Host "✅ hill_cipher.py copiado" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Correção concluída!" -ForegroundColor Green
Write-Host "Agora execute: docker-compose down -v" -ForegroundColor Yellow
Write-Host "Depois: docker-compose up -d --build" -ForegroundColor Yellow