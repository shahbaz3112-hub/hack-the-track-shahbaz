import streamlit as st

def render_anomaly_detection(df, selected_driver):
    st.subheader("⚠️ Anomaly Detection")

    driver_df = df[df["DriverName"] == selected_driver]
    anomalies = driver_df[driver_df["AnomalyFlag"] == True]

    if anomalies.empty:
        st.success("No anomalies detected for this driver.")
    else:
        st.write("Anomalous laps based on Lap Delta threshold:")
        st.dataframe(anomalies[["Laps", "Lap Time", "Lap Delta"]])