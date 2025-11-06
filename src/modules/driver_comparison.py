import streamlit as st
import plotly.express as px

def render_driver_comparison(df):
    st.subheader("🧑‍🤝‍🧑 Driver Comparison")

    drivers = df["DriverName"].dropna().unique()
    selected_drivers = st.multiselect(
        "Select Drivers to Compare",
        options=sorted(drivers),
        default=sorted(drivers)[:2]
    )

    if selected_drivers:
        compare_df = df[df["DriverName"].isin(selected_drivers)]
        lap_min, lap_max = int(compare_df["Laps"].min()), int(compare_df["Laps"].max())
        lap_range = st.slider("Select Lap Range", lap_min, lap_max, (lap_min, lap_max))
        compare_df = compare_df[compare_df["Laps"].between(*lap_range)]

        fig = px.line(
            compare_df,
            x="Laps",
            y="Lap Time",
            color="DriverName",
            markers=True,
            title="Lap Time Comparison Across Drivers",
            labels={"Laps": "Lap Number", "Lap Time": "Lap Time (s)", "DriverName": "Driver"}
        )
        fig.update_layout(legend_title_text="Driver", height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one driver to compare.")