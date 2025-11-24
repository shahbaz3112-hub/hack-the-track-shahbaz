from src.data_ingestion import ingest_pipeline
from src.preprocessing import preprocess_pipeline
from src.modeling import prepare_model_data, train_model, predict_lap_time

input_file_path = r"input_data"
target_file_path = r"output_data\processed_race_data.csv"

# Step 1: Load and preprocess data
print("******************************* Starting Data Ingestion ******************************")
try:
    raw_df = ingest_pipeline(input_file_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

print("****************************** Starting Data Preprocessing *****************************")
try:
    clean_df = preprocess_pipeline(raw_df)
except Exception as e:
    print(f"Error during preprocessing: {e}")
    exit(1)

print("******************************Starting Modeling Pipeline ********************************")
X, y = prepare_model_data(clean_df)

if X.empty or y.empty:
    print("❌ No data available for modeling. Check preprocessing or feature selection.")
    exit()

# Step 3: Train model
model, metrics = train_model(X, y, model_type="random_forest")
print("Model trained")
# print("📊 Performance Metrics:", metrics)

# Step 4: Predict lap times
predictions = predict_lap_time(model, clean_df)
clean_df["Predicted Lap Time"] = predictions

# Calculate Lap Delta: difference from previous lap time per driver
clean_df["Lap Delta"] = clean_df.groupby("DriverName")["Lap Time"].diff()

# Step 5: Flag anomalies using dynamic threshold
error = abs(clean_df["Lap Time"] - clean_df["Predicted Lap Time"])
threshold = error.mean() + 2 * error.std()
clean_df["AnomalyFlag"] = error > threshold

print("******************************Loading data for dashbaord********************************")
# Step 6: Save processed data for dashboard
# Define desired columns
desired_columns = ["DriverName", "Laps", "S1", "S2", "S3", "Lap Time", "Predicted Lap Time", "Lap Delta", "Pit Stop", "AnomalyFlag"]
# Filter only those that exist in the dataframe
columns_to_keep = [col for col in desired_columns if col in clean_df.columns]
# Save safely
clean_df[columns_to_keep].to_csv(target_file_path, index=False)
print(f"📁 Processed data saved to {target_file_path}")