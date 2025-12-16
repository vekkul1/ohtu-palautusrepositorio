Run the web interface for the Rock Paper Scissors app.

Install dependencies with Poetry and run the server:

```bash
poetry install
poetry run uvicorn src.web:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 in your browser.
