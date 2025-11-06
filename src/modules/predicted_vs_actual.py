import streamlit as st
import plotly.express as px

def render_predicted_vs_actual(df, selected_driver):
    driver_df = df[df["DriverName"] == selected_driver]

    if "Predicted Lap Time" in driver_df.columns:
        st.subheader("🤖 Predicted vs Actual Lap Time")

        fig = px.line(
            driver_df,
            x="Laps",
            y=["Lap Time", "Predicted Lap Time"],
            markers=True,
            title="Model Prediction vs Actual",
            labels={"value": "Lap Time (s)", "variable": "Type"}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)