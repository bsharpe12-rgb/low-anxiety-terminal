import os
import json
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & THEME INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Low-Anxiety Terminal",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom injection for a modern, sleek dark-mode trading interface
st.markdown("""
    <style>
        /* Base page background */
        .stApp {
            background-color: #0d0f12;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Modern, minimalist card container styling */
        .trader-card {
            background-color: #161a1f;
            border: 1px solid #242b35;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* High-contrast metrics */
        .metric-title {
            color: #64748b;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }
        
        .metric-value {
            color: #10b981; /* Glow green */
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        .metric-subtitle {
            color: #94a3b8;
            font-size: 0.9rem;
            margin-top: 4px;
        }

        /* Subtle button styling */
        .stButton>button {
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            border-radius: 6px;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            border-color: #10b981;
            color: #10b981;
            background-color: #0f172a;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOAD DATA FROM YOUR DATA ENGINE
# ==========================================
@st.cache_data(ttl=0)
def load_market_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(BASE_DIR, "business_bundle.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

data = load_market_data()

# ==========================================
# 3. HEADER
# ==========================================
st.markdown("<h1 style='text-align: center; font-weight: 800; color: #f8fafc;'>THE LOW-ANXIETY TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 40px;'>No noise. No panic. Automated, quiet compounding.</p>", unsafe_allow_html=True)

# ==========================================
# 4. LIVE MARKET VIBE (FROM YOUR CODE ENGINE)
# ==========================================
st.markdown("### 🟢 Today's Market Vibe")

if data and "daily_script" in data:
    vibe_text = data["daily_script"]
else:
    vibe_text = (
        "The S&P 500 is breathing normally. Smart money is quietly rotating "
        "out of overvalued sectors and scaling into high-yield, high-quality dividend "
        "compounders (SCHD / DGRO). No actions needed. Keep your automated deposits active."
    )

st.markdown(f"""
    <div class="trader-card">
        <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1; margin: 0;">
            "{vibe_text}"
        </p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. THE INTERACTIVE COMPOUNDING ENGINE
# ==========================================
st.markdown("### ⚙️ The Autopilot Calculator")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p style='color: #94a3b8; margin-bottom: 2px;'>Starting Balance ($)</p>", unsafe_allow_html=True)
    starting_balance = st.number_input("", min_value=0, value=1000, step=100, label_visibility="collapsed")
    
    st.markdown("<p style='color: #94a3b8; margin-top: 15px; margin-bottom: 2px;'>Monthly Deposit ($)</p>", unsafe_allow_html=True)
    monthly_deposit = st.number_input("", min_value=0, value=250, step=50, label_visibility="collapsed")

with col2:
    st.markdown("<p style='color: #94a3b8; margin-bottom: 2px;'>Time Horizon (Years)</p>", unsafe_allow_html=True)
    years = st.slider("", min_value=1, max_value=40, value=15, label_visibility="collapsed")
    
    st.markdown("<p style='color: #94a3b8; margin-top: 15px; margin-bottom: 2px;'>Assumed Return (%)</p>", unsafe_allow_html=True)
    annual_return = st.slider("", min_value=1, max_value=15, value=8, label_visibility="collapsed")

# Simple compound interest calculation: A = P(1 + r/n)^(nt) + PMT * [((1 + r/n)^(nt) - 1) / (r/n)]
r = annual_return / 100.0
n = 12
t = years
total_value = starting_balance * (1 + r/n)**(n*t)
for i in range(1, int(n*t) + 1):
    total_value += monthly_deposit * (1 + r/n)**(n*t - i)

total_invested = starting_balance + (monthly_deposit * 12 * years)
total_gained = max(0.0, total_value - total_invested)

st.markdown(f"""
    <div class="trader-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="metric-title">Projected Net Worth</div>
                <div class="metric-value">${total_value:,.2f}</div>
            </div>
            <div style="text-align: right;">
                <div class="metric-title" style="color: #64748b;">Free Passive Gains</div>
                <div class="metric-value" style="color: #38bdf8;">${total_gained:,.2f}</div>
            </div>
        </div>
        <div class="metric-subtitle" style="margin-top: 15px; font-size: 0.85rem; border-top: 1px solid #242b35; padding-top: 10px;">
            Based on a total out-of-pocket investment of <b>${total_invested:,.2f}</b> over {years} years.
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 6. FOOTER CALL-TO-ACTION
# ==========================================
st.markdown("<br><hr style='border: 0; border-top: 1px solid #242b35;'><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #64748b;'>Ready to take full control? Grab our completely free "
    "<a href='https://payhip.com' style='color: #10b981; text-decoration: none; font-weight: 600;'>Low-Anxiety Investing Blueprint</a> on Payhip.</p>", 
    unsafe_allow_html=True
)
