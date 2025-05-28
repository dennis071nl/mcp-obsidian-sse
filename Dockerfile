# Use Python 3.12 for compliance met pyproject.toml
FROM python:3.12-slim

# Werkomgeving
WORKDIR /app

# Kopieer alle bestanden van de repo
COPY . .

# Installeer package in editable mode
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -e .

# Expose poort voor SSE/commands
EXPOSE 8000

# Start de server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
