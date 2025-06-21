# 🧠 Synthesia - Backend

This is the backend service for **Synthesia**, a web-based application for document summarization and information extraction using Large Language Models (LLMs). The backend is built with **Python 3.13** and **FastAPI**, supports multiple LLM providers (local and cloud), and stores processed results in **MongoDB**.

---

## 📦 Technologies Used

- **Python 3.13**
- **FastAPI**
- **Pydantic v2**
- **MongoDB with Motor**
- **Uvicorn** (ASGI server)
- **dotenv** (environment management)
- **Ollama / Groq** (LLM integrations)
- **demjson3** for repairing malformed JSON

---

## 🗂 Project Structure

```
backend/
├── src/
│   ├── routers/              # RESTful API endpoints
│   ├── core/                 # Configuration, exceptions, constants
│   ├── models/               # Pydantic and DB schemas
│   ├── services/             # Business logic and integrations
│   ├── controllers/          # Controllers for routing logic
│   └── main.py               # App entry point
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## ⚙️ Requirements

- Python 3.13
- MongoDB v6 or later

> ⚠️ **Note**: To use local LLMs, make sure [Ollama](https://ollama.com/) is installed and running on your machine.

---

## 🚀 Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Tratt0re/Synthesia_BE.git
cd Synthesia_BE
```

2. **Create a virtual environment:**

```bash
python3.13 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment:**

Create a `.env` file with the following content:

```
MONGO_URI=your_mongodb_uri
MONGO_DB_NAME=your_db_name
LLM_SERVICE=local
GROQ_API_KEY=""
```

> You can set `LLM_SERVICE` to `ollama` or `groq`.

5. **Start the API server:**

```bash
uvicorn src.main:app --reload
```

> Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger API documentation.

---

## 🧠 Features

- 📄 **Summarization** from raw text or uploaded PDF/TXT files
- 🧾 **Entity Extraction** from unstructured text
- 🔍 **Full Document Analysis** (summary + entities)
- 🗃 **Automatic Storage** of results with deduplication and history tracking
- 🔐 **User Identification** via browser metadata headers
- 📑 **Paginated Retrieval** and Deletion of results

---

## 🧪 API Testing

FastAPI provides an automatic documentation and test UI at:

📍 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📁 Main Dependencies

```txt
fastapi
pydantic
motor
demjson3
uvicorn
python-dotenv
ollama
pdfminer.six
pdfplumber
```

See `requirements.txt` for the full list.

---

## 📝 License

Distributed under the **Apache 2.0 License**.  
See `LICENSE` for more details.

---

## 👤 Author

**Salvatore De Luca**  
Bachelor Thesis – 2025  
Università Pegaso
