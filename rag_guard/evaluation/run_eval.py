import csv
from pathlib import Path
from rag_guard.pipeline.pipeline import guard


DATASET = Path(__file__).resolve().parents[2] / "evaluation" / "evaluation_dataset.csv"


# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------
def load_dataset():

    rows = []

    with open(DATASET, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows.append({
                "prompt": row["prompt"].strip(),
                "label": row["label"].strip(),
                "expected_policy": row["expected_policy"].strip()
            })

    return rows


# -------------------------------------------------
# PREDICTION MAPPING
# -------------------------------------------------
def predict_label(action: str):

    if action in ["block", "restrict", "warn"]:
        return "malicious"

    return "benign"


# -------------------------------------------------
# MAIN EVALUATION
# -------------------------------------------------
def evaluate():

    data = load_dataset()

    TP = FP = TN = FN = 0
    policy_match = 0
    malicious_total = 0

    for row in data:

        result = guard(row["prompt"])

        decision = result["decision"]["action"]
        retrieved = result["policies_retrieved"]

        predicted = predict_label(decision)

        # ---- confusion matrix ----
        if row["label"] == "malicious":
            malicious_total += 1

            if predicted == "malicious":
                TP += 1

                if row["expected_policy"] in retrieved:
                    policy_match += 1

            else:
                FN += 1

        else:
            if predicted == "malicious":
                FP += 1
            else:
                TN += 1

    # ---- metrics ----
    total = TP + TN + FP + FN

    accuracy = (TP + TN) / total
    precision = TP / (TP + FP + 1e-9)
    recall = TP / (TP + FN + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)
    fpr = FP / (FP + TN + 1e-9)
    policy_acc = policy_match / (malicious_total + 1e-9)

    # ---- print ----
    print("\n=== RAG Guard Evaluation ===\n")

    print("Samples:", total)
    print("TP:", TP, "FP:", FP, "TN:", TN, "FN:", FN)

    print("\nAccuracy:", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1:", round(f1, 4))
    print("False Positive Rate:", round(fpr, 4))
    print("Policy Attribution:", round(policy_acc, 4))


# -------------------------------------------------
# ENTRY
# -------------------------------------------------
if __name__ == "__main__":
    evaluate()

