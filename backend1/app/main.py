from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.crm import router as crm_router

app = FastAPI(title="AI CRM Chatbot Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"],
)

app.include_router(chat_router)
app.include_router(crm_router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "modules": ["general-chatbot", "crm"],
    }


@app.get("/")
def root():
    return {"message": "FastAPI backend running"}
