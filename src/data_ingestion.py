import pandas as pd

def load_data(path, chunk_size=10000):
    """
    Load race lap data from CSV in chunks and concatenate.
    """
    print(f"📥 Loading data from {path}...")
    chunks = []
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        chunks.append(chunk)
    df = pd.concat(chunks, ignore_index=True)
    return df

def clean_time_columns(df):
    """
    Convert time columns to seconds and handle missing values.
    """
    time_cols = ["Lap Time", "Elapsed Time", "S1", "S2", "S3", "S1a", "S1b", "S2a", "S2b", "S3a", "S3b"]
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col], errors='coerce').dt.total_seconds()
    return df

def add_features(df):
    """
    Add lap delta, pit stop detection, and sector ratios.
    """
    df = df.sort_values(by=["Name", "Laps"])
    df["Lap Delta"] = df.groupby("Name")["Lap Time"].diff()
    df["Pit Stop"] = df["Lap Delta"] > 10  # crude threshold, tune as needed
    df["Sector Ratio"] = (df["S1"] + df["S2"] + df["S3"]) / df["Lap Time"]
    return df

def ingest_pipeline(path):
    """
    Full ingestion pipeline: load, clean, feature engineer.
    """
    print("Inside ingest_pipeline function")
    print(f"Loading data from path: {path}")
    df = load_data(path)
    # df = clean_time_columns(df)
    # df = add_features(df)
    return df