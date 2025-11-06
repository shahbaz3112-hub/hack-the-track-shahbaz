import streamlit as st

def render_pit_stop_detection(df, selected_driver):
    st.subheader("🛠️ Pit Stop Detection")

    driver_df = df[df["DriverName"] == selected_driver]
    pit_laps = driver_df[driver_df["Pit Stop"] == True]["Laps"].tolist()

    if pit_laps:
        st.info(f"Pit stops detected on laps: {pit_laps}")
    else:
        st.success("No pit stops detected for this driver.")