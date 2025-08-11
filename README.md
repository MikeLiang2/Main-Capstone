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
### Quick Start
If you’re new to Docker, the easiest way to run the entire project is to execute the startup script:
```bash
./start.sh
```
This script handles building, migrating, and starting all the necessary containers.

### Manual Docker Compose Commands
#### First Time Setup
Before running the containers manually, make sure the `backend/alembic/versions` directory exists. If it doesn’t, create it:
```bash
mkdir -p backend/alembic/versions
```
Also, make sure Docker and Docker Compose are installed and running on your machine.  
Then, from the project root directory, run:
```bash
docker compose up --build
```
This will:
- Build and start the backend FastAPI server on http://localhost:8000
- Build and start the frontend Vue app served via nginx on http://localhost:5173
- Start a PostgreSQL database container
- Start the database migration service to apply schema changes

#### Subsequent Runs (After Initial Build)
To start the containers without rebuilding, simply run:
```bash
docker compose up
```

### Stop the containers
```bash
docker compose down
```

### Remove the containers
```bash
docker compose down -v
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
