import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Screener.in Glow Up", layout="wide")

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
    <style>
        /* App background */
        .stApp {background-color: #0e1117; color: #f5f5f5; font-family: 'Inter', sans-serif;}
        /* Main header */
        .main-title {font-size:2.2rem; font-weight:700; color:#00c39a; text-align:center; margin-bottom:0.3rem;}
        .bigdata {font-size:1rem; color:#cbd5e1; text-align:center; margin-bottom:20px;}
        /* Metric cards */
        .metric-card {background:#1b1f2a; border-radius:15px; padding:15px; text-align:center; box-shadow:0 0 12px rgba(0,0,0,0.3); margin-bottom:10px;}
        .metric-title {color:#a0a0a0; font-size:13px;}
        .metric-value {color:#00c39a; font-size:20px; font-weight:600;}
        /* Graph container */
        .graph-container {background-color: #1b1f2a; border-radius: 16px; padding: 25px; box-shadow: 0 0 18px rgba(0,0,0,0.4); margin-bottom: 25px;}
        /* Footer */
        .footer {text-align:center; margin-top:30px; color:#666; font-size:13px;}
        /* Table colors */
        .stDataFrame th {background-color:#1b1f2a !important; color:#00c39a !important;}
        .stDataFrame td {background-color:#111419 !important; color:#cbd5e1 !important;}
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# DATA
# -------------------------------
companies = [
    "Tata Motors", "Maruti Suzuki", "M & M", "Hyundai Motor",
    "Force Motors", "Olectra Greentech", "Mercury EV-Tech"
]

profiles = {
    "Tata Motors": {"Price": 701, "Change": -1.67, "Market Cap": "2,57,980 Cr", "HighLow": "948 / 536",
                    "PE": 12.0, "Book": 315, "Div": 0.84, "ROCE": 20.0, "ROE": 28.1},
    "Maruti Suzuki": {"Price": 16117, "Change": 0.87, "Market Cap": "5,06,714 Cr", "HighLow": "18000 / 9600",
                    "PE": 34.9, "Book": 1200, "Div": 0.84, "ROCE": 21.7, "ROE": 18.2},
    "M & M": {"Price": 3494, "Change": 2.15, "Market Cap": "4,34,532 Cr", "HighLow": "4200 / 1800",
                    "PE": 31.7, "Book": 850, "Div": 0.73, "ROCE": 13.9, "ROE": 15.5},
    "Hyundai Motor": {"Price": 2445, "Change": -7.74, "Market Cap": "1,98,682 Cr", "HighLow": "3000 / 1500",
                    "PE": 36.9, "Book": 600, "Div": 0.87, "ROCE": 54.3, "ROE": 25.1},
    "Force Motors": {"Price": 15898, "Change": 52.40, "Market Cap": "20,947 Cr", "HighLow": "18500 / 8000",
                    "PE": 34.7, "Book": 2100, "Div": 0.24, "ROCE": 30.0, "ROE": 22.8},
    "Olectra Greentech": {"Price": 1545, "Change": 8.46, "Market Cap": "12,681 Cr", "HighLow": "2000 / 800",
                    "PE": 90.0, "Book": 300, "Div": 0.03, "ROCE": 20.5, "ROE": 12.3},
    "Mercury EV-Tech": {"Price": 47, "Change": 304.08, "Market Cap": "888 Cr", "HighLow": "85 / 15",
                    "PE": 94.5, "Book": 25, "Div": 0.00, "ROCE": 5.2, "ROE": 8.1}
}

# -------------------------------
# SESSION STATE FOR COMPANY SELECTION
# -------------------------------
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None

if st.session_state.selected_company is None:
    st.markdown("<div class='main-title'>✨ Screener.in Glow Up</div>", unsafe_allow_html=True)
    st.caption("Stock analysis and screening tool for investors in India.")
    q = st.text_input("🔍 Search for company")
    show = [c for c in companies if q.lower() in c.lower()] if q else companies
    company = st.selectbox("Or pick...", show)
    if st.button("Analyze This Company"):
        st.session_state.selected_company = company
        st.stop()
    st.write("Quick:", ", ".join(show))
    st.stop()

company = st.session_state.selected_company
cinfo = profiles[company]

if st.button("← Change company"):
    st.session_state.selected_company = None
    st.stop()

# -------------------------------
# COMPANY HEADER + METRICS
# -------------------------------
st.markdown(f"<div class='main-title'>🚗 {company} Ltd Dashboard</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='bigdata'>Price: <b>₹{cinfo['Price']}</b>  |  Change: <b style='color:{'green' if cinfo['Change']>0 else 'red'}'>{cinfo['Change']}%</b>  |  Market Cap: ₹{cinfo['Market Cap']}<br>"
    f"High/Low: {cinfo['HighLow']} | P/E: {cinfo['PE']} | Book Value: ₹{cinfo['Book']} | Dividend: {cinfo['Div']}% | ROCE: {cinfo['ROCE']}% | ROE: {cinfo['ROE']}%</div>",
    unsafe_allow_html=True
)

cols = st.columns(4)
metrics = [("Price", f"₹{cinfo['Price']}", f"{cinfo['Change']}%"),
           ("P/E", cinfo['PE'], None),
           ("Dividend Yield", f"{cinfo['Div']}%", None),
           ("ROE", f"{cinfo['ROE']}%", None)]

for i, (label, val, delta) in enumerate(metrics):
    with cols[i]:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>{label}</div><div class='metric-value'>{val}</div>{'' if not delta else f'<div class=\"metric-title\">Δ {delta}</div>'}</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# CANDLESTICK + VOLUME CHART
# -------------------------------
with st.container():
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    
    period_days = 180
    np.random.seed(abs(hash(company)) % 10**6)
    price_base = cinfo['Price']
    price = np.cumsum(np.random.normal(0, 3, period_days)) + price_base
    openp = price - np.random.uniform(2, 5, period_days)
    closep = price + np.random.uniform(-2, 5, period_days)
    highp = np.maximum(openp, closep) + np.random.uniform(0, 3, period_days)
    lowp = np.minimum(openp, closep) - np.random.uniform(0, 3, period_days)
    volume = np.abs(np.random.normal(2e6, 5e5, period_days)).astype(int)
    dates = pd.date_range(end=datetime.today(), periods=period_days)
    
    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=openp,
        high=highp,
        low=lowp,
        close=closep,
        increasing_line_color='#00c39a',
        decreasing_line_color='#ff4b4b',
        name="Price"
    )])

    fig.add_trace(go.Bar(
        x=dates,
        y=volume,
        name="Volume",
        marker_color="rgba(0,195,154,0.15)",
        yaxis='y2'
    ))

    fig.update_layout(
        yaxis2=dict(overlaying='y', side='right', showgrid=False),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#f5f5f5"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# PROS / CONS
# -------------------------------
st.markdown("### 🟩 Pros")
st.success("• Company has reduced debt.\n• Good profit growth 37.2% CAGR (5 yrs).\n• Strong ROE track record.")
st.markdown("### 🟥 Cons")
st.error("• Promoter holding has decreased over last 3 years: -3.83%")
st.markdown("---")

# -------------------------------
# PEERS TABLE
# -------------------------------
st.markdown("Peer Comparison")
d = pd.DataFrame({
    "Name": ["Maruti Suzuki", "M & M", company, "Hyundai Motor", "Force Motors"],
    "CMP": [16117, 3494, cinfo['Price'], 2445, 15898],
    "P/E": [34.8, 31.7, cinfo['PE'], 36.9, 34.7],
    "Market Cap": [506714, 434532, 257980, 198682, 20947],
    "Net Profit Qtr": [3792, 4376, 4003, 1335, 176],
    "ROCE (%)": [21.7, 13.9, 19.97, 54.25, 29.99]
})
st.dataframe(d, use_container_width=True)
st.markdown("---")

# -------------------------------
# QUARTERLY RESULTS
# -------------------------------
st.markdown("Quarterly Results")
dfq = pd.DataFrame({
    "": ["Sales +", "Expenses +", "Operating Profit", "Net Profit"],
    "Jun 2022": [71935, 69522, 2413, -4951],
    "Sep 2022": [79611, 74039, 5572, -898],
    "Dec 2022": [86489, 77668, 8820, 3043],
    "Mar 2023": [105932, 92818, 13114, 5496]
})
st.dataframe(dfq, use_container_width=True)
st.markdown("---")

# -------------------------------
# PROFIT & LOSS
# -------------------------------
st.markdown("Profit & Loss")
st.dataframe(pd.DataFrame({
    "": ["Sales +", "Expenses +", "Operating Profit", "Net Profit"],
    "Mar 2022": [278454, 253734, 24720, -11309],
    "Mar 2023": [345967, 314151, 31816, 2690],
    "Mar 2024": [434016, 376192, 57824, 31807],
    "Mar 2025": [439695, 384479, 55216, 28149],
}), use_container_width=True)
st.markdown("---")

# -------------------------------
# BALANCE SHEET
# -------------------------------
st.markdown("### 🧾 Balance Sheet")
st.dataframe(pd.DataFrame({
    "": ["Equity Capital", "Reserves", "Total Liabilities", "Total Assets"],
    "Mar 2024": [767, 84151, 369521, 369521],
    "Mar 2025": [736, 115408, 376973, 376973]
}), use_container_width=True)
st.markdown("---")

# -------------------------------
# CASH FLOW
# -------------------------------
st.markdown("### 💳 Cash Flow")
st.dataframe(pd.DataFrame({
    "": ["Cash from Op", "Cash from Investing", "Net Cash Flow"],
    "Mar 2024": [67915, -22781, 8128],
    "Mar 2025": [63102, -49982, -5666]
}), use_container_width=True)
st.markdown("---")

# -------------------------------
# FINANCIAL RATIOS
# -------------------------------
st.markdown("### 📐 Financial Ratios")
ratios = {
    "": ["P/E", "P/B", "ROE %", "ROCE %", "Div Yield %"],
    "Current": [cinfo['PE'], 2.2, cinfo['ROE'], cinfo['ROCE'], cinfo['Div']],
    "Industry Avg": [18.5, 3.1, 18.5, 15.2, 1.2]
}
st.dataframe(pd.DataFrame(ratios), use_container_width=True)
st.markdown("---")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<div class='footer'>Market Pulse | Streamlit + Python Only</div>", unsafe_allow_html=True)
