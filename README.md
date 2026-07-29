# 🚀 TalentAI – AI-Powered Resume Screening & Recruitment Platform

TalentAI is a production-grade, enterprise-scale recruitment platform that leverages Artificial Intelligence to streamline the hiring process. It enables recruiters to efficiently manage job postings, screen resumes, analyze candidates, and make data-driven hiring decisions through a modern microservice architecture.

The platform combines a high-performance **Next.js** frontend, **FastAPI** microservices, advanced **Machine Learning** pipelines, and cloud-native **DevOps** infrastructure to deliver a scalable and intelligent recruitment ecosystem.

---

## 📖 Features

### 👨‍💼 Candidate Portal
- AI-powered resume analysis
- Resume upload and profile management
- Job search and recommendations
- Application tracking
- Company exploration
- Secure authentication

### 🏢 Recruiter Portal
- Recruiter dashboard
- Job posting management
- Candidate management
- Resume screening
- Applicant tracking
- Hiring analytics
- Company profile management

### ⚙️ Admin Portal
- User management
- Recruiter verification
- Platform analytics
- Reports dashboard
- System monitoring
- Notification management

### 🤖 AI & Machine Learning
- Resume parsing
- Resume-job matching
- Candidate recommendation engine
- Skill extraction
- ATS scoring
- Semantic search
- AI-powered analytics

### 🔐 Security & Authentication
- JWT Authentication
- Role-based access control
- OTP verification
- Two-factor authentication
- Secure API Gateway

---

# 🏗️ Project Architecture

TalentAI follows a **Microservice Architecture** for scalability and maintainability.

```
TalentAI
│
├── apps/
│   ├── frontend
│   └── api-gateway
│
├── services/
│   ├── auth-service
│   ├── resume-service
│   ├── job-service
│   ├── recommendation-service
│   ├── analytics-service
│   └── notification-service
│
├── ml/
│   ├── resume-parser
│   ├── recommender
│   ├── classifiers
│   └── embeddings
│
├── shared/
│
├── infrastructure/
│
├── docs/
│
└── scripts/
```

---

# 📂 Repository Structure

| Directory | Description |
|-----------|-------------|
| **apps/** | Frontend and API Gateway applications |
| **services/** | Backend microservices |
| **ml/** | Machine Learning models and pipelines |
| **shared/** | Shared utilities, types and schemas |
| **docs/** | Documentation and architecture |
| **infrastructure/** | Docker, Kubernetes, Terraform and monitoring |
| **scripts/** | Automation and deployment scripts |
| **.github/** | GitHub workflows and CI/CD |

---

# 🛠️ Tech Stack

## Frontend

- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Hook Form
- Zod
- Axios

---

## Backend

- FastAPI
- Python 3.11+
- SQLAlchemy
- Pydantic
- JWT Authentication

---

## Database & Storage

- PostgreSQL
- Redis
- RabbitMQ
- MinIO

---

## Machine Learning

- Scikit-learn
- Hugging Face Transformers
- Sentence Transformers
- FAISS
- Pandas
- NumPy

---

## DevOps

- Docker
- Docker Compose
- Kubernetes
- Terraform
- NGINX
- Prometheus
- Grafana
- Loki
- GitHub Actions

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/TalentAI.git

cd TalentAI
```

---

## Install Frontend

```bash
cd apps/frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:3000
```

---

## Install Backend

```bash
cd services

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs on

```
http://localhost:8000
```

---

# 📊 System Components

- Resume Screening Engine
- Job Recommendation Engine
- Resume Parser
- ATS Scoring Engine
- Candidate Ranking
- Recruiter Dashboard
- Admin Dashboard
- Authentication Service
- Notification Service
- Analytics Service

---

# 📈 Machine Learning Pipeline

```
Resume
     │
     ▼
Resume Parser
     │
     ▼
Skill Extraction
     │
     ▼
Embedding Generation
     │
     ▼
Semantic Matching
     │
     ▼
Candidate Ranking
     │
     ▼
ATS Score
```

---

# 🔐 Authentication Flow

```
User

 │

 ▼

Login/Register

 │

 ▼

JWT Authentication

 │

 ▼

Role Validation

 │

 ▼

Candidate / Recruiter / Admin Dashboard
```

---

# 📦 Future Enhancements

- AI Interview Assistant
- Video Interview Analysis
- Resume Builder
- Multi-language Resume Parsing
- AI Chatbot
- Calendar Integration
- Email Automation
- Real-time Notifications
- Interview Scheduling
- AI Hiring Insights

---

# 🤝 Contributing

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to the branch

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Authors

- **Sumit Kosta**  
  - GitHub: https://github.com/sumitkosta001

- **Rutuparna Pradhan**  
  - GitHub: https://github.com/rutu-parna

---

## ⭐ If you found this project useful, consider giving it a Star!