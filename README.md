# TalentAI - AI-Powered Resume Screening & Recruitment Platform

TalentAI is a production-grade, enterprise-ready recruitment platform combining a Next.js frontend, microservice backend based on FastAPI, state-of-the-art NLP machine learning pipelines, and robust DevOps automation.

## Project Structure Overview

The repository is structured as a monorepo:

- **`apps/`**: Applications directly interacting with users or routing traffic (Frontend, API Gateway).
- **`services/`**: Core backend microservices handling specific business logic (Auth, Resume, Job, Analytics, Recommendation, Notification).
- **`ml/`**: Machine Learning development, parser components, classifiers, and recommender engines.
- **`infrastructure/`**: Deployment, orchestration, and monitoring configuration (Docker, K8s, Terraform, Prometheus/Grafana/Loki).
- **`shared/`**: Common types, schemas, and utilities shared across services and applications.
- **`docs/`**: Project architecture, API, database schemas, and meeting notes.
- **`scripts/`**: Automation scripts for database setup, backups, and deployments.
- **`.github/`**: CI/CD workflows and repository templates.

## Tech Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui.
- **API Gateway & Microservices**: FastAPI (Python 3.11+).
- **Database**: PostgreSQL (Relational Database).
- **Cache**: Redis.
- **Message Queue**: RabbitMQ.
- **Object Storage**: MinIO (S3-compatible).
- **Machine Learning**: scikit-learn, HuggingFace Transformers, Sentence Transformers, FAISS.
- **DevOps/Ops**: Docker, Kubernetes, NGINX, Terraform, Prometheus, Grafana, Loki.
