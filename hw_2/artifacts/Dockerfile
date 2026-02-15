FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-lang-cyrillic \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir latex-gen-hw==0.1.0

WORKDIR /app

COPY example_table.py generate_pdf.py ./
COPY artifacts/image.png ./artifacts/

CMD python example_table.py && python generate_pdf.py
