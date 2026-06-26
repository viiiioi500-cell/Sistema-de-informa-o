#!/bin/bash
echo "Configurando Container 3 (Sniffer)..."

# Copia hill_cipher.py para o container3
if [ -f "hill_cipher.py" ]; then
    cp hill_cipher.py container3/
    echo "✅ hill_cipher.py copiado para container3/"
else
    echo "❌ hill_cipher.py não encontrado na raiz"
fi

# Cria shared se não existir
mkdir -p shared

echo "✅ Setup do Container 3 concluído!"
echo "Execute: docker-compose up -d --build"