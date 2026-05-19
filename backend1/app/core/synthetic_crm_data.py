from __future__ import annotations

import random

import pandas as pd
from faker import Faker


fake = Faker()

LEAD_SOURCES = [
    "Website",
    "Facebook Ads",
    "Instagram",
    "Google Ads",
    "Referral",
    "LinkedIn",
    "Chatbot",
]

INDUSTRIES = [
    "Retail",
    "Healthcare",
    "Finance",
    "Education",
    "Real Estate",
    "E-commerce",
    "Technology",
]

CAMPAIGN_TYPES = [
    "Email Marketing",
    "Festival Offer",
    "Product Launch",
    "Discount Campaign",
    "Retargeting",
    "Awareness Campaign",
]

QUERY_TYPES = [
    "Billing Inquiry",
    "Technical Support",
    "Refund Request",
    "Product Inquiry",
    "Feature Request",
    "Order Delay",
    "Account Access",
]

ISSUE_SUMMARIES = {
    "Billing Inquiry": [
        "Customer was charged twice for the subscription.",
        "Invoice amount does not match the selected plan.",
        "Customer requested payment receipt.",
        "Refund not received after cancellation.",
    ],
    "Technical Support": [
        "Unable to login to the dashboard.",
        "Application crashes during checkout.",
        "Customer cannot reset password.",
        "Website loads very slowly on mobile devices.",
    ],
    "Refund Request": [
        "Customer wants refund for accidental purchase.",
        "Refund requested for defective product.",
        "Customer cancelled order and requested refund.",
        "Refund delayed beyond expected timeline.",
    ],
    "Product Inquiry": [
        "Customer asked about premium plan features.",
        "Client requested product demo.",
        "Customer wants pricing details.",
        "Inquiry about AI automation capabilities.",
    ],
    "Feature Request": [
        "Customer requested dark mode feature.",
        "User wants WhatsApp integration.",
        "Client suggested multi-language support.",
        "Customer requested advanced analytics dashboard.",
    ],
    "Order Delay": [
        "Customer reported delayed shipment.",
        "Order tracking information not updating.",
        "Package delivery delayed due to logistics issue.",
        "Customer has not received order confirmation.",
    ],
    "Account Access": [
        "Customer account locked after failed login attempts.",
        "Two-factor authentication not working.",
        "User unable to access admin panel.",
        "Password reset email not received.",
    ],
}

TICKET_STATUS = ["Open", "Closed", "Pending", "Resolved"]
PRIORITY_LEVELS = ["Low", "Medium", "High", "Critical"]
PRODUCTS = [
    "CRM Suite",
    "AI Assistant",
    "Analytics Dashboard",
    "Marketing Tool",
    "Automation Platform",
]
DEPARTMENTS = ["Support", "Technical", "Billing", "Sales"]


def build_synthetic_dataset(*, leads: int, campaigns: int, tickets: int) -> dict[str, pd.DataFrame]:
    lead_rows = []
    for index in range(leads):
        lead_rows.append(
            {
                "lead_id": index + 1,
                "customer_name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "company": fake.company(),
                "industry": random.choice(INDUSTRIES),
                "lead_source": random.choice(LEAD_SOURCES),
                "budget": random.randint(1000, 50000),
                "interest_level": random.choice(["Low", "Medium", "High"]),
                "status": random.choice(["New", "Qualified", "Converted", "Lost"]),
                "city": fake.city(),
                "created_at": fake.date_this_year(),
            }
        )

    campaign_rows = []
    for index in range(campaigns):
        campaign_rows.append(
            {
                "campaign_id": index + 1,
                "campaign_name": f"{random.choice(CAMPAIGN_TYPES)} {index + 1}",
                "campaign_type": random.choice(CAMPAIGN_TYPES),
                "target_industry": random.choice(INDUSTRIES),
                "budget": random.randint(5000, 100000),
                "clicks": random.randint(100, 10000),
                "impressions": random.randint(1000, 100000),
                "conversions": random.randint(10, 500),
                "conversion_rate": round(random.uniform(1.0, 25.0), 2),
                "status": random.choice(["Active", "Paused", "Completed"]),
                "launch_date": fake.date_this_year(),
            }
        )

    ticket_rows = []
    for index in range(tickets):
        query_type = random.choice(QUERY_TYPES)
        ticket_rows.append(
            {
                "ticket_id": index + 1,
                "customer_name": fake.name(),
                "email": fake.email(),
                "query_type": query_type,
                "issue_summary": random.choice(ISSUE_SUMMARIES[query_type]),
                "product": random.choice(PRODUCTS),
                "priority": random.choice(PRIORITY_LEVELS),
                "status": random.choice(TICKET_STATUS),
                "assigned_department": random.choice(DEPARTMENTS),
                "response_time_hours": random.randint(1, 72),
                "satisfaction_score": random.randint(1, 5),
                "created_at": fake.date_this_year(),
            }
        )

    return {
        "leads": pd.DataFrame(lead_rows),
        "campaigns": pd.DataFrame(campaign_rows),
        "tickets": pd.DataFrame(ticket_rows),
    }
