---

# Personalized AI Career and Skills Advisor 🎯

An AI-powered platform that helps students in India discover personalized career paths, map their skills, and prepare for the fast-evolving job market.
Built using **Google Cloud’s Generative AI**, **FastAPI**, **React**, and modern web technologies.

---

## 🚀 Overview

Students today face overwhelming career choices, often without personalized guidance. Traditional career counseling struggles to keep up with emerging roles and industry-required skills.

This project solves that by leveraging **Generative AI + Data-driven Skill Mapping** to create a **personalized career advisor** that:

* Understands each student’s profile, interests, and aptitudes.
* Recommends tailored career paths aligned with the future job market.
* Provides actionable learning roadmaps, skill-gap analysis, and resources.

---

## ✨ Features

### Core Features

* 🔍 **Student Profiling**: Intake via quizzes, psychometric tests, or academic data.
* 🎯 **Personalized Career Recommendations** powered by Google Generative AI.
* 📊 **Skill Gap Analysis** comparing student’s current skills vs. industry needs.
* 🛠 **Learning Roadmaps** with curated resources (courses, projects, certifications).
* 🔗 **Job Role & Industry Insights** (salary trends, demand forecasts, growth rate).

### Advanced Features

* 🤖 **AI Chatbot Mentor** for career queries and skill guidance.
* 📅 **Career Planner Dashboard** with short-term & long-term goals.
* 🔍 **Internship & Job Suggestions** (via APIs like LinkedIn Jobs, Internshala).
* 📈 **Progress Tracking & Reports** (skills learned, certifications completed).
* 🌐 **Multilingual Support** for accessibility across India.

### Future Enhancements

* 🎓 **Alumni & Mentor Connect** – AI-powered mentor matching.
* 🧭 **AI-Powered Roadmap Adjustments** as markets evolve.
* 🛡 **Privacy-first Design** ensuring secure student data storage.

---

## 🏗 Tech Stack

### Frontend

* **React.js + Tailwind CSS** → Modern, responsive UI.
* **Vite** → Fast bundler for development & builds.

### Backend

* **FastAPI (Python)** → Lightweight, fast backend framework.
* **REST APIs** → For seamless frontend-backend communication.

### AI & ML

* **Google Cloud Vertex AI (PaLM APIs)** → Personalized career advice & natural language understanding.
* **Scikit-learn / TensorFlow** → For skill-gap prediction and profiling models.

### Database

* **PostgreSQL** → Relational DB for student profiles, recommendations, progress.
* **Firestore (optional)** → For real-time updates (progress dashboards, chat).

### Infrastructure

* **Google Cloud Run / App Engine** → Scalable deployment.
* **Render** → For backend hosting (prototype).
* **Docker** → Containerization for portability.
* **CI/CD with GitHub Actions** → Automated testing and deployment.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/CodeMosaic7/Next-Step.git
cd Next-Step
```

---

### 2. Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload
```

Backend will start at: **[http://localhost:8000](http://localhost:8000)**

---

### 3. Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at: **[http://localhost:5173](http://localhost:5173)**

---

### 4. Environment Variables

Create a `.env.local` file inside the **frontend** folder.
For teamwork, commit only `.env.template` and add `.env` to `.gitignore`.

📄 **`.env.template`**

```env
# ================================
# 🔥 Firebase Config
# ================================
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project_id.firebasestorage.app
VITE_FIREBASE_MESSAGE_SENDER_ID=your_message_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_FIREBASE_MEASUREMENT_ID=your_measurement_id

# ================================
# 🌐 Backend API
# ================================
BACKEND_URL=http://localhost:8000   # for local dev
# BACKEND_URL=https://your-backend.onrender.com  # for production

# ================================
# 🤖 Google Cloud / Vertex AI
# ================================
GOOGLE_PROJECT_ID=your_google_project_id
GOOGLE_VERTEX_LOCATION=us-central1
GOOGLE_API_KEY=your_google_api_key   # or service account via backend
```

---

## 🏛 System Architecture

```bash
Frontend (React + Vite)  <-->  Backend (FastAPI)  <-->  AI Layer (Google Vertex AI)
                                         |
                                         v
                               PostgreSQL Database
```

---

## 🚦 Agile Development Workflow

1. Requirement Gathering & SRS
2. System Design & Architecture
3. Feature Implementation (Sprint-based)
4. Testing (Unit, Integration, UAT)
5. Deployment on Google Cloud / Render
6. Feedback & Iteration

---

## 📌 Roadmap

1. Define problem & requirements
2. Create system architecture & SRS
3. Build student profiling module
4. Integrate Google Generative AI for recommendations
5. Implement skill-gap analysis engine
6. Develop frontend dashboard & chatbot
7. Deploy MVP on Google Cloud
8. Add advanced features (mentor connect, multilingual support)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch (`feature-new`)
3. Commit changes and push
4. Submit a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** – see the LICENSE file for details.

---
