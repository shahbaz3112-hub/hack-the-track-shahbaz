import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(path):
    """
    Load processed race data with predictions.
    """
    return pd.read_csv(path)

def main():
    st.set_page_config(page_title="RaceIQ Dashboard", layout="wide")
    st.title("🏎️ RaceIQ: Racing Pre-Analysis Dashboard")
    file_path = r"data\processed_race_data.csv"
    df = load_data(file_path)

    # Sidebar filters
    st.sidebar.header("🔍 Filter Drivers")
    drivers = df["DriverName"].dropna().unique()
    selected_driver = st.sidebar.selectbox("Select Driver", sorted(drivers))

    driver_df = df[df["DriverName"] == selected_driver]

    # Lap Time Trend
    st.subheader(f"📈 Lap Time Trend for {selected_driver}")
    fig = px.line(driver_df, x="Laps", y="Lap Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Sector Breakdown
    st.subheader("📊 Sector Performance")
    sector_fig = px.bar(
        driver_df,
        x="Laps",
        y=["S1", "S2", "S3"],
        title="Sector Times per Lap",
        labels={"value": "Time (s)", "variable": "Sector"}
    )
    st.plotly_chart(sector_fig, use_container_width=True)

    # Pit Stop Detection
    st.subheader("🛠️ Pit Stop Detection")
    pit_laps = driver_df[driver_df["Pit Stop"] == True]["Laps"].tolist()
    if pit_laps:
        st.info(f"Pit stops detected on laps: {pit_laps}")
    else:
        st.success("No pit stops detected for this driver.")

    # Predicted vs Actual Lap Time
    if "Predicted Lap Time" in driver_df.columns:
        st.subheader("🤖 Predicted vs Actual Lap Time")
        pred_fig = px.line(
            driver_df,
            x="Laps",
            y=["Lap Time", "Predicted Lap Time"],
            markers=True,
            title="Model Prediction vs Actual"
        )
        st.plotly_chart(pred_fig, use_container_width=True)

    # Anomaly Flag
    st.subheader("⚠️ Anomaly Detection")
    anomalies = driver_df[driver_df["AnomalyFlag"] == True]
    st.write(anomalies[["Laps", "Lap Time", "Lap Delta"]])

if __name__ == "__main__":
    main()