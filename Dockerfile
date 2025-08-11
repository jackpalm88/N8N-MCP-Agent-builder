# ── 1. Bāzes attēls ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── 2. Darba mape un kods ───────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ── 3. Vides mainīgie (ja vajag) ────────────────────────────────────────────────
ENV PYTHONPATH=/app \
    FLASK_ENV=production

# ── 4. Klausītais ports (dok. nolūkam) ─────────────────────────────────────────
EXPOSE 5000

# ── 5. Starta komanda ──────────────────────────────────────────────────────────
CMD ["python", "main.py"]


