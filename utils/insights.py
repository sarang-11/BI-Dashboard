from utils.data_loader import load_data

# utils/insights.py

def generate_summary(df):
    # generate your insights summary from df
    total_revenue = df["Revenue"].sum()
    avg_csat = df["CSAT"].mean()
    total_tickets = df["Tickets"].sum()
    avg_resolution = df["Resolution Time (hrs)"].mean()

    summary = f"""
    - **Total Revenue**: ${total_revenue:,.0f}
    - **Average CSAT**: {avg_csat:.1f}/100
    - **Total Tickets**: {total_tickets}
    - **Avg. Resolution Time**: {avg_resolution:.1f} hours
    """
    return summary
'''
- We are actively serving **{total_clients} clients**.
- **{top_client}** is the top revenue-generating client.
- Avg. CSAT score: **{avg_csat:.1f}/100**
- **{delayed_projects} project(s)** are delayed and require attention.
'''