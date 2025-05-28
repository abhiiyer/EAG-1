import streamlit as st
import pandas as pd
from pathlib import Path

CSV_PATH = Path("output/submitted_leads.csv")

st.set_page_config(page_title="HNI Lead Dashboard", layout="wide")
st.title("📊 HNI Lead Dashboard")

if not CSV_PATH.exists():
    st.warning("No leads submitted yet.")
    st.stop()

# Load data
df = pd.read_csv(CSV_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Drop exact duplicates (same name, company, city, trigger, source), keep latest timestamp
dedup_cols = ["name", "company", "city", "trigger", "source"]
df = df.sort_values("timestamp").drop_duplicates(subset=dedup_cols, keep="last")


# Filters
with st.sidebar:
    st.header("🔍 Filter Leads")
    cities = st.multiselect("City", sorted(df["city"].unique()), default=df["city"].unique())
    sources = st.multiselect("Lead Source", sorted(df["source"].unique()), default=df["source"].unique())

data_sources = st.multiselect("Data Source", sorted(df["data_source"].unique()), default=df["data_source"].unique())
#contact_filter = st.selectbox("Has Contact Info?", ["Both", "Yes", "No"])



# Apply filters
#filtered_df = df[df["city"].isin(cities) & df["source"].isin(sources)]
filtered_df = df[
    (df["city"].isin(cities)) &
    (df["source"].isin(sources)) &
    (df["data_source"].isin(data_sources))
]


#if contact_filter == "Yes":
#    filtered_df = filtered_df[filtered_df["has_contact"].astype(str).str.lower() == "true"]
#elif contact_filter == "No":
#    filtered_df = filtered_df[filtered_df["has_contact"].astype(str).str.lower() == "false"]

# Show data
st.write(f"### Showing {len(filtered_df)} lead(s)")
st.dataframe(filtered_df, use_container_width=True)

# Download
st.download_button("📥 Download Filtered Leads as CSV",
                   data=filtered_df.to_csv(index=False),
                   file_name="filtered_hni_leads.csv",
                   mime="text/csv")
