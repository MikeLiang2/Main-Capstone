# 🚀 Capstone Project

A fullstack application with a Python FastAPI backend and a Vue 3 + Vite frontend.

---
## 📦 Requirements

- **Python**: `>= 3.13`
- **Node.js**: `>= 22.17`
- **npm**: (comes with Node.js)
- **Docker** and **Docker Compose** (for containerized setup)

---

## 🐳 Run the Project with Docker
### Run the containers:
**Make sure the `backend/alembic/versions` directory exists. If not, create it.**  
Make sure Docker and Docker Compose are installed and running on your machine.
From the project root, run:
```bash
docker compose up --build
```
This will:
- Build and start the backend FastAPI server on http://localhost:8000
- Build and start the frontend Vue app served via nginx on http://localhost:5173
- Start a PostgreSQL database container

### Stop the containers
```bash
docker-compose down
```

## 🔧 Setup Instructions (Only if without Docker)
### 1. Backend Setup (Local development)
```bash
cd backend
python -m venv venv
# Activate virtual environment:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend Setup (Local development)
```bash
cd ../frontend
npm install
```

## ▶️ Run the Project Locally (without Docker)
### 1. Start Backend Server
In a new terminal:
```bash
cd backend
# Activate virtual environment:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
uvicorn app.main:app --reload
```

### 2. Start Frontend Dev Server
In another terminal:
```bash
cd frontend
npm run dev
```

## 📁 Project Structure
```css
Capstone/
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   └── ...
├── dbm.sql
├── docker-compose.yml
├── package.json
├── README.md
```

## 📝 Notes
- The backend runs on http://localhost:8000
- The frontend runs on http://localhost:5173
