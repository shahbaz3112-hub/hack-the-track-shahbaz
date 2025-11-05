import pandas as pd
import json

# Time columns to convert
TIME_COLUMNS = [
    "Lap Time", "Elapsed Time", "S1", "S2", "S3",
    "S1a", "S1b", "S2a", "S2b", "S3a", "S3b"
]

def convert_to_seconds(time_str):
    """
    Convert time string like '2:13.572' to float seconds.
    """
    try:
        if ":" in time_str:
            minutes, seconds = time_str.split(":")
            return float(minutes) * 60 + float(seconds)
        else:
            return float(time_str)
    except:
        return pd.NA


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
    # Replace placeholders
    df.replace(["--", "N/A", "NaN", ""], pd.NA, inplace=True)

    # Convert time strings to seconds
    for col in ["S1", "S2", "S3", "Lap Time"]:
        df[col] = df[col].apply(convert_to_seconds)

    # Create 'DriverName' column
    df["DriverName"] = df["FirstName"].fillna("") + " " + df["LastName"].fillna("")
    
    # Drop rows missing key features
    df = df.dropna(subset=["S1", "S2", "S3", "Lap Time"])
     # Add lap counter per driver
    df["Laps"] = df.groupby("DriverName").cumcount() + 1
    # Create synthetic Pit Stop flag based on Lap Time spikes or missing sectors
    df["Pit Stop"] = df.apply(
    lambda row: (
        pd.isna(row["S1"]) or pd.isna(row["S2"]) or pd.isna(row["S3"]) or row["Lap Time"] > 100
        ),
        axis=1
    )

    return df
