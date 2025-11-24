# 🏎️ RaceIQ: Racing Event Post-Analysis Platform

## 📌 Project Overview
RaceIQ is a data engineering and analytics solution designed to deliver pre-analysis of racing events.  
It combines historical race data, predictive modeling, and an interactive dashboard to help uncover patterns, optimize pit strategies, and forecast lap times.

## ⚙️ Tech Stack

- **Languages**: Python (Pandas, NumPy, PySpark)
- **Visualization**: Streamlit, Plotly
- **Modeling**: Scikit-learn, RandomForest
- **Orchestration**: Apache Airflow (optional)
- **Version Control**: GitHub

## 🧱 Project Structure

```bash
racing-dashboard/
│
├── data/                      # Raw and processed datasets
├── notebooks/                 # EDA and prototyping
├── src/                       # Core modules
│   ├── data_ingestion.py      # Load and chunk large CSVs
│   ├── preprocessing.py       # Clean, transform, and engineer features
│   ├── modeling.py            # Train and evaluate lap time prediction models
│   └── dashboard.py           # Streamlit dashboard app
│
├── dags/                      # Airflow DAGs (optional)
│   └── racing_pipeline.py
│
├── main.py                    # Runner script
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation
```
## 🚀 Getting Started

To set up the project locally:

```bash
# Step 1: Clone the Repo
git clone https://github.com/shahbaz3112-hub/hack-the-track-shahbaz.git
cd hack-the-track-shahbaz

#Step 2: Setup Environment & Install dependencies
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# Step 3: Run the main script
python main.py

# Step 4: Launch the Dashboard:
streamlit run src/dashboard.py
```

## 📊 Dashboard Features
- **Lap Time Trends**: Visualize lap-by-lap performance for each driver
- **Sector Analysis**: Compare S1, S2, S3 times across laps
- **Pit Stop Detection**: Flag laps with missing sectors or unusually long lap times
- **Predicted vs Actual Lap Time**: Overlay model predictions and compute prediction error
- **Lap Delta Tracking**: Show lap-to-lap time differences to highlight performance shifts
- **Anomaly Detection**: Identify outlier laps using dynamic thresholds and prediction deviation
- **Driver Filtering**: Select individual drivers to explore personalized lap insights
- **Fastest Lap Highlighting**: Automatically detect and mark each driver's fastest lap

## 🧠 What's Next

- Add driver-to-driver comparison view
- Visualize anomaly categories (e.g., pit stop, prediction miss)
- Export driver reports as PDF
- Integrate telemetry data for richer insights