import streamlit as st
import plotly.express as px
import pandas as pd

def app(df: pd.DataFrame):
    st.header("Team Performance")

    teams = df["Team"].unique().tolist()
    selected_teams = st.multiselect("Select Teams", teams, default=teams)

    filtered_df = df[df["Team"].isin(selected_teams)]

    # Radar chart data preparation
    radar_df = filtered_df.groupby("Team").agg({
        "Revenue": "sum",
        "Tickets": "sum",
        "CSAT": "mean",
        "Resolution Time (hrs)": "mean"
    }).reset_index()

    import plotly.graph_objects as go

    categories = ["Revenue", "Tickets", "CSAT", "Resolution Time (hrs)"]

    fig = go.Figure()

    for i, row in radar_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["Revenue"], row["Tickets"], row["CSAT"], row["Resolution Time (hrs)"]],
            theta=categories,
            fill='toself',
            name=row["Team"]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, radar_df[categories].max().max()*1.2]
            )
        ),
        showlegend=True,
        title="Team Performance Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)
