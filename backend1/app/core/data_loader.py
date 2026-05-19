from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data"


LEADS_DTYPES = {
    "lead_id": "int32",
    "customer_name": "string",
    "email": "string",
    "phone": "string",
    "company": "string",
    "industry": "category",
    "lead_source": "category",
    "budget": "int32",
    "interest_level": "category",
    "status": "category",
    "city": "string",
}

CAMPAIGNS_DTYPES = {
    "campaign_id": "int32",
    "campaign_name": "string",
    "campaign_type": "category",
    "target_industry": "category",
    "budget": "int32",
    "clicks": "int32",
    "impressions": "int32",
    "conversions": "int32",
    "conversion_rate": "float32",
    "status": "category",
}

TICKETS_DTYPES = {
    "ticket_id": "int32",
    "customer_name": "string",
    "email": "string",
    "query_type": "category",
    "issue_summary": "string",
    "product": "category",
    "priority": "category",
    "status": "category",
    "assigned_department": "category",
    "response_time_hours": "int32",
    "satisfaction_score": "int32",
}


def _read_csv(filename: str, dtypes: dict[str, str], date_columns: list[str]) -> pd.DataFrame:
    frame = pd.read_csv(
        DATA_DIR / filename,
        dtype=dtypes,
        parse_dates=date_columns,
    )
    return frame


@lru_cache(maxsize=1)
def get_leads_df() -> pd.DataFrame:
    return _read_csv("crm_leads.csv", LEADS_DTYPES, ["created_at"])


@lru_cache(maxsize=1)
def get_campaigns_df() -> pd.DataFrame:
    return _read_csv("crm_campaigns.csv", CAMPAIGNS_DTYPES, ["launch_date"])


@lru_cache(maxsize=1)
def get_tickets_df() -> pd.DataFrame:
    return _read_csv("crm_support_tickets.csv", TICKETS_DTYPES, ["created_at"])


@lru_cache(maxsize=1)
def get_dataset_context() -> dict[str, object]:
    leads_df = get_leads_df()
    campaigns_df = get_campaigns_df()
    tickets_df = get_tickets_df()

    return {
        "leads_columns": list(leads_df.columns),
        "campaigns_columns": list(campaigns_df.columns),
        "tickets_columns": list(tickets_df.columns),
        "lead_count": len(leads_df),
        "campaign_count": len(campaigns_df),
        "ticket_count": len(tickets_df),
    }


def clear_data_caches() -> None:
    get_leads_df.cache_clear()
    get_campaigns_df.cache_clear()
    get_tickets_df.cache_clear()
    get_dataset_context.cache_clear()
