# Usa un'immagine di base Python specifica con la versione 3.11.4
FROM python:3.11.4

# Imposta il percorso di lavoro all'interno del contenitore
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro del contenitore
COPY requirements.txt .

# Installa le dipendenze specificate nel file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia il contenuto dell'attuale directory (la tua applicazione) nella directory di lavoro del contenitore
COPY . .

# Avvia l'applicazione quando il contenitore viene eseguito
CMD ["python", "app.py"]
