
# Shark HQ Dashboard – robust version
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Shark HQ", page_icon="🦈", layout="wide")

DATA_DIR = (Path(__file__).resolve().parent / "data").expanduser()

@st.cache_data(ttl=3600)
def load_overview() -> pd.DataFrame:
    # Try database
    if "DB_URI" in st.secrets:
        try:
            from sqlalchemy import create_engine
            engine = create_engine(st.secrets["DB_URI"])
            q = (
                "SELECT date, channel, revenue, orders, gross_margin "
                "FROM fact_sales_daily "
                "WHERE date >= CURRENT_DATE - INTERVAL '12 months'"
            )
            return pd.read_sql(q, engine)
        except Exception as e:
            st.error(f"Database error: {e}")

    # Try CSV
    csv_path = DATA_DIR / "sales_overview.csv"
    if csv_path.exists():
        try:
            return pd.read_csv(csv_path, parse_dates=["date"])
        except Exception as e:
            st.error(f"CSV read error: {e}")

    # Demo fallback
    st.warning("No data found – displaying demo figures.")
    today = pd.Timestamp.today().normalize()
    return pd.DataFrame({
        "date": pd.date_range(end=today, periods=30),
        "channel": ["Store", "E-Com"] * 15,
        "revenue": [20000] * 30,
        "orders": [150] * 30,
        "gross_margin": [8000] * 30,
    })

df = load_overview()

st.sidebar.header("Filters")
period = st.sidebar.selectbox("Period", ["30 D", "90 D", "12 M"], index=0)
channel = st.sidebar.multiselect("Channel", sorted(df["channel"].unique()), default=list(df["channel"].unique()))

cutoff_days = {"30 D": 30, "90 D": 90, "12 M": 365}[period]
cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=cutoff_days)
filtered = df[(df["date"] >= cutoff) & (df["channel"].isin(channel))]

c1, c2, c3 = st.columns(3)
c1.metric("Revenue", f"AED {filtered['revenue'].sum():,.0f}")
c2.metric("Orders", int(filtered['orders'].sum()))
gm = (filtered['gross_margin'].sum() / max(filtered['revenue'].sum(), 1)) * 100
c3.metric("Gross Margin %", f"{gm:.1f}%")

st.markdown("### Revenue trend")
st.line_chart(filtered.groupby("date")["revenue"].sum())

st.markdown("### Channel split (last 30 days)")
recent = filtered[filtered["date"] >= pd.Timestamp.today().normalize() - pd.Timedelta(days=30)]
st.bar_chart(recent.groupby("channel")["revenue"].sum())

st.caption(f"Data as of {date.today():%d %b %Y}")
