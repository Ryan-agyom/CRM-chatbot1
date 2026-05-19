from app.core.ai_provider import generate_reply
from app.core.analytics_engine import generate_real_analytics
from app.core.chat_actions import try_handle_chat_action
from app.core.memory import remember
from app.core.prompts import build_prompt
from app.core.router import route_conversation
from app.core.sessions import append_message, get_history
from app.services.crm_service import crm_service


def _format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "none"


def _is_crm_summary_question(message: str) -> bool:
    normalized_message = message.lower()
    return any(
        term in normalized_message
        for term in (
            "summarize",
            "summary",
            "overview",
            "current crm",
            "how many leads",
            "how many campaigns",
            "how many support tickets",
            "obvious trends",
        )
    )


def _build_crm_summary_reply() -> str:
    leads = crm_service.list_leads()
    campaigns = crm_service.list_campaigns()
    tickets = crm_service.list_support_tickets()
    insights = crm_service.get_insights()

    lead_names = [f"{lead['customer_name']} ({lead['lead_source']})" for lead in leads[:5]]
    campaign_names = [f"{campaign['campaign_name']} [{campaign['target_industry']}]" for campaign in campaigns[:5]]
    ticket_samples = [
        f"{ticket['customer_name']}: {ticket['query_type']} ({ticket['assigned_department']}, {ticket['status']})"
        for ticket in tickets[:5]
    ]

    return "\n".join(
        [
            "CRM Summary",
            "",
            f"Counts: {len(leads)} leads, {len(campaigns)} campaigns, {len(tickets)} support tickets.",
            "",
            f"Lead examples: {_format_list(lead_names)}.",
            f"Campaign examples: {_format_list(campaign_names)}.",
            f"Ticket examples: {_format_list(ticket_samples)}.",
            "",
            "Insights:",
            f"Common complaints: {_format_list(insights['customerInsights']['commonComplaints'])}.",
            f"Likely conversions: {insights['predictiveAnalysis']['likelyToConvert']} leads currently look ready.",
            f"Churn risk: {insights['predictiveAnalysis']['likelyToChurn']}.",
            f"Trending products: {_format_list(insights['predictiveAnalysis']['trendingProducts'])}.",
        ]
    )


async def process_chat(message, session_id):
    action_reply = try_handle_chat_action(message)
    if action_reply:
        append_message(session_id, "user", message)
        append_message(session_id, "assistant", action_reply)
        remember(session_id, {"last_module": "crm", "last_action": "mutation"})
        return {
            "sessionId": session_id,
            "reply": action_reply,
        }

    analytics_reply = generate_real_analytics(message)
    if analytics_reply:
        append_message(session_id, "user", message)
        append_message(session_id, "assistant", analytics_reply)
        remember(session_id, {"last_module": "crm"})
        return {
            "sessionId": session_id,
            "reply": analytics_reply,
        }

    history = get_history(session_id)
    module = route_conversation(message)
    if module == "crm" and _is_crm_summary_question(message):
        reply = _build_crm_summary_reply()
    else:
        prompt = build_prompt(message=message, history=history, module=module)
        reply = await generate_reply(prompt)

    append_message(session_id, "user", message)
    append_message(session_id, "assistant", reply)
    remember(session_id, {"last_module": module})
    return {
        "sessionId": session_id,
        "reply": reply,
    }
