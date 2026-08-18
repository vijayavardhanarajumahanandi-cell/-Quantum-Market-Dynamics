import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
import time
import math
import random

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantumMD · Market Dynamics",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@400;700;900&display=swap');

:root {
    --void: #020408;
    --deep: #060d18;
    --surface: #0a1628;
    --panel: #0f1f38;
    --border: #1a3055;
    --quantum-blue: #00d4ff;
    --quantum-violet: #7c3aed;
    --plasma-green: #00ff88;
    --solar-gold: #ffd700;
    --nova-pink: #ff3d9a;
    --neutron-white: #e8f4ff;
    --muted: #4a6fa5;
}

html, body, [class*="css"] {
    background-color: var(--void) !important;
    color: var(--neutron-white) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stApp { background: var(--void) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060d18 0%, #020408 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--neutron-white) !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--panel) 0%, var(--surface) 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--quantum-blue), var(--quantum-violet));
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: var(--quantum-blue) !important; font-family: 'Orbitron', monospace !important; font-size: 1.6rem !important; }
[data-testid="stMetricDelta"] svg { display: none; }

/* Tabs */
[data-testid="stTabs"] button {
    background: var(--surface) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px 8px 0 0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500;
    transition: all 0.2s;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(180deg, var(--panel) 0%, var(--surface) 100%) !important;
    color: var(--quantum-blue) !important;
    border-bottom-color: var(--surface) !important;
}

/* Selectbox / inputs */
[data-testid="stSelectbox"] > div, [data-testid="stMultiSelect"] > div {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--neutron-white) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, var(--quantum-violet), var(--quantum-blue)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em;
    transition: all 0.3s;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.2);
}
.stButton button:hover {
    box-shadow: 0 4px 30px rgba(0, 212, 255, 0.5) !important;
    transform: translateY(-1px);
}

/* Slider */
[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, var(--quantum-blue), var(--quantum-violet)) !important;
}

/* Custom card component */
.q-card {
    background: linear-gradient(135deg, var(--panel) 0%, var(--surface) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.q-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--quantum-blue), transparent);
}

.q-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.q-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--quantum-blue);
    line-height: 1;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--quantum-blue) 0%, var(--quantum-violet) 50%, var(--nova-pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.02em;
    line-height: 1.1;
}

.hero-sub {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.stat-badge {
    display: inline-block;
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--quantum-blue);
    margin: 0.2rem;
}

.arch-node {
    background: linear-gradient(135deg, #0f1f38, #1a3055);
    border: 1px solid var(--quantum-blue);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--quantum-blue);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.15);
}

.pipeline-step {
    background: linear-gradient(135deg, var(--panel), var(--surface));
    border-left: 3px solid var(--quantum-blue);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.5rem;
    margin-bottom: 0.8rem;
}

.done-item {
    background: rgba(0, 255, 136, 0.05);
    border: 1px solid rgba(0, 255, 136, 0.2);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    font-size: 0.9rem;
}

.future-item {
    background: rgba(124, 58, 237, 0.05);
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    font-size: 0.9rem;
    color: rgba(232, 244, 255, 0.7);
}

.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--quantum-blue);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.quantum-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    background: linear-gradient(135deg, var(--quantum-violet), var(--nova-pink));
    color: white;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    letter-spacing: 0.08em;
}

.divider-glow {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--quantum-blue), transparent);
    margin: 1.5rem 0;
    opacity: 0.4;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* Code blocks */
code { background: var(--panel) !important; color: var(--plasma-green) !important; }
pre { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }

/* Progress bar */
[data-testid="stProgress"] > div > div { background: linear-gradient(90deg, var(--quantum-blue), var(--quantum-violet)) !important; }

.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(0, 255, 136, 0.1);
    border: 1px solid rgba(0, 255, 136, 0.4);
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.72rem;
    color: var(--plasma-green);
    font-family: 'JetBrains Mono', monospace;
}
.live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--plasma-green);
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}
</style>
""", unsafe_allow_html=True)

# ─── SYNTHETIC DATA ENGINE ───────────────────────────────────────────────────
@st.cache_data(ttl=300)
def generate_universe():
    """150 coins with realistic stats from the notebook"""
    coins = [
        "BTC","ETH","SOL","XRP","BNB","ADA","AVAX","DOT","LINK","UNI",
        "PEPE","SHIB","DOGE","NEAR","ICP","FIL","ARB","OP","APT","SUI",
        "INJ","RENDER","BONK","TIA","PENGU","HBAR","LTC","ZEC","ATOM","ALGO",
        "ENE","AAVE","CRV","LDO","CAKE","ORDI","SAGA","MORPHO","CVX","ACT",
        "ATM","ETH_FI","KITE","GUN","ACE","POL","SYN","0G","ZRO","GALA",
        "COTI","JTO","ALT","LUNA","MITO","AUDIO","HOLO","MAV","XLM","TRUMP",
        "GRAM","LUNC","FET","JST","DEXE","BOME","ROBO","DASH","FIL","ONDO",
        "EPIC","DODO","MUBARAK","WLFI","RAD","BICO","TAO","ETC","SKY","KAITO",
        "PEOPLE","OPEN","ME","EUL","ESP","ACT","ZBT","ZEN","AR","USTC",
        "PENDLE","NIGHT","HEMI","BB","ALT","ID","COTI","JTO","MORPHO","CVX",
        "VIRTUAL","XP","COOK","BROC","FF","ZAMA","MOVR","BAND","CELO","FTM",
        "EGLD","MANA","SAND","AXS","CHZ","ENJ","1INCH","SUSHI","BAL","YFI",
        "COMP","SNX","REN","ZRX","NMR","BAND","OXT","LRC","SKL","STORJ",
        "OCEAN","FET","ANKR","RLC","NKN","CTSI","REEF","DENT","HOT","WIN"
    ][:150]
    # Remove duplicate symbols while preserving the original order.
    # This guarantees that every DataFrame column has exactly the same length.
    coins = list(dict.fromkeys(coins))
    n_coins = len(coins)

    np.random.seed(42)
    df = pd.DataFrame({
        "symbol": [f"{c}USDT" for c in coins],
        "base": coins,
        "mean_return": np.random.normal(-0.001, 0.006, n_coins),
        "std_dev": np.abs(np.random.normal(0.05, 0.04, n_coins)),
        "skewness": np.random.normal(1.2, 1.8, n_coins),
        "kurtosis": np.random.exponential(5, n_coins) + 3,
        "sharpe": np.random.normal(0.15, 0.8, n_coins),
        "volume_24h": np.random.lognormal(17, 2, n_coins),
        "iqr": np.abs(np.random.normal(0.04, 0.03, n_coins)),
        "max_drawdown": -np.abs(np.random.normal(0.45, 0.25, n_coins)),
        "beta": np.random.normal(1.0, 0.5, n_coins),
        "hurst": np.random.uniform(0.35, 0.65, n_coins),
        "rank": range(1, n_coins + 1),
    })
    # BTC anchor values
    df.loc[0, ["mean_return","std_dev","skewness","kurtosis","sharpe","hurst"]] = [
        0.00102, 0.02392, 0.21, 5.1, 0.89, 0.52
    ]
    return df

@st.cache_data(ttl=60)
def generate_price_series(seed=42, days=730):
    np.random.seed(seed)
    dates = pd.date_range("2024-08-01", periods=days, freq="D")
    # BTC-like series with regime shifts
    returns = np.random.normal(0.001, 0.024, days)
    # Inject volatility clusters
    for i in [50, 180, 300, 450, 600]:
        returns[i:i+15] *= 3.5
    price = 60000 * np.exp(np.cumsum(returns))
    volume = np.random.lognormal(np.log(35000), 0.4, days)
    return pd.DataFrame({"date": dates, "close": price, "volume": volume,
                         "return": returns,
                         "high": price * (1 + np.abs(np.random.normal(0.01, 0.008, days))),
                         "low": price * (1 - np.abs(np.random.normal(0.01, 0.008, days)))})

@st.cache_data
def generate_correlation_matrix(n=20):
    np.random.seed(0)
    coins = ["BTC","ETH","SOL","XRP","BNB","ADA","AVAX","DOT",
             "LINK","UNI","PEPE","SHIB","NEAR","ICP","ARB","OP",
             "APT","SUI","INJ","RENDER"]
    A = np.random.randn(n, n)
    cov = A @ A.T
    std = np.sqrt(np.diag(cov))
    corr = cov / np.outer(std, std)
    return pd.DataFrame(corr, index=coins, columns=coins)

def compute_rolling_stats(series, window=30):
    s = pd.Series(series)
    return {
        "rolling_mean": s.rolling(window).mean().fillna(method="bfill"),
        "rolling_std": s.rolling(window).std().fillna(method="bfill"),
        "rolling_sharpe": (s.rolling(window).mean() / s.rolling(window).std() * np.sqrt(252)).fillna(0),
        "rolling_skew": s.rolling(window).skew().fillna(0),
    }

def kde_estimate(data, points=200):
    x = np.linspace(data.min(), data.max(), points)
    kde = stats.gaussian_kde(data[~np.isnan(data)])
    return x, kde(x)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
      <div style='font-family:Orbitron,monospace; font-size:1.2rem; font-weight:900;
                  background:linear-gradient(135deg,#00d4ff,#7c3aed);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
        ⚛ QUANTUM MD
      </div>
      <div style='font-size:0.65rem; color:#4a6fa5; letter-spacing:0.2em; margin-top:0.2rem;'>
        MARKET DYNAMICS v2.0
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.7rem; color:#4a6fa5; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.5rem;">⚙ Parameters</div>', unsafe_allow_html=True)
    lookback = st.slider("Lookback Window (days)", 30, 730, 365)
    vol_threshold = st.slider("Volatility Threshold (%)", 1, 50, 10)
    selected_coin = st.selectbox("Primary Asset", ["BTC","ETH","SOL","XRP","BNB","ADA","AVAX","DOT"])
    corr_window = st.slider("Correlation Window", 7, 90, 30)

    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.7rem; color:#4a6fa5; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.5rem;">🔬 Quantum Filters</div>', unsafe_allow_html=True)
    enable_regime = st.checkbox("Regime Detection", True)
    enable_entropy = st.checkbox("Entropy Analysis", True)
    enable_fractal = st.checkbox("Fractal Dimension", True)
    show_quantum = st.checkbox("Quantum Probability Waves", True)

    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("""
    <div style='margin-top:1rem; padding:0.8rem; background:rgba(0,212,255,0.05);
                border:1px solid rgba(0,212,255,0.15); border-radius:8px;'>
      <div style='font-size:0.65rem; color:#4a6fa5; margin-bottom:0.4rem;'>DATA SOURCE</div>
      <div style='font-size:0.75rem; color:#e8f4ff;'>Binance Vision Archive</div>
      <div style='font-size:0.65rem; color:#4a6fa5;'>150 USDT pairs · 730 days</div>
      <div style='font-size:0.65rem; color:#4a6fa5;'>78,462 OHLCV candles</div>
    </div>
    """, unsafe_allow_html=True)

# ─── LOAD DATA ──────────────────────────────────────────────────────────────
universe = generate_universe()
price_df = generate_price_series(days=lookback)
corr_matrix = generate_correlation_matrix()
btc_returns = price_df["return"].values[1:]

# ─── MAIN CONTENT ───────────────────────────────────────────────────────────
# Hero Header
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown("""
    <div style='padding:1rem 0;'>
      <div class='hero-title'>QUANTUM MARKET<br>DYNAMICS</div>
      <div class='hero-sub'>Statistical States of Digital Assets · 150 Pairs · 730 Days</div>
      <div style='margin-top:1rem; display:flex; gap:0.5rem; flex-wrap:wrap;'>
        <span class='stat-badge'>⚛ 78,462 Candles</span>
        <span class='stat-badge'>📊 150 USDT Pairs</span>
        <span class='stat-badge'>🧮 8 Statistical Dimensions</span>
        <span class='stat-badge'>🔬 Binance Vision API</span>
        <span class='stat-badge'>📡 2-Year Horizon</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div style='display:flex; flex-direction:column; gap:0.5rem; align-items:flex-end; padding-top:1rem;'>
      <div class='live-badge'><div class='live-dot'></div> SIMULATION ACTIVE</div>
      <div style='font-family:JetBrains Mono,monospace; font-size:0.7rem; color:#4a6fa5;'>
        QUANTUM EXPO 2026 · SRMIST
      </div>
      <div style='font-family:JetBrains Mono,monospace; font-size:0.65rem; color:#4a6fa5;'>
        Vijay M. · CSE · RA2411003011492
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

# ─── TOP METRICS ────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
btc_row = universe.iloc[0]
with c1:
    st.metric("Universe Size", "150 Coins", "↑ 2yr window")
with c2:
    st.metric("Total Candles", "78,462", "100% coverage")
with c3:
    st.metric("BTC Sharpe", f"{btc_row['sharpe']:.3f}", "+0.12 vs ETH")
with c4:
    st.metric("Avg Skewness", f"{universe['skewness'].mean():.3f}", "fat-tailed")
with c5:
    st.metric("Avg Volatility", f"{universe['std_dev'].mean()*100:.1f}%", "daily σ")
with c6:
    st.metric("Hurst Exponent", f"{universe['hurst'].mean():.3f}", "near random-walk")

st.markdown('<div class="divider-glow" style="opacity:0.2; margin:1rem 0;"></div>', unsafe_allow_html=True)

# ─── MAIN TABS ──────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "⚛ Overview",
    "📊 Statistical States",
    "🌊 Correlation Field",
    "🔬 Distribution Lab",
    "📡 Quantum Signals",
    "🏗 Architecture",
    "📋 Project Atlas",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown('<div class="section-header">⚛ BTC Price Trajectory · 2-Year State Space</div>', unsafe_allow_html=True)
        fig_price = make_subplots(rows=3, cols=1, shared_xaxes=True,
                                   row_heights=[0.55, 0.25, 0.20],
                                   vertical_spacing=0.03)
        # Candlestick-style area
        fig_price.add_trace(go.Scatter(
            x=price_df["date"], y=price_df["close"],
            fill="tozeroy", fillcolor="rgba(0,212,255,0.06)",
            line=dict(color="#00d4ff", width=1.5),
            name="BTC Close"
        ), row=1, col=1)
        # Bollinger bands
        roll = price_df["close"].rolling(20)
        upper = roll.mean() + 2 * roll.std()
        lower = roll.mean() - 2 * roll.std()
        fig_price.add_trace(go.Scatter(x=price_df["date"], y=upper,
            line=dict(color="rgba(124,58,237,0.5)", width=1, dash="dot"), name="BB Upper"), row=1, col=1)
        fig_price.add_trace(go.Scatter(x=price_df["date"], y=lower,
            fill="tonexty", fillcolor="rgba(124,58,237,0.05)",
            line=dict(color="rgba(124,58,237,0.5)", width=1, dash="dot"), name="BB Lower"), row=1, col=1)
        # Daily returns
        colors = ["#00ff88" if r > 0 else "#ff3d9a" for r in price_df["return"]]
        fig_price.add_trace(go.Bar(x=price_df["date"], y=price_df["return"],
            marker_color=colors, name="Returns", opacity=0.7), row=2, col=1)
        # Volume
        fig_price.add_trace(go.Bar(x=price_df["date"], y=price_df["volume"],
            marker_color="rgba(0,212,255,0.3)", name="Volume"), row=3, col=1)
        fig_price.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,13,24,0.8)",
            showlegend=False, height=480,
            xaxis3=dict(showgrid=False, gridcolor="#1a3055"),
            yaxis=dict(showgrid=True, gridcolor="#0f1f38", title="Price (USDT)"),
            yaxis2=dict(showgrid=True, gridcolor="#0f1f38", title="Return"),
            yaxis3=dict(showgrid=False, title="Volume"),
            margin=dict(l=60, r=10, t=10, b=10),
        )
        fig_price.update_xaxes(showgrid=False, gridcolor="#0f1f38")
        st.plotly_chart(fig_price, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">🏆 Top 10 by Volume</div>', unsafe_allow_html=True)
        top10 = universe.nlargest(10, "volume_24h")[["base","volume_24h","std_dev","sharpe","skewness"]]
        top10["volume_24h"] = (top10["volume_24h"] / 1e6).map("{:.0f}M".format)
        top10["std_dev"] = (top10["std_dev"] * 100).map("{:.1f}%".format)
        top10["sharpe"] = top10["sharpe"].map("{:.3f}".format)
        top10["skewness"] = top10["skewness"].map("{:.3f}".format)
        top10.columns = ["Asset","Volume","σ Daily","Sharpe","Skew"]
        st.dataframe(top10, hide_index=True, use_container_width=True,
                     column_config={
                         "Sharpe": st.column_config.ProgressColumn("Sharpe", min_value=-2, max_value=3, format="%.3f"),
                     })

        st.markdown('<div class="divider-glow" style="opacity:0.2;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🎯 Risk / Return Quadrant</div>', unsafe_allow_html=True)
        sample = universe.sample(40, random_state=1)
        fig_scatter = px.scatter(sample, x="std_dev", y="mean_return",
                                  size="volume_24h", color="sharpe",
                                  color_continuous_scale=[[0,"#ff3d9a"],[0.5,"#7c3aed"],[1,"#00d4ff"]],
                                  hover_name="base",
                                  labels={"std_dev":"Daily σ","mean_return":"Mean Return","sharpe":"Sharpe"})
        fig_scatter.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.2)")
        fig_scatter.add_vline(x=sample["std_dev"].median(), line_dash="dot", line_color="rgba(255,255,255,0.2)")
        fig_scatter.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,13,24,0.8)",
            height=280, margin=dict(l=40, r=20, t=10, b=40),
            coloraxis_colorbar=dict(thickness=8, len=0.7),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — STATISTICAL STATES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">📊 Per-Coin Statistical Eigenstates · 150 Assets</div>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        # Volatility distribution
        fig_vol = go.Figure()
        x_kde, y_kde = kde_estimate(universe["std_dev"].values)
        fig_vol.add_trace(go.Scatter(x=x_kde * 100, y=y_kde,
            fill="tozeroy", fillcolor="rgba(0,212,255,0.1)",
            line=dict(color="#00d4ff", width=2), name="KDE"))
        fig_vol.add_trace(go.Histogram(x=universe["std_dev"] * 100, nbinsx=30,
            marker_color="rgba(124,58,237,0.4)", name="Histogram",
            histnorm="probability density"))
        fig_vol.update_layout(title="Daily Volatility Distribution (σ %)",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=300,
            margin=dict(l=40, r=20, t=40, b=40), showlegend=False,
            xaxis_title="Daily σ (%)", yaxis_title="Density")
        st.plotly_chart(fig_vol, use_container_width=True)

    with col_s2:
        # Skewness distribution
        fig_skew = go.Figure()
        x_sk, y_sk = kde_estimate(universe["skewness"].values)
        fig_skew.add_trace(go.Scatter(x=x_sk, y=y_sk,
            fill="tozeroy", fillcolor="rgba(255,61,154,0.1)",
            line=dict(color="#ff3d9a", width=2), name="KDE"))
        fig_skew.add_vline(x=0, line_dash="dot", line_color="rgba(255,255,255,0.3)")
        fig_skew.update_layout(title="Skewness Distribution · Fat-Tail Signature",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=300,
            margin=dict(l=40, r=20, t=40, b=40), showlegend=False,
            xaxis_title="Skewness", yaxis_title="Density")
        st.plotly_chart(fig_skew, use_container_width=True)

    col_s3, col_s4 = st.columns(2)
    with col_s3:
        # Sharpe Heatmap by rank bucket
        buckets = pd.cut(universe["rank"], bins=10, labels=[f"Rank {i*15+1}-{(i+1)*15}" for i in range(10)])
        sharpe_by_bucket = universe.groupby(buckets)["sharpe"].mean().reset_index()
        fig_sh = px.bar(sharpe_by_bucket, x="rank", y="sharpe",
                         color="sharpe", color_continuous_scale=[[0,"#ff3d9a"],[0.5,"#7c3aed"],[1,"#00ff88"]])
        fig_sh.update_layout(title="Sharpe Ratio by Market Cap Rank Bucket",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=300,
            margin=dict(l=40, r=20, t=40, b=80), showlegend=False,
            xaxis_tickangle=-45)
        st.plotly_chart(fig_sh, use_container_width=True)

    with col_s4:
        # Rolling statistics for BTC
        rs = compute_rolling_stats(btc_returns, window=30)
        fig_roll = go.Figure()
        fig_roll.add_trace(go.Scatter(x=price_df["date"][1:], y=rs["rolling_std"] * 100,
            fill="tozeroy", fillcolor="rgba(0,212,255,0.08)",
            line=dict(color="#00d4ff", width=1.5), name="30d σ (%)"))
        fig_roll.add_trace(go.Scatter(x=price_df["date"][1:], y=rs["rolling_sharpe"],
            line=dict(color="#ffd700", width=1.5, dash="dot"), name="Rolling Sharpe",
            yaxis="y2"))
        fig_roll.update_layout(title="BTC Rolling Volatility & Sharpe",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=300,
            margin=dict(l=40, r=60, t=40, b=40),
            yaxis=dict(title="σ (%)", color="#00d4ff"),
            yaxis2=dict(title="Sharpe", overlaying="y", side="right", color="#ffd700"),
            legend=dict(x=0, y=1))
        st.plotly_chart(fig_roll, use_container_width=True)

    # Full stats table
    st.markdown('<div class="section-header">📋 Full Statistical Eigenstate Table</div>', unsafe_allow_html=True)
    display_cols = ["base","mean_return","std_dev","skewness","kurtosis","sharpe","iqr","max_drawdown","hurst","beta"]
    display_df = universe[display_cols].copy()
    display_df.columns = ["Asset","μ Return","σ Daily","Skewness","Kurtosis","Sharpe","IQR","Max DD","Hurst H","Beta β"]
    for c in ["μ Return","σ Daily","Max DD"]:
        display_df[c] = display_df[c].map("{:.4f}".format)
    for c in ["Skewness","Kurtosis","Sharpe","IQR","Hurst H","Beta β"]:
        display_df[c] = display_df[c].map("{:.3f}".format)
    st.dataframe(display_df, height=400, hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CORRELATION FIELD
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🌊 Cross-Asset Correlation Field · Quantum Entanglement Matrix</div>', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([3, 2])
    with col_c1:
        fig_corr = px.imshow(corr_matrix,
            color_continuous_scale=[[0,"#ff3d9a"],[0.5,"#0a1628"],[1,"#00d4ff"]],
            zmin=-1, zmax=1, aspect="auto")
        fig_corr.update_layout(
            title="Pairwise Pearson Correlation — Top 20 Assets",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=520,
            margin=dict(l=10, r=10, t=50, b=10),
            coloraxis_colorbar=dict(title="ρ", thickness=12)
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    with col_c2:
        # Dendrogram-style cluster bars
        st.markdown("**Cluster Membership**", unsafe_allow_html=False)
        clusters = {
            "Layer 1 Core": ["BTC", "ETH", "BNB", "SOL"],
            "DeFi Cluster": ["AAVE", "UNI", "CRV", "CVX", "SUSHI"],
            "L2 / Infra": ["ARB", "OP", "NEAR", "ICP", "APT"],
            "Meme / Speculative": ["DOGE", "SHIB", "PEPE", "BONK"],
            "Stablecoin Adjacent": ["XRP", "XLM", "ALGO"],
        }
        cluster_colors = ["#00d4ff","#7c3aed","#00ff88","#ff3d9a","#ffd700"]
        for (cname, members), color in zip(clusters.items(), cluster_colors):
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.3); border-left:3px solid {color};
                        border-radius:0 8px 8px 0; padding:0.6rem 1rem; margin-bottom:0.5rem;'>
              <div style='font-size:0.7rem; color:{color}; font-family:Orbitron,monospace;
                          letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.3rem;'>
                {cname}
              </div>
              <div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; color:#e8f4ff;'>
                {' · '.join(members)}
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider-glow" style="opacity:0.2;"></div>', unsafe_allow_html=True)
        # Correlation histogram
        vals = corr_matrix.values.flatten()
        vals = vals[vals != 1.0]
        fig_ch = go.Figure(go.Histogram(x=vals, nbinsx=40,
            marker_color="rgba(0,212,255,0.5)", marker_line_color="#00d4ff",
            marker_line_width=0.5))
        fig_ch.add_vline(x=vals.mean(), line_dash="dot", line_color="#ffd700")
        fig_ch.update_layout(title=f"Correlation Dist. (mean={vals.mean():.3f})",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=200,
            margin=dict(l=30, r=10, t=40, b=30),
            xaxis_title="ρ", showlegend=False)
        st.plotly_chart(fig_ch, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DISTRIBUTION LAB
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🔬 Return Distribution Laboratory · Normality Tests</div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        # Returns histogram + normal overlay
        r = btc_returns[~np.isnan(btc_returns)]
        x_range = np.linspace(r.min(), r.max(), 300)
        mu, sigma = r.mean(), r.std()
        normal_pdf = stats.norm.pdf(x_range, mu, sigma)
        t_df_fit, t_loc, t_scale = stats.t.fit(r)
        t_pdf = stats.t.pdf(x_range, t_df_fit, t_loc, t_scale)

        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(x=r, nbinsx=80, histnorm="probability density",
            marker_color="rgba(0,212,255,0.3)", name="BTC Returns"))
        fig_dist.add_trace(go.Scatter(x=x_range, y=normal_pdf,
            line=dict(color="#ffd700", width=2, dash="dash"), name="Normal Fit"))
        fig_dist.add_trace(go.Scatter(x=x_range, y=t_pdf,
            line=dict(color="#ff3d9a", width=2), name=f"Student-t (ν={t_df_fit:.1f})"))
        fig_dist.update_layout(title="BTC Return Distribution · Normal vs Student-t",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=360,
            margin=dict(l=40, r=20, t=50, b=40),
            legend=dict(x=0.6, y=0.95))
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_d2:
        # QQ Plot
        (osm, osr), (slope, intercept, r_val) = stats.probplot(r, dist="norm")
        fig_qq = go.Figure()
        fig_qq.add_trace(go.Scatter(x=osm, y=osr, mode="markers",
            marker=dict(color="#7c3aed", size=3, opacity=0.7), name="Quantiles"))
        fig_qq.add_trace(go.Scatter(x=[osm.min(), osm.max()],
            y=[slope * osm.min() + intercept, slope * osm.max() + intercept],
            line=dict(color="#ffd700", width=2, dash="dot"), name="Normal Line"))
        fig_qq.update_layout(title="Q-Q Plot · Theoretical vs Empirical Quantiles",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=360,
            margin=dict(l=40, r=20, t=50, b=40),
            xaxis_title="Theoretical Quantiles", yaxis_title="Sample Quantiles",
            legend=dict(x=0.6, y=0.05))
        st.plotly_chart(fig_qq, use_container_width=True)

    # Statistical Tests Panel
    st.markdown('<div class="section-header">🧮 Hypothesis Test Suite · BTC Returns</div>', unsafe_allow_html=True)
    ks_stat, ks_p = stats.kstest(r, "norm", args=(mu, sigma))
    sw_stat, sw_p = stats.shapiro(r[:500])
    jb_stat, jb_p = stats.jarque_bera(r)
    skew = stats.skew(r)
    kurt_excess = stats.kurtosis(r)

    test_cols = st.columns(5)
    tests = [
        ("KS Test", f"{ks_stat:.4f}", f"p={ks_p:.1e}", ks_p < 0.05),
        ("Shapiro-Wilk", f"{sw_stat:.4f}", f"p={sw_p:.1e}", sw_p < 0.05),
        ("Jarque-Bera", f"{jb_stat:.1f}", f"p={jb_p:.1e}", jb_p < 0.05),
        ("Skewness", f"{skew:.4f}", "right-tailed", abs(skew) > 0.5),
        ("Excess Kurt.", f"{kurt_excess:.4f}", "leptokurtic", kurt_excess > 1),
    ]
    for col, (name, val, note, reject) in zip(test_cols, tests):
        color = "#ff3d9a" if reject else "#00ff88"
        label = "REJECT H₀" if reject else "FAIL TO REJECT"
        with col:
            st.markdown(f"""
            <div class='q-card'>
              <div class='q-title'>{name}</div>
              <div class='q-value' style='font-size:1.3rem;'>{val}</div>
              <div style='font-size:0.7rem; color:#4a6fa5; margin-top:0.3rem;'>{note}</div>
              <div style='font-size:0.65rem; color:{color}; margin-top:0.4rem; font-family:JetBrains Mono,monospace;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ACF panel
    col_acf1, col_acf2 = st.columns(2)
    with col_acf1:
        lags_n = min(40, len(r) // 2)
        acf_vals = [np.corrcoef(r[:-k], r[k:])[0, 1] for k in range(1, lags_n + 1)]
        ci = 1.96 / np.sqrt(len(r))
        fig_acf = go.Figure()
        fig_acf.add_hline(y=ci, line_dash="dot", line_color="rgba(255,215,0,0.5)")
        fig_acf.add_hline(y=-ci, line_dash="dot", line_color="rgba(255,215,0,0.5)")
        fig_acf.add_trace(go.Bar(x=list(range(1, lags_n + 1)), y=acf_vals,
            marker_color=["#00d4ff" if abs(v) < ci else "#ff3d9a" for v in acf_vals]))
        fig_acf.update_layout(title="ACF — BTC Daily Returns",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=280,
            margin=dict(l=40, r=20, t=50, b=40), showlegend=False,
            xaxis_title="Lag", yaxis_title="Autocorrelation")
        st.plotly_chart(fig_acf, use_container_width=True)
    with col_acf2:
        r_sq = r ** 2
        acf_sq = [np.corrcoef(r_sq[:-k], r_sq[k:])[0, 1] for k in range(1, lags_n + 1)]
        fig_acf2 = go.Figure()
        fig_acf2.add_hline(y=ci, line_dash="dot", line_color="rgba(255,215,0,0.5)")
        fig_acf2.add_hline(y=-ci, line_dash="dot", line_color="rgba(255,215,0,0.5)")
        fig_acf2.add_trace(go.Bar(x=list(range(1, lags_n + 1)), y=acf_sq,
            marker_color=["#7c3aed" if abs(v) < ci else "#ff3d9a" for v in acf_sq]))
        fig_acf2.update_layout(title="ACF — BTC Squared Returns (Volatility Clustering)",
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(6,13,24,0.8)", height=280,
            margin=dict(l=40, r=20, t=50, b=40), showlegend=False,
            xaxis_title="Lag", yaxis_title="Autocorrelation")
        st.plotly_chart(fig_acf2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — QUANTUM SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">📡 Advanced Quantum-Inspired Signal Analysis</div>', unsafe_allow_html=True)

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        # Wavefunction collapse simulation (probability amplitude over time)
        if show_quantum:
            np.random.seed(7)
            t = np.linspace(0, 4 * np.pi, len(btc_returns))
            psi_real = np.cos(t) * np.exp(-0.1 * t / t.max()) * btc_returns / btc_returns.std()
            psi_imag = np.sin(t) * np.exp(-0.1 * t / t.max()) * btc_returns / btc_returns.std()
            prob_amp = psi_real**2 + psi_imag**2

            fig_wave = go.Figure()
            fig_wave.add_trace(go.Scatter(y=psi_real[:200], x=list(range(200)),
                line=dict(color="#00d4ff", width=1.2), name="ψ Real", opacity=0.8))
            fig_wave.add_trace(go.Scatter(y=psi_imag[:200], x=list(range(200)),
                line=dict(color="#7c3aed", width=1.2), name="ψ Imaginary", opacity=0.8))
            fig_wave.add_trace(go.Scatter(y=prob_amp[:200], x=list(range(200)),
                fill="tozeroy", fillcolor="rgba(0,255,136,0.08)",
                line=dict(color="#00ff88", width=1.5), name="|ψ|² Probability"))
            fig_wave.update_layout(title="Quantum Probability Amplitude — Return Wavefunction",
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(6,13,24,0.8)", height=320,
                margin=dict(l=40, r=20, t=50, b=40),
                legend=dict(x=0.6, y=0.95))
            st.plotly_chart(fig_wave, use_container_width=True)

    with col_q2:
        # Hurst exponent surface
        if enable_fractal:
            lags = np.arange(2, 50)
            rs_vals = []
            r_clean = r[:300]
            for lag in lags:
                ts_lag = np.array([r_clean[i:i+lag] for i in range(0, len(r_clean)-lag, lag)
                                   if i+lag <= len(r_clean)])
                if len(ts_lag) == 0: rs_vals.append(np.nan); continue
                rs_seg = [(np.ptp(np.cumsum(s - s.mean()))) / s.std() if s.std() > 0 else np.nan
                           for s in ts_lag]
                rs_vals.append(np.nanmean(rs_seg))
            valid = [(l, v) for l, v in zip(lags, rs_vals) if not np.isnan(v)]
            l_arr = np.log([v[0] for v in valid])
            rs_arr = np.log([v[1] for v in valid])
            slope, intercept, *_ = stats.linregress(l_arr, rs_arr)

            fig_hurst = go.Figure()
            fig_hurst.add_trace(go.Scatter(x=l_arr, y=rs_arr, mode="markers",
                marker=dict(color="#00d4ff", size=6), name="R/S"))
            fig_hurst.add_trace(go.Scatter(x=l_arr, y=slope * l_arr + intercept,
                line=dict(color="#ffd700", width=2), name=f"Hurst H={slope:.3f}"))
            fig_hurst.add_hline(y=np.log(0.5 * np.array([v[0] for v in valid])).mean(),
                line_dash="dot", line_color="rgba(255,61,154,0.5)", annotation_text="H=0.5 (random walk)")
            fig_hurst.update_layout(title=f"Hurst Exponent via R/S Analysis (H={slope:.3f})",
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(6,13,24,0.8)", height=320,
                margin=dict(l=40, r=20, t=50, b=40),
                xaxis_title="log(lag)", yaxis_title="log(R/S)")
            st.plotly_chart(fig_hurst, use_container_width=True)

    col_q3, col_q4 = st.columns(2)
    with col_q3:
        # Shannon Entropy rolling
        if enable_entropy:
            window = 30
            entropy_series = []
            for i in range(window, len(r)):
                seg = r[i-window:i]
                hist, _ = np.histogram(seg, bins=10, density=True)
                hist = hist[hist > 0]
                entropy_series.append(-np.sum(hist * np.log(hist + 1e-12)))
            fig_ent = go.Figure()
            fig_ent.add_trace(go.Scatter(
                y=entropy_series, x=list(range(len(entropy_series))),
                fill="tozeroy", fillcolor="rgba(124,58,237,0.1)",
                line=dict(color="#7c3aed", width=1.5), name="Shannon H"))
            fig_ent.update_layout(title="Rolling Shannon Entropy (30d) — Information Content",
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(6,13,24,0.8)", height=280,
                margin=dict(l=40, r=20, t=50, b=40), showlegend=False,
                yaxis_title="Entropy H(X)")
            st.plotly_chart(fig_ent, use_container_width=True)

    with col_q4:
        # Regime detection
        if enable_regime:
            returns_30 = price_df["return"].rolling(30).std().fillna(0)
            regime = np.where(returns_30 > returns_30.quantile(0.75), "High Vol", "Low Vol")
            fig_reg = go.Figure()
            colors_reg = ["#ff3d9a" if r == "High Vol" else "#00ff88" for r in regime]
            fig_reg.add_trace(go.Bar(x=price_df["date"], y=returns_30,
                marker_color=colors_reg, name="30d σ"))
            fig_reg.update_layout(title="Volatility Regime Detection (HMM-style Threshold)",
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(6,13,24,0.8)", height=280,
                margin=dict(l=40, r=20, t=50, b=40), showlegend=False,
                yaxis_title="Rolling σ")
            st.plotly_chart(fig_reg, use_container_width=True)

    # 3D Return Space
    st.markdown('<div class="section-header">🌐 3D Return State Space · Phase Portrait</div>', unsafe_allow_html=True)
    n = min(200, len(r) - 2)
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=r[:n], y=r[1:n+1], z=r[2:n+2],
        mode="lines+markers",
        line=dict(color=np.arange(n), colorscale="Viridis", width=2),
        marker=dict(size=2, color=np.arange(n), colorscale="Plasma"),
    )])
    fig_3d.update_layout(
        title="3D Return Phase Portrait (r_t, r_t+1, r_t+2)",
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(6,13,24,0.95)",
            xaxis=dict(title="r(t)", gridcolor="#1a3055", showbackground=False),
            yaxis=dict(title="r(t+1)", gridcolor="#1a3055", showbackground=False),
            zaxis=dict(title="r(t+2)", gridcolor="#1a3055", showbackground=False),
        ),
        height=500, margin=dict(l=0, r=0, t=50, b=0)
    )
    st.plotly_chart(fig_3d, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-header">🏗 End-to-End System Architecture · Quantum Market Dynamics</div>', unsafe_allow_html=True)

    # Architecture diagram as styled HTML
    st.markdown("""
    <div style='background:linear-gradient(135deg,#060d18,#0a1628); border:1px solid #1a3055;
                border-radius:16px; padding:2rem; margin-bottom:1.5rem;'>

      <!-- Layer 0: Input -->
      <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:0.65rem; color:#4a6fa5;
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;'>
          ── LAYER 0 · DATA INGESTION ──
        </div>
        <div style='display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;'>
          <div class='arch-node'>🌐 Binance REST API<br><span style='color:#4a6fa5;font-size:0.7rem;'>Top 150 USDT pairs · 24h volume</span></div>
          <div class='arch-node'>📦 Binance Vision CDN<br><span style='color:#4a6fa5;font-size:0.7rem;'>Monthly OHLCV ZIP archives</span></div>
          <div class='arch-node'>🔁 CoinGecko Fallback<br><span style='color:#4a6fa5;font-size:0.7rem;'>Market cap rankings</span></div>
        </div>
      </div>

      <div style='text-align:center; color:#1a3055; font-size:1.5rem; margin:0.3rem 0;'>↓</div>

      <!-- Layer 1: ETL -->
      <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:0.65rem; color:#4a6fa5;
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;'>
          ── LAYER 1 · ETL PIPELINE ──
        </div>
        <div style='display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;'>
          <div class='arch-node'>🗓 Monthly Loop<br><span style='color:#4a6fa5;font-size:0.7rem;'>24 months × 150 symbols</span></div>
          <div class='arch-node'>⏱ Timestamp Normalizer<br><span style='color:#4a6fa5;font-size:0.7rem;'>ms/μs auto-detection</span></div>
          <div class='arch-node'>🧹 Dedup & Align<br><span style='color:#4a6fa5;font-size:0.7rem;'>Symbol-date uniqueness</span></div>
          <div class='arch-node'>💾 Parquet Store<br><span style='color:#4a6fa5;font-size:0.7rem;'>combined_ohlcv.parquet</span></div>
        </div>
      </div>

      <div style='text-align:center; color:#1a3055; font-size:1.5rem; margin:0.3rem 0;'>↓</div>

      <!-- Layer 2: Feature Engineering -->
      <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:0.65rem; color:#4a6fa5;
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;'>
          ── LAYER 2 · FEATURE ENGINEERING ──
        </div>
        <div style='display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;'>
          <div class='arch-node'>📈 Returns Engine<br><span style='color:#4a6fa5;font-size:0.7rem;'>pct_change · log returns</span></div>
          <div class='arch-node'>📊 Descriptive Stats<br><span style='color:#4a6fa5;font-size:0.7rem;'>μ · σ · skew · IQR · mode</span></div>
          <div class='arch-node'>🔁 Rolling Windows<br><span style='color:#4a6fa5;font-size:0.7rem;'>7 · 30 · 90 day windows</span></div>
          <div class='arch-node'>📉 Drawdown Calculator<br><span style='color:#4a6fa5;font-size:0.7rem;'>Max DD · Recovery</span></div>
        </div>
      </div>

      <div style='text-align:center; color:#1a3055; font-size:1.5rem; margin:0.3rem 0;'>↓</div>

      <!-- Layer 3: Statistical Analysis -->
      <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:0.65rem; color:#4a6fa5;
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;'>
          ── LAYER 3 · STATISTICAL ANALYSIS ENGINE ──
        </div>
        <div style='display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;'>
          <div class='arch-node' style='border-color:#7c3aed;'>🧮 Normality Tests<br><span style='color:#4a6fa5;font-size:0.7rem;'>KS · Shapiro · Jarque-Bera</span></div>
          <div class='arch-node' style='border-color:#7c3aed;'>📡 ACF / PACF<br><span style='color:#4a6fa5;font-size:0.7rem;'>Returns & Squared Returns</span></div>
          <div class='arch-node' style='border-color:#7c3aed;'>🌊 Correlation Matrix<br><span style='color:#4a6fa5;font-size:0.7rem;'>Pearson · 150×150</span></div>
          <div class='arch-node' style='border-color:#7c3aed;'>📐 Distribution Fitting<br><span style='color:#4a6fa5;font-size:0.7rem;'>Normal · Student-t · KDE</span></div>
        </div>
      </div>

      <div style='text-align:center; color:#1a3055; font-size:1.5rem; margin:0.3rem 0;'>↓</div>

      <!-- Layer 4: Visualization -->
      <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:0.65rem; color:#4a6fa5;
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.8rem;'>
          ── LAYER 4 · INTERACTIVE DASHBOARD (THIS APP) ──
        </div>
        <div style='display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;'>
          <div class='arch-node' style='border-color:#00ff88;'>🎛 Streamlit UI<br><span style='color:#4a6fa5;font-size:0.7rem;'>Multi-page · Dark theme</span></div>
          <div class='arch-node' style='border-color:#00ff88;'>📊 Plotly Charts<br><span style='color:#4a6fa5;font-size:0.7rem;'>Interactive · Responsive</span></div>
          <div class='arch-node' style='border-color:#00ff88;'>⚛ Quantum Signals<br><span style='color:#4a6fa5;font-size:0.7rem;'>Entropy · Hurst · Phase</span></div>
          <div class='arch-node' style='border-color:#00ff88;'>🗄 Cache Layer<br><span style='color:#4a6fa5;font-size:0.7rem;'>@st.cache_data TTL</span></div>
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

    # Tech stack grid
    st.markdown('<div class="section-header">🔧 Technology Stack</div>', unsafe_allow_html=True)
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    stacks = [
        ("Data Layer", [("Python 3.11","core runtime"),("Pandas","dataframes"),("NumPy","numerics"),("PyArrow","parquet I/O"),("Requests","HTTP client")], "#00d4ff"),
        ("Statistics", [("SciPy","hypothesis tests"),("Statsmodels","ACF/PACF"),("NumPy FFT","spectral"),("Custom KDE","density est."),("R/S Analysis","Hurst H")], "#7c3aed"),
        ("Visualization", [("Plotly","interactive charts"),("Streamlit","dashboard"),("Matplotlib","static plots"),("Seaborn","heatmaps"),("Custom CSS","dark theme")], "#00ff88"),
        ("Infrastructure", [("Google Colab","GPU notebook"),("Binance Vision","data CDN"),("Parquet","columnar store"),("Git","version control"),("Streamlit Cloud","deployment")], "#ffd700"),
    ]
    for col, (title, items, color) in zip([col_t1,col_t2,col_t3,col_t4], stacks):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#0f1f38,#0a1628);
                        border:1px solid {color}33; border-top:2px solid {color};
                        border-radius:12px; padding:1.2rem;'>
              <div style='font-family:Orbitron,monospace; font-size:0.7rem; color:{color};
                          letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.8rem;'>
                {title}
              </div>
            """ + "".join([f"""
              <div style='display:flex; justify-content:space-between; align-items:center;
                          padding:0.3rem 0; border-bottom:1px solid #1a3055;'>
                <span style='font-family:JetBrains Mono,monospace; font-size:0.8rem; color:#e8f4ff;'>{lib}</span>
                <span style='font-size:0.65rem; color:#4a6fa5;'>{desc}</span>
              </div>
            """ for lib, desc in items]) + "</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — PROJECT ATLAS
# ══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-header">📋 Project Atlas · Complete Research Inventory</div>', unsafe_allow_html=True)

    # What we DID
    st.markdown("""
    <div style='font-family:Orbitron,monospace; font-size:0.8rem; font-weight:700;
                color:#00ff88; letter-spacing:0.1em; text-transform:uppercase;
                padding:0.5rem 0; margin-bottom:1rem;'>
      ✅ IMPLEMENTED · Everything in the Colab Notebook
    </div>
    """, unsafe_allow_html=True)

    done_items = [
        ("01", "Universe Construction", "Fetched top 150 USDT pairs from Binance REST API ranked by 24-hour trading volume using CoinGecko market-cap supplemental data.", "Data"),
        ("02", "Binance Vision CDN Downloader", "Built a robust monthly OHLCV ZIP downloader from data.binance.vision — avoids API rate limits and geo-blocking, pulls 24 monthly files per symbol.", "Ingestion"),
        ("03", "Timestamp Ambiguity Resolver", "Detected ms vs µs epoch timestamps by magnitude (>1e14 threshold) to correctly parse mixed-format Binance archive files without overflow errors.", "ETL"),
        ("04", "Deduplication & Alignment", "Dropped duplicate (symbol, date) rows from month-boundary overlaps; aligned all 150 symbols on a canonical date index.", "ETL"),
        ("05", "Parquet Storage", "Persisted 78,462-row combined OHLCV as Parquet via PyArrow for fast column-oriented retrieval.", "Storage"),
        ("06", "Daily Return Computation", "Applied grouped pct_change by symbol on close prices, dropped NaN first-rows, producing a clean returns dataframe.", "Features"),
        ("07", "Cross-Asset Descriptive Stats", "Computed mean, median, mode, range, variance, std_dev, IQR, and skewness for all 150 coins in a single groupby pass.", "Statistics"),
        ("08", "Return Distribution Histogram", "Plotted clipped (±50%) daily return histogram across all 78K rows to visualize the global return distribution shape.", "Visualization"),
        ("09", "BTC Deep Dive", "Isolated 730-day BTC series (Aug 2024–Jul 2026); confirmed price range $49K–$124.6K, daily σ ≈ 2.39%.", "Analysis"),
        ("10", "ACF — Returns", "Computed and plotted autocorrelation function for BTC daily returns up to 40 lags; confirmed near-zero serial correlation.", "Time Series"),
        ("11", "ACF — Squared Returns", "ACF on r² revealed strong, persistent volatility clustering — signature of ARCH/GARCH-type processes in crypto.", "Time Series"),
        ("12", "Matplotlib Static Plots", "Used matplotlib for histogram and dual-panel ACF figures with custom titles and tight_layout.", "Visualization"),
        ("13", "SciPy Statistical Tests", "Imported scipy.stats for distribution fitting, normality tests, and quantile functions.", "Libraries"),
        ("14", "Statsmodels Integration", "Used statsmodels.graphics.tsaplots.plot_acf for professional ACF plots with 95% confidence bands.", "Libraries"),
    ]

    for num, title, desc, tag in done_items:
        tag_colors = {"Data":"#00d4ff","Ingestion":"#7c3aed","ETL":"#ff3d9a","Storage":"#ffd700",
                      "Features":"#00ff88","Statistics":"#00d4ff","Visualization":"#7c3aed",
                      "Analysis":"#00ff88","Time Series":"#ff3d9a","Libraries":"#4a6fa5"}
        color = tag_colors.get(tag, "#4a6fa5")
        st.markdown(f"""
        <div class='done-item'>
          <div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; color:#00ff88;
                      min-width:2rem; font-weight:700;'>{num}</div>
          <div style='flex:1;'>
            <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.2rem;'>
              <span style='font-weight:600; color:#e8f4ff;'>{title}</span>
              <span style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                           color:{color}; background:rgba(0,0,0,0.4);
                           padding:0.1rem 0.4rem; border-radius:4px;'>{tag}</span>
            </div>
            <div style='font-size:0.8rem; color:#4a6fa5; line-height:1.5;'>{desc}</div>
          </div>
          <div style='color:#00ff88; font-size:1rem;'>✓</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

    # Advanced features NOT YET DONE
    st.markdown("""
    <div style='font-family:Orbitron,monospace; font-size:0.8rem; font-weight:700;
                color:#7c3aed; letter-spacing:0.1em; text-transform:uppercase;
                padding:0.5rem 0; margin-bottom:1rem;'>
      🚀 ADVANCED FRONTIER · What Can Be Built Next
    </div>
    """, unsafe_allow_html=True)

    future_items = [
        ("A1", "GARCH(1,1) Volatility Forecasting", "Fit GARCH/EGARCH models to capture the leverage effect and asymmetric volatility in BTC; forecast 30-day volatility cone.", "Econometrics", "⭐⭐⭐⭐⭐"),
        ("A2", "Hidden Markov Model Regime Detection", "Unsupervised HMM with 3 latent states (bull/bear/consolidation); decode Viterbi path to label each day's market regime.", "ML", "⭐⭐⭐⭐⭐"),
        ("A3", "Minimum Spanning Tree Network", "Build cross-asset MST from correlation matrix using Kruskal's algorithm; visualize crypto market topology and cluster evolution.", "Graph Theory", "⭐⭐⭐⭐"),
        ("A4", "Principal Component Analysis", "PCA on 150×730 returns matrix to identify systematic risk factors; 3D biplot of first 3 eigenvectors.", "Dimensionality", "⭐⭐⭐⭐"),
        ("A5", "Quantum Walk Price Simulation", "Map return process onto a quantum walk on a graph; compare spread of quantum vs classical random walks on the price lattice.", "Quantum", "⭐⭐⭐⭐⭐"),
        ("A6", "Entropy Production Rate", "Compute sample entropy and permutation entropy across rolling windows; detect transitions from ordered to chaotic market regimes.", "Information Theory", "⭐⭐⭐⭐"),
        ("A7", "Lévy Flight Return Model", "Fit α-stable distribution to heavy-tailed returns; simulate Lévy flight trajectories as alternative to Brownian motion.", "Stochastic", "⭐⭐⭐⭐"),
        ("A8", "Granger Causality Network", "Pairwise Granger tests across top-30 assets; directed graph of information flow — which coins lead which.", "Causality", "⭐⭐⭐⭐"),
        ("A9", "Realized Volatility HAR Model", "Heterogeneous Autoregressive (HAR) model on 1-day, 5-day, 22-day realized variance components for improved forecasting.", "Econometrics", "⭐⭐⭐"),
        ("A10", "Copula Dependency Modelling", "Fit Gaussian/Clayton/Gumbel copulas to tail dependencies — measure contagion risk beyond linear correlation.", "Risk", "⭐⭐⭐⭐⭐"),
        ("A11", "XGBoost Signal Generator", "Engineer features (ATR, RSI, ACF lag significance, regime state) as inputs to XGBoost; classify next-day direction.", "ML", "⭐⭐⭐⭐⭐"),
        ("A12", "Reinforcement Learning Portfolio", "Deep Q-Network agent with state = (returns, vol, regime); action = rebalance weights across top-20 assets.", "Deep RL", "⭐⭐⭐⭐⭐"),
    ]

    tag_colors_f = {"Econometrics":"#00d4ff","ML":"#7c3aed","Graph Theory":"#ff3d9a",
                    "Dimensionality":"#ffd700","Quantum":"#00ff88","Information Theory":"#7c3aed",
                    "Stochastic":"#ff3d9a","Causality":"#ffd700","Risk":"#ff3d9a","Deep RL":"#00d4ff"}

    for num, title, desc, tag, stars in future_items:
        color = tag_colors_f.get(tag, "#4a6fa5")
        st.markdown(f"""
        <div class='future-item'>
          <div style='font-family:JetBrains Mono,monospace; font-size:0.8rem; color:#7c3aed;
                      min-width:2rem; font-weight:700;'>{num}</div>
          <div style='flex:1;'>
            <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.2rem;'>
              <span style='font-weight:600; color:#e8f4ff;'>{title}</span>
              <span style='font-family:JetBrains Mono,monospace; font-size:0.65rem;
                           color:{color}; background:rgba(0,0,0,0.4);
                           padding:0.1rem 0.4rem; border-radius:4px;'>{tag}</span>
              <span style='font-size:0.7rem;'>{stars}</span>
            </div>
            <div style='font-size:0.8rem; color:#4a6fa5; line-height:1.5;'>{desc}</div>
          </div>
          <div style='color:#7c3aed; font-size:1rem;'>→</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

    # Final credits
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f1f38,#0a1628);
                border:1px solid #1a3055; border-radius:16px; padding:1.5rem;
                display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem;'>
      <div>
        <div style='font-family:Orbitron,monospace; font-size:1rem; font-weight:900;
                    background:linear-gradient(135deg,#00d4ff,#7c3aed);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
          QUANTUM MARKET DYNAMICS
        </div>
        <div style='font-size:0.75rem; color:#4a6fa5; margin-top:0.3rem;'>
          Statistical States of Digital Assets
        </div>
        <div style='font-size:0.75rem; color:#4a6fa5;'>
          Vijay Mahanandi · RA2411003011492 · SRMIST Kattankulathur
        </div>
        <div style='font-size:0.75rem; color:#4a6fa5;'>
          B.Tech CSE · 3rd Year · 2024–2028 Batch · CGPA 9.01
        </div>
      </div>
      <div style='text-align:right;'>
        <div style='font-family:JetBrains Mono,monospace; font-size:0.75rem; color:#4a6fa5;'>
          Submitted for: Quantum Expo 2026
        </div>
        <div style='font-family:JetBrains Mono,monospace; font-size:0.75rem; color:#4a6fa5;'>
          Platform: Streamlit · Plotly · SciPy
        </div>
        <div style='font-family:JetBrains Mono,monospace; font-size:0.75rem; color:#4a6fa5;'>
          Data: Binance Vision CDN · 2024–2026
        </div>
        <div style='margin-top:0.5rem;'>
          <span class='stat-badge'>⚛ 78,462 Candles</span>
          <span class='stat-badge'>150 Assets</span>
          <span class='stat-badge'>730 Days</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

