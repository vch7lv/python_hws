import os
import shutil
import subprocess
import sys
from pathlib import Path

from latex_gen import document, figure, table


def main() -> int:
    root = Path(__file__).parent.resolve()
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    data = [
        ["Тема", "Баллы", "Статус"],
        ["Таблицы в LaTeX", "10", "Сдано"],
        ["Рисунки в LaTeX", "10", "Сдано"],
        ["Итого", "20", "---"],
    ]
    table_tex = table(data)
    fig_tex = figure("image.png", width="0.35\\textwidth", caption="Пример рисунка")
    body = table_tex + "\n\n" + fig_tex
    full_doc = document(
        body,
        title="Отчёт: таблица и рисунок",
        author="python_hws",
        packages=["graphicx"],
    )

    tex_path = artifacts / "report.tex"
    tex_path.write_text(full_doc, encoding="utf-8")

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "report.tex"],
        cwd=artifacts,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    print(f"PDF: {artifacts / 'report.pdf'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
