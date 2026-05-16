<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=AI%20Resume%20Screener%20&%20Job%20Matcher&fontSize=40&animation=fadeIn&fontAlignY=38&desc=Intelligent%20HR%20Assistant%20NLP&descAlignY=55&descAlign=50" alt="Header" width="100%" />
</div>

    <strong>An advanced, AI-powered recruitment platform designed to automate resume screening, rank candidates, and match them with the perfect job opportunities using Google's Gemini LLM.</strong>
  </p>

  <p align="center">
    <a href="#-features">Features</a> •
    <a href="#%EF%B8%8F-tech-stack">Tech Stack</a> •
    <a href="#-installation--setup">Installation</a> •
    <a href="#-system-architecture">Architecture</a> •
    <a href="#-team">Team</a>
  </p>
  
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
    <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" />
  </p>
</div>

---

## ✨ Features

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">📄 Intelligent Resume Parsing</h3>
      <p align="center">Automatically extract key information (skills, experience, education) from uploaded PDF resumes using advanced text extraction and NLP techniques.</p>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">🎯 Smart Job Matching</h3>
      <p align="center">Utilizes Google Gemini AI to analyze candidate profiles and match them with the most suitable job openings based on semantic similarity and skill overlap.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3 align="center">🤖 HR Assistant Chatbot</h3>
      <p align="center">An integrated conversational AI assistant to help recruiters query candidate data, schedule interviews, and get instant insights into the talent pool.</p>
    </td>
    <td width="50%" valign="top">
      <h3 align="center">📊 Analytics Dashboard</h3>
      <p align="center">Visual representation of screening metrics, candidate pipelines, and recruitment efficiency, enabling data-driven HR decisions.</p>
    </td>
  </tr>
</table>

## 🛠️ Tech Stack

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,postgres,html,css,js,git" />
  </a>
</p>

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **AI/ML:** Google GenAI (Gemini), HuggingFace Transformers, Scikit-learn
- **Frontend:** Vanilla HTML5, CSS3, JavaScript, Jinja2
- **Authentication:** JWT, bcrypt

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL
- Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/manmathk31/Automatic-Resume-Screener-and-Job-Matcher.git
cd Automatic-Resume-Screener-and-Job-Matcher/backend
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the `backend` directory and add the following configuration:
```env
ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@localhost:5432/resume_db
SECRET_KEY=your_super_secret_key
GEMINI_API_KEY=your_gemini_api_key
FRONTEND_URL=http://localhost:8000
```

### 5. Database Migrations
Initialize your database schema by running the Alembic migrations:
```bash
alembic upgrade head
```

### 6. Run the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The application will be accessible at `http://localhost:8000`.

## 📈 System Architecture

```mermaid
graph TD
    A[Client UI / Browser] -->|REST API| B(FastAPI Backend)
    B --> C{JWT Authentication}
    C -->|Valid| D[(PostgreSQL DB)]
    B --> E[PDF Parser & Extractor]
    E --> F[HuggingFace Embeddings]
    B --> G[Google Gemini AI]
    G --> H[Job Matching Engine]
    H --> B
    B --> A
    
    classDef client fill:#f9f,stroke:#333,stroke-width:2px;
    classDef backend fill:#bbf,stroke:#333,stroke-width:2px;
    classDef db fill:#fbb,stroke:#333,stroke-width:2px;
    classDef ai fill:#bfb,stroke:#333,stroke-width:2px;
    
    class A client;
    class B backend;
    class D db;
    class G,F ai;
```

## 👥 Team

We are a dedicated team of developers who built this platform for Datathon 2026.

<div align="center">
  <table align="center">
    <tr>
      <td align="center" width="150">
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Manmath" width="100px;" alt="Manmath"/><br />
        <b>Manmath Kornule</b><br>(Leader)
      </td>
      <td align="center" width="150">
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Vishal" width="100px;" alt="Vishal"/><br />
        <b>Vishal Shende</b>
      </td>
      <td align="center" width="150">
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Pratik" width="100px;" alt="Pratik"/><br />
        <b>Pratik Mane</b>
      </td>
      <td align="center" width="150">
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Kishor" width="100px;" alt="Kishor"/><br />
        <b>Kishor Kaple</b>
      </td>
    </tr>
  </table>
</div>

---
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=60&text=Made%20with%20%E2%9D%A4%EF%B8%8F%20for%20Datathon%202026&fontSize=16" alt="Footer" />
</div>
