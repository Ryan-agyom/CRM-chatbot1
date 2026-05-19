def route_conversation(message:str):
    message = message.lower()

    crm_keywords = [
        "lead",
        "campaign",
        "crm",
        "ticket",
        "customer",
        "company",
        "support",
        "industry",
        "satisfaction",
        "response time",
    ]
    for keyword in crm_keywords:
        if keyword in message:
            return "crm"
        
    return "general"
