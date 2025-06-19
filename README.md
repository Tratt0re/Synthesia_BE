# 🧠 Synthesia - Backend

Questo è il backend del progetto **Synthesia**, un'applicazione web per la sintesi documentale basata su modelli linguistici di grandi dimensioni (LLM). Il backend è sviluppato in **Python 3.13** utilizzando il framework **FastAPI**, con supporto alla gestione di modelli locali e cloud, e persistenza dei dati tramite **MongoDB**.

## 📦 Tecnologie Utilizzate

- **Python 3.13**
- **FastAPI**
- **Pydantic**
- **Motor (MongoDB async client)**
- **Uvicorn** (per il server ASGI)
- **dotenv** (gestione variabili d’ambiente)
- **Ollama / WatsonX / HuggingFace / Groq** (integrazione opzionale con modelli LLM)

## 🗂 Struttura del progetto

```
backend/
├── app/
│   ├── routers/          # Endpoint API RESTful
│   ├── core/             # Configurazione e costanti
│   ├── models/           # Schemi dati Pydantic e MongoDB
│   ├── services/         # Logica dei servizi per la gestione LLM e varie
│   └── app.py            # Punto di ingresso principale dell'app
├── .env                  # Variabili d’ambiente
├── requirements.txt      # Dipendenze del progetto
└── README.md             # Questo file
```

## ⚙️ Requisiti

- Python 3.13
- MongoDB 6 o superiore

## 🚀 Installazione

1. **Clona il repository e accedi alla cartella del backend:**

```bash
git clone https://github.com/Tratt0re/Synthesia_BE.git
```

2. **Crea un ambiente virtuale:**

```bash
virtualenv venv --python=3.13
source venv/bin/activate
```

3. **Installa le dipendenze:**

```bash
pip install -r requirements.txt
```

4. **Configura il file `.env`:**

Crea un file `.env` nella root del backend con le seguenti variabili:

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=synthesia
MODEL_PROVIDER=local
```

> Puoi modificare `MODEL_PROVIDER` per usare provider cloud come `watsonx`, `huggingface`, ecc.

5. **Avvia il server FastAPI:**

```bash
uvicorn app.main:app --reload
```

L'app sarà disponibile su: [http://localhost:8000](http://localhost:8000)

## 🔐 Sicurezza

- Comunicazioni HTTPS consigliate in ambienti di produzione
- Input sanitization e CORS configurabili
- Supporto a sessioni anonime senza autenticazione

## 🧪 Test API

Una volta avviato il server, puoi testare l’API documentata su:

[http://localhost:8000/docs](http://localhost:8000/docs)

## 📁 Dipendenze principali

```txt
fastapi
pydantic
uvicorn
motor
python-dotenv
llama-index
```

## 📝 Licenza

Distribuito con licenza **Apache 2.0**.  
Consulta il file `LICENSE` nella root del progetto principale.

---

## 👤 Autore

Salvatore De Luca  
Tesi di Laurea Triennale – 2025  
Università Pegaso
