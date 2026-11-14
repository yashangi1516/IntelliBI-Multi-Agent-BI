# IntelliBI — Multi-Agent Business Intelligence System

**Project type:** BCA Major Project  
**Frontend:** HTML, CSS, JavaScript  
**Backend:** Python, FastAPI  
**Database:** SQLite  
**Data processing:** Pandas  
**Agent architecture:** AI Orchestrator with specialist business-analysis agents

## 1. Project overview

IntelliBI is a local web application for uploading CSV and Excel business datasets. The backend validates the uploaded file, stores it, calculates data-quality statistics, previews records, and coordinates specialist agents to produce an initial business analysis.

The included agents are:
- Data Analyst Agent — dataset size, missing values, duplicates and numeric fields.
- Sales Agent — identifies likely sales/revenue measures and summarizes them.
- Financial Agent — estimates profit when revenue and cost fields are detected.
- Marketing Agent — highlights common values in a categorical field.
- Visualization Agent — identifies numeric fields suitable for charts.
- Report Agent — summarizes the agents that ran.
- Decision Agent — provides general next-step recommendations.
- AI Orchestrator — coordinates the specialist agents.

**Important:** These are rule-based demonstration agents. They are not autonomous business experts and their outputs must be checked against the meaning and quality of the source data. Gemini API integration is not claimed as completed in this build.

## 2. Requirements

- Python 3.10 or later
- VS Code (recommended)
- A modern browser

## 3. Installation on Windows

Open the IntelliBI project folder in VS Code.

### Terminal 1 — backend

```powershell
cd backend
python -m venv ..\venv
..\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If PowerShell blocks activation, run this for the current terminal only, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
..\venv\Scripts\Activate.ps1
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation: `http://127.0.0.1:8000/docs`.

### Terminal 2 — frontend

Open a second VS Code terminal:

```powershell
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` in your browser.

Keep both terminals running.

## 4. Test the application

1. On the IntelliBI page, scroll to **Analyze your dataset**.
2. Choose `frontend/sample_data/sales_data.csv`.
3. Click **Upload & analyze**.
4. Review row/column counts, missing values, duplicates, column names, preview, agent findings and recommendations.
5. Refresh the saved dataset list to see previously uploaded files.

Expected sample dataset summary: 10 rows, 9 columns, 0 missing values and 0 duplicate rows.

## 5. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend health check |
| POST | `/api/datasets/upload` | Upload and analyze CSV/Excel |
| GET | `/api/datasets` | List uploaded datasets |
| GET | `/api/datasets/{dataset_id}/preview` | Preview a stored dataset |

## 6. Storage

Uploaded source files are saved in `backend/uploads/`. SQLite database is created at `backend/database/intellibi.db`. These folders are created automatically when the application runs.

## 7. Limitations and future scope

- Agent findings use transparent, rule-based heuristics; they do not replace domain review.
- Column detection is based on common words such as `revenue`, `sales`, `cost`, and `expense`.
- The application is intended for local academic demonstration, not production deployment.
- Future improvements: Gemini integration with an API key, interactive charts, authentication, role-based access, exportable PDF reports, stronger validation, and deployment with environment-based configuration.

## 8. Academic submission checklist

Before submission:
- Run the backend and frontend on the target computer.
- Upload the sample dataset and capture screenshots of the dashboard, API docs, upload response, and agent analysis.
- Replace the student/institute details in the report template with accurate information.
- Add your own explanation of implementation, testing, results, limitations, and learning.
- Do not claim Gemini-powered responses or cloud deployment unless you implement and test them.
