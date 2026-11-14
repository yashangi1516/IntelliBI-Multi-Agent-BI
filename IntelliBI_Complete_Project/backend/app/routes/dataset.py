import uuid
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.database.connection import get_connection
from app.agents.business_agents import run_all_agents

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])
BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

def read_dataset(file_path: Path, extension: str):
    if extension == ".csv":
        try:
            return pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="latin-1")
    return pd.read_excel(file_path)

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    original_name = file.filename or "dataset"
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Maximum upload size is 10 MB.")

    stored_name = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / stored_name

    try:
        file_path.write_bytes(content)
        df = read_dataset(file_path, extension)
        if df.empty or len(df.columns) == 0:
            raise ValueError("The dataset has no usable data.")
        if len(df.columns) > 100:
            raise ValueError("Dataset contains too many columns.")

        preview = df.head(10).astype(object).where(pd.notna(df.head(10)), None)
        summary = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": [str(c) for c in df.columns],
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "preview": preview.to_dict(orient="records"),
        }
        analysis = run_all_agents(df)

        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO datasets (filename, file_path) VALUES (?, ?)",
                (original_name, str(file_path))
            )
            dataset_id = cursor.lastrowid
            connection.commit()

        return {
            "success": True,
            "message": "Dataset uploaded and analyzed successfully.",
            "dataset_id": dataset_id,
            "filename": original_name,
            "summary": summary,
            "analysis": analysis,
        }
    except (ValueError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Unable to read dataset: {error}")
    except Exception as error:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Dataset processing failed: {error}")

@router.get("")
def list_datasets():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, filename, uploaded_at FROM datasets ORDER BY id DESC"
        ).fetchall()
    return {"success": True, "datasets": [dict(row) for row in rows]}

@router.get("/{dataset_id}/preview")
def get_dataset_preview(dataset_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT filename, file_path FROM datasets WHERE id = ?", (dataset_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    path = Path(row["file_path"])
    if not path.exists():
        raise HTTPException(status_code=404, detail="Stored dataset file is missing.")
    df = read_dataset(path, path.suffix.lower())
    preview = df.head(20).astype(object).where(pd.notna(df.head(20)), None)
    return {
        "success": True,
        "filename": row["filename"],
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "preview": preview.to_dict(orient="records"),
    }
