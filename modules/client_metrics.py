import streamlit as st
import plotly.express as px
import pandas as pd

def app(df: pd.DataFrame):
    st.header("Client Metrics")

    # Filters
    clients = df["Client"].unique().tolist()
    services = df["Service"].unique().tolist()
    months = df["Month"].unique().tolist()
    statuses = df["Status"].unique().tolist()

    selected_clients = st.multiselect("Select Clients", clients, default=clients)
    selected_services = st.multiselect("Select Services", services, default=services)
    selected_months = st.multiselect("Select Months", months, default=months)
    selected_statuses = st.multiselect("Select Statuses", statuses, default=statuses)

    # Filter dataframe
    filtered_df = df[
        (df["Client"].isin(selected_clients)) &
        (df["Service"].isin(selected_services)) &
        (df["Month"].isin(selected_months)) &
        (df["Status"].isin(selected_statuses))
    ]

    # KPIs
    total_revenue = filtered_df["Revenue"].sum()
    avg_csat = filtered_df["CSAT"].mean()
    total_tickets = filtered_df["Tickets"].sum()
    avg_resolution = filtered_df["Resolution Time (hrs)"].mean()

    # Use of custom CSS class for metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.0f}", delta=None, help="Total revenue from selected clients and services.")
    col2.metric("Average CSAT", f"{avg_csat:.1f}", delta=None, help="Customer Satisfaction score based on the selected filters.")
    col3.metric("Total Tickets", f"{total_tickets}", delta=None, help="Total tickets reported for the selected filters.")
    col4.metric("Avg. Resolution Time (hrs)", f"{avg_resolution:.1f}", delta=None, help="Average time taken to resolve issues.")

    # Dynamic Summary Insights
    st.subheader("Summary Insights")
    insights = f'''
    <div class="insight-card">
        <h4>Total Revenue</h4>
        <p>${total_revenue:,.0f}</p>
    </div>
    <div class="insight-card">
        <h4>Average CSAT</h4>
        <p>{avg_csat:.1f}/100</p>
    </div>
    <div class="insight-card">
        <h4>Total Tickets</h4>
        <p>{total_tickets}</p>
    </div>
    <div class="insight-card">
        <h4>Avg. Resolution Time</h4>
        <p>{avg_resolution:.1f} hours</p>
    </div>
    '''
    st.markdown(insights, unsafe_allow_html=True)

    # Monthly Revenue Trend
    monthly_revenue = filtered_df.groupby("Month")["Revenue"].sum().reset_index()
    fig1 = px.line(monthly_revenue, x="Month", y="Revenue", title="Monthly Revenue Trend", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Ticket Status Breakdown Pie Chart
    status_counts = filtered_df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig2 = px.pie(status_counts, values="Count", names="Status", title="Ticket Status Breakdown")
    st.plotly_chart(fig2, use_container_width=True)

    # CSAT Distribution Histogram
    fig3 = px.histogram(filtered_df, x="CSAT", nbins=20, title="CSAT Score Distribution")
    st.plotly_chart(fig3, use_container_width=True)

    # Revenue by Client Bar Chart
    revenue_client = filtered_df.groupby("Client")["Revenue"].sum().reset_index()
    fig4 = px.bar(revenue_client, x="Client", y="Revenue", title="Revenue by Client")
    st.plotly_chart(fig4, use_container_width=True)

    # Export filtered data
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download Filtered Data as CSV", data=csv, file_name="filtered_client_metrics.csv", mime="text/csv")
