import streamlit as st
import plotly.express as px

def render_lap_time_trend(df, selected_driver):
    st.subheader(f"📈 Lap Time Trend for {selected_driver}")

    driver_df = df[df["DriverName"] == selected_driver]

    fig = px.line(
        driver_df,
        x="Laps",
        y="Lap Time",
        markers=True,
        title=f"Lap Time Trend for {selected_driver}",
        labels={"Laps": "Lap Number", "Lap Time": "Lap Time (s)"}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)