from typing import List, Optional


def _escape_latex(text: str) -> str:
    result = text
    for old, new in [
        ("\\", "\\textbackslash{}"),
        ("&", "\\&"),
        ("%", "\\%"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("$", "\\$"),
        ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
    ]:
        result = result.replace(old, new)
    return result


def table(rows: List[List[str]], escape_cells: bool = True) -> str:
    if not rows:
        return ""
    num_cols = len(rows[0])
    col_spec = "|" + "c|" * num_cols
    lines = ["\\begin{tabular}{" + col_spec + "}", "\\hline"]

    def cell_text(cell: str) -> str:
        return _escape_latex(str(cell)) if escape_cells else str(cell)

    for i, row in enumerate(rows):
        if len(row) != num_cols:
            raise ValueError(f"Row {i} has {len(row)} columns, expected {num_cols}")
        line = " & ".join(cell_text(c) for c in row) + " \\\\"
        lines.append(line)
        lines.append("\\hline")
    lines.append("\\end{tabular}")
    return "\n".join(lines)


def figure(
    image_path: str,
    width: str = "0.5\\textwidth",
    caption: str = "",
    label: str = "",
) -> str:
    lines = [
        "\\begin{figure}[htbp]",
        "\\centering",
        f"\\includegraphics[width={width}]{{{image_path}}}",
    ]
    if caption:
        lines.append(f"\\caption{{{_escape_latex(caption)}}}")
    if label:
        lines.append(f"\\label{{{label}}}")
    lines.append("\\end{figure}")
    return "\n".join(lines)


def document(
    body: str,
    title: str = "",
    author: str = "",
    packages: Optional[List[str]] = None,
) -> str:
    packages = packages or []
    lines = [
        "\\documentclass[11pt]{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[T2A]{fontenc}",
    ]
    for pkg in packages:
        lines.append(f"\\usepackage{{{pkg}}}")
    lines.append("\\begin{document}")
    if title:
        lines.append(f"\\title{{{_escape_latex(title)}}}")
        if author:
            lines.append(f"\\author{{{_escape_latex(author)}}}")
        lines.append("\\maketitle")
    lines.append("")
    lines.append(body)
    lines.append("\\end{document}")
    return "\n".join(lines)
