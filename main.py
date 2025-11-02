from src.data_ingestion import ingest_pipeline
from src.preprocessing import preprocess_pipeline

file_path = "D:\Hackathon\HackTheTrack\Dataset\race_data\Qualifying1-6-Laps.csv"
ingest_pipeline(file_path)
print("*** Starting Data Ingestion ***")
try:
    raw_df = ingest_pipeline(file_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

print("*** Starting Data Preprocessing ***")
try:
    clean_df = preprocess_pipeline(raw_df)
except Exception as e:
    print(f"Error during preprocessing: {e}")
    exit(1)