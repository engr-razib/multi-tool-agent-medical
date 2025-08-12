
# Backend README

- Convert your CSVs: put CSVs into backend/data/ and run `python backend/db_scripts/csv_to_sqlite.py`.
- Start app: `uvicorn backend.app.main:app --reload --port 8000`
- Endpoint: POST /ask with JSON {"text": "your question"}
