from pathlib import Path

from latex_gen import document, table


def main() -> None:
    data = [
        ["Тема", "Баллы", "Статус"],
        ["Таблицы в LaTeX", "10", "Сдано"],
        ["Рисунки в LaTeX", "10", "Сдано"],
        ["Итого", "20", "---"],
    ]
    table_tex = table(data)
    full_doc = document(table_tex, title="Пример таблицы", author="python_hws")
    out_path = Path(__file__).parent / "artifacts" / "example.tex"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_doc, encoding="utf-8")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
