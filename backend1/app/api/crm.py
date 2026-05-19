from fastapi import APIRouter, status

from app.models.schemas import (
    AppointmentRequest,
    CampaignCreateRequest,
    LeadCreateRequest,
    LeadQualificationRequest,
    SeedRequest,
    SupportTicketCreateRequest,
)
from app.services.crm_service import crm_service


router = APIRouter(prefix="/api/crm", tags=["crm"])


@router.get("/")
def crm_overview():
    return crm_service.get_overview()


@router.get("/overview")
def crm_overview_detailed():
    return crm_service.get_overview()


@router.get("/leads")
def list_leads():
    return crm_service.list_leads()


@router.post("/leads", status_code=status.HTTP_201_CREATED)
def create_lead(request: LeadCreateRequest):
    return crm_service.create_lead(request.model_dump())


@router.post("/leads/qualify")
def qualify_lead(request: LeadQualificationRequest):
    return crm_service.qualify_lead(request.model_dump())


@router.post("/appointments", status_code=status.HTTP_201_CREATED)
def schedule_appointment(request: AppointmentRequest):
    return crm_service.schedule_appointment(request.model_dump())


@router.get("/campaigns")
def list_campaigns():
    return crm_service.list_campaigns()


@router.post("/campaigns", status_code=status.HTTP_201_CREATED)
def create_campaign(request: CampaignCreateRequest):
    return crm_service.create_campaign(request.model_dump())


@router.get("/support/tickets")
def list_support_tickets():
    return crm_service.list_support_tickets()


@router.post("/support/tickets", status_code=status.HTTP_201_CREATED)
def create_support_ticket(request: SupportTicketCreateRequest):
    return crm_service.create_support_ticket(request.model_dump())


@router.get("/analytics/insights")
def get_insights():
    return crm_service.get_insights()


@router.post("/dev/seed", status_code=status.HTTP_201_CREATED)
def seed_synthetic_crm_data(request: SeedRequest):
    return crm_service.seed_synthetic_crm_data(
        leads=request.leads,
        campaigns=request.campaigns,
        tickets=request.tickets,
    )
