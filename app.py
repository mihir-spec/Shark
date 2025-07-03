"""Main entry‑point for Shark HQ dashboard."""
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="Shark HQ",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent / "data"

@st.cache_data(ttl=3600)
def load_overview() -> pd.DataFrame:
    import os
    if "DB_URI" in st.secrets:
        from sqlalchemy import create_engine
        engine = create_engine(st.secrets["DB_URI"])
        query = """
            SELECT date, channel, revenue, orders, gross_margin
            FROM fact_sales_daily
            WHERE date >= CURRENT_DATE - INTERVAL '12 months'
        """
        df = pd.read_sql(query, engine)
    else:
        df = pd.read_csv(DATA_DIR / "sales_overview.csv", parse_dates=["date"])
    return df

df = load_overview()

st.sidebar.header("Filters")
period = st.sidebar.selectbox("Period", ["30 D", "90 D", "12 M"], index=0)
channel = st.sidebar.multiselect(
    "Channel",
    options=sorted(df["channel"].unique()),
    default=list(df["channel"].unique()),
)

days_lookup = {"30 D": 30, "90 D": 90, "12 M": 365}
cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=days_lookup[period])

mask = (df["date"] >= cutoff) & (df["channel"].isin(channel))
df_f = df.loc[mask]

col1, col2, col3 = st.columns(3, gap="large")
col1.metric("Revenue", f"AED {df_f['revenue'].sum():,.0f}")
col2.metric("Orders", int(df_f['orders'].sum()))
margin_pct = (df_f['gross_margin'].sum() / max(df_f['revenue'].sum(), 1)) * 100
col3.metric("Gross Margin %", f"{margin_pct:.1f}%")

st.markdown("### Revenue trend")
st.line_chart(df_f.groupby("date")["revenue"].sum())

st.markdown("### Channel split (last 30 days)")
last30 = df_f[df_f["date"] >= pd.Timestamp.today().normalize() - pd.Timedelta(days=30)]
st.bar_chart(last30.groupby("channel")["revenue"].sum())

st.caption(f"Data as of {date.today().strftime('%d %b %Y')}")
