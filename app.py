import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from html import escape

st.set_page_config(
    page_title="Atlas V9 - Dealer Intelligence ",
    page_icon="🧠",
    layout="wide"
)

# =========================
# DESIGN
# =========================

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37,99,235,0.28) 0%, rgba(2,6,23,0.96) 32%, #020617 100%);
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 1.3rem;
        padding-bottom: 3rem;
        max-width: 98%;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #e5e7eb !important;
    }

    .hero {
        background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.90));
        border: 1px solid rgba(96,165,250,0.28);
        border-radius: 24px;
        padding: 24px 28px;
        margin-bottom: 18px;
        box-shadow: 0 22px 55px rgba(0,0,0,0.45);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 900;
        letter-spacing: -0.03em;
        color: #f8fafc !important;
    }

    .hero-subtitle {
        color: #93c5fd !important;
        font-size: 14px;
        margin-top: 4px;
    }

    .control-box {
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 20px;
        padding: 18px;
        margin: 10px 0 18px 0;
        box-shadow: 0 14px 30px rgba(0,0,0,0.28);
    }

    .card, .card-blue, .card-green, .card-red, .card-gold, .card-purple {
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.45);
        min-height: 118px;
    }

    .card {
        background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(30,41,59,0.90));
        border: 1px solid rgba(148,163,184,0.25);
    }
    .card-blue {
        background: linear-gradient(135deg, rgba(30,64,175,0.38), rgba(15,23,42,0.96));
        border: 1px solid rgba(96,165,250,0.36);
    }
    .card-green {
        background: linear-gradient(135deg, rgba(21,128,61,0.34), rgba(15,23,42,0.96));
        border: 1px solid rgba(74,222,128,0.34);
    }
    .card-red {
        background: linear-gradient(135deg, rgba(153,27,27,0.38), rgba(15,23,42,0.96));
        border: 1px solid rgba(248,113,113,0.36);
    }
    .card-gold {
        background: linear-gradient(135deg, rgba(180,83,9,0.36), rgba(15,23,42,0.96));
        border: 1px solid rgba(251,191,36,0.34);
    }
    .card-purple {
        background: linear-gradient(135deg, rgba(109,40,217,0.36), rgba(15,23,42,0.96));
        border: 1px solid rgba(196,181,253,0.34);
    }

    .emotion-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(17,24,39,0.96));
        border: 1px solid rgba(148,163,184,0.26);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.40);
        min-height: 142px;
    }
    .emotion-score {
        font-size: 38px;
        font-weight: 950;
        letter-spacing: -0.04em;
        margin-top: 4px;
        color: #f8fafc !important;
    }
    .emotion-title {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 900;
        color: #93c5fd !important;
    }
    .emotion-sub {
        font-size: 13px;
        color: #cbd5e1 !important;
        margin-top: 6px;
    }
    .emotion-extreme-greed {border-color: rgba(34,197,94,0.55); background: linear-gradient(135deg, rgba(22,101,52,0.52), rgba(15,23,42,0.96));}
    .emotion-greed {border-color: rgba(74,222,128,0.38); background: linear-gradient(135deg, rgba(21,128,61,0.34), rgba(15,23,42,0.96));}
    .emotion-neutral {border-color: rgba(96,165,250,0.38); background: linear-gradient(135deg, rgba(30,64,175,0.30), rgba(15,23,42,0.96));}
    .emotion-fear {border-color: rgba(251,191,36,0.40); background: linear-gradient(135deg, rgba(180,83,9,0.34), rgba(15,23,42,0.96));}
    .emotion-extreme-fear {border-color: rgba(248,113,113,0.50); background: linear-gradient(135deg, rgba(153,27,27,0.48), rgba(15,23,42,0.96));}

    .label {
        color: #94a3b8 !important;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .value {
        color: #f8fafc !important;
        font-size: 26px;
        font-weight: 900;
        margin-top: 6px;
    }
    .small {
        color: #cbd5e1 !important;
        font-size: 13px;
        margin-top: 3px;
    }

    .section-box {
        background: rgba(15,23,42,0.74);
        border: 1px solid rgba(148,163,184,0.20);
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 12px;
    }

    .pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        white-space: nowrap;
    }
    .pill-high {background: rgba(239,68,68,0.18); color: #fecaca !important; border: 1px solid rgba(248,113,113,0.40);}
    .pill-med {background: rgba(245,158,11,0.18); color: #fde68a !important; border: 1px solid rgba(251,191,36,0.40);}
    .pill-low {background: rgba(59,130,246,0.18); color: #bfdbfe !important; border: 1px solid rgba(96,165,250,0.40);}
    .pill-ok {background: rgba(34,197,94,0.18); color: #bbf7d0 !important; border: 1px solid rgba(74,222,128,0.40);}
    .pill-purple {background: rgba(168,85,247,0.18); color: #e9d5ff !important; border: 1px solid rgba(196,181,253,0.40);}

    .table-wrap {
        background: rgba(15,23,42,0.78);
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 18px;
        overflow: auto;
        max-height: 620px;
        margin-bottom: 18px;
        box-shadow: 0 16px 38px rgba(0,0,0,0.35);
    }

    table.atlas-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        color: #e5e7eb !important;
        background: rgba(15,23,42,0.96) !important;
    }

    table.atlas-table th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: #111827 !important;
        color: #bfdbfe !important;
        font-weight: 900;
        text-align: left;
        padding: 11px 12px;
        border-bottom: 1px solid rgba(96,165,250,0.38);
        white-space: nowrap;
    }

    table.atlas-table td {
        padding: 10px 12px;
        border-bottom: 1px solid rgba(148,163,184,0.10);
        color: #e5e7eb !important;
        white-space: nowrap;
    }

    table.atlas-table tr:nth-child(even) td {
        background: rgba(30,41,59,0.42) !important;
    }
    table.atlas-table tr:hover td {
        background: rgba(37,99,235,0.20) !important;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        background: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid rgba(148,163,184,0.32) !important;
        border-radius: 12px !important;
    }

    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(147,197,253,0.35) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }

    hr {border-color: rgba(148,163,184,0.16);}
</style>
""", unsafe_allow_html=True)

# =========================
# UI HELPERS
# =========================

def fmt_num(x, decimals=2):
    try:
        if pd.isna(x):
            return ""
        return f"{float(x):,.{decimals}f}"
    except Exception:
        return str(x)


def fmt_int(x):
    try:
        if pd.isna(x):
            return ""
        return f"{int(float(x)):,}"
    except Exception:
        return str(x)


def risk_pill(x):
    x = str(x)
    if x == "High":
        return '<span class="pill pill-high">High</span>'
    if x == "Medium":
        return '<span class="pill pill-med">Medium</span>'
    if x == "Low":
        return '<span class="pill pill-low">Low</span>'
    return '<span class="pill pill-ok">Normal</span>'


def dna_pill(x):
    x = str(x)
    if "Execution" in x or "Review" in x:
        return f'<span class="pill pill-high">{escape(x)}</span>'
    if "A-Book" in x or "Normal" in x:
        return f'<span class="pill pill-ok">{escape(x)}</span>'
    if "Scalper" in x or "News" in x:
        return f'<span class="pill pill-med">{escape(x)}</span>'
    return f'<span class="pill pill-purple">{escape(x)}</span>'


def render_table(df, title=None, max_rows=100, numeric_cols=None, pill_cols=None):
    if title:
        st.markdown(f"### {title}")
    if df is None or df.empty:
        st.warning("No data for current filters.")
        return

    view = df.head(max_rows).copy()
    numeric_cols = numeric_cols or []
    pill_cols = pill_cols or {}

    for col in view.columns:
        if col in pill_cols:
            view[col] = view[col].apply(pill_cols[col])
        elif col in numeric_cols:
            view[col] = view[col].apply(lambda v: fmt_num(v, 2))
        else:
            view[col] = view[col].apply(lambda v: "" if pd.isna(v) else escape(str(v)))

    html = view.to_html(index=False, escape=False, classes="atlas-table")
    st.markdown(f'<div class="table-wrap">{html}</div>', unsafe_allow_html=True)


def card(label, value, small, css_class="card"):
    st.markdown(f"""
    <div class="{css_class}">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="small">{small}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 Atlas V9 - Intelligence Briefing</div>
    <div class="hero-subtitle">Triple CRM Parser • Intelligence Briefing • Anomaly Detector • Early Warning Radar • Dealer Action Center</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload CRM report: old Orders CSV/TXT, ClosedDeals XLSX, or OpenDeals XLSX",
    type=["csv", "txt", "xlsx"]
)

if uploaded_file is None:
    st.info("Upload the old Orders export, ClosedDeals Excel report, or OpenDeals Excel report.")
    st.stop()

# =========================
# PARSERS
# =========================

OLD_COLUMNS = [
    "Ticket", "Trading Account", "Trade Command", "Volume", "Open Time", "Close Time",
    "Profit", "Symbol", "Swap", "Commission"
]


def clean_number(value):
    if pd.isna(value):
        return 0.0
    value = str(value).strip()
    if value == "" or value.lower() in ["nan", "none", "< empty >"]:
        return 0.0
    value = value.replace(" ", "").replace(",", "")
    try:
        return float(value)
    except Exception:
        return 0.0


def clean_text(value):
    if pd.isna(value):
        return ""
    value = str(value).strip()
    if value.lower() in ["nan", "none", "< empty >"]:
        return ""
    return value


def parse_duration_to_seconds(value):
    if pd.isna(value):
        return np.nan
    if isinstance(value, pd.Timedelta):
        return value.total_seconds()
    text = str(value).strip()
    if text == "" or text.lower() in ["nan", "none", "< empty >"]:
        return np.nan
    try:
        # CRM format can be DD.HH:MM:SS or HH:MM:SS
        if "." in text and ":" in text:
            day_part, time_part = text.split(".", 1)
            return int(day_part) * 86400 + pd.to_timedelta(time_part).total_seconds()
        if ":" in text:
            return pd.to_timedelta(text).total_seconds()
        return float(text)
    except Exception:
        return np.nan


def load_old_orders(file):
    raw = pd.read_csv(
        file,
        sep="\t",
        header=None,
        names=OLD_COLUMNS,
        dtype=str,
        encoding="utf-8-sig",
        engine="python"
    )

    df = pd.DataFrame()
    df["Source Report"] = "Old Orders CSV"
    df["Ticket"] = raw["Ticket"].apply(clean_text)
    df["Deal Id"] = df["Ticket"]
    df["Position Id"] = ""
    df["Client Id"] = ""
    df["Trading Account"] = raw["Trading Account"].apply(clean_text)
    df["Trade Command"] = raw["Trade Command"].apply(clean_text)
    df["Direction"] = df["Trade Command"]
    df["Symbol"] = raw["Symbol"].apply(clean_text).str.upper()
    df["Asset"] = df["Symbol"]
    df["Volume"] = raw["Volume"].apply(clean_number)
    df["MT lots"] = df["Volume"]
    df["Open Time"] = pd.to_datetime(raw["Open Time"], errors="coerce", format="%Y.%m.%d %H:%M:%S.%f")
    df["Close Time"] = pd.to_datetime(raw["Close Time"], errors="coerce", format="%Y.%m.%d %H:%M:%S.%f")
    df["Open Rate"] = np.nan
    df["Close Rate"] = np.nan
    df["Profit"] = raw["Profit"].apply(clean_number)
    df["Pnl ABC"] = df["Profit"]
    df["Pnl Pips"] = np.nan
    df["Swap ABC"] = raw["Swap"].apply(clean_number)
    df["Trading Commission ABC"] = raw["Commission"].apply(clean_number)
    df["Spread ABC"] = 0.0
    df["Spread in Pips"] = np.nan
    df["Margin Used ABC"] = np.nan
    df["Business Group"] = ""
    df["Close Reason"] = ""
    df["Open Reason"] = ""
    df["Trading Platform"] = ""
    df["Close Country From Ip"] = ""
    df["Open Country From Ip"] = ""
    df["Account Manager"] = ""
    df["Net PnL"] = df["Pnl ABC"] + df["Swap ABC"] + df["Trading Commission ABC"]
    df["Duration Seconds"] = (df["Close Time"] - df["Open Time"]).dt.total_seconds()
    return df


def load_closed_deals(file):
    raw = pd.read_excel(file, sheet_name=0, dtype=object)
    raw.columns = [str(c).strip() for c in raw.columns]

    df = pd.DataFrame()
    df["Source Report"] = "ClosedDeals XLSX"
    df["Ticket"] = raw.get("Deal Id", "").apply(clean_text) if "Deal Id" in raw else ""
    df["Deal Id"] = df["Ticket"]
    df["Position Id"] = raw.get("Position Id", "").apply(clean_text) if "Position Id" in raw else ""
    df["Client Id"] = raw.get("Client Id", "").apply(clean_text) if "Client Id" in raw else ""
    df["Trading Account"] = raw.get("Account", "").apply(clean_text) if "Account" in raw else ""
    df["Trade Command"] = raw.get("Direction", "").apply(clean_text) if "Direction" in raw else ""
    df["Direction"] = df["Trade Command"]
    df["Symbol"] = raw.get("Asset", "").apply(clean_text).str.upper() if "Asset" in raw else ""
    df["Asset"] = df["Symbol"]
    df["Volume"] = raw.get("MT lots", 0).apply(clean_number) if "MT lots" in raw else 0.0
    df["MT lots"] = df["Volume"]
    df["Open Time"] = pd.to_datetime(raw.get("Open Time"), errors="coerce") if "Open Time" in raw else pd.NaT
    df["Close Time"] = pd.to_datetime(raw.get("Close Time"), errors="coerce") if "Close Time" in raw else pd.NaT
    df["Open Rate"] = raw.get("Open Rate", np.nan).apply(clean_number) if "Open Rate" in raw else np.nan
    df["Close Rate"] = raw.get("Close Rate", np.nan).apply(clean_number) if "Close Rate" in raw else np.nan
    df["Profit"] = raw.get("Pnl ABC", 0).apply(clean_number) if "Pnl ABC" in raw else 0.0
    df["Pnl ABC"] = df["Profit"]
    df["Pnl Pips"] = raw.get("Pnl Pips", np.nan).apply(clean_number) if "Pnl Pips" in raw else np.nan
    df["Swap ABC"] = raw.get("Swap ABC", 0).apply(clean_number) if "Swap ABC" in raw else 0.0
    df["Trading Commission ABC"] = raw.get("Trading Commission ABC", 0).apply(clean_number) if "Trading Commission ABC" in raw else 0.0
    df["Spread ABC"] = raw.get("Spread ABC", 0).apply(clean_number) if "Spread ABC" in raw else 0.0
    df["Spread in Pips"] = raw.get("Spread in Pips", np.nan).apply(clean_number) if "Spread in Pips" in raw else np.nan
    df["Margin Used ABC"] = raw.get("Margin Used ABC", np.nan).apply(clean_number) if "Margin Used ABC" in raw else np.nan
    df["Business Group"] = raw.get("Business Group", "").apply(clean_text) if "Business Group" in raw else ""
    df["Close Reason"] = raw.get("Close Reason", "").apply(clean_text) if "Close Reason" in raw else ""
    df["Open Reason"] = raw.get("Open Reason", "").apply(clean_text) if "Open Reason" in raw else ""
    df["Trading Platform"] = raw.get("Trading Platform", "").apply(clean_text) if "Trading Platform" in raw else ""
    df["Close Country From Ip"] = raw.get("Close Country From Ip", "").apply(clean_text) if "Close Country From Ip" in raw else ""
    df["Open Country From Ip"] = raw.get("Open Country From Ip", "").apply(clean_text) if "Open Country From Ip" in raw else ""
    df["Account Manager"] = raw.get("Account Manager", "").apply(clean_text) if "Account Manager" in raw else ""
    df["Net PnL"] = df["Pnl ABC"] + df["Swap ABC"] + df["Trading Commission ABC"]

    computed_duration = (df["Close Time"] - df["Open Time"]).dt.total_seconds()
    if "Deal Duration" in raw:
        report_duration = raw["Deal Duration"].apply(parse_duration_to_seconds)
        df["Duration Seconds"] = computed_duration.fillna(report_duration)
    else:
        df["Duration Seconds"] = computed_duration
    return df



def load_open_deals(file):
    raw = pd.read_excel(file, sheet_name=0, dtype=object)
    raw.columns = [str(c).strip() for c in raw.columns]

    df = pd.DataFrame()
    df["Source Report"] = "OpenDeals XLSX"
    df["Ticket"] = raw.get("Deal Id", "").apply(clean_text) if "Deal Id" in raw else ""
    df["Deal Id"] = df["Ticket"]
    df["Position Id"] = raw.get("Position Id", "").apply(clean_text) if "Position Id" in raw else ""
    df["Client Id"] = raw.get("Client Id", "").apply(clean_text) if "Client Id" in raw else ""
    df["Trading Account"] = raw.get("Account", "").apply(clean_text) if "Account" in raw else ""
    df["Trade Command"] = raw.get("Direction", "").apply(clean_text) if "Direction" in raw else ""
    df["Direction"] = df["Trade Command"]
    df["Symbol"] = raw.get("Asset", "").apply(clean_text).str.upper() if "Asset" in raw else ""
    df["Asset"] = df["Symbol"]
    df["Volume"] = raw.get("MT lots", 0).apply(clean_number) if "MT lots" in raw else 0.0
    df["MT lots"] = df["Volume"]
    df["Open Time"] = pd.to_datetime(raw.get("Open Time"), errors="coerce") if "Open Time" in raw else pd.NaT
    df["Close Time"] = pd.NaT
    df["Open Rate"] = raw.get("Open Rate", np.nan).apply(clean_number) if "Open Rate" in raw else np.nan
    df["Close Rate"] = np.nan
    df["Current Rate"] = raw.get("Current Rate", np.nan).apply(clean_number) if "Current Rate" in raw else np.nan

    # Open deals usually have empty PnL fields. Keep columns stable anyway.
    df["Profit"] = raw.get("Pnl ABC", 0).apply(clean_number) if "Pnl ABC" in raw else 0.0
    df["Pnl ABC"] = df["Profit"]
    df["Pnl Pips"] = raw.get("Pnl Pips", np.nan).apply(clean_number) if "Pnl Pips" in raw else np.nan
    df["Swap ABC"] = raw.get("Swap ABC", 0).apply(clean_number) if "Swap ABC" in raw else 0.0
    df["Trading Commission ABC"] = raw.get("Trading Commission ABC", 0).apply(clean_number) if "Trading Commission ABC" in raw else 0.0
    df["Spread ABC"] = 0.0
    df["Spread in Pips"] = np.nan
    df["Margin Used ABC"] = raw.get("Margin Used ABC", np.nan).apply(clean_number) if "Margin Used ABC" in raw else np.nan
    df["Margin Used PBC"] = raw.get("Margin Used PBC", np.nan).apply(clean_number) if "Margin Used PBC" in raw else np.nan
    df["Margin level %"] = raw.get("Margin level %", np.nan).apply(clean_number) if "Margin level %" in raw else np.nan
    df["Volume ABC"] = raw.get("Volume ABC", np.nan).apply(clean_number) if "Volume ABC" in raw else np.nan
    df["Volume PBC"] = raw.get("Volume PBC", np.nan).apply(clean_number) if "Volume PBC" in raw else np.nan
    df["Buy Amount"] = raw.get("Buy Amount", np.nan).apply(clean_number) if "Buy Amount" in raw else np.nan
    df["Sell Amount"] = raw.get("Sell Amount", np.nan).apply(clean_number) if "Sell Amount" in raw else np.nan
    df["Buy Asset"] = raw.get("Buy Asset", "").apply(clean_text) if "Buy Asset" in raw else ""
    df["Sell Asset"] = raw.get("Sell Asset", "").apply(clean_text) if "Sell Asset" in raw else ""

    df["Business Group"] = raw.get("Business Group", "").apply(clean_text) if "Business Group" in raw else ""
    df["Close Reason"] = ""
    df["Open Reason"] = raw.get("Open Reason", "").apply(clean_text) if "Open Reason" in raw else ""
    df["Trading Platform"] = raw.get("Trading Platform", "").apply(clean_text) if "Trading Platform" in raw else ""
    df["Close Country From Ip"] = ""
    df["Open Country From Ip"] = ""
    df["Account Manager"] = raw.get("Account Manager", "").apply(clean_text) if "Account Manager" in raw else ""
    df["Net PnL"] = df["Pnl ABC"] + df["Swap ABC"] + df["Trading Commission ABC"]

    now_ts = pd.Timestamp.now()
    df["Duration Seconds"] = (now_ts - df["Open Time"]).dt.total_seconds()
    return df

def load_any_report(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".xlsx"):
        preview = pd.read_excel(uploaded_file, sheet_name=0, nrows=5, dtype=object)
        preview_cols = {str(c).strip() for c in preview.columns}
        uploaded_file.seek(0)

        if "Close Time" in preview_cols or "Deal Duration" in preview_cols or "Close Reason" in preview_cols:
            return load_closed_deals(uploaded_file)

        if "Current Rate" in preview_cols or "Margin Used ABC" in preview_cols or "Volume ABC" in preview_cols:
            return load_open_deals(uploaded_file)

        # Safe fallback: try ClosedDeals structure first
        return load_closed_deals(uploaded_file)

    return load_old_orders(uploaded_file)

try:
    trades = load_any_report(uploaded_file)
except Exception as e:
    st.error(f"Could not parse report: {e}")
    st.stop()

# Keep only trades
trades["Trade Command"] = trades["Trade Command"].astype(str).str.strip()
trades = trades[trades["Trade Command"].str.upper().isin(["BUY", "SELL"])]

if trades.empty:
    st.error("No Buy/Sell trades found in this report.")
    st.stop()

trades["Duration Seconds"] = pd.to_numeric(trades["Duration Seconds"], errors="coerce").fillna(0).clip(lower=0)
trades["Date"] = trades["Open Time"].dt.date
trades["Hour"] = trades["Open Time"].dt.hour.fillna(-1).astype(int)
trades["Trading Account"] = trades["Trading Account"].astype(str)
trades["Symbol"] = trades["Symbol"].astype(str).str.upper().str.strip()

report_type = trades["Source Report"].iloc[0]

# =========================
# CONTROLS
# =========================

st.markdown('<div class="control-box">', unsafe_allow_html=True)
ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([1.2, 1, 1, 1, 1.2])

with ctrl1:
    symbols = ["ALL"] + sorted([s for s in trades["Symbol"].dropna().unique().tolist() if s])
    selected_symbol = st.selectbox("Symbol", symbols)

with ctrl2:
    min_trades_filter = st.number_input("Minimum Trades", value=3, min_value=1, step=1)

with ctrl3:
    short_duration_threshold = st.number_input("Short Duration Seconds", value=60, min_value=1, step=10)

with ctrl4:
    a_book_min_trades = st.number_input("A-Book Min Trades", value=10, min_value=1, step=1)

with ctrl5:
    view_limit = st.number_input("Rows Displayed", value=40, min_value=10, step=10)

st.markdown('</div>', unsafe_allow_html=True)

if selected_symbol != "ALL":
    filtered = trades[trades["Symbol"] == selected_symbol].copy()
else:
    filtered = trades.copy()

# =========================
# ANALYTICS HELPERS
# =========================

def normalize_score(series):
    series = pd.Series(series).fillna(0).astype(float)
    if len(series) == 0 or series.max() == series.min():
        return pd.Series([0] * len(series), index=series.index)
    return ((series - series.min()) / (series.max() - series.min()) * 100).fillna(0)


def risk_level(score):
    if score >= 75:
        return "High"
    if score >= 50:
        return "Medium"
    if score >= 25:
        return "Low"
    return "Normal"


def mode_value(series):
    s = series.dropna().astype(str)
    s = s[s != ""]
    if s.empty:
        return ""
    return s.mode().iloc[0]


def top_symbol(series):
    s = series.dropna().astype(str)
    if s.empty:
        return ""
    return s.value_counts().index[0]


def classify_dna(row):
    short_pct = row.get("Short_Trade_%", 0)
    avg_dur = row.get("Avg_Duration_Sec", 0)
    symbols = row.get("Symbols_Traded", 0)
    pnl = row.get("Net_PnL", 0)
    trades_count = row.get("Trades", 0)
    top_sym = row.get("Top_Symbol", "")
    top_sym_pct = row.get("Top_Symbol_%", 0)
    hour_conc = row.get("Top_Hour_Profit_%", 0)

    if pnl > 0 and trades_count >= a_book_min_trades and short_pct < 40 and symbols >= 2:
        return "A-Book Candidate"
    if short_pct >= 70 and avg_dur <= 300:
        return "Execution Review Required"
    if hour_conc >= 70 and pnl > 0:
        return "Time-Window Specialist"
    if short_pct >= 60:
        return "Scalper"
    if avg_dur <= 1800:
        return "Intraday Trader"
    if avg_dur <= 14400:
        return "Day Trader"
    if avg_dur <= 432000:
        if top_sym_pct >= 80 and top_sym:
            return f"{top_sym} Specialist"
        return "Swing Trader"
    if avg_dur > 432000:
        return "Position Trader"
    return "Low Confidence"


def detective_reason(row):
    reasons = []
    if row["Short_Trade_%"] >= 70:
        reasons.append("Very high short-duration concentration")
    elif row["Short_Trade_%"] >= 40:
        reasons.append("Elevated short-duration concentration")
    if row["Top_Symbol_%"] >= 80:
        reasons.append(f"High symbol concentration in {row['Top_Symbol']}")
    if row["Top_Hour_Profit_%"] >= 60:
        reasons.append("PnL concentrated in narrow time window")
    if row["Net_PnL"] > 0:
        reasons.append("Positive profitability")
    if row["Spread_Revenue"] > 0:
        reasons.append("Generates spread revenue")
    if row["Trades"] >= 50:
        reasons.append("High trade frequency")
    return " | ".join(reasons) if reasons else "No strong pattern detected"



def build_exposure_summary_for_actions(data):
    """Creates a compact exposure summary for Dealer Action Center."""
    if data is None or data.empty:
        return pd.DataFrame()

    exposure_base = data.copy()
    exposure_base["Direction_UP"] = exposure_base["Trade Command"].astype(str).str.upper()
    exposure_base["Long_MT_Lots"] = np.where(exposure_base["Direction_UP"] == "BUY", exposure_base["Volume"], 0.0)
    exposure_base["Short_MT_Lots"] = np.where(exposure_base["Direction_UP"] == "SELL", exposure_base["Volume"], 0.0)

    if "Volume ABC" in exposure_base.columns:
        exposure_base["Long_Volume_ABC"] = np.where(
            exposure_base["Direction_UP"] == "BUY",
            pd.to_numeric(exposure_base["Volume ABC"], errors="coerce").fillna(0),
            0.0,
        )
        exposure_base["Short_Volume_ABC"] = np.where(
            exposure_base["Direction_UP"] == "SELL",
            pd.to_numeric(exposure_base["Volume ABC"], errors="coerce").fillna(0),
            0.0,
        )
    else:
        exposure_base["Long_Volume_ABC"] = 0.0
        exposure_base["Short_Volume_ABC"] = 0.0

    exposure_summary = exposure_base.groupby("Symbol").agg(
        Positions=("Ticket", "count"),
        Clients=("Trading Account", "nunique"),
        Long_MT_Lots=("Long_MT_Lots", "sum"),
        Short_MT_Lots=("Short_MT_Lots", "sum"),
        Long_Volume_ABC=("Long_Volume_ABC", "sum"),
        Short_Volume_ABC=("Short_Volume_ABC", "sum"),
        Margin_Used_ABC=("Margin Used ABC", "sum"),
        Avg_Age_Hours=("Duration Seconds", lambda x: x.mean() / 3600 if len(x) else 0),
        Max_Age_Hours=("Duration Seconds", lambda x: x.max() / 3600 if len(x) else 0),
    ).reset_index()

    exposure_summary["Net_MT_Lots"] = exposure_summary["Long_MT_Lots"] - exposure_summary["Short_MT_Lots"]
    exposure_summary["Gross_MT_Lots"] = exposure_summary["Long_MT_Lots"] + exposure_summary["Short_MT_Lots"]
    exposure_summary["Net_Volume_ABC"] = exposure_summary["Long_Volume_ABC"] - exposure_summary["Short_Volume_ABC"]
    exposure_summary["Gross_Volume_ABC"] = exposure_summary["Long_Volume_ABC"] + exposure_summary["Short_Volume_ABC"]
    exposure_summary["Net_Bias_%"] = np.where(
        exposure_summary["Gross_MT_Lots"] > 0,
        abs(exposure_summary["Net_MT_Lots"]) / exposure_summary["Gross_MT_Lots"] * 100,
        0,
    )
    total_gross = exposure_summary["Gross_MT_Lots"].sum()
    exposure_summary["Concentration_%"] = np.where(
        total_gross > 0,
        exposure_summary["Gross_MT_Lots"] / total_gross * 100,
        0,
    )
    return exposure_summary.sort_values(["Concentration_%", "Gross_MT_Lots"], ascending=False)




def emotion_level(score):
    try:
        score = float(score)
    except Exception:
        score = 50
    if score >= 80:
        return "Extreme Greed"
    if score >= 60:
        return "Greed"
    if score >= 40:
        return "Neutral"
    if score >= 20:
        return "Fear"
    return "Extreme Fear"


def emotion_css(level):
    level = str(level)
    if level == "Extreme Greed":
        return "emotion-card emotion-extreme-greed"
    if level == "Greed":
        return "emotion-card emotion-greed"
    if level == "Neutral":
        return "emotion-card emotion-neutral"
    if level == "Fear":
        return "emotion-card emotion-fear"
    return "emotion-card emotion-extreme-fear"


def emotion_pill(x):
    x = str(x)
    if x == "Extreme Greed":
        return '<span class="pill pill-ok">Extreme Greed</span>'
    if x == "Greed":
        return '<span class="pill pill-low">Greed</span>'
    if x == "Neutral":
        return '<span class="pill pill-purple">Neutral</span>'
    if x == "Fear":
        return '<span class="pill pill-med">Fear</span>'
    return '<span class="pill pill-high">Extreme Fear</span>'


def render_emotion_card(title, score, level, subtitle):
    css = emotion_css(level)
    st.markdown(f"""
    <div class="{css}">
        <div class="emotion-title">{escape(str(title))}</div>
        <div class="emotion-score">{float(score):.0f}</div>
        <div class="value" style="font-size:20px; margin-top:0px;">{escape(str(level))}</div>
        <div class="emotion-sub">{escape(str(subtitle))}</div>
    </div>
    """, unsafe_allow_html=True)


def build_retail_emotion_index(data):
    """Builds Atlas Retail Emotion Index from broker behaviour/positioning data.

    Scale: 0 = extreme fear / short crowd bias, 50 = neutral, 100 = extreme greed / long crowd bias.
    For OpenDeals this is live positioning. For ClosedDeals/Orders it is behaviour-based flow.
    """
    if data is None or data.empty:
        return pd.DataFrame(), {"score": 50, "level": "Neutral", "subtitle": "No data"}

    d = data.copy()
    d["Direction_UP"] = d["Trade Command"].astype(str).str.upper()
    d["Long_MT_Lots"] = np.where(d["Direction_UP"] == "BUY", pd.to_numeric(d["Volume"], errors="coerce").fillna(0), 0.0)
    d["Short_MT_Lots"] = np.where(d["Direction_UP"] == "SELL", pd.to_numeric(d["Volume"], errors="coerce").fillna(0), 0.0)

    # Use all available broker-side fields, but keep safe fallbacks for older reports.
    for col in ["Margin Used ABC", "Net PnL", "Duration Seconds"]:
        if col not in d.columns:
            d[col] = 0.0
        d[col] = pd.to_numeric(d[col], errors="coerce").fillna(0)

    d["Short_Trade_Flag"] = np.where(d["Duration Seconds"] <= short_duration_threshold, 1, 0)

    rei = d.groupby("Symbol").agg(
        Trades=("Ticket", "count"),
        Clients=("Trading Account", "nunique"),
        Long_MT_Lots=("Long_MT_Lots", "sum"),
        Short_MT_Lots=("Short_MT_Lots", "sum"),
        Margin_Used_ABC=("Margin Used ABC", "sum"),
        Net_PnL=("Net PnL", "sum"),
        Short_Trades=("Short_Trade_Flag", "sum"),
    ).reset_index()

    rei["Gross_MT_Lots"] = rei["Long_MT_Lots"] + rei["Short_MT_Lots"]
    rei["Net_MT_Lots"] = rei["Long_MT_Lots"] - rei["Short_MT_Lots"]
    rei["Net_Bias_%"] = np.where(rei["Gross_MT_Lots"] > 0, abs(rei["Net_MT_Lots"]) / rei["Gross_MT_Lots"] * 100, 0)
    total_gross = rei["Gross_MT_Lots"].sum()
    rei["Concentration_%"] = np.where(total_gross > 0, rei["Gross_MT_Lots"] / total_gross * 100, 0)
    rei["Short_Trade_%"] = np.where(rei["Trades"] > 0, rei["Short_Trades"] / rei["Trades"] * 100, 0)

    rei["Positioning_Component"] = rei["Net_Bias_%"].clip(0, 100)
    rei["Concentration_Component"] = (rei["Concentration_%"] * 2).clip(0, 100)
    rei["Margin_Component"] = normalize_score(rei["Margin_Used_ABC"].clip(lower=0))
    rei["Profit_Component"] = normalize_score(rei["Net_PnL"].clip(lower=0))
    rei["Duration_Component"] = rei["Short_Trade_%"].clip(0, 100)

    rei["Emotion_Pressure"] = (
        rei["Positioning_Component"] * 0.40
        + rei["Concentration_Component"] * 0.20
        + rei["Margin_Component"] * 0.20
        + rei["Profit_Component"] * 0.10
        + rei["Duration_Component"] * 0.10
    ).round(2)

    rei["Bias_Direction"] = np.where(rei["Net_MT_Lots"] > 0, "Long / Greed", np.where(rei["Net_MT_Lots"] < 0, "Short / Fear", "Balanced"))
    sign = np.where(rei["Net_MT_Lots"] > 0, 1, np.where(rei["Net_MT_Lots"] < 0, -1, 0))
    rei["Retail_Emotion_Index"] = (50 + sign * (rei["Emotion_Pressure"] / 2)).clip(0, 100).round(1)
    rei["Emotion_Level"] = rei["Retail_Emotion_Index"].apply(emotion_level)

    def drivers(row):
        parts = []
        if row["Net_Bias_%"] >= 70:
            parts.append("strong one-sided positioning")
        if row["Concentration_%"] >= 25:
            parts.append("high symbol concentration")
        if row["Margin_Component"] >= 70:
            parts.append("high margin pressure")
        if row["Profit_Component"] >= 70:
            parts.append("clients winning on symbol")
        if row["Short_Trade_%"] >= 40:
            parts.append("duration compression")
        if not parts:
            parts.append("balanced flow")
        return " | ".join(parts)

    rei["Main_Drivers"] = rei.apply(drivers, axis=1)
    rei = rei.sort_values("Retail_Emotion_Index", ascending=False)

    # General index: weighted by gross activity, with fallback to trade count.
    weights = rei["Gross_MT_Lots"].copy()
    if weights.sum() <= 0:
        weights = rei["Trades"]
    if weights.sum() > 0:
        general_score = float((rei["Retail_Emotion_Index"] * weights).sum() / weights.sum())
    else:
        general_score = 50.0
    general_level = emotion_level(general_score)

    top_greed = rei.sort_values("Retail_Emotion_Index", ascending=False).head(1)
    top_fear = rei.sort_values("Retail_Emotion_Index", ascending=True).head(1)
    subtitle = "Weighted by symbol activity"
    if not top_greed.empty and not top_fear.empty:
        subtitle = f"Greediest: {top_greed.iloc[0]['Symbol']} | Fearful: {top_fear.iloc[0]['Symbol']}"

    general = {"score": general_score, "level": general_level, "subtitle": subtitle}
    return rei, general

def build_dealer_action_center(account_df, data, report_type):
    """Turns analytics into an operational dealer queue."""
    actions = []

    def add(priority, category, item, score, recommendation, evidence):
        actions.append({
            "Priority": priority,
            "Category": category,
            "Item": item,
            "Attention Score": round(float(score), 2),
            "Recommendation": recommendation,
            "Evidence": evidence,
        })

    # 1) Open exposure actions
    exposure_summary = pd.DataFrame()
    if "OpenDeals" in str(report_type):
        exposure_summary = build_exposure_summary_for_actions(data)
        for _, row in exposure_summary.head(8).iterrows():
            score = min(100, row["Concentration_%"] * 1.5 + row["Net_Bias_%"] * 0.45 + min(row["Margin_Used_ABC"] / 10000, 20))
            if row["Concentration_%"] >= 35 or row["Net_Bias_%"] >= 75:
                priority = "Urgent" if score >= 75 else "Review Today"
                side = "Long" if row["Net_MT_Lots"] > 0 else "Short"
                add(
                    priority,
                    "Exposure",
                    str(row["Symbol"]),
                    score,
                    "Review hedge / monitor one-sided exposure",
                    f"Concentration {row['Concentration_%']:.1f}% | Net bias {row['Net_Bias_%']:.1f}% | Net {side} {abs(row['Net_MT_Lots']):.2f} lots | Clients {int(row['Clients'])}",
                )
            elif row["Concentration_%"] >= 20:
                add(
                    "Monitor",
                    "Exposure",
                    str(row["Symbol"]),
                    score,
                    "Monitor symbol concentration",
                    f"Concentration {row['Concentration_%']:.1f}% | Gross {row['Gross_MT_Lots']:.2f} lots",
                )

    # 2) Execution / investigation actions
    if account_df is not None and not account_df.empty:
        high_risk = account_df.sort_values("Dealer_Attention_Score", ascending=False).head(10)
        for _, row in high_risk.iterrows():
            if row["Atlas_Risk_Score"] >= 65 or "Execution" in str(row["Trader_DNA"]):
                add(
                    "Urgent" if row["Dealer_Attention_Score"] >= 75 else "Review Today",
                    "Investigation",
                    f"Account {row['Trading Account']}",
                    row["Dealer_Attention_Score"],
                    "Review execution quality / account behaviour",
                    f"DNA {row['Trader_DNA']} | Risk {row['Atlas_Risk_Score']:.1f} | Short {row['Short_Trade_%']:.1f}% | Top symbol {row['Top_Symbol']} {row['Top_Symbol_%']:.1f}%",
                )

        # 3) A-book opportunity actions
        if "A_Book_Candidate" in account_df.columns:
            abook = account_df[account_df["A_Book_Candidate"]].sort_values("A_Book_Score", ascending=False).head(8)
            for _, row in abook.iterrows():
                add(
                    "Opportunity",
                    "A-Book",
                    f"Account {row['Trading Account']}",
                    row["A_Book_Score"],
                    "Consider A-book / hedging review",
                    f"Net PnL {row['Net_PnL']:.2f} | Trades {int(row['Trades'])} | DNA {row['Trader_DNA']} | Short {row['Short_Trade_%']:.1f}%",
                )

        # 4) Broker revenue opportunity actions
        if "Spread_Revenue" in account_df.columns:
            revenue = account_df.sort_values("Spread_Revenue", ascending=False).head(6)
            for _, row in revenue.iterrows():
                if row["Spread_Revenue"] > 0:
                    add(
                        "Opportunity",
                        "Revenue",
                        f"Account {row['Trading Account']}",
                        min(100, row["Spread_Revenue"] / max(account_df["Spread_Revenue"].max(), 1) * 100),
                        "Protect / retain high-revenue client",
                        f"Spread revenue {row['Spread_Revenue']:.2f} | Net PnL {row['Net_PnL']:.2f} | Trades {int(row['Trades'])}",
                    )

    if not actions:
        add("Monitor", "System", "No critical actions", 10, "No immediate action required", "Current report does not show major concentration or investigation triggers.")

    action_df = pd.DataFrame(actions)
    priority_rank = {"Urgent": 1, "Review Today": 2, "Opportunity": 3, "Monitor": 4}
    action_df["_rank"] = action_df["Priority"].map(priority_rank).fillna(9)
    action_df = action_df.sort_values(["_rank", "Attention Score"], ascending=[True, False]).drop(columns=["_rank"])
    return action_df, exposure_summary



# =========================
# INTELLIGENCE BRIEFING HELPERS
# =========================

def report_detection_metadata(data, report_type):
    cols = set(data.columns)
    rtype = str(report_type)
    evidence = []
    confidence = 60
    if "OpenDeals" in rtype or "Current Rate" in cols or "Margin Used ABC" in cols:
        detected = "Open Deals"
        if "Current Rate" in cols:
            evidence.append("Current Rate present")
        if "Margin Used ABC" in cols:
            evidence.append("Margin Used present")
        if "Close Time" not in cols or data["Close Time"].isna().all():
            evidence.append("No effective close time")
        confidence = min(100, 70 + len(evidence) * 10)
    elif "ClosedDeals" in rtype or "Close Reason" in cols or "Deal Duration" in cols:
        detected = "Closed Deals"
        if "Close Reason" in cols:
            evidence.append("Close Reason present")
        if "Deal Duration" in cols:
            evidence.append("Deal Duration present")
        if "Close Time" in cols:
            evidence.append("Close Time present")
        confidence = min(100, 70 + len(evidence) * 10)
    else:
        detected = "Legacy Orders"
        evidence.append("Fallback parser")
        confidence = 70
    return detected, confidence, " | ".join(evidence)


def briefing_card(title, main, body, style=""):
    css = "briefing-card" + (" " + style if style else "")
    html = f"""
    <div class=\"{css}\">
        <div class=\"briefing-title\">{escape(str(title))}</div>
        <div class=\"briefing-main\">{escape(str(main))}</div>
        <div class=\"briefing-body\">{escape(str(body))}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def build_current_snapshot(account_df, data, rei_df, rei_general, exposure_summary, report_type):
    snap = {
        "report_type": str(report_type),
        "trades": int(len(data)),
        "accounts": int(account_df["Trading Account"].nunique()) if account_df is not None and not account_df.empty else 0,
        "net_pnl": float(pd.to_numeric(data.get("Net PnL", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
        "spread_revenue": float(pd.to_numeric(data.get("Spread ABC", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
        "margin_used": float(pd.to_numeric(data.get("Margin Used ABC", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
        "retail_emotion": float(rei_general.get("score", 50)) if isinstance(rei_general, dict) else 50,
        "top_attention_account": str(account_df.sort_values("Dealer_Attention_Score", ascending=False).iloc[0]["Trading Account"]) if account_df is not None and not account_df.empty and "Dealer_Attention_Score" in account_df.columns else "",
        "a_book_candidates": int(account_df.get("A_Book_Candidate", pd.Series(dtype=bool)).sum()) if account_df is not None and not account_df.empty and "A_Book_Candidate" in account_df.columns else 0,
        "high_risk_accounts": int((account_df.get("Risk_Level", pd.Series(dtype=str)) == "High").sum()) if account_df is not None and not account_df.empty and "Risk_Level" in account_df.columns else 0,
    }
    snap["symbol_exposure"] = {}
    if exposure_summary is not None and not exposure_summary.empty:
        top_exp = exposure_summary.sort_values("Concentration_%", ascending=False).iloc[0]
        snap["top_exposure_symbol"] = str(top_exp["Symbol"])
        snap["top_exposure_concentration"] = float(top_exp.get("Concentration_%", 0))
        snap["top_exposure_net_bias"] = float(top_exp.get("Net_Bias_%", 0))
        for _, r in exposure_summary.iterrows():
            sym = str(r.get("Symbol", ""))
            if sym:
                snap["symbol_exposure"][sym] = {
                    "concentration": float(r.get("Concentration_%", 0)),
                    "net_bias": float(r.get("Net_Bias_%", 0)),
                    "net_lots": float(r.get("Net_MT_Lots", 0)),
                    "gross_lots": float(r.get("Gross_MT_Lots", 0)),
                    "clients": float(r.get("Clients", 0)),
                }
    else:
        snap["top_exposure_symbol"] = ""
        snap["top_exposure_concentration"] = 0.0
        snap["top_exposure_net_bias"] = 0.0
    snap["symbol_emotion"] = {}
    if rei_df is not None and not rei_df.empty:
        g = rei_df.sort_values("Retail_Emotion_Index", ascending=False).iloc[0]
        f = rei_df.sort_values("Retail_Emotion_Index", ascending=True).iloc[0]
        snap["greediest_symbol"] = str(g["Symbol"])
        snap["greediest_score"] = float(g["Retail_Emotion_Index"])
        snap["fearful_symbol"] = str(f["Symbol"])
        snap["fearful_score"] = float(f["Retail_Emotion_Index"])
        for _, r in rei_df.iterrows():
            sym = str(r.get("Symbol", ""))
            if sym:
                snap["symbol_emotion"][sym] = {
                    "score": float(r.get("Retail_Emotion_Index", 50)),
                    "level": str(r.get("Emotion_Level", "Neutral")),
                    "drivers": str(r.get("Main_Drivers", "")),
                }
    else:
        snap["greediest_symbol"] = ""
        snap["greediest_score"] = 50.0
        snap["fearful_symbol"] = ""
        snap["fearful_score"] = 50.0
    return snap


def compare_snapshots(previous, current):
    if not previous:
        return pd.DataFrame([{"Change": "No baseline yet", "Previous": "-", "Current": "Current report loaded", "Impact": "Save this report as baseline to activate What Changed"}])
    rows = []
    def add(label, key, fmt="num"):
        old = previous.get(key, 0)
        new = current.get(key, 0)
        if fmt == "text":
            if str(old) != str(new):
                rows.append({"Change": label, "Previous": old, "Current": new, "Impact": "Changed"})
        else:
            try:
                diff = float(new) - float(old)
                if abs(diff) > 0.01:
                    rows.append({"Change": label, "Previous": f"{float(old):,.2f}", "Current": f"{float(new):,.2f}", "Impact": f"{diff:+,.2f}"})
            except Exception:
                pass
    add("Report type", "report_type", "text")
    add("Trades", "trades")
    add("Accounts", "accounts")
    add("Net PnL", "net_pnl")
    add("Retail Emotion", "retail_emotion")
    add("Top exposure symbol", "top_exposure_symbol", "text")
    add("Top exposure concentration %", "top_exposure_concentration")
    add("Top exposure net bias %", "top_exposure_net_bias")
    add("Greediest symbol", "greediest_symbol", "text")
    add("Greediest score", "greediest_score")
    add("Most fearful symbol", "fearful_symbol", "text")
    add("Fearful score", "fearful_score")
    if not rows:
        rows.append({"Change": "No major change", "Previous": "Baseline", "Current": "Current", "Impact": "Stable"})
    return pd.DataFrame(rows)


def pct_change(old, new):
    try:
        old = float(old)
        new = float(new)
        if abs(old) < 1e-9:
            return 100.0 if abs(new) > 1e-9 else 0.0
        return (new - old) / abs(old) * 100
    except Exception:
        return 0.0


def severity_from_score(score):
    if score >= 80:
        return "High"
    if score >= 55:
        return "Medium"
    if score >= 30:
        return "Low"
    return "Info"


def build_anomaly_detector(previous, current):
    if not previous:
        return pd.DataFrame([{
            "Severity": "Info",
            "Anomaly": "No baseline saved yet",
            "Previous": "-",
            "Current": "Current report loaded",
            "Change": "-",
            "Impact Score": 0,
            "Suggested Action": "Save this report as baseline, then upload the next report to activate anomaly detection"
        }])

    rows = []

    def add_metric(name, key, importance=1.0, action="Review change", unit=""):
        old = previous.get(key, 0)
        new = current.get(key, 0)
        try:
            old_f = float(old)
            new_f = float(new)
        except Exception:
            return
        diff = new_f - old_f
        pct = pct_change(old_f, new_f)
        if abs(diff) < 0.01 and abs(pct) < 1:
            return
        impact = min(100, abs(pct) * importance)
        if key in ["retail_emotion", "top_exposure_concentration", "top_exposure_net_bias"]:
            impact = min(100, abs(diff) * importance)
        rows.append({
            "Severity": severity_from_score(impact),
            "Anomaly": name,
            "Previous": f"{old_f:,.2f}{unit}",
            "Current": f"{new_f:,.2f}{unit}",
            "Change": f"{diff:+,.2f}{unit} ({pct:+.1f}%)",
            "Impact Score": round(impact, 1),
            "Suggested Action": action
        })

    def add_text(name, key, importance=45, action="Investigate why this changed"):
        old = str(previous.get(key, ""))
        new = str(current.get(key, ""))
        if old and new and old != new:
            rows.append({
                "Severity": severity_from_score(importance),
                "Anomaly": name,
                "Previous": old,
                "Current": new,
                "Change": "Changed",
                "Impact Score": importance,
                "Suggested Action": action
            })

    add_metric("Trade count changed", "trades", 0.65, "Check whether activity spike/drop is normal")
    add_metric("Active accounts changed", "accounts", 0.70, "Review client participation change")
    add_metric("Net PnL changed", "net_pnl", 0.55, "Check if change is concentrated in few accounts or symbols")
    add_metric("Spread revenue changed", "spread_revenue", 0.70, "Review revenue quality and active clients")
    add_metric("Margin used changed", "margin_used", 0.75, "Review leverage pressure and exposure risk")
    add_metric("Retail Emotion shifted", "retail_emotion", 2.0, "Review crowded positioning and symbol drivers", "")
    add_metric("A-book candidates changed", "a_book_candidates", 7.0, "Review newly qualified or lost A-book candidates")
    add_metric("High-risk accounts changed", "high_risk_accounts", 9.0, "Open Dealer Action Center and investigate top accounts")
    add_text("Top exposure symbol changed", "top_exposure_symbol", 60, "Review exposure dashboard and hedge requirement")
    add_metric("Top exposure concentration changed", "top_exposure_concentration", 2.5, "Check concentration in the leading symbol", "%")
    add_metric("Top exposure net bias changed", "top_exposure_net_bias", 1.8, "Check one-sided flow and hedge risk", "%")
    add_text("Greediest symbol changed", "greediest_symbol", 50, "Review Retail Emotion Index drivers")
    add_metric("Greediest score changed", "greediest_score", 1.8, "Check whether crowd behaviour became extreme")
    add_text("Most fearful symbol changed", "fearful_symbol", 40, "Review fearful/short crowded symbols")
    add_metric("Fearful score changed", "fearful_score", 1.5, "Check whether risk shifted to the other side")

    # Per-symbol exposure anomalies
    prev_exp = previous.get("symbol_exposure", {}) or {}
    cur_exp = current.get("symbol_exposure", {}) or {}
    for sym in sorted(set(prev_exp) | set(cur_exp)):
        old = prev_exp.get(sym, {})
        new = cur_exp.get(sym, {})
        old_c = old.get("concentration", 0)
        new_c = new.get("concentration", 0)
        diff_c = new_c - old_c
        if abs(diff_c) >= 8:
            impact = min(100, abs(diff_c) * 4 + new_c * 0.6)
            rows.append({
                "Severity": severity_from_score(impact),
                "Anomaly": f"{sym} exposure concentration moved",
                "Previous": f"{old_c:,.2f}%",
                "Current": f"{new_c:,.2f}%",
                "Change": f"{diff_c:+,.2f} pts",
                "Impact Score": round(impact, 1),
                "Suggested Action": "Review symbol exposure, top accounts and hedge requirement"
            })
        old_b = old.get("net_bias", 0)
        new_b = new.get("net_bias", 0)
        diff_b = new_b - old_b
        if abs(diff_b) >= 15:
            impact = min(100, abs(diff_b) * 2.5)
            rows.append({
                "Severity": severity_from_score(impact),
                "Anomaly": f"{sym} net bias shifted",
                "Previous": f"{old_b:,.2f}%",
                "Current": f"{new_b:,.2f}%",
                "Change": f"{diff_b:+,.2f} pts",
                "Impact Score": round(impact, 1),
                "Suggested Action": "Check whether client flow became one-sided"
            })

    # Per-symbol retail emotion anomalies
    prev_emo = previous.get("symbol_emotion", {}) or {}
    cur_emo = current.get("symbol_emotion", {}) or {}
    for sym in sorted(set(prev_emo) | set(cur_emo)):
        old = prev_emo.get(sym, {})
        new = cur_emo.get(sym, {})
        old_s = old.get("score", 50)
        new_s = new.get("score", 50)
        diff_s = new_s - old_s
        if abs(diff_s) >= 12:
            impact = min(100, abs(diff_s) * 3)
            rows.append({
                "Severity": severity_from_score(impact),
                "Anomaly": f"{sym} Retail Emotion shifted",
                "Previous": f"{old_s:,.0f} ({old.get('level','Neutral')})",
                "Current": f"{new_s:,.0f} ({new.get('level','Neutral')})",
                "Change": f"{diff_s:+,.0f} pts",
                "Impact Score": round(impact, 1),
                "Suggested Action": "Review REI drivers and check if exposure confirms the emotion shift"
            })

    if not rows:
        rows.append({
            "Severity": "Info",
            "Anomaly": "No material anomalies detected",
            "Previous": "Baseline",
            "Current": "Current",
            "Change": "Stable",
            "Impact Score": 0,
            "Suggested Action": "Continue normal monitoring"
        })

    sev_rank = {"High": 1, "Medium": 2, "Low": 3, "Info": 4}
    out = pd.DataFrame(rows)
    out["_rank"] = out["Severity"].map(sev_rank).fillna(9)
    out = out.sort_values(["_rank", "Impact Score"], ascending=[True, False]).drop(columns=["_rank"])
    return out


def build_early_warning_radar(account_df, data, rei_df, exposure_summary):
    warnings = []
    def add(level, theme, warning, evidence, action):
        rank = {"Urgent": 1, "Warning": 2, "Watch": 3, "Opportunity": 4}.get(level, 9)
        warnings.append({"Level": level, "Theme": theme, "Warning": warning, "Evidence": evidence, "Suggested Action": action, "_rank": rank})
    if exposure_summary is not None and not exposure_summary.empty:
        for _, r in exposure_summary.head(10).iterrows():
            if r.get("Concentration_%", 0) >= 35 or r.get("Net_Bias_%", 0) >= 80:
                add("Urgent", "Exposure", f"{r['Symbol']} concentration / one-sided risk", f"Concentration {r.get('Concentration_%',0):.1f}% | Net bias {r.get('Net_Bias_%',0):.1f}% | Clients {int(r.get('Clients',0))}", "Review hedge and top accounts immediately")
            elif r.get("Concentration_%", 0) >= 22:
                add("Watch", "Exposure", f"{r['Symbol']} rising concentration", f"Concentration {r.get('Concentration_%',0):.1f}%", "Monitor through the session")
    if rei_df is not None and not rei_df.empty:
        for _, r in rei_df.head(8).iterrows():
            score = float(r.get("Retail_Emotion_Index", 50))
            if score >= 85 or score <= 15:
                add("Warning", "Retail Emotion", f"{r['Symbol']} {r.get('Emotion_Level','')} extreme", f"REI {score:.0f} | {r.get('Main_Drivers','')}", "Expect emotional crowd behaviour; monitor exposure")
    if account_df is not None and not account_df.empty:
        risky = account_df[(account_df["Atlas_Risk_Score"] >= 70) | (account_df["Dealer_Attention_Score"] >= 80)].head(8)
        for _, r in risky.iterrows():
            add("Warning", "Account", f"Account {r['Trading Account']} requires review", f"DNA {r.get('Trader_DNA','')} | Attention {r.get('Dealer_Attention_Score',0):.1f} | Risk {r.get('Atlas_Risk_Score',0):.1f}", "Open account drilldown / review execution")
        if "A_Book_Candidate" in account_df.columns:
            ab = account_df[account_df["A_Book_Candidate"]].sort_values("A_Book_Score", ascending=False).head(5)
            for _, r in ab.iterrows():
                add("Opportunity", "A-Book", f"Account {r['Trading Account']} may deserve A-book review", f"A-book score {r.get('A_Book_Score',0):.1f} | PnL {r.get('Net_PnL',0):,.2f}", "Review routing / hedging decision")
    if not warnings:
        add("Watch", "System", "No major early warnings", "Report appears stable", "Continue normal monitoring")
    return pd.DataFrame(warnings).sort_values(["_rank"]).drop(columns=["_rank"])


def build_broker_story(account_df, data, action_df, rei_df, rei_general, exposure_summary, report_meta):
    detected, conf, evidence = report_meta
    lines = [f"Atlas detected a {detected} report with {conf}% confidence ({evidence})."]
    if isinstance(rei_general, dict):
        lines.append(f"General retail emotion is {rei_general.get('score',50):.0f}/100 ({rei_general.get('level','Neutral')}).")
    if exposure_summary is not None and not exposure_summary.empty:
        r = exposure_summary.sort_values("Concentration_%", ascending=False).iloc[0]
        side = "long" if r.get("Net_MT_Lots",0) > 0 else "short" if r.get("Net_MT_Lots",0) < 0 else "balanced"
        lines.append(f"Main live exposure focus is {r['Symbol']}: {r.get('Concentration_%',0):.1f}% concentration with {r.get('Net_Bias_%',0):.1f}% net bias ({side}).")
    if account_df is not None and not account_df.empty:
        top = account_df.sort_values("Dealer_Attention_Score", ascending=False).iloc[0]
        lines.append(f"Top account requiring attention is {top['Trading Account']} ({top.get('Trader_DNA','Unknown')}) with dealer attention score {top.get('Dealer_Attention_Score',0):.1f}.")
    if action_df is not None and not action_df.empty:
        urgent = (action_df["Priority"] == "Urgent").sum()
        review = (action_df["Priority"] == "Review Today").sum()
        opp = (action_df["Priority"] == "Opportunity").sum()
        lines.append(f"Action queue: {urgent} urgent, {review} review today, {opp} opportunity items.")
    return " ".join(lines)

# =========================
# ACCOUNT SUMMARY
# =========================

base = filtered.copy()

account_summary = (
    base.groupby("Trading Account")
    .agg(
        Trades=("Ticket", "count"),
        Total_Volume=("Volume", "sum"),
        Net_PnL=("Net PnL", "sum"),
        Gross_PnL=("Pnl ABC", "sum"),
        Swap=("Swap ABC", "sum"),
        Commission=("Trading Commission ABC", "sum"),
        Spread_Revenue=("Spread ABC", "sum"),
        Avg_Pips=("Pnl Pips", "mean"),
        Total_Pips=("Pnl Pips", "sum"),
        Avg_Margin_Used=("Margin Used ABC", "mean"),
        Avg_Duration_Sec=("Duration Seconds", "mean"),
        Median_Duration_Sec=("Duration Seconds", "median"),
        Short_Trades=("Duration Seconds", lambda x: (x <= short_duration_threshold).sum()),
        Symbols_Traded=("Symbol", "nunique"),
        Winning_Trades=("Net PnL", lambda x: (x > 0).sum()),
        Losing_Trades=("Net PnL", lambda x: (x < 0).sum()),
        Active_Days=("Date", "nunique"),
        Top_Symbol=("Symbol", top_symbol),
        Business_Group=("Business Group", mode_value),
        Platform=("Trading Platform", mode_value),
        Close_Reason_Main=("Close Reason", mode_value),
        Open_Reason_Main=("Open Reason", mode_value),
    )
    .reset_index()
)

account_summary = account_summary[account_summary["Trades"] >= min_trades_filter].copy()

if account_summary.empty:
    st.warning("No accounts match current filters.")
    st.stop()

account_summary["Short_Trade_%"] = account_summary["Short_Trades"] / account_summary["Trades"] * 100
account_summary["Win_Rate_%"] = account_summary["Winning_Trades"] / account_summary["Trades"] * 100
account_summary["Profit_Per_Trade"] = account_summary["Net_PnL"] / account_summary["Trades"]
account_summary["Trades_Per_Day"] = account_summary["Trades"] / account_summary["Active_Days"].replace(0, 1)

# Top symbol concentration
symbol_counts = base.groupby(["Trading Account", "Symbol"]).size().reset_index(name="Symbol_Trades")
total_counts = base.groupby("Trading Account").size().reset_index(name="Total_Trades")
symbol_counts = symbol_counts.merge(total_counts, on="Trading Account", how="left")
symbol_counts["Symbol_%"] = symbol_counts["Symbol_Trades"] / symbol_counts["Total_Trades"] * 100
top_symbol_pct = symbol_counts.sort_values(["Trading Account", "Symbol_%"], ascending=[True, False]).drop_duplicates("Trading Account")
account_summary = account_summary.merge(
    top_symbol_pct[["Trading Account", "Symbol_%"]].rename(columns={"Symbol_%": "Top_Symbol_%"}),
    on="Trading Account",
    how="left"
)
account_summary["Top_Symbol_%"] = account_summary["Top_Symbol_%"].fillna(0)

# Time-of-day profit concentration
hour_profit = base.groupby(["Trading Account", "Hour"])["Net PnL"].sum().reset_index()
positive_totals = hour_profit.groupby("Trading Account")["Net PnL"].apply(lambda x: x[x > 0].sum()).reset_index(name="Positive_Hour_PnL")
top_hour = hour_profit.sort_values(["Trading Account", "Net PnL"], ascending=[True, False]).drop_duplicates("Trading Account")
top_hour = top_hour.merge(positive_totals, on="Trading Account", how="left")
top_hour["Top_Hour_Profit_%"] = np.where(
    top_hour["Positive_Hour_PnL"] > 0,
    top_hour["Net PnL"].clip(lower=0) / top_hour["Positive_Hour_PnL"] * 100,
    0
)
account_summary = account_summary.merge(
    top_hour[["Trading Account", "Hour", "Top_Hour_Profit_%"]].rename(columns={"Hour": "Top_Profit_Hour"}),
    on="Trading Account",
    how="left"
)
account_summary["Top_Hour_Profit_%"] = account_summary["Top_Hour_Profit_%"].fillna(0)

# Scores
account_summary["Short_Duration_Score"] = normalize_score(account_summary["Short_Trade_%"])
account_summary["Frequency_Score"] = normalize_score(account_summary["Trades"])
account_summary["Profitability_Score"] = normalize_score(account_summary["Net_PnL"].clip(lower=0))
account_summary["Symbol_Concentration_Score"] = normalize_score(account_summary["Top_Symbol_%"])
account_summary["Time_Concentration_Score"] = normalize_score(account_summary["Top_Hour_Profit_%"])
account_summary["Margin_Aggression_Score"] = normalize_score(account_summary["Avg_Margin_Used"].fillna(0))

account_summary["Atlas_Risk_Score"] = (
    account_summary["Short_Duration_Score"] * 0.28
    + account_summary["Frequency_Score"] * 0.16
    + account_summary["Profitability_Score"] * 0.18
    + account_summary["Symbol_Concentration_Score"] * 0.16
    + account_summary["Time_Concentration_Score"] * 0.12
    + account_summary["Margin_Aggression_Score"] * 0.10
).round(2)

account_summary["Dealer_Attention_Score"] = (
    account_summary["Atlas_Risk_Score"] * 0.55
    + normalize_score(abs(account_summary["Net_PnL"])) * 0.25
    + normalize_score(account_summary["Spread_Revenue"].clip(lower=0)) * 0.10
    + normalize_score(account_summary["Trades"]) * 0.10
).round(2)

account_summary["Risk_Level"] = account_summary["Atlas_Risk_Score"].apply(risk_level)
account_summary["Trader_DNA"] = account_summary.apply(classify_dna, axis=1)
account_summary["Detective_Reason"] = account_summary.apply(detective_reason, axis=1)

account_summary["A_Book_Score"] = (
    normalize_score(account_summary["Net_PnL"].clip(lower=0)) * 0.32
    + normalize_score(account_summary["Trades"]) * 0.15
    + normalize_score(account_summary["Symbols_Traded"]) * 0.18
    + (100 - account_summary["Short_Duration_Score"]) * 0.22
    + normalize_score(account_summary["Spread_Revenue"].clip(lower=0)) * 0.13
).round(2)

account_summary["A_Book_Candidate"] = (
    (account_summary["Net_PnL"] > 0)
    & (account_summary["Trades"] >= a_book_min_trades)
    & (account_summary["Short_Trade_%"] < 40)
)

account_summary = account_summary.sort_values("Dealer_Attention_Score", ascending=False)

# =========================
# KPI CARDS
# =========================

total_accounts = account_summary["Trading Account"].nunique()
total_trades = base["Ticket"].count()
total_pnl = base["Net PnL"].sum()
spread_revenue = base["Spread ABC"].sum()
short_trade_pct = (base["Duration Seconds"] <= short_duration_threshold).sum() / total_trades * 100 if total_trades else 0
high_risk_accounts = (account_summary["Risk_Level"] == "High").sum()
a_book_count = account_summary["A_Book_Candidate"].sum()

k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
with k1: card("Report", str(report_type).replace(" ", "<br>"), "Detected format", "card-purple")
with k2: card("Accounts", fmt_int(total_accounts), "Filtered accounts", "card")
with k3: card("Trades", fmt_int(total_trades), "Buy/Sell deals", "card-blue")
with k4: card("Net PnL", fmt_num(total_pnl), "Profit + swap + commission", "card-green" if total_pnl >= 0 else "card-red")
with k5: card("Spread Revenue", fmt_num(spread_revenue), "Available in ClosedDeals", "card-gold")
with k6: card("Short Trades", f"{short_trade_pct:.1f}%", f"≤ {short_duration_threshold}s", "card")
with k7: card("A-Book", fmt_int(a_book_count), "Potential candidates", "card-green")

st.divider()

# =========================
# DEALER ACTION CENTER
# =========================

action_df, exposure_action_summary = build_dealer_action_center(account_summary, base, report_type)

st.subheader("🎯 Dealer Action Center")
st.caption("Atlas converts the report into an operational queue: what to check, why it matters, and what action to take.")

urgent_count = (action_df["Priority"] == "Urgent").sum()
review_count = (action_df["Priority"] == "Review Today").sum()
opportunity_count = (action_df["Priority"] == "Opportunity").sum()
monitor_count = (action_df["Priority"] == "Monitor").sum()

ac1, ac2, ac3, ac4 = st.columns(4)
with ac1: card("Urgent", fmt_int(urgent_count), "Act now", "card-red" if urgent_count else "card")
with ac2: card("Review Today", fmt_int(review_count), "Needs dealer check", "card-gold" if review_count else "card")
with ac3: card("Opportunities", fmt_int(opportunity_count), "A-book / revenue", "card-green" if opportunity_count else "card")
with ac4: card("Monitor", fmt_int(monitor_count), "No immediate action", "card-blue")

render_table(
    action_df,
    "Top Dealer Actions",
    max_rows=20,
    numeric_cols=["Attention Score"],
)

# =========================
# RETAIL EMOTION INDEX
# =========================

rei_df, rei_general = build_retail_emotion_index(base)

# =========================
# ATLAS INTELLIGENCE BRIEFING
# =========================

report_meta = report_detection_metadata(base, report_type)
current_snapshot = build_current_snapshot(account_summary, base, rei_df, rei_general, exposure_action_summary, report_type)
previous_snapshot = st.session_state.get("atlas_baseline_snapshot")
changes_df = compare_snapshots(previous_snapshot, current_snapshot)
anomaly_df = build_anomaly_detector(previous_snapshot, current_snapshot)
early_warning_df = build_early_warning_radar(account_summary, base, rei_df, exposure_action_summary)
broker_story = build_broker_story(account_summary, base, action_df, rei_df, rei_general, exposure_action_summary, report_meta)

st.divider()
st.subheader("🧠 Atlas Intelligence Briefing")
st.caption("One-page senior dealer interpretation: report detection, today's story, anomaly detection and early warnings.")

b1, b2, b3 = st.columns(3)
with b1:
    briefing_card("Report Detection", f"{report_meta[0]} • {report_meta[1]}%", report_meta[2], "briefing-card-green")
with b2:
    briefing_card("Today's Story", rei_general.get("level", "Neutral"), broker_story, "briefing-card-purple")
with b3:
    top_warning = early_warning_df.iloc[0]
    style = "briefing-card-red" if top_warning["Level"] == "Urgent" else "briefing-card-gold" if top_warning["Level"] == "Warning" else "briefing-card-green" if top_warning["Level"] == "Opportunity" else ""
    briefing_card("Main Focus", top_warning["Warning"], f"{top_warning['Evidence']} • Action: {top_warning['Suggested Action']}", style)

c_save, c_info = st.columns([1, 3])
with c_save:
    if st.button("Save Current Report as Baseline"):
        st.session_state["atlas_baseline_snapshot"] = current_snapshot
        st.success("Baseline saved. Upload the next report to activate What Changed.")
with c_info:
    st.markdown("<div class='section-box'><b>How to use:</b> save a baseline after a normal report, then upload the next report. Atlas will highlight changes in exposure, emotion, accounts and risk.</div>", unsafe_allow_html=True)

cc1, cc2 = st.columns(2)
with cc1:
    render_table(anomaly_df, "🚨 What Changed & Anomaly Detector", max_rows=20, numeric_cols=["Impact Score"])
with cc2:
    render_table(early_warning_df, "🚨 Early Warning Radar", max_rows=20)


st.divider()
st.subheader("🧭 Retail Emotion Index")
st.caption("Atlas measures crowd emotion from broker-side client behaviour: positioning bias, concentration, margin pressure, profitability and duration compression.")

if rei_df.empty:
    st.warning("Retail Emotion Index unavailable for this report.")
else:
    r1, r2, r3, r4, r5 = st.columns(5)
    with r1:
        render_emotion_card("General Index", rei_general["score"], rei_general["level"], rei_general["subtitle"])

    top_greed = rei_df.sort_values("Retail_Emotion_Index", ascending=False).head(1)
    top_fear = rei_df.sort_values("Retail_Emotion_Index", ascending=True).head(1)
    top_conc = rei_df.sort_values("Concentration_%", ascending=False).head(1)
    top_pressure = rei_df.sort_values("Emotion_Pressure", ascending=False).head(1)

    with r2:
        if not top_greed.empty:
            row = top_greed.iloc[0]
            render_emotion_card(row["Symbol"], row["Retail_Emotion_Index"], row["Emotion_Level"], f"Greediest symbol | {row['Bias_Direction']}")
    with r3:
        if not top_fear.empty:
            row = top_fear.iloc[0]
            render_emotion_card(row["Symbol"], row["Retail_Emotion_Index"], row["Emotion_Level"], f"Most fearful symbol | {row['Bias_Direction']}")
    with r4:
        if not top_conc.empty:
            row = top_conc.iloc[0]
            render_emotion_card(row["Symbol"], row["Retail_Emotion_Index"], row["Emotion_Level"], f"Top concentration {row['Concentration_%']:.1f}%")
    with r5:
        if not top_pressure.empty:
            row = top_pressure.iloc[0]
            render_emotion_card(row["Symbol"], row["Retail_Emotion_Index"], row["Emotion_Level"], f"Highest pressure {row['Emotion_Pressure']:.1f}")

    rei_cols = [
        "Symbol", "Retail_Emotion_Index", "Emotion_Level", "Bias_Direction", "Trades", "Clients",
        "Long_MT_Lots", "Short_MT_Lots", "Net_MT_Lots", "Gross_MT_Lots", "Net_Bias_%",
        "Concentration_%", "Margin_Used_ABC", "Net_PnL", "Short_Trade_%", "Main_Drivers"
    ]
    render_table(
        rei_df[rei_cols],
        "Symbol Retail Emotion Map",
        max_rows=25,
        numeric_cols=rei_cols,
        pill_cols={"Emotion_Level": emotion_pill}
    )

st.divider()

# =========================
# TABS
# =========================

tabs = st.tabs([
    "🧭 Retail Emotion",
    "📡 Open Exposure",
    "🕵️ Detective",
    "🧬 Trader DNA",
    "🏆 Winning Clients",
    "✅ A-Book Candidates",
    "⏱️ Duration",
    "💰 Profit Source",
    "🕒 Time of Day",
    "🚪 Close Behavior",
    "🔍 Account Drilldown",
    "📤 Export"
])

num_cols = [
    "Atlas_Risk_Score", "Dealer_Attention_Score", "Net_PnL", "Gross_PnL", "Swap", "Commission",
    "Spread_Revenue", "Win_Rate_%", "Short_Trade_%", "Top_Symbol_%", "Top_Hour_Profit_%",
    "Avg_Duration_Sec", "Median_Duration_Sec", "A_Book_Score", "Profit_Per_Trade", "Avg_Pips", "Avg_Margin_Used"
]


with tabs[0]:
    st.subheader("🧭 Retail Emotion Index")
    st.caption("0 = extreme fear / short crowd bias, 50 = neutral, 100 = extreme greed / long crowd bias. For OpenDeals this acts as live positioning sentiment.")

    if rei_df.empty:
        st.warning("Retail Emotion Index unavailable for this report.")
    else:
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            render_emotion_card("General Retail Emotion", rei_general["score"], rei_general["level"], rei_general["subtitle"])
        with c2:
            long_symbols = rei_df[rei_df["Net_MT_Lots"] > 0]
            if not long_symbols.empty:
                r = long_symbols.sort_values("Retail_Emotion_Index", ascending=False).iloc[0]
                render_emotion_card(f"{r['Symbol']} Long Bias", r["Retail_Emotion_Index"], r["Emotion_Level"], r["Main_Drivers"])
            else:
                card("Long Bias", "None", "No net-long symbol", "card")
        with c3:
            short_symbols = rei_df[rei_df["Net_MT_Lots"] < 0]
            if not short_symbols.empty:
                r = short_symbols.sort_values("Retail_Emotion_Index", ascending=True).iloc[0]
                render_emotion_card(f"{r['Symbol']} Short Bias", r["Retail_Emotion_Index"], r["Emotion_Level"], r["Main_Drivers"])
            else:
                card("Short Bias", "None", "No net-short symbol", "card")

        fig_rei = px.bar(
            rei_df.sort_values("Retail_Emotion_Index", ascending=False).head(30),
            x="Symbol",
            y="Retail_Emotion_Index",
            color="Emotion_Level",
            title="Retail Emotion Index by Symbol",
            hover_data=["Bias_Direction", "Net_Bias_%", "Concentration_%", "Main_Drivers"]
        )
        fig_rei.update_layout(template="plotly_dark", height=440, paper_bgcolor="#020617", plot_bgcolor="#020617", yaxis_range=[0, 100])
        fig_rei.add_hline(y=50, line_dash="dot", line_color="rgba(255,255,255,0.45)")
        st.plotly_chart(fig_rei, use_container_width=True)

        rei_cols = [
            "Symbol", "Retail_Emotion_Index", "Emotion_Level", "Bias_Direction", "Trades", "Clients",
            "Long_MT_Lots", "Short_MT_Lots", "Net_MT_Lots", "Gross_MT_Lots", "Net_Bias_%",
            "Concentration_%", "Margin_Used_ABC", "Net_PnL", "Short_Trade_%", "Main_Drivers"
        ]
        render_table(
            rei_df[rei_cols],
            "Full Retail Emotion Breakdown",
            max_rows=int(view_limit),
            numeric_cols=rei_cols,
            pill_cols={"Emotion_Level": emotion_pill}
        )


with tabs[1]:
    st.subheader("📡 Live Exposure Monitor")

    exposure_base = base.copy()
    exposure_base["Direction_UP"] = exposure_base["Trade Command"].astype(str).str.upper()
    exposure_base["Long_MT_Lots"] = np.where(exposure_base["Direction_UP"] == "BUY", exposure_base["Volume"], 0.0)
    exposure_base["Short_MT_Lots"] = np.where(exposure_base["Direction_UP"] == "SELL", exposure_base["Volume"], 0.0)

    if "Volume ABC" in exposure_base.columns:
        exposure_base["Long_Volume_ABC"] = np.where(exposure_base["Direction_UP"] == "BUY", pd.to_numeric(exposure_base["Volume ABC"], errors="coerce").fillna(0), 0.0)
        exposure_base["Short_Volume_ABC"] = np.where(exposure_base["Direction_UP"] == "SELL", pd.to_numeric(exposure_base["Volume ABC"], errors="coerce").fillna(0), 0.0)
    else:
        exposure_base["Long_Volume_ABC"] = 0.0
        exposure_base["Short_Volume_ABC"] = 0.0

    exposure_summary = exposure_base.groupby("Symbol").agg(
        Positions=("Ticket", "count"),
        Clients=("Trading Account", "nunique"),
        Long_MT_Lots=("Long_MT_Lots", "sum"),
        Short_MT_Lots=("Short_MT_Lots", "sum"),
        Long_Volume_ABC=("Long_Volume_ABC", "sum"),
        Short_Volume_ABC=("Short_Volume_ABC", "sum"),
        Margin_Used_ABC=("Margin Used ABC", "sum"),
        Avg_Age_Hours=("Duration Seconds", lambda x: x.mean() / 3600 if len(x) else 0),
        Max_Age_Hours=("Duration Seconds", lambda x: x.max() / 3600 if len(x) else 0),
    ).reset_index()

    exposure_summary["Net_MT_Lots"] = exposure_summary["Long_MT_Lots"] - exposure_summary["Short_MT_Lots"]
    exposure_summary["Gross_MT_Lots"] = exposure_summary["Long_MT_Lots"] + exposure_summary["Short_MT_Lots"]
    exposure_summary["Net_Volume_ABC"] = exposure_summary["Long_Volume_ABC"] - exposure_summary["Short_Volume_ABC"]
    exposure_summary["Gross_Volume_ABC"] = exposure_summary["Long_Volume_ABC"] + exposure_summary["Short_Volume_ABC"]
    exposure_summary["Net_Bias_%"] = np.where(
        exposure_summary["Gross_MT_Lots"] > 0,
        abs(exposure_summary["Net_MT_Lots"]) / exposure_summary["Gross_MT_Lots"] * 100,
        0
    )
    total_gross = exposure_summary["Gross_MT_Lots"].sum()
    exposure_summary["Concentration_%"] = np.where(total_gross > 0, exposure_summary["Gross_MT_Lots"] / total_gross * 100, 0)

    def exposure_recommendation(row):
        recs = []
        if row["Concentration_%"] >= 35:
            recs.append("Top concentration: monitor symbol exposure closely")
        if row["Net_Bias_%"] >= 80 and row["Gross_MT_Lots"] > 0:
            side = "Long" if row["Net_MT_Lots"] > 0 else "Short"
            recs.append(f"Strong one-sided {side} exposure: consider hedge/review")
        elif row["Net_Bias_%"] >= 60:
            recs.append("Directional bias elevated: monitor")
        if row["Clients"] <= 2 and row["Gross_MT_Lots"] > 0:
            recs.append("Exposure driven by few clients")
        if row["Margin_Used_ABC"] > 0 and row["Margin_Used_ABC"] >= exposure_summary["Margin_Used_ABC"].quantile(0.85):
            recs.append("High margin usage concentration")
        if not recs:
            recs.append("Balanced / normal monitoring")
        return " | ".join(recs)

    exposure_summary["Recommendation"] = exposure_summary.apply(exposure_recommendation, axis=1)
    exposure_summary = exposure_summary.sort_values(["Concentration_%", "Gross_MT_Lots"], ascending=False)

    e1, e2, e3, e4, e5 = st.columns(5)
    with e1: card("Symbols", fmt_int(exposure_summary["Symbol"].nunique()), "Open exposure symbols", "card-blue")
    with e2: card("Open Positions", fmt_int(exposure_summary["Positions"].sum()), "Current open deals", "card")
    with e3: card("Gross MT Lots", fmt_num(exposure_summary["Gross_MT_Lots"].sum()), "Long + short", "card-purple")
    with e4: card("Net MT Lots", fmt_num(exposure_summary["Net_MT_Lots"].sum()), "Long - short", "card-gold")
    with e5: card("Margin Used", fmt_num(exposure_summary["Margin_Used_ABC"].sum()), "ABC currency", "card-red" if exposure_summary["Margin_Used_ABC"].sum() > 0 else "card")

    exp_cols = [
        "Symbol", "Positions", "Clients", "Long_MT_Lots", "Short_MT_Lots", "Net_MT_Lots",
        "Gross_MT_Lots", "Net_Bias_%", "Concentration_%", "Long_Volume_ABC", "Short_Volume_ABC",
        "Net_Volume_ABC", "Margin_Used_ABC", "Avg_Age_Hours", "Max_Age_Hours", "Recommendation"
    ]
    render_table(
        exposure_summary[exp_cols],
        "📡 Live Exposure by Symbol",
        max_rows=int(view_limit),
        numeric_cols=exp_cols
    )

    fig_exp = px.bar(
        exposure_summary.head(25),
        x="Symbol",
        y=["Long_MT_Lots", "Short_MT_Lots"],
        title="Long vs Short MT Lots by Symbol",
        barmode="group"
    )
    fig_exp.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig_exp, use_container_width=True)

    fig_conc = px.scatter(
        exposure_summary.head(30),
        x="Net_Bias_%",
        y="Concentration_%",
        size="Gross_MT_Lots",
        color="Margin_Used_ABC",
        hover_data=["Symbol", "Positions", "Clients", "Recommendation"],
        title="Exposure Risk Map: Net Bias vs Concentration"
    )
    fig_conc.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig_conc, use_container_width=True)

    st.subheader("👤 Client Exposure Concentration")
    client_exposure = exposure_base.groupby(["Trading Account", "Symbol"]).agg(
        Positions=("Ticket", "count"),
        Direction_Main=("Trade Command", mode_value),
        MT_Lots=("Volume", "sum"),
        Margin_Used_ABC=("Margin Used ABC", "sum"),
        Avg_Age_Hours=("Duration Seconds", lambda x: x.mean() / 3600 if len(x) else 0),
        Business_Group=("Business Group", mode_value),
        Platform=("Trading Platform", mode_value)
    ).reset_index().sort_values("MT_Lots", ascending=False)
    render_table(client_exposure, "Largest Client Open Exposures", max_rows=int(view_limit), numeric_cols=["Positions","MT_Lots","Margin_Used_ABC","Avg_Age_Hours"])


with tabs[2]:
    detective_cols = [
        "Trading Account", "Dealer_Attention_Score", "Atlas_Risk_Score", "Risk_Level", "Trader_DNA",
        "Trades", "Net_PnL", "Spread_Revenue", "Short_Trade_%", "Top_Symbol", "Top_Symbol_%",
        "Top_Profit_Hour", "Top_Hour_Profit_%", "Business_Group", "Detective_Reason"
    ]
    render_table(
        account_summary[detective_cols],
        "🕵️ Dealer Attention Queue",
        max_rows=int(view_limit),
        numeric_cols=num_cols,
        pill_cols={"Risk_Level": risk_pill, "Trader_DNA": dna_pill}
    )
    fig = px.scatter(
        account_summary.head(40),
        x="Short_Trade_%",
        y="Net_PnL",
        size="Trades",
        color="Trader_DNA",
        hover_data=["Trading Account", "Risk_Level", "Detective_Reason"],
        title="Detective Map: Short Duration vs Net PnL"
    )
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    dna_summary = account_summary.groupby("Trader_DNA").agg(
        Accounts=("Trading Account", "count"),
        Trades=("Trades", "sum"),
        Net_PnL=("Net_PnL", "sum"),
        Spread_Revenue=("Spread_Revenue", "sum"),
        Avg_Risk=("Atlas_Risk_Score", "mean")
    ).reset_index().sort_values("Accounts", ascending=False)
    render_table(dna_summary, "🧬 Trader DNA Summary", numeric_cols=num_cols, pill_cols={"Trader_DNA": dna_pill})
    fig = px.treemap(dna_summary, path=["Trader_DNA"], values="Accounts", color="Net_PnL", title="Trader DNA Population Map")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    winning_cols = [
        "Trading Account", "Net_PnL", "Spread_Revenue", "Trades", "Win_Rate_%", "Avg_Pips",
        "Profit_Per_Trade", "Avg_Duration_Sec", "Short_Trade_%", "Symbols_Traded", "Trader_DNA", "Risk_Level"
    ]
    winners = account_summary.sort_values("Net_PnL", ascending=False)
    render_table(winners[winning_cols], "🏆 Most Winning Clients", max_rows=int(view_limit), numeric_cols=num_cols, pill_cols={"Risk_Level": risk_pill, "Trader_DNA": dna_pill})
    fig = px.bar(winners.head(25), x="Trading Account", y="Net_PnL", color="Trader_DNA", title="Top 25 Winning Clients")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[5]:
    a_book_candidates = account_summary[account_summary["A_Book_Candidate"]].sort_values("A_Book_Score", ascending=False)
    a_cols = [
        "Trading Account", "A_Book_Score", "Net_PnL", "Spread_Revenue", "Trades", "Win_Rate_%",
        "Avg_Duration_Sec", "Short_Trade_%", "Symbols_Traded", "Top_Symbol", "Business_Group", "Trader_DNA"
    ]
    render_table(a_book_candidates[a_cols] if not a_book_candidates.empty else pd.DataFrame(), "✅ Potential A-Book Candidates", max_rows=int(view_limit), numeric_cols=num_cols, pill_cols={"Trader_DNA": dna_pill})
    if not a_book_candidates.empty:
        fig = px.bar(a_book_candidates.head(25), x="Trading Account", y="A_Book_Score", color="Net_PnL", title="A-Book Candidate Score")
        fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
        st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
    bins = [0, 30, 60, 300, 1800, 14400, 86400, 432000, np.inf]
    labels = ["0-30s", "30-60s", "1-5m", "5-30m", "30m-4h", "4h-1d", "1d-5d", "5d+"]
    duration_df = base.copy()
    duration_df["Duration Bucket"] = pd.cut(duration_df["Duration Seconds"], bins=bins, labels=labels, include_lowest=True)
    duration_summary = duration_df.groupby("Duration Bucket", observed=False).agg(
        Trades=("Ticket", "count"),
        Net_PnL=("Net PnL", "sum"),
        Accounts=("Trading Account", "nunique")
    ).reset_index()
    render_table(duration_summary, "⏱️ Duration Distribution", numeric_cols=["Net_PnL"])
    fig = px.bar(duration_summary, x="Duration Bucket", y="Trades", color="Net_PnL", title="Trade Duration Buckets")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[7]:
    source = base.groupby(["Trading Account", "Symbol"]).agg(
        Trades=("Ticket", "count"),
        Net_PnL=("Net PnL", "sum"),
        Spread_Revenue=("Spread ABC", "sum"),
        Avg_Duration_Sec=("Duration Seconds", "mean")
    ).reset_index().sort_values("Net_PnL", ascending=False)
    render_table(source, "💰 Profit Source by Account & Symbol", max_rows=int(view_limit), numeric_cols=num_cols)
    sym = base.groupby("Symbol").agg(Trades=("Ticket", "count"), Net_PnL=("Net PnL", "sum"), Spread_Revenue=("Spread ABC", "sum"), Accounts=("Trading Account", "nunique")).reset_index().sort_values("Net_PnL", ascending=False)
    fig = px.bar(sym.head(25), x="Symbol", y="Net_PnL", color="Spread_Revenue", title="Symbol Profit Source")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[8]:
    hourly = base[base["Hour"] >= 0].groupby("Hour").agg(
        Trades=("Ticket", "count"),
        Net_PnL=("Net PnL", "sum"),
        Spread_Revenue=("Spread ABC", "sum"),
        Accounts=("Trading Account", "nunique")
    ).reset_index()
    render_table(hourly, "🕒 Time-of-Day Analysis", numeric_cols=num_cols)
    fig = px.bar(hourly, x="Hour", y="Net_PnL", color="Trades", title="PnL by Trading Hour")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617", plot_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[9]:
    close_reason = base.copy()
    close_reason["Close Reason"] = close_reason["Close Reason"].replace("", "Unknown")
    close_summary = close_reason.groupby("Close Reason").agg(
        Trades=("Ticket", "count"),
        Net_PnL=("Net PnL", "sum"),
        Accounts=("Trading Account", "nunique"),
        Avg_Duration_Sec=("Duration Seconds", "mean")
    ).reset_index().sort_values("Trades", ascending=False)
    render_table(close_summary, "🚪 Close Behavior Analysis", numeric_cols=num_cols)
    fig = px.pie(close_summary, values="Trades", names="Close Reason", title="Close Reason Distribution")
    fig.update_layout(template="plotly_dark", height=430, paper_bgcolor="#020617")
    st.plotly_chart(fig, use_container_width=True)

with tabs[10]:
    selected_account = st.selectbox("Select Account", account_summary["Trading Account"].astype(str).tolist())
    acc = account_summary[account_summary["Trading Account"].astype(str) == str(selected_account)].iloc[0]
    d1, d2, d3, d4, d5, d6 = st.columns(6)
    with d1: card("DNA", acc["Trader_DNA"], "Classification", "card-purple")
    with d2: card("Risk", acc["Risk_Level"], f"Score {acc['Atlas_Risk_Score']}", "card-red" if acc["Risk_Level"] == "High" else "card")
    with d3: card("Net PnL", fmt_num(acc["Net_PnL"]), "Account result", "card-green" if acc["Net_PnL"] >= 0 else "card-red")
    with d4: card("Trades", fmt_int(acc["Trades"]), "Total deals", "card-blue")
    with d5: card("Top Symbol", acc["Top_Symbol"], f"{acc['Top_Symbol_%']:.1f}%", "card-gold")
    with d6: card("A-Book", fmt_num(acc["A_Book_Score"]), "Candidate score", "card-green")

    st.markdown(f'<div class="section-box"><b>Detective Explanation:</b><br>{escape(acc["Detective_Reason"])}</div>', unsafe_allow_html=True)

    if "notes" not in st.session_state:
        st.session_state.notes = {}
    current_note = st.session_state.notes.get(str(selected_account), {"Status": "Unreviewed", "Note": ""})
    n1, n2 = st.columns([1, 3])
    with n1:
        status = st.selectbox("Dealer Status", ["Unreviewed", "Investigating", "Legitimate", "A-Book", "Execution Review", "Restricted"], index=["Unreviewed", "Investigating", "Legitimate", "A-Book", "Execution Review", "Restricted"].index(current_note.get("Status", "Unreviewed")))
    with n2:
        note = st.text_input("Dealer Note", value=current_note.get("Note", ""))
    if st.button("Save Note"):
        st.session_state.notes[str(selected_account)] = {"Status": status, "Note": note}
        st.success("Note saved for this session.")

    acc_trades = base[base["Trading Account"].astype(str) == str(selected_account)].sort_values("Open Time", ascending=False)
    display_trade_cols = ["Ticket", "Trading Account", "Trade Command", "Volume", "Symbol", "Open Time", "Close Time", "Duration Seconds", "Pnl ABC", "Pnl Pips", "Swap ABC", "Trading Commission ABC", "Spread ABC", "Net PnL", "Open Reason", "Close Reason", "Business Group", "Trading Platform"]
    display_trade_cols = [c for c in display_trade_cols if c in acc_trades.columns]
    render_table(acc_trades[display_trade_cols], "Account Trade History", max_rows=int(view_limit), numeric_cols=num_cols + ["Volume", "Pnl ABC", "Pnl Pips", "Spread ABC"])

with tabs[11]:
    st.subheader("📤 Export Atlas Reports")
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    with col_exp1:
        st.download_button("Download Account Summary", account_summary.to_csv(index=False).encode("utf-8"), "atlas_v9_account_summary.csv", "text/csv")
    with col_exp2:
        st.download_button("Download Normalized Trades", base.to_csv(index=False).encode("utf-8"), "atlas_v9_normalized_trades.csv", "text/csv")
    with col_exp3:
        notes_df = pd.DataFrame([{"Trading Account": k, **v} for k, v in st.session_state.get("notes", {}).items()])
        st.download_button("Download Dealer Notes", notes_df.to_csv(index=False).encode("utf-8"), "atlas_v9_dealer_notes.csv", "text/csv")

    with st.expander("Show Normalized Data Columns"):
        st.write(list(base.columns))
