# 🤖 Chatbot Assistant for Training

A **FastAPI-based backend chatbot assistant** designed for training, experimentation, and analytics use cases. This project provides a modular backend with database connectivity, CRUD operations, and chatbot logic, making it suitable for learning, prototyping, and extending into production-ready AI services.

---

## 📌 Project Overview

This repository demonstrates how to build a **chatbot-enabled backend service** using **FastAPI**, with support for:

* REST APIs using FastAPI
* Database integration (SQL-based)
* CRUD operations
* Chatbot logic (Python-based)
* Structured project layout
* Easy extensibility for ML / NLP models

It is especially useful for:

* Backend training projects
* AI/ML engineers learning API-driven chatbot systems
* FastAPI + database integration practice

---

## 🗂️ Project Structure

```text
chatbot_assistant_for_training/
│
├── routers/                   # API route definitions
├── chatbot.py                 # Core chatbot logic
├── chatbot.ipynb              # Notebook for experimentation
├── main.py                    # FastAPI app entry point
├── database.py                # Database connection setup
├── crud.py                    # CRUD operations
├── dp.sql                     # SQL schema / queries
├── check_database_connection.py
├── main_check_SQLdatabase.py  # DB connectivity checks
├── create_structure.py        # Project structure helper
├── Procfile                   # Deployment configuration (e.g. Heroku)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── LICENSE
```

---

## 🚀 Features

* ⚡ **FastAPI** for high-performance APIs
* 🧠 **Chatbot logic in Python**
* 🗄️ **SQL Database support**
* 🔄 **CRUD operations**
* 🧪 **Notebook for testing & experimentation**
* ☁️ **Deployment-ready** (Procfile included)

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **FastAPI**
* **Uvicorn**
* **SQL (via database.py)**
* **Pydantic**
* **Jupyter Notebook**

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/eldesokye/chatbot_assistant_for_training.git
cd chatbot_assistant_for_training
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
uvicorn main:app --reload
```

Once running, open:

* API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testing Database Connection

You can test the database setup using:

```bash
python check_database_connection.py
```

or

```bash
python main_check_SQLdatabase.py
```

---

## 🧠 Chatbot Logic

* Core chatbot functionality is implemented in `chatbot.py`
* Designed to be extended with:

  * NLP models
  * ML pipelines
  * LLM APIs (OpenAI, HuggingFace, etc.)

---

## ☁️ Deployment

A `Procfile` is included for easy deployment on platforms like **Heroku**:

```text
web: uvicorn main:app --host=0.0.0.0 --port=${PORT}
```

---

## 🔮 Future Improvements

* Add authentication (JWT / OAuth2)
* Integrate LLMs (OpenAI, Azure, HuggingFace)
* Add logging & monitoring
* Dockerize the application
* CI/CD pipeline

---

## 👨‍💻 Author

**Hesham El Desoky**
Backend & Machine Learning Engineer

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

⭐ If you find this project helpful, consider giving it a star!
