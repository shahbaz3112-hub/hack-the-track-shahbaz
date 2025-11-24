import streamlit as st
import pandas as pd

# Import modular dashboard components
from modules.lap_time_trend import render_lap_time_trend
from modules.sector_performance import render_sector_performance
from modules.pit_stop_detection import render_pit_stop_detection
from modules.predicted_vs_actual import render_predicted_vs_actual
from modules.anomaly_detection import render_anomaly_detection
from modules.driver_comparison import render_driver_comparison

def load_data(path):
    """Load processed race data with predictions."""
    return pd.read_csv(path)

def main():
    st.set_page_config(page_title="RaceIQ Dashboard", layout="wide")
    st.title("🏎️ RaceIQ: Racing Post-Analysis Dashboard")

    file_path = r"output_data/processed_race_data.csv"
    df = load_data(file_path)

    # Sidebar filters
    st.sidebar.header("🔍 Filter Drivers")
    drivers = df["DriverName"].dropna().unique()
    selected_driver = st.sidebar.selectbox("Select Driver", sorted(drivers))

    # Tabbed layout
    tabs = st.tabs([
        "Lap Time Trend",
        "Sector Performance",
        "Pit Stop Detection",
        "Predicted vs Actual",
        "Anomaly Detection",
        "Driver Comparison",
        "Export Data"
    ])

    with tabs[0]:
        render_lap_time_trend(df, selected_driver)

    with tabs[1]:
        render_sector_performance(df, selected_driver)

    with tabs[2]:
        render_pit_stop_detection(df, selected_driver)

    with tabs[3]:
        render_predicted_vs_actual(df, selected_driver)

    with tabs[4]:
        render_anomaly_detection(df, selected_driver)

    with tabs[5]:
        render_driver_comparison(df)
    with tabs[6]:
        st.subheader("📤 Export Driver Data")
        export_df = df[df["DriverName"] == selected_driver]

        # 📊 Summary KPIs
        st.markdown("### 📊 Summary Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Laps", export_df["Laps"].nunique())
        col2.metric("Avg Lap Time (s)", f"{export_df['Lap Time'].mean():.2f}")
        col3.metric("Fastest Lap (s)", f"{export_df['Lap Time'].min():.2f}")

        col4, col5 = st.columns(2)
        col4.metric("Pit Stops", export_df["Pit Stop"].sum())
        col5.metric("Anomalies", export_df["AnomalyFlag"].sum())

        # 🧾 Preview and Download for selected driver
        st.markdown("### 🧾 Driver Data Preview")
        st.dataframe(export_df.head(10))

        csv_driver = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Driver CSV",
            data=csv_driver,
            file_name=f"{selected_driver}_race_data.csv",
            mime="text/csv"
        )

        # 🧑‍🤝‍🧑 Comparison Data Export
        st.markdown("### 🧑‍🤝‍🧑 Export Comparison Data")
        st.info("Select multiple drivers in the Driver Comparison tab to enable this export.")

        # Check if multiple drivers were selected in comparison module
        comparison_drivers = st.multiselect(
            "Select Drivers for Comparison Export",
            options=sorted(df["DriverName"].dropna().unique()),
            default=[]
        )

        if len(comparison_drivers) >= 2:
            compare_df = df[df["DriverName"].isin(comparison_drivers)]
            st.dataframe(compare_df.head(10))

            csv_compare = compare_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Comparison CSV",
                data=csv_compare,
                file_name="driver_comparison_data.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()