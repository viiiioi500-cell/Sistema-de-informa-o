FROM python:3.9-slim

WORKDIR /app

COPY hill_cipher.py .
COPY receiver.py .

RUN pip install numpy

CMD ["python", "receiver.py"]