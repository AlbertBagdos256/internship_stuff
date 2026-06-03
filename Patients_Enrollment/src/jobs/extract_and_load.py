import pandas as pd
from src.utils import get_engine, load_sql, validate_and_clean_patient, get_logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SQL_PATH = BASE_DIR / "sql_queries" / "extracting_patients.sql"

engine = get_engine()
logger = get_logger(__name__)

def run_pipeline(query_path: str, filename: str, data_type: str) -> None:
    logger.info("Starting pipeline")
    query = load_sql(SQL_PATH)

    chunks = pd.read_sql(
        query,
        engine,
        chunksize = 5000
    )

    for i, chunk in enumerate(chunks):
        # validation 
        if data_type == "patient":
            chunk = validate_and_clean_patient(chunk)
        logger.info(f"Chunk {i} processed successfully | Rows={len(chunk)}")
        chunk.to_csv(
            filename,
            mode="a", # appending chunks to the existing file
            header = (i == 0),  # only write header once
            index=False
        )





if __name__ == "__main__":
    run_pipeline("../sql_queries/extracting.sql", "patients.csv", "patient")