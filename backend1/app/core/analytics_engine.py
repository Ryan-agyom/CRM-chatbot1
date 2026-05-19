from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from functools import lru_cache

import pandas as pd

from app.core.data_loader import get_campaigns_df, get_leads_df, get_tickets_df


TOP_N_REGEX = re.compile(r"\btop\s+(\d+)\b")


@dataclass(frozen=True)
class QueryResult:
    reply: str
    matched: bool = True


class CRMAnalyticsEngine:
    def __init__(self) -> None:
        self._connection = sqlite3.connect(":memory:", check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._bootstrap()

    def _bootstrap(self) -> None:
        leads_df = get_leads_df().copy()
        tickets_df = get_tickets_df().copy()
        campaigns_df = get_campaigns_df().copy()

        leads_df["created_at"] = leads_df["created_at"].dt.strftime("%Y-%m-%d")
        tickets_df["created_at"] = tickets_df["created_at"].dt.strftime("%Y-%m-%d")
        campaigns_df["launch_date"] = campaigns_df["launch_date"].dt.strftime("%Y-%m-%d")

        leads_df.to_sql("leads", self._connection, index=False, if_exists="replace")
        tickets_df.to_sql("tickets", self._connection, index=False, if_exists="replace")
        campaigns_df.to_sql("campaigns", self._connection, index=False, if_exists="replace")

        self._connection.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_leads_customer_name ON leads(customer_name);
            CREATE INDEX IF NOT EXISTS idx_leads_company ON leads(company);
            CREATE INDEX IF NOT EXISTS idx_leads_industry ON leads(industry);
            CREATE INDEX IF NOT EXISTS idx_tickets_customer_name ON tickets(customer_name);
            CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
            CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
            CREATE INDEX IF NOT EXISTS idx_tickets_department ON tickets(assigned_department);
            CREATE INDEX IF NOT EXISTS idx_tickets_query_type ON tickets(query_type);
            CREATE INDEX IF NOT EXISTS idx_campaigns_target_industry ON campaigns(target_industry);
            CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);

            CREATE VIEW IF NOT EXISTS tickets_enriched AS
            SELECT
                t.ticket_id,
                t.customer_name,
                t.email,
                t.query_type,
                t.issue_summary,
                t.product,
                t.priority,
                t.status AS ticket_status,
                t.assigned_department,
                t.response_time_hours,
                t.satisfaction_score,
                t.created_at AS ticket_created_at,
                l.lead_id,
                l.company,
                l.industry,
                l.lead_source,
                l.status AS lead_status,
                l.city
            FROM tickets t
            LEFT JOIN leads l
                ON t.customer_name = l.customer_name;
            """
        )

    def _query_dataframe(self, sql: str, params: tuple[object, ...] = ()) -> pd.DataFrame:
        return pd.read_sql_query(sql, self._connection, params=params)

    def _top_n(self, question: str, default: int = 5, maximum: int = 10) -> int:
        match = TOP_N_REGEX.search(question)
        if not match:
            return default
        return max(1, min(int(match.group(1)), maximum))

    def answer(self, question: str) -> QueryResult | None:
        normalized = " ".join(question.lower().split())

        for handler in (
            self._answer_open_ticket_count_by_company,
            self._answer_top_company_by_ticket_volume,
            self._answer_top_client_ticket_volume,
            self._answer_most_common_query,
            self._answer_best_campaign,
            self._answer_high_priority_ticket_count,
            self._answer_average_response_time,
            self._answer_average_satisfaction,
            self._answer_ticket_count_by_department,
            self._answer_campaign_performance_by_industry,
        ):
            result = handler(normalized)
            if result:
                return result

        return None

    def _answer_top_company_by_ticket_volume(self, question: str) -> QueryResult | None:
        company_terms = ("company", "companies", "organization", "organisations", "organizations")
        ticket_terms = ("support ticket", "tickets", "ticket volume")
        top_terms = ("most", "highest", "top")
        if not any(term in question for term in company_terms):
            return None
        if not any(term in question for term in ticket_terms):
            return None
        if not any(term in question for term in top_terms):
            return None
        if "open" in question:
            return None

        limit = self._top_n(question, default=5)
        result = self._query_dataframe(
            """
            SELECT
                company,
                COUNT(*) AS ticket_count,
                COUNT(DISTINCT customer_name) AS client_count
            FROM tickets_enriched
            WHERE company IS NOT NULL
            GROUP BY company
            ORDER BY ticket_count DESC, company ASC
            LIMIT ?
            """,
            (limit,),
        )
        if result.empty:
            return QueryResult(
                "I could not map support tickets to companies from the current data, so no company-level join answer is available."
            )

        top_row = result.iloc[0]
        lines = [
            (
                f"The company with the most support tickets is '{top_row['company']}' "
                f"with {int(top_row['ticket_count'])} tickets across "
                f"{int(top_row['client_count'])} matched client record(s)."
            )
        ]
        if limit > 1:
            lines.append("")
            lines.append("Top matched companies by support tickets:")
            for row in result.itertuples(index=False):
                lines.append(f"- {row.company}: {int(row.ticket_count)} tickets")
        lines.append("")
        lines.append("This answer uses only ticket rows that could be joined to lead records by customer name.")
        return QueryResult("\n".join(lines))

    def _answer_top_client_ticket_volume(self, question: str) -> QueryResult | None:
        if "most common query" in question or "common issue" in question:
            return None
        if any(term in question for term in ("department", "team", "company", "companies", "industry")):
            return None
        has_client_or_customer = any(term in question for term in ("client", "clients", "customer", "customers"))
        has_ticket_term = any(term in question for term in ("ticket", "tickets"))
        if not ("most tickets" in question or (has_client_or_customer and has_ticket_term)):
            return None

        limit = self._top_n(question, default=5)
        result = self._query_dataframe(
            """
            SELECT
                customer_name,
                COUNT(*) AS ticket_count,
                MAX(company) AS company
            FROM tickets_enriched
            GROUP BY customer_name
            ORDER BY ticket_count DESC, customer_name ASC
            LIMIT ?
            """,
            (limit,),
        )
        if result.empty:
            return None

        lines = ["Top clients with the most support tickets:"]
        for row in result.itertuples(index=False):
            if pd.notna(row.company):
                lines.append(f"- {row.customer_name} ({row.company}): {int(row.ticket_count)} tickets")
            else:
                lines.append(f"- {row.customer_name}: {int(row.ticket_count)} tickets")
        return QueryResult("\n".join(lines))

    def _answer_most_common_query(self, question: str) -> QueryResult | None:
        if not any(term in question for term in ("common query", "most common issue", "frequent query", "frequent issue", "query type")):
            return None

        result = self._query_dataframe(
            """
            SELECT query_type, COUNT(*) AS ticket_count
            FROM tickets
            GROUP BY query_type
            ORDER BY ticket_count DESC, query_type ASC
            LIMIT 1
            """
        )
        if result.empty:
            return None
        row = result.iloc[0]
        return QueryResult(f"The most common query type is '{row['query_type']}' with {int(row['ticket_count'])} tickets.")

    def _answer_best_campaign(self, question: str) -> QueryResult | None:
        if not any(term in question for term in ("best campaign", "highest conversion", "top campaign", "best performing campaign")):
            return None

        result = self._query_dataframe(
            """
            SELECT campaign_name, conversion_rate, target_industry, status
            FROM campaigns
            ORDER BY conversion_rate DESC, conversions DESC
            LIMIT 1
            """
        )
        if result.empty:
            return None
        row = result.iloc[0]
        return QueryResult(
            f"The best campaign is '{row['campaign_name']}' in {row['target_industry']} with a {float(row['conversion_rate']):.2f}% conversion rate and status '{row['status']}'."
        )

    def _answer_high_priority_ticket_count(self, question: str) -> QueryResult | None:
        if not any(term in question for term in ("high priority", "critical tickets", "urgent tickets")):
            return None

        priority = "High"
        if "critical" in question:
            priority = "Critical"

        result = self._query_dataframe(
            """
            SELECT COUNT(*) AS total_count
            FROM tickets
            WHERE priority = ?
            """,
            (priority,),
        )
        return QueryResult(f"There are {int(result.iloc[0]['total_count'])} {priority.lower()} support tickets.")

    def _answer_open_ticket_count_by_company(self, question: str) -> QueryResult | None:
        if "open" not in question:
            return None
        if not any(term in question for term in ("company", "companies")):
            return None
        if "ticket" not in question:
            return None

        limit = self._top_n(question, default=5)
        result = self._query_dataframe(
            """
            SELECT
                company,
                COUNT(*) AS open_ticket_count
            FROM tickets_enriched
            WHERE company IS NOT NULL AND LOWER(ticket_status) = 'open'
            GROUP BY company
            ORDER BY open_ticket_count DESC, company ASC
            LIMIT ?
            """,
            (limit,),
        )
        if result.empty:
            return QueryResult("No open tickets could be mapped to companies from the current joined dataset.")

        lines = ["Companies with the most open support tickets:"]
        for row in result.itertuples(index=False):
            lines.append(f"- {row.company}: {int(row.open_ticket_count)} open tickets")
        return QueryResult("\n".join(lines))

    def _answer_average_response_time(self, question: str) -> QueryResult | None:
        if "response time" not in question and "resolution time" not in question:
            return None

        if any(term in question for term in ("department", "team")):
            result = self._query_dataframe(
                """
                SELECT
                    assigned_department,
                    AVG(response_time_hours) AS avg_response_time
                FROM tickets
                GROUP BY assigned_department
                ORDER BY avg_response_time DESC, assigned_department ASC
                LIMIT 5
                """
            )
            lines = ["Average response time by department:"]
            for row in result.itertuples(index=False):
                lines.append(f"- {row.assigned_department}: {float(row.avg_response_time):.2f} hours")
            return QueryResult("\n".join(lines))

        if "company" in question:
            result = self._query_dataframe(
                """
                SELECT
                    company,
                    AVG(response_time_hours) AS avg_response_time,
                    COUNT(*) AS ticket_count
                FROM tickets_enriched
                WHERE company IS NOT NULL
                GROUP BY company
                HAVING COUNT(*) >= 1
                ORDER BY avg_response_time DESC, ticket_count DESC, company ASC
                LIMIT 5
                """
            )
            if result.empty:
                return QueryResult("No company-linked tickets were available to compute response-time joins.")
            lines = ["Average response time by company:"]
            for row in result.itertuples(index=False):
                lines.append(
                    f"- {row.company}: {float(row.avg_response_time):.2f} hours across {int(row.ticket_count)} ticket(s)"
                )
            return QueryResult("\n".join(lines))

        result = self._query_dataframe(
            "SELECT AVG(response_time_hours) AS avg_response_time FROM tickets"
        )
        return QueryResult(f"The average support ticket response time is {float(result.iloc[0]['avg_response_time']):.2f} hours.")

    def _answer_average_satisfaction(self, question: str) -> QueryResult | None:
        if "satisfaction" not in question and "rating" not in question:
            return None

        if "company" in question:
            result = self._query_dataframe(
                """
                SELECT
                    company,
                    AVG(satisfaction_score) AS avg_satisfaction,
                    COUNT(*) AS ticket_count
                FROM tickets_enriched
                WHERE company IS NOT NULL
                GROUP BY company
                ORDER BY avg_satisfaction DESC, ticket_count DESC, company ASC
                LIMIT 5
                """
            )
            if result.empty:
                return QueryResult("No company-linked tickets were available to compute satisfaction by company.")
            lines = ["Top companies by average ticket satisfaction:"]
            for row in result.itertuples(index=False):
                lines.append(
                    f"- {row.company}: {float(row.avg_satisfaction):.2f}/5 across {int(row.ticket_count)} ticket(s)"
                )
            return QueryResult("\n".join(lines))

        result = self._query_dataframe(
            "SELECT AVG(satisfaction_score) AS avg_satisfaction FROM tickets"
        )
        return QueryResult(f"The average ticket satisfaction score is {float(result.iloc[0]['avg_satisfaction']):.2f} out of 5.")

    def _answer_ticket_count_by_department(self, question: str) -> QueryResult | None:
        if "department" not in question and "team" not in question:
            return None
        if "ticket" not in question:
            return None

        result = self._query_dataframe(
            """
            SELECT assigned_department, COUNT(*) AS ticket_count
            FROM tickets
            GROUP BY assigned_department
            ORDER BY ticket_count DESC, assigned_department ASC
            """
        )
        if result.empty:
            return None
        lines = ["Support ticket count by department:"]
        for row in result.itertuples(index=False):
            lines.append(f"- {row.assigned_department}: {int(row.ticket_count)} tickets")
        return QueryResult("\n".join(lines))

    def _answer_campaign_performance_by_industry(self, question: str) -> QueryResult | None:
        if "campaign" not in question:
            return None
        if not any(term in question for term in ("industry", "industries")):
            return None

        result = self._query_dataframe(
            """
            SELECT
                target_industry,
                AVG(conversion_rate) AS avg_conversion_rate,
                SUM(conversions) AS total_conversions,
                COUNT(*) AS campaign_count
            FROM campaigns
            GROUP BY target_industry
            ORDER BY avg_conversion_rate DESC, total_conversions DESC, target_industry ASC
            LIMIT 5
            """
        )
        if result.empty:
            return None
        lines = ["Campaign performance by target industry:"]
        for row in result.itertuples(index=False):
            lines.append(
                f"- {row.target_industry}: {float(row.avg_conversion_rate):.2f}% average conversion rate across {int(row.campaign_count)} campaign(s)"
            )
        return QueryResult("\n".join(lines))


@lru_cache(maxsize=1)
def get_analytics_engine() -> CRMAnalyticsEngine:
    return CRMAnalyticsEngine()


def generate_real_analytics(question: str) -> str | None:
    result = get_analytics_engine().answer(question)
    return result.reply if result else None


def clear_analytics_engine_cache() -> None:
    get_analytics_engine.cache_clear()
