import pandas as pd

"""
    Cleans and standardizes patient data for downstream ETL processing.

    Steps:
    - Handles missing values
    - Standardizes text fields
    - Removes invalid characters from names
    - Normalizes categorical values

    Returns a cleaned copy of the DataFrame.
"""

def validate_and_clean_patient(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # -----------------------------
    # Missing value handling
    # -----------------------------
    df["DEATHDATE"] = df["DEATHDATE"].fillna(pd.NA)
    df["PASSPORT"] = df["PASSPORT"].fillna("UNKNOWN")
    df["DRIVERS"] = df["DRIVERS"].fillna("UNKNOWN")

    # -----------------------------
    # String normalization
    # -----------------------------
    df["FIRST"] = (
        df["FIRST"]
        .astype("string")
        .str.replace(r"\d+", "", regex=True)
        .str.strip()
    )

    df["LAST"] = (
        df["LAST"]
        .astype("string")
        .str.replace(r"\d+", "", regex=True)
        .str.strip()
    )

    # -----------------------------
    # Standardize categorical values
    # -----------------------------
    df["GENDER"] = (
        df["GENDER"]
        .astype("string")
        .str.upper()
        .fillna("UNKNOWN")
    )

    # -----------------------------
    # Optional: basic data quality flags
    # -----------------------------
    df["HAS_INVALID_NAME"] = (
        df["FIRST"].str.contains(r"\d", na=False) |
        df["LAST"].str.contains(r"\d", na=False)
    )

    return df