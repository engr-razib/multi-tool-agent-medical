# 🩺 Multi-Tool AI Medical Agent

A multi-tool AI agent that can:

- 📊 Query medical datasets (Heart Disease, Cancer, Diabetes) directly from SQLite databases.
- 🌐 Search the web for general medical knowledge (definitions, symptoms, cures).
- 🤖 Automatically decide whether to use dataset queries or online search based on user questions.

## 📁 Project Structure

```text
multi-tool-agent-medical/
├── backend/                     # FastAPI backend server
│   ├── app.py                  # Main server entry
│   ├── db_tools/               # Database tools for medical datasets
│   │   ├── base_tool.py        # Base tool with safe SQL execution
│   │   ├── heart_disease_tool.py
│   │   ├── cancer_tool.py
│   │   ├── diabetes_tool.py
│   ├── web_tools/              # Web scraping / search tools
│   │   ├── medical_web_search.py
│   ├── utils/                  # Utility scripts
│   │   ├── csv_to_sqlite.py    # Convert CSV datasets to SQLite
│   ├── tests/                  # Unit tests
│       ├── test_db_tools.py    # Tests for DB tools
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── components/         # UI components
│   │   ├── api.js              # API calls to backend
├── data/                        # CSV datasets
│   ├── heart.csv
│   ├── cancer.csv
│   ├── diabetes.csv
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── README.md



````

---

## 📦 Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/multi-tool-agent-medical.git
cd multi-tool-agent-medical
````

### 2️⃣ Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## 🛠️ Dataset Preparation

Download the datasets from Kaggle:

* [Heart Disease Dataset](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)
* [Cancer Prediction Dataset](https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset)
* [Diabetes Dataset](https://www.kaggle.com/datasets/mathchi/diabetes-data-set)

Place the `.csv` files in the `data/` folder.

Then run:

```bash
python backend/utils/csv_to_sqlite.py
```

This will create:

```
data/heart_disease.db
data/cancer.db
data/diabetes.db
```

---

## 🚀 Running the Backend

From the project root:

```bash
uvicorn backend.app:app --reload --port 8000
```

Backend will be available at:

```
http://localhost:8000
```

---

## 💻 Running the Frontend

```bash
cd frontend
npm start
```

Frontend will be available at:

```
http://localhost:3000
```

---

## 🧪 Running Unit Tests

```bash
pytest backend/tests
```

---

## 🌐 Deployment Guide

### **Option 1 — Docker**

1. Build Docker images:

```bash
docker-compose build
```

2. Start containers:

```bash
docker-compose up -d
```

3. Access:

   * Backend → `http://<server-ip>:8000`
   * Frontend → `http://<server-ip>:3000`

---

### **Option 2 — Manual VPS Deployment**

1. **Install Dependencies**:

   ```bash
   sudo apt update && sudo apt install python3-pip python3-venv nodejs npm nginx
   ```
2. **Setup Backend**:

   ```bash
   cd /var/www/multi-tool-agent-medical
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn backend.app:app --host 0.0.0.0 --port 8000
   ```
3. **Setup Frontend**:

   ```bash
   cd frontend
   npm install
   npm run build
   ```
4. **Configure Nginx**:

   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           root /var/www/multi-tool-agent-medical/frontend/build;
           index index.html;
           try_files $uri /index.html;
       }

       location /api/ {
           proxy_pass http://127.0.0.1:8000/;
       }
   }
   ```
5. **Restart Nginx**:

   ```bash
   sudo systemctl restart nginx
   ```

---

## 🔑 API Endpoints

* **POST /ask**
  Request:

  ```json
  { "question": "What is the average age of patients with heart disease?" }
  ```

  Response:

  ```json
  { "answer": "The average age is 54 years." }
  ```

---

## 🛡 Security Features

* **Safe SQL Execution** — Only `SELECT` queries allowed.
* **Whitelisted Tables** — No arbitrary table access.
* **Web Search Restricted** — Only medical topics allowed.

---


