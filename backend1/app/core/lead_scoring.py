def score_lead(payload: dict) -> int:
    budget_score = min(int(payload.get("budget", 0)) / 1000, 40)
    interest_score = min(int(payload.get("interest_level", 0)) * 10, 30)
    size_score = min(int(payload.get("company_size", 0)) / 5, 20)
    timeline_days = max(int(payload.get("purchase_timeline", 365)), 1)
    timeline_score = max(10 - min(timeline_days / 3, 10), 0)
    score = int(round(budget_score + interest_score + size_score + timeline_score))
    return max(0, min(score, 100))
