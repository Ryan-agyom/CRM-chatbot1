from __future__ import annotations

from pathlib import Path
from datetime import date

import pandas as pd

from app.core.cache_utils import clear_backend_caches
from app.core.data_loader import (
    CAMPAIGNS_DTYPES,
    DATA_DIR,
    LEADS_DTYPES,
    TICKETS_DTYPES,
    get_campaigns_df,
    get_leads_df,
    get_tickets_df,
)


class CRMRepository:
    def __init__(self) -> None:
        self._data_dir = Path(DATA_DIR)

    def list_leads(self) -> list[dict]:
        frame = get_leads_df().copy()
        return self._serialize(frame)

    def list_campaigns(self) -> list[dict]:
        frame = get_campaigns_df().copy()
        return self._serialize(frame)

    def list_tickets(self) -> list[dict]:
        frame = get_tickets_df().copy()
        return self._serialize(frame)

    def create_lead(self, payload: dict) -> dict:
        frame = get_leads_df().copy()
        record = {
            "lead_id": int(frame["lead_id"].max()) + 1 if not frame.empty else 1,
            **payload,
            "created_at": date.today().isoformat(),
        }
        updated = self._append_record(frame, record)
        self._write_csv("crm_leads.csv", updated, LEADS_DTYPES, ["created_at"])
        return self._serialize(pd.DataFrame([record]))[0]

    def create_campaign(self, payload: dict) -> dict:
        frame = get_campaigns_df().copy()
        record = {
            "campaign_id": int(frame["campaign_id"].max()) + 1 if not frame.empty else 1,
            **payload,
            "launch_date": payload.get("launch_date") or date.today().isoformat(),
        }
        updated = self._append_record(frame, record)
        self._write_csv("crm_campaigns.csv", updated, CAMPAIGNS_DTYPES, ["launch_date"])
        return self._serialize(pd.DataFrame([record]))[0]

    def create_ticket(self, payload: dict) -> dict:
        frame = get_tickets_df().copy()
        record = {
            "ticket_id": int(frame["ticket_id"].max()) + 1 if not frame.empty else 1,
            **payload,
            "created_at": date.today().isoformat(),
        }
        updated = self._append_record(frame, record)
        self._write_csv("crm_support_tickets.csv", updated, TICKETS_DTYPES, ["created_at"])
        return self._serialize(pd.DataFrame([record]))[0]

    def replace_all(self, *, leads: pd.DataFrame, campaigns: pd.DataFrame, tickets: pd.DataFrame) -> dict:
        self._write_csv("crm_leads.csv", leads, LEADS_DTYPES, ["created_at"])
        self._write_csv("crm_campaigns.csv", campaigns, CAMPAIGNS_DTYPES, ["launch_date"])
        self._write_csv("crm_support_tickets.csv", tickets, TICKETS_DTYPES, ["created_at"])
        return {
            "leads": len(leads),
            "campaigns": len(campaigns),
            "tickets": len(tickets),
        }

    def snapshot(self) -> dict[str, list[dict]]:
        return {
            "leads": self.list_leads(),
            "campaigns": self.list_campaigns(),
            "tickets": self.list_tickets(),
        }

    def _write_csv(
        self,
        filename: str,
        frame: pd.DataFrame,
        dtypes: dict[str, str],
        date_columns: list[str],
    ) -> None:
        normalized = frame.copy()
        for column in date_columns:
            normalized[column] = pd.to_datetime(normalized[column]).dt.strftime("%Y-%m-%d")
        ordered_columns = list(dtypes.keys()) + date_columns
        normalized = normalized[ordered_columns]
        normalized.to_csv(self._data_dir / filename, index=False)
        clear_backend_caches()

    @staticmethod
    def _serialize(frame: pd.DataFrame) -> list[dict]:
        serialized = frame.copy()
        for column in serialized.columns:
            if pd.api.types.is_datetime64_any_dtype(serialized[column]):
                serialized.loc[:, column] = serialized[column].dt.strftime("%Y-%m-%d")
        return serialized.to_dict(orient="records")

    @staticmethod
    def _append_record(frame: pd.DataFrame, record: dict) -> pd.DataFrame:
        row = {column: record.get(column) for column in frame.columns}
        return pd.concat([frame, pd.DataFrame([row], columns=frame.columns)], ignore_index=True)


crm_repository = CRMRepository()
