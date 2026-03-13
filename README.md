AI Architecture Efficiency Analyzer - MVP

Run locally:

1. Create Python venv and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start FastAPI backend

```bash
uvicorn app:app --reload --port 8000
```

3. In another terminal start Streamlit frontend

```bash
streamlit run streamlit_app.py
```

Notes:
- The classifier includes a small local heuristic fallback if you don't provide a Gemini API key.
- To integrate Gemini, paste the prompt in `classifiers/gemini_prompt.txt` into your Gemini playground and use the example request code in `classifiers/task_classifier.py`.
