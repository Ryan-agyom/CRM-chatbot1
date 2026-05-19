from app.core.data_loader import get_dataset_context


def build_prompt(message, history, module):

    dataset_context = get_dataset_context()

    history_text = "\\n".join([
        f"{item['role']}: {item['content']}"
        for item in history[-10:]
    ])

    return f'''
You are an AI CRM analytics assistant.

Available datasets:

Leads Dataset:
Columns: {dataset_context["leads_columns"]}

Campaign Dataset:
Columns: {dataset_context["campaigns_columns"]}

Support Tickets Dataset:
Columns: {dataset_context["tickets_columns"]}

Dataset Counts:
- Leads: {dataset_context["lead_count"]}
- Campaigns: {dataset_context["campaign_count"]}
- Tickets: {dataset_context["ticket_count"]}

Conversation History:
{history_text}

User Question:
{message}

Rules:
- Answer ONLY using CRM business context
- Be concise
- Give analytical insights
- Never hallucinate fake database access
- If the question needs exact aggregates or joins, prefer saying what is missing rather than guessing
'''
