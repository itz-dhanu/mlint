import re
import json

def audit_notebook(code: str) -> dict:
    issues = []
    lines = code.split("\n")

    has_split = any("train_test_split" in l for l in lines)
    has_fit_transform = any("fit_transform" in l for l in lines)
    has_scaler = any(s in code for s in ["StandardScaler", "MinMaxScaler", "RobustScaler"])

    # 1. Data Leakage
    if has_scaler and has_fit_transform and has_split:
        split_line = next((i for i, l in enumerate(lines) if "train_test_split" in l), 999)
        ft_line = next((i for i, l in enumerate(lines) if "fit_transform" in l), 0)
        if ft_line < split_line:
            issues.append({
                "severity": "critical",
                "category": "Data Leakage",
                "title": "Scaler fitted before train_test_split",
                "description": f"fit_transform() is called on line ~{ft_line+1} before train_test_split on line ~{split_line+1}",
                "fix": "Fit scaler only on X_train, then use transform() on X_test"
            })

    # 2. Reproducibility - random_state
    if has_split and "random_state" not in code:
        issues.append({
            "severity": "warning",
            "category": "Reproducibility",
            "title": "Missing random_state in train_test_split",
            "description": "train_test_split is used without random_state — results will differ every run",
            "fix": "Add random_state=42 to train_test_split()"
        })

    # 3. Evaluating on training data
    if "y_train" in code and ("accuracy_score(y_train" in code or "predict(X_train" in code):
        issues.append({
            "severity": "critical",
            "category": "Evaluation Issues",
            "title": "Model evaluated on training data",
            "description": "Model is being tested on X_train/y_train instead of test data",
            "fix": "Use X_test and y_test for final evaluation"
        })

    # 4. Hardcoded file paths
    for i, line in enumerate(lines):
        if re.search(r'["\']C:\\|["\']C:/|/home/|/Users/', line):
            issues.append({
                "severity": "warning",
                "category": "Code Quality",
                "title": "Hardcoded file path detected",
                "description": f"Line ~{i+1}: Hardcoded path found — won't work on other machines",
                "fix": "Use relative paths or os.path / pathlib"
            })
            break

    # 5. No baseline model
    if "RandomForest" in code or "XGB" in code or "SVC" in code:
        if "DummyClassifier" not in code and "baseline" not in code.lower():
            issues.append({
                "severity": "suggestion",
                "category": "Methodology",
                "title": "No baseline model",
                "description": "A complex model is used without any baseline comparison",
                "fix": "Add a DummyClassifier to compare against your model"
            })

    # 6. No cross-validation
    if "cross_val" not in code and has_split:
        issues.append({
            "severity": "suggestion",
            "category": "Methodology",
            "title": "No cross-validation",
            "description": "Model is evaluated on a single train/test split only",
            "fix": "Use cross_val_score() for more reliable evaluation"
        })

    # 7. Accuracy on potentially imbalanced data
    if "accuracy_score" in code and "classification_report" not in code:
        issues.append({
            "severity": "warning",
            "category": "Evaluation Issues",
            "title": "Only accuracy metric used",
            "description": "accuracy_score alone can be misleading on imbalanced datasets",
            "fix": "Add classification_report() and confusion_matrix() for full evaluation"
        })

    # Score
    critical = sum(1 for i in issues if i["severity"] == "critical")
    warning = sum(1 for i in issues if i["severity"] == "warning")
    score = max(0, 100 - (critical * 25) - (warning * 10) - (len(issues) * 3))

    summary = "Great notebook!" if not issues else f"Found {len(issues)} issue(s) — {critical} critical, {warning} warnings."

    return {"summary": summary, "score": score, "issues": issues}