# 🔬 MLint — ML Experiment Auditor

> Upload your Jupyter notebook and instantly detect ML bad practices — data leakage, wrong evaluation, reproducibility issues, and more.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Gradio](https://img.shields.io/badge/Built%20with-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Live Demo
👉 [Try it on HuggingFace Spaces](https://huggingface.co/spaces/itz-dhanu/mlint)

---

## 💡 What is MLint?

MLint is a free, open-source tool that audits your Jupyter notebooks for common ML mistakes that beginners and even intermediate practitioners often miss.

No API key needed. No internet required. Runs fully offline.

---

## 🔍 What It Detects

| Severity | Category | Example |
|---|---|---|
| 🔴 Critical | Data Leakage | Scaler fitted before train_test_split |
| 🔴 Critical | Evaluation Issues | Model tested on training data |
| 🟡 Warning | Reproducibility | Missing random_state |
| 🟡 Warning | Evaluation Issues | Only accuracy used, no classification report |
| 🟡 Warning | Code Quality | Hardcoded file paths |
| 🟢 Suggestion | Methodology | No baseline model |
| 🟢 Suggestion | Methodology | No cross-validation |

---

## 🛠️ Setup & Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/mlint.git
cd mlint
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

**4. Open browser**
```
http://127.0.0.1:7860
```

---

## 🧪 Test It

Upload the included `sample_notebook.ipynb` — it contains intentional mistakes:
- ❌ Data leakage (scaler fitted before split)
- ❌ Model evaluated on training data
- ❌ Missing random_state
- ❌ Hardcoded file path
- ❌ No baseline model
- ❌ Accuracy-only evaluation

MLint catches all of them.

---

## 📁 Project Structure

```
mlint/
├── app.py                  # Gradio UI
├── parser.py               # Jupyter notebook parser
├── auditor.py              # Rule-based ML audit engine
├── requirements.txt        # Dependencies
├── sample_notebook.ipynb   # Test notebook with intentional mistakes
└── README.md
```

---

## 📦 Dependencies

```
gradio
nbformat
```

No LLM API needed. Fully rule-based and offline.

---

## 👤 Author

**Dhanusree**  
AI/ML Student | Pharmacovigilance + NLP  
[LinkedIn](#) | [HuggingFace](#)

---

## ⭐ If this helped you, give it a star!
