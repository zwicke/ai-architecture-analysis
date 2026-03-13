import pandas as pd
from typing import IO

REQUIRED_COLS = {"timestamp","model","prompt","input_tokens","output_tokens","latency","request_id"}


def load_and_validate_csv(file: IO):
    df = pd.read_csv(file)
    cols = set(df.columns.map(str))
    missing = REQUIRED_COLS - cols
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    # ensure numeric columns
    df["input_tokens"] = pd.to_numeric(df.get("input_tokens", 0)).fillna(0).astype(int)
    df["output_tokens"] = pd.to_numeric(df.get("output_tokens", 0)).fillna(0).astype(int)
    df["retry_count"] = pd.to_numeric(df.get("retry_count", 0)).fillna(0).astype(int)
    return df
