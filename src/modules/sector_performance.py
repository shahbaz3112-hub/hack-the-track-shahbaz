import streamlit as st
import plotly.express as px

def render_sector_performance(df, selected_driver):
    st.subheader("📊 Sector Performance")

    driver_df = df[df["DriverName"] == selected_driver]

    fig = px.bar(
        driver_df,
        x="Laps",
        y=["S1", "S2", "S3"],
        title="Sector Times per Lap",
        labels={"value": "Time (s)", "variable": "Sector"}
    )
    fig.update_layout(barmode="stack", height=400)
    st.plotly_chart(fig, use_container_width=True)