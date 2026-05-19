import pandas as pd

leads_df = pd.read_csv("data/crm_leads.csv")
tickets_df = pd.read_csv("data/crm_support_tickets.csv")
campaigns_df = pd.read_csv("data/crm_campaigns.csv")


def get_top_ticket_clients():
    top_clients = (
        tickets_df["customer_name"]
        .value_counts()
        .head(5)
    )

    result = "Top clients with most support tickets:\n\n"

    for name, count in top_clients.items():
        result += f"{name} → {count} tickets\n"

    return result

def get_most_common_query():
    top_query = tickets_df["query_type"].value_counts().idxmax()
    count = tickets_df["query_type"].value_counts().max()

    return f"The most common query type is '{top_query}' with {count} tickets."

def get_best_campaign():
    best = campaigns_df.sort_values(
        by="conversion_rate",
        ascending=False
    ).iloc[0]

    return (
        f"Best campaign: {best['campaign_name']} "
        f"with conversion rate {best['conversion_rate']}%"
    )