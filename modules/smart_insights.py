import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
from utils.insights import generate_summary

def app(df: pd.DataFrame):
    st.header("Smart Insights & Forecasting")

    # Ensure required columns are present
    required_columns = ["Month", "Revenue", "Status", "Client", "Project", "Deadline"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns: {', '.join(missing_cols)}")
        return

    # Monthly Revenue Forecast
    monthly_rev = df.groupby("Month")["Revenue"].sum().reset_index()

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    monthly_rev["Month_num"] = monthly_rev["Month"].apply(lambda x: month_order.index(x) if x in month_order else -1)
    monthly_rev = monthly_rev[monthly_rev["Month_num"] >= 0].sort_values("Month_num")

    if monthly_rev.empty:
        st.warning("No valid monthly revenue data available.")
        return

    X = monthly_rev["Month_num"].values.reshape(-1, 1)
    y = monthly_rev["Revenue"].values

    try:
        model = LinearRegression()
        model.fit(X, y)

        future_months = np.array(range(monthly_rev["Month_num"].max() + 1,
                                       monthly_rev["Month_num"].max() + 4)).reshape(-1, 1)
        forecast = model.predict(future_months)
        forecast_months = [month_order[i % 12] for i in future_months.flatten()]

        forecast_df = pd.DataFrame({
            "Month": forecast_months,
            "Forecasted Revenue": forecast
        })

        fig = px.line(monthly_rev, x="Month", y="Revenue", title="Monthly Revenue with Forecast", markers=True,
                      template="plotly_dark")  # Change to "plotly_white" if using light mode
        fig.add_scatter(x=forecast_df["Month"], y=forecast_df["Forecasted Revenue"],
                        mode='lines+markers', name="Forecast")

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error in forecasting: {e}")

    # Insights Summary
    st.subheader("Insights Summary")
    try:
        summary = generate_summary(df)  # Corrected: pass df
        st.markdown(summary)
    except Exception as e:
        st.error(f"Error generating insights: {e}")

    # Critical Projects Alert
    st.subheader("Critical Projects Alert")
    try:
        critical_projects = df[df["Status"].str.lower() == "critical"]
        if critical_projects.empty:
            st.write("No critical projects at the moment.")
        else:
            st.dataframe(critical_projects[["Client", "Project", "Status", "Deadline"]])
    except Exception as e:
        st.error(f"Error displaying critical projects: {e}")
