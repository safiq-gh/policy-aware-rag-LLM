import json

def enforce(evaluator_output: str):

    try:
        data = json.loads(evaluator_output)
    except:
        return {
            "action": "block",
            "message": "Invalid evaluator output"
        }

    # ---- Normalize risk ----
    risk = data.get("risk_level", "").lower()

    if risk in ["critical", "severe", "extreme"]:
        risk = "high"
    if risk in ["moderate"]:
        risk = "medium"

    # ---- Decision logic ----
    if not data.get("violated", False):
        return {"action": "allow", "message": "Prompt allowed"}

    if risk == "low":
        return {"action": "warn", "message": "Potential policy violation"}

    if risk == "medium":
        return {"action": "restrict", "message": "Partial restriction applied"}

    if risk == "high":
        return {"action": "block", "message": "Prompt blocked due to policy violation"}

    return {"action": "block", "message": "Unknown risk level"}
