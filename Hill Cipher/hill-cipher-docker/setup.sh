#!/bin/bash

# Copia o hill_cipher.py para as pastas dos containers
cp hill_cipher.py container1/
cp hill_cipher.py container2/

# Cria uma chave compartilhada
echo "Matriz Chave: [[3, 3], [2, 5]]" > shared/key.txt

echo "Setup completo! Execute 'docker-compose up --build' para iniciar"