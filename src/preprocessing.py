import pandas as pd
import json

# Time columns to convert
TIME_COLUMNS = [
    "Lap Time", "Elapsed Time", "S1", "S2", "S3",
    "S1a", "S1b", "S2a", "S2b", "S3a", "S3b"
]

def convert_time_to_seconds(df, cols):
    """
    Convert time strings (e.g., '01:02.8') to seconds.
    Handles '--' and missing values.
    """
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col].replace("--", pd.NA), errors='coerce').dt.total_seconds()
    return df

def engineer_features(df):
    """
    Add derived features: lap delta, pit stop flag, sector ratio, subsector variability.
    """
    df["Laps"] = pd.to_numeric(df["Laps"], errors='coerce')
    df = df.sort_values(by=["Name", "Laps"])
    df["Lap Delta"] = df.groupby("Name")["Lap Time"].diff()
    df["Pit Stop"] = df["Lap Delta"] > 10  # crude threshold
    df["Sector Ratio"] = (df["S1"] + df["S2"] + df["S3"]) / df["Lap Time"]
    df["Subsector StdDev"] = df[["S1a", "S1b", "S2a", "S2b", "S3a", "S3b"]].std(axis=1)
    df["AnomalyFlag"] = df["Lap Delta"] > df["Lap Delta"].quantile(0.95)
    return df

def parse_json_column(df, col):
    """
    Extract driver name from nested JSON in 'drivers' column.
    """
    def extract_driver_name(val):
        try:
            data = json.loads(val)
            return data.get("", {}).get("driverName", None)
        except Exception:
            return None
    df["DriverName"] = df[col].apply(extract_driver_name)
    return df

def normalize_metadata(df):
    """
    Clean and standardize metadata columns.
    """
    if "Class" in df.columns:
        df["Class"] = df["Class"].str.strip().str.upper()
    if "Flag" in df.columns:
        df["Flag"] = df["Flag"].str.strip().str.title()
    return df

def fallback_driver_name(df):
    """
    Fill missing DriverName using FirstName + LastName.
    """
    if "DriverName" in df.columns and "FirstName" in df.columns and "LastName" in df.columns:
        df["DriverName"] = df["DriverName"].fillna(df["FirstName"] + " " + df["LastName"])
    return df

def drop_unused_columns(df):
    """
    Drop columns like Additional1–Additional8 if mostly empty.
    """
    drop_cols = [col for col in df.columns if "Additional" in col]
    df.drop(columns=drop_cols, inplace=True, errors='ignore')
    return df

def preprocess_pipeline(df):
    """
    Full preprocessing pipeline.
    """
    df = convert_time_to_seconds(df, TIME_COLUMNS)
    df = engineer_features(df)
    if "drivers" in df.columns:
        df = parse_json_column(df, "drivers")
    df = fallback_driver_name(df)
    df = normalize_metadata(df)
    df = drop_unused_columns(df)
    return df