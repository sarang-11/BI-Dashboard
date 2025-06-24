import pandas as pd
import streamlit as st
import difflib
import ssl

REQUIRED_COLUMNS = {
    "Client", "Project", "Revenue", "Tickets", "CSAT",
    "Team", "Service", "Status", "Deadline", "Month", "Resolution Time (hrs)"
}

COLUMN_VARIANTS = {
    "client": ["client", "customer", "account"],
    "project": ["project", "proj", "job"],
    "revenue": ["revenue", "sales", "income", "amount"],
    "tickets": ["tickets", "issues", "cases", "requests"],
    "csat": ["csat", "customer satisfaction", "satisfaction", "score"],
    "team": ["team", "group", "department"],
    "service": ["service", "product", "offering"],
    "status": ["status", "state", "progress"],
    "deadline": ["deadline", "due date", "due", "target date"],
    "month": ["month", "period", "timeframe"],
    "resolution time (hrs)": ["resolution time (hrs)", "resolution time", "time to resolve", "resolution_hrs"]
}

def map_columns(df):
    new_columns = {}
    lowered_cols = [col.lower() for col in df.columns]

    for req_col in REQUIRED_COLUMNS:
        variants = COLUMN_VARIANTS[req_col.lower()]
        matched_col = None
        for variant in variants:
            matches = difflib.get_close_matches(variant, lowered_cols, n=1, cutoff=0.8)
            if matches:
                matched_col = df.columns[lowered_cols.index(matches[0])]
                break
        if matched_col:
            new_columns[matched_col] = req_col
        else:
            new_columns[req_col] = None

    df_renamed = df.rename(columns=new_columns)

    missing = [col for col in REQUIRED_COLUMNS if col not in df_renamed.columns or df_renamed[col].isnull().all()]
    for col in missing:
        if col in ["Revenue", "Tickets", "CSAT", "Resolution Time (hrs)"]:
            df_renamed[col] = 0
        elif col == "Deadline":
            df_renamed[col] = pd.to_datetime("2099-12-31")
        else:
            df_renamed[col] = ""

    try:
        df_renamed["Deadline"] = pd.to_datetime(df_renamed["Deadline"])
    except Exception:
        df_renamed["Deadline"] = pd.to_datetime("2099-12-31")

    for num_col in ["Revenue", "Tickets", "CSAT", "Resolution Time (hrs)"]:
        df_renamed[num_col] = pd.to_numeric(df_renamed[num_col], errors="coerce").fillna(0)

    return df_renamed

def convert_gsheet_url_to_csv(url: str) -> str:
    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    except Exception:
        return ""

def load_data():
    # Unique keys for both file_uploader and text_input
    uploaded_file = st.sidebar.file_uploader("Upload dataset (CSV, Excel)", type=["csv", "xlsx"], key="dataset_uploader")
    google_sheet_url = st.sidebar.text_input("Or paste Google Sheet URL (public/shared)", key="gsheet_url")

    df = None
    error_msg = ""

    try:
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        elif google_sheet_url:
            if "docs.google.com" in google_sheet_url:
                csv_url = convert_gsheet_url_to_csv(google_sheet_url)
                # Ensure SSL context is set to avoid certificate errors
                ssl._create_default_https_context = ssl._create_unverified_context
                df = pd.read_csv(csv_url)
            else:
                error_msg = "Invalid Google Sheet URL."
    except Exception as e:
        error_msg = f"Error loading file: {e}"

    if df is not None:
        df = map_columns(df)
    else:
        # If no file is uploaded or there's an error, use default demo data
        st.sidebar.error(error_msg or "Using default demo data.")
        df = pd.read_csv("data/mock_data.csv")
        df = map_columns(df)

    return df
