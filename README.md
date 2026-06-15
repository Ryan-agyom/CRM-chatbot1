# 🤖 AI-Powered Chatbot + CRM Platform

A full-stack application combining an intelligent AI chatbot with comprehensive CRM functionality. Build, manage, and analyze customer relationships while providing conversational AI support—all in one integrated platform.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Configuration](#environment-configuration)
- [Running Locally](#running-locally)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [CRM Modules](#crm-modules)
- [Scripts & Utilities](#scripts--utilities)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project is a modern, full-stack web application that integrates:
- **AI Chatbot**: Powered by Gemini API for intelligent conversations
- **CRM System**: Complete customer relationship management tools
- **Predictive Analytics**: Machine learning models for lead scoring, campaign conversion, ticket prioritization, and response time prediction
- **Real-time Analytics**: SQL-based insights and analytics dashboard

Perfect for businesses looking to automate customer interactions while maintaining comprehensive customer data management.

---

## ✨ Key Features

### Chatbot Features
- 🗣️ **Natural Language Processing**: AI-powered conversations using Google Gemini
- 💾 **Conversation Memory**: Maintains context across multiple interactions
- 🔄 **Smart Intent Detection**: Automatically understands user intent
- 📊 **Session Management**: Tracks and manages user sessions

### CRM Features
- 👥 **Lead Management**: Capture, track, and qualify leads
- 📅 **Appointment Scheduling**: Schedule and manage customer appointments
- 📧 **Campaign Management**: Create and track marketing campaigns
- 🎫 **Support Tickets**: Manage customer support requests
- 📈 **CRM Analytics**: Get insights across leads, campaigns, and tickets
- 🤖 **Lead Prediction**: AI-driven lead scoring and qualification
- 🎯 **Campaign Analytics**: Predict campaign conversion rates
- ⚡ **Ticket Intelligence**: Predict ticket priority and response times

---

## 🛠️ Tech Stack

### Frontend
- **React 18.3** - Modern UI framework
- **Vite 5.4** - Lightning-fast build tool
- **React Router 6.28** - Client-side routing
- **CSS3** - Styling

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - ASGI server
- **Python 3.10+** - Core language

### AI & Data
- **LangChain 1.3.1** - LLM orchestration and chains
- **Google Gemini API** - Large language model
- **Scikit-learn** - Machine learning algorithms
- **Pandas** - Data manipulation
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **DuckDB 1.5** - SQL analytics database

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## 📁 Project Structure

```
project-root/
├── frontend/                          # React + Vite frontend application
│   ├── src/
│   │   ├── components/               # Reusable React components
│   │   ├── pages/                    # Page components (HomePage, CRMPage)
│   │   ├── services/                 # API service layer (chatService, etc.)
│   │   ├── store/                    # State management
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── styles/                   # Global styling
│   │   └── utils/                    # Utility functions
│   ├── package.json                  # NPM dependencies
│   └── index.html                    # Entry point
│
├── backend1/                          # Python FastAPI backend
│   ├── app/
│   │   ├── api/                      # API route handlers
│   │   │   ├── chat.py              # Chatbot endpoints
│   │   │   └── crm.py               # CRM endpoints
│   │   ├── core/                     # Core business logic
│   │   │   ├── ai_provider.py       # Gemini API integration
│   │   │   ├── cache_utils.py       # Caching logic
│   │   │   ├── crm_repository.py    # CRM data access
│   │   │   ├── intent_extractor.py  # AI intent detection
│   │   │   ├── chat_actions.py      # Chat action handlers
│   │   │   ├── memory.py            # Conversation memory
│   │   │   └── prompts.py           # AI prompts templates
│   │   ├── services/                 # Business services
│   │   │   ├── chatbot_service.py   # Chat logic
│   │   │   ├── crm_service.py       # CRM operations
│   │   │   ├── lead_prediction_service.py
│   │   │   ├── ticket_prediction_service.py
│   │   │   └── campaign_prediction_service.py
│   │   ├── ml/                       # Machine learning models
│   │   │   ├── lead_status_model.py
│   │   │   ├── ticket_priority_model.py
│   │   │   ├── ticket_response_time_model.py
│   │   │   ├── campaign_conversion_model.py
│   │   │   └── text_selector.py
│   │   ├── models/
│   │   │   └── schemas.py           # Pydantic data models
│   │   └── main.py                  # FastAPI application setup
│   ├── scripts/                       # Utility scripts
│   │   ├── generate_synthetic_data.py    # Generate test data
│   │   ├── train_*.py               # Model training scripts
│   │   ├── predict_*.py             # Prediction scripts
│   │   └── compare_*.py             # Model comparison tools
│   ├── data/                          # CSV data files
│   │   ├── crm_campaigns.csv
│   │   ├── crm_leads.csv
│   │   └── crm_support_tickets.csv
│   ├── models/                        # Trained ML models (.joblib files)
│   ├── requirements.txt               # Python dependencies
│   └── app/main.py                   # Application entry point
│
├── docker/                            # Docker configuration
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
│
├── docs/                              # Documentation
│   ├── architecture.md               # System architecture
│   └── deploy-free-cpu.md            # Cloud deployment guide
│
├── docker-compose.yml                 # Multi-container setup
├── .env.example                       # Environment variables template
└── README.md                          # This file
```

---

## ✅ Prerequisites

Before getting started, ensure you have:

- **Node.js 16+** and **npm** (for frontend)
- **Python 3.10+** (for backend)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **Google Gemini API Key** (free tier available at [Google AI Studio](https://aistudio.google.com))

### Verify Installations

```bash
# Check Node.js and npm
node --version
npm --version

# Check Python
python --version

# Check Docker (optional)
docker --version
docker-compose --version
```

---

## 🚀 Quick Start

### 1️⃣ Clone & Navigate
```bash
cd c:\Users\Ryan\Desktop\Chatbot+CRM
```

### 2️⃣ Setup Environment Variables
```bash
# Copy template
cp .env.example .env

# Edit .env with your settings (see Environment Configuration below)
```

### 3️⃣ Start Backend (Terminal 1)
```bash
cd backend1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4️⃣ Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 5️⃣ Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Health Check**: http://localhost:8000/api/health

---

## 🔐 Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Application Settings
PORT=8000
FRONTEND_URL=http://localhost:5173
VITE_API_URL=http://localhost:8000/api

# AI Provider Configuration
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_API_BASE_URL=https://generativelanguage.googleapis.com/v1beta

# Optional: Database/Cache Settings
# Add any additional environment variables your app needs
```

### Getting Your Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key"
3. Create a new API key in Google Cloud Console
4. Copy and paste it into your `.env` file

---

## 🏃 Running Locally

### Start Backend Only

```bash
cd backend1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
Uvicorn running on http://0.0.0.0:8000
Press CTRL+C to quit
```

### Start Frontend Only

```bash
cd frontend
npm install
npm run dev
```

**Expected output:**
```
  VITE v5.4.10  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Run Both (Recommended for Development)

Open two terminals side-by-side:
- **Terminal 1**: Backend (`cd backend1 && uvicorn app.main:app --reload`)
- **Terminal 2**: Frontend (`cd frontend && npm run dev`)

---

## 🐳 Docker Deployment

### Using Docker Compose (All-in-One)

```bash
docker-compose up --build
```

This will:
- Build and start the backend service on port 8000
- Build and start the frontend service on port 5173
- Automatically link frontend to backend API

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Access Services
- Frontend: http://localhost:5173
- Backend: http://localhost:8000/api

---

## 📡 API Endpoints

### Health & Status
```
GET /api/health
```
Returns the health status and available modules.

### Chatbot Endpoints
```
POST /api/chat
```
Send a message to the AI chatbot and receive a response.

### CRM Endpoints

#### Overview & Analytics
```
GET /api/crm/overview          # Get CRM overview dashboard
GET /api/crm/analytics/insights # Get analytical insights
```

#### Leads Management
```
GET /api/crm/leads                    # List all leads
POST /api/crm/leads                   # Create a new lead
POST /api/crm/leads/qualify           # AI-powered lead qualification
POST /api/crm/leads/predict           # Predict lead status
```

#### Appointments
```
POST /api/crm/appointments            # Schedule an appointment
```

#### Campaigns
```
GET /api/crm/campaigns                # List campaigns
POST /api/crm/campaigns               # Create a campaign
POST /api/crm/campaigns/predict       # Predict campaign conversion
```

#### Support Tickets
```
GET /api/crm/support/tickets          # List support tickets
POST /api/crm/support/tickets         # Create a new ticket
POST /api/crm/support/tickets/predict # Predict ticket priority & response time
```

#### Development
```
POST /api/crm/dev/seed                # Seed database with sample data
```

---

## 🧠 CRM Modules

### Sales CRM
Manage the complete sales lifecycle:
- **Lead Capture**: Collect leads from chatbot interactions
- **Lead Qualification**: Automatically score and qualify leads using AI
- **Appointment Scheduling**: Schedule follow-up meetings
- **Upsell Readiness**: Identify upsell opportunities

### Marketing CRM
Drive marketing success:
- **Segmentation**: Organize customers by attributes
- **Campaign Management**: Create and launch campaigns
- **Campaign Analytics**: Track performance and ROI
- **Personalization**: Deliver personalized messaging

### Support CRM
Provide excellent customer support:
- **Ticket Management**: Create and track support tickets
- **Multilingual Support**: Handle support in multiple languages
- **FAQ Integration**: Provide instant answers via AI
- **Routing**: Automatically route tickets to appropriate teams

### Analytics & Predictions
Make data-driven decisions:
- **Lead Scoring**: AI-driven lead prioritization
- **Predictive Analytics**: Forecast campaign conversion rates
- **Ticket Analytics**: Predict priority and response times
- **SQL Analytics**: Join-style questions across datasets

---

## 🛠️ Scripts & Utilities

### Generate Synthetic Data
```bash
cd backend1
python scripts/generate_synthetic_data.py
```
Creates sample CRM data (leads, campaigns, tickets) for testing and development.

### Train ML Models
```bash
# Train lead status prediction model
python scripts/train_lead_status_model.py

# Train campaign conversion model
python scripts/train_campaign_conversion_model.py

# Train ticket priority model
python scripts/train_ticket_priority_model.py

# Train ticket response time model
python scripts/train_ticket_response_time_model.py
```

### Make Predictions
```bash
# Predict lead status
python scripts/predict_lead_status.py

# Predict ticket outcome
python scripts/predict_ticket_outcome.py
```

### Compare Models
```bash
# Compare different lead status models
python scripts/compare_lead_status_models.py

# Compare campaign conversion models
python scripts/compare_campaign_conversion_models.py

# Compare ticket priority models
python scripts/compare_ticket_priority_models.py

# Compare ticket response time models
python scripts/compare_ticket_response_time_models.py
```

---

## 🔍 API Response Examples

### Chat Request
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help with my order"}'
```

### CRM Overview
```bash
curl http://localhost:8000/api/crm/overview
```

### Create Lead
```bash
curl -X POST http://localhost:8000/api/crm/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "phone": "123-456-7890"
  }'
```

---

## 📖 Additional Documentation

- **Architecture**: See [docs/architecture.md](docs/architecture.md) for detailed system design
- **Cloud Deployment**: See [docs/deploy-free-cpu.md](docs/deploy-free-cpu.md) for free tier hosting options

---

## ❓ Troubleshooting

### Backend Port Already in Use
```bash
# Change port
uvicorn app.main:app --port 8001 --reload
```

### Frontend Can't Connect to Backend
- Verify backend is running: `http://localhost:8000/api/health`
- Check `.env` file has correct `VITE_API_URL`
- Ensure CORS is enabled in backend (it is by default)

### Missing Dependencies
```bash
# Reinstall backend dependencies
cd backend1
pip install --upgrade -r requirements.txt

# Reinstall frontend dependencies
cd frontend
npm install
```

### Gemini API Not Working
- Verify API key is correct in `.env`
- Check internet connection
- Ensure API is enabled in Google Cloud Console

### Docker Issues
```bash
# Clear Docker cache and rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

---

## 🚀 Next Steps

1. **Customize**: Modify prompts in `backend1/app/core/prompts.py`
2. **Train Models**: Run training scripts to improve predictions
3. **Deploy**: Follow [docs/deploy-free-cpu.md](docs/deploy-free-cpu.md) for cloud hosting
4. **Integrate**: Connect to your own CRM database instead of CSV files
5. **Extend**: Add new API endpoints and features

---

## 📝 License & Support

For questions or issues, check the documentation or modify the code to suit your needs.

Happy coding! 🎉


```bash
cd backend1
python scripts/generate_synthetic_data.py
```

Or reseed through the API:

```http
POST /api/crm/dev/seed
Content-Type: application/json
```

Example body:

```json
{
  "leads": 40,
  "campaigns": 8,
  "tickets": 20
}
```
