import pandas as pd
from utils.transform import validate_and_clean_patient


def test_cleaning_names():
    df = pd.DataFrame({
        "FIRST": ["Damon455", "Thi53"],
        "LAST": ["Langosh790", "Wunsch504"],
        "GENDER": ["m", "f"]
    })

    result = validate_and_clean_patient(df)

    assert result["FIRST"].iloc[0] == "Damon"
    assert result["FIRST"].iloc[1] == "Thi"
    assert result["GENDER"].iloc[0] == "M"