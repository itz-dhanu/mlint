import nbformat

def extract_code_from_notebook(filepath: str) -> str:
    """
    Reads a .ipynb file and extracts all code cells as a single string.
    Each cell is numbered for reference in the audit report.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    code_cells = []
    cell_number = 1

    for cell in notebook.cells:
        if cell.cell_type == "code":
            source = cell.source.strip()
            if source:  # skip empty cells
                code_cells.append(f"# --- Cell {cell_number} ---\n{source}")
                cell_number += 1

    full_code = "\n\n".join(code_cells)
    return full_code


def get_notebook_summary(filepath: str) -> dict:
    """
    Returns a quick summary of the notebook structure.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    total_cells = len(notebook.cells)
    code_cells = [c for c in notebook.cells if c.cell_type == "code" and c.source.strip()]
    markdown_cells = [c for c in notebook.cells if c.cell_type == "markdown"]

    return {
        "total_cells": total_cells,
        "code_cells": len(code_cells),
        "markdown_cells": len(markdown_cells),
        "kernel": notebook.metadata.get("kernelspec", {}).get("display_name", "Unknown")
    }
