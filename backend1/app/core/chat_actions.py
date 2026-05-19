from __future__ import annotations

import re

from app.services.crm_service import crm_service


EMAIL_REGEX = re.compile(r"[\w.\-+]+@[\w.\-]+\.\w+")
PHONE_REGEX = re.compile(r"(\+?\d[\d\s\-()]{7,}\d)")
NUMBER_REGEX = re.compile(r"\b\d+(?:\.\d+)?\b")


def try_handle_chat_action(message: str) -> str | None:
    normalized = " ".join(message.lower().split())

    if _is_lead_creation_request(normalized):
        return _handle_lead_creation(message)
    if _is_ticket_creation_request(normalized):
        return _handle_ticket_creation(message)
    if _is_campaign_creation_request(normalized):
        return _handle_campaign_creation(message)

    return None


def _is_lead_creation_request(message: str) -> bool:
    return any(term in message for term in ("add lead", "create lead", "new lead")) or (
        "add " in message and " as a lead" in message
    )


def _is_ticket_creation_request(message: str) -> bool:
    return any(term in message for term in ("create ticket", "add ticket", "support ticket", "new ticket"))


def _is_campaign_creation_request(message: str) -> bool:
    return any(term in message for term in ("create campaign", "add campaign", "new campaign"))


def _extract_named_field(message: str, *field_names: str) -> str | None:
    for field_name in field_names:
        pattern = re.compile(
            rf"{field_name}\s*(?:is|=|:)?\s*['\"]?([^,;\n]+?)['\"]?(?=(?:\s+\w+\s*(?:is|=|:))|[,;\n]|$)",
            re.IGNORECASE,
        )
        match = pattern.search(message)
        if match:
            return match.group(1).strip(" .")
    return None


def _extract_email(message: str) -> str | None:
    match = EMAIL_REGEX.search(message)
    return match.group(0) if match else None


def _extract_phone(message: str) -> str | None:
    match = PHONE_REGEX.search(message)
    return match.group(1).strip() if match else None


def _extract_name_after_phrase(message: str, phrase: str) -> str | None:
    pattern = re.compile(rf"{phrase}\s+(.+?)(?:\s+with|\s+email|\s+phone|\s+company|\s+industry|,|$)", re.IGNORECASE)
    match = pattern.search(message)
    if match:
        return match.group(1).strip(" .,'\"")
    return None


def _extract_name_before_lead(message: str) -> str | None:
    pattern = re.compile(r"add\s+(.+?)\s+as\s+a\s+lead", re.IGNORECASE)
    match = pattern.search(message)
    if match:
        return match.group(1).strip(" .,'\"")
    return None


def _extract_number_after_label(message: str, label: str) -> int | float | None:
    pattern = re.compile(rf"{label}\s*(?:is|=|:)?\s*(\d+(?:\.\d+)?)", re.IGNORECASE)
    match = pattern.search(message)
    if not match:
        return None
    value = match.group(1)
    return float(value) if "." in value else int(value)


def _handle_lead_creation(message: str) -> str:
    customer_name = (
        _extract_named_field(message, "customer_name", "name")
        or _extract_name_before_lead(message)
        or _extract_name_after_phrase(message, "create lead for")
        or _extract_name_after_phrase(message, "add lead for")
    )
    email = _extract_email(message)
    phone = _extract_phone(message)
    company = _extract_named_field(message, "company")
    industry = _extract_named_field(message, "industry")
    lead_source = _extract_named_field(message, "lead_source", "source") or "Chatbot"
    budget = int(_extract_number_after_label(message, "budget") or 0)
    interest_level = _extract_named_field(message, "interest_level", "interest") or "Medium"
    status = _extract_named_field(message, "status") or "New"
    city = _extract_named_field(message, "city")

    missing = []
    if not customer_name:
        missing.append("name")
    if not email:
        missing.append("email")
    if not company:
        missing.append("company")
    if not industry:
        missing.append("industry")

    if missing:
        missing_text = ", ".join(missing)
        return (
            f"I can add the lead, but I still need: {missing_text}. "
            "Use a message like: add lead name=Ryan Jain, email=ryan@example.com, company=OpenAI Test Co, industry=Technology."
        )

    lead = crm_service.create_lead(
        {
            "customer_name": customer_name,
            "email": email,
            "phone": phone,
            "company": company,
            "industry": industry,
            "lead_source": lead_source,
            "budget": budget,
            "interest_level": interest_level,
            "status": status,
            "city": city,
        }
    )
    return (
        f"Lead created successfully for {lead['customer_name']} at {lead['company']}. "
        f"Lead ID is {lead['lead_id']} and status is {lead['status']}."
    )


def _handle_ticket_creation(message: str) -> str:
    customer_name = (
        _extract_named_field(message, "customer_name", "name")
        or _extract_name_after_phrase(message, "create ticket for")
        or _extract_name_after_phrase(message, "add ticket for")
    )
    email = _extract_email(message)
    query_type = _extract_named_field(message, "query_type", "type", "issue type")
    issue_summary = _extract_named_field(message, "issue_summary", "issue", "summary", "problem")
    product = _extract_named_field(message, "product")
    priority = _extract_named_field(message, "priority") or "Medium"
    status = _extract_named_field(message, "status") or "Open"
    assigned_department = _extract_named_field(message, "assigned_department", "department") or "Support"
    response_time_hours = int(_extract_number_after_label(message, "response_time_hours") or 0)
    satisfaction_score = int(_extract_number_after_label(message, "satisfaction_score") or 3)

    missing = []
    for field_name, field_value in (
        ("name", customer_name),
        ("email", email),
        ("query type", query_type),
        ("issue summary", issue_summary),
        ("product", product),
    ):
        if not field_value:
            missing.append(field_name)

    if missing:
        return (
            f"I can create the support ticket, but I still need: {', '.join(missing)}. "
            "Use a message like: create ticket name=Ryan Jain, email=ryan@example.com, query_type=Technical Support, issue=Login issue, product=CRM Suite."
        )

    ticket = crm_service.create_support_ticket(
        {
            "customer_name": customer_name,
            "email": email,
            "query_type": query_type,
            "issue_summary": issue_summary,
            "product": product,
            "priority": priority,
            "status": status,
            "assigned_department": assigned_department,
            "response_time_hours": response_time_hours,
            "satisfaction_score": satisfaction_score,
        }
    )
    return (
        f"Support ticket created for {ticket['customer_name']}. "
        f"Ticket ID is {ticket['ticket_id']} with status {ticket['status']} in {ticket['assigned_department']}."
    )


def _handle_campaign_creation(message: str) -> str:
    campaign_name = _extract_named_field(message, "campaign_name", "name")
    campaign_type = _extract_named_field(message, "campaign_type", "type")
    target_industry = _extract_named_field(message, "target_industry", "industry")
    budget = int(_extract_number_after_label(message, "budget") or 0)
    clicks = int(_extract_number_after_label(message, "clicks") or 0)
    impressions = int(_extract_number_after_label(message, "impressions") or 0)
    conversions = int(_extract_number_after_label(message, "conversions") or 0)
    conversion_rate = float(_extract_number_after_label(message, "conversion_rate") or 0.0)
    status = _extract_named_field(message, "status") or "Active"

    missing = []
    for field_name, field_value in (
        ("campaign name", campaign_name),
        ("campaign type", campaign_type),
        ("target industry", target_industry),
    ):
        if not field_value:
            missing.append(field_name)

    if missing:
        return (
            f"I can create the campaign, but I still need: {', '.join(missing)}. "
            "Use a message like: create campaign campaign_name=June Launch, campaign_type=Email Marketing, target_industry=Technology, budget=12000."
        )

    campaign = crm_service.create_campaign(
        {
            "campaign_name": campaign_name,
            "campaign_type": campaign_type,
            "target_industry": target_industry,
            "budget": budget,
            "clicks": clicks,
            "impressions": impressions,
            "conversions": conversions,
            "conversion_rate": conversion_rate,
            "status": status,
        }
    )
    return (
        f"Campaign created successfully: {campaign['campaign_name']}. "
        f"Campaign ID is {campaign['campaign_id']} and status is {campaign['status']}."
    )
