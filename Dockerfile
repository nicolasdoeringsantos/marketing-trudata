FROM python:3.11-slim

WORKDIR /app

# Não salva arquivos de cache .pyc no container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /app

EXPOSE 8080

CMD ["python", "start.py"]
