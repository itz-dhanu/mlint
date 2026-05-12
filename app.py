import gradio as gr
from parser import extract_code_from_notebook, get_notebook_summary
from auditor import audit_notebook
import tempfile
import os

SEVERITY_EMOJI = {
    "critical": "🔴",
    "warning": "🟡",
    "suggestion": "🟢"
}

def get_score_label(score: int) -> str:
    if score >= 85:
        return "✅ Great notebook!"
    elif score >= 60:
        return "⚠️ Needs some fixes"
    else:
        return "❌ Serious issues found"

def format_report(audit: dict, summary: dict) -> str:
    lines = []

    # Header
    score = audit.get("score", 0)
    lines.append(f"## 📊 MLint Audit Report\n")
    lines.append(f"**Notebook Summary:** {summary['code_cells']} code cells | {summary['markdown_cells']} markdown cells | Kernel: {summary['kernel']}\n")
    lines.append(f"### Score: {score}/100 — {get_score_label(score)}\n")
    lines.append(f"**Overall:** {audit.get('summary', '')}\n")
    lines.append("---\n")

    # Issues
    issues = audit.get("issues", [])
    if not issues:
        lines.append("🎉 No issues found! Your notebook looks clean.")
        return "\n".join(lines)

    # Group by severity
    for severity in ["critical", "warning", "suggestion"]:
        group = [i for i in issues if i.get("severity") == severity]
        if not group:
            continue

        emoji = SEVERITY_EMOJI[severity]
        lines.append(f"### {emoji} {severity.upper()}S ({len(group)})\n")

        for issue in group:
            lines.append(f"**[{issue.get('category', '')}] {issue.get('title', '')}**")
            lines.append(f"- 🔍 **Issue:** {issue.get('description', '')}")
            lines.append(f"- 🛠️ **Fix:** {issue.get('fix', '')}")
            lines.append("")

    return "\n".join(lines)


def run_audit(file):
    if file is None:
        return "⚠️ Please upload a Jupyter notebook (.ipynb) file."

    filepath = file.name

    if not filepath.endswith(".ipynb"):
        return "❌ Invalid file type. Please upload a `.ipynb` file."

    try:
        code = extract_code_from_notebook(filepath)
        summary = get_notebook_summary(filepath)

        if not code.strip():
            return "⚠️ No code cells found in this notebook."

        audit = audit_notebook(code)
        report = format_report(audit, summary)
        return report

    except Exception as e:
        return f"❌ Error during audit: {str(e)}"


# Gradio UI
with gr.Blocks(title="MLint — ML Notebook Auditor", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🔬 MLint — ML Experiment Auditor
    **Upload your Jupyter notebook and get an instant AI-powered audit.**  
    Detects data leakage, evaluation mistakes, reproducibility issues, and more.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="📁 Upload your .ipynb file",
                file_types=[".ipynb"]
            )
            audit_btn = gr.Button("🚀 Run Audit", variant="primary")

        with gr.Column(scale=2):
            output = gr.Markdown(label="Audit Report", value="Your audit report will appear here...")

    audit_btn.click(fn=run_audit, inputs=file_input, outputs=output)

    gr.Markdown("""
    ---
    **Checks:** Data Leakage | Evaluation Issues | Reproducibility | Methodology | Code Quality  
    Built with Claude API + Gradio | [GitHub](#) | [HuggingFace Spaces](#)
    """)

if __name__ == "__main__":
    app.launch(share=True)
