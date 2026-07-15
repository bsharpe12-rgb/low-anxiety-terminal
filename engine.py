import os
import json
import random
import yfinance as yf
from google import genai

# ==========================================
# 1. LIVE SECTOR & INDEX SCRAPER
# ==========================================
def fetch_live_market_data():
    print("🔍 Fetching live market index & sector data...")
    
    market_metrics = {
        "market_trend": "flat",
        "sectors_jumped": [],
        "sectors_dipped": [],
        "top_etf": random.choice(["V-O-O", "V-T-I", "D-G-R-O", "S-C-H-D"])
    }
    
    # 1. Fetch S&P 500 Index Movement
    try:
        sp500 = yf.Ticker("^GSPC")
        today_data = sp500.history(period="1d")
        if not today_data.empty:
            open_price = today_data['Open'].iloc[0]
            close_price = today_data['Close'].iloc[0]
            pct_change = ((close_price - open_price) / open_price) * 100
            direction = "gained" if pct_change >= 0 else "lost"
            market_metrics["market_trend"] = f"{direction} roughly {abs(pct_change):.2f}%"
        else:
            market_metrics["market_trend"] = "remained relatively flat"
    except Exception as e:
        print(f"⚠️ S&P 500 data unavailable: {e}")
        market_metrics["market_trend"] = "shifted sideways"

    # 2. Fetch Dynamic Sector Jumps and Dips
    sectors = {
        "Technology (XLK)": "XLK",
        "Financials (XLF)": "XLF",
        "Energy (XLE)": "XLE",
        "Healthcare (XLV)": "XLV"
    }
    
    for sector_name, ticker in sectors.items():
        try:
            sec_ticker = yf.Ticker(ticker)
            sec_data = sec_ticker.history(period="1d")
            if not sec_data.empty:
                s_open = sec_data['Open'].iloc[0]
                s_close = sec_data['Close'].iloc[0]
                change = ((s_close - s_open) / s_open) * 100
                
                formatted_info = f"{sector_name} ({'+' if change >= 0 else ''}{change:.2f}%)"
                if change >= 0:
                    market_metrics["sectors_jumped"].append(formatted_info)
                else:
                    market_metrics["sectors_dipped"].append(formatted_info)
        except Exception as e:
            print(f"⚠️ Failed to pull sector {ticker}: {e}")

    # Fallbacks in case of network lag/market close issues
    if not market_metrics["sectors_jumped"]:
        market_metrics["sectors_jumped"] = ["Growth sectors"]
    if not market_metrics["sectors_dipped"]:
        market_metrics["sectors_dipped"] = ["Defensive sectors"]

    return market_metrics

# ==========================================
# 2. SECTOR-DETAIL SCRIPT GENERATOR
# ==========================================
def generate_daily_voiceover(market_data):
    print("🤖 Building highly-detailed sector analysis script via Gemini...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("⚠️ Warning: GEMINI_API_KEY environment variable not found.")
        return None
        
    client = genai.Client(api_key=api_key)
    
    movement = market_data.get("market_trend")
    jumps = ", ".join(market_data.get("sectors_jumped", []))
    dips = ", ".join(market_data.get("sectors_dipped", []))
    anchor_asset = market_data.get("top_etf")
    
    # Keeping the variety engine intact
    hooks = [
        "The stock market just wrapped another major trading session, and the movement behind the scenes was massive.",
        "If you saw your portfolio move today, you need to understand the real story of what just went down on Wall Street.",
        "We've got the closing bell numbers in, and today was a classic example of market rotation. Let's look at the charts."
    ]
    
    vibes = [
        "Speak like an elite, straight-shooting financial coach. Keep the pace intense, smart, and highly analytical.",
        "Be conversational, direct, and authoritative. Break down the data with high-value energy so it's simple to digest."
    ]
    
    chosen_hook = random.choice(hooks)
    chosen_vibe = random.choice(vibes)
    
    prompt = f"""
    You are a premium short-form financial educator. 
    Write an incredibly informative, high-energy 50-to-60-second video script explaining today's real stock market shifts.
    
    Tone Direction: {chosen_vibe}
    Hook to adapt: {chosen_hook}
    
    Live Market Data for Scripting:
    - Overall S&P 500 direction today: The market {movement}
    - Sectors that saw a JUMP (gained ground): {jumps}
    - Sectors that saw a DIP (lost ground): {dips}
    - Recommended Core Anchor ETF: {anchor_asset}
    
    Strict Script Structure Requirements:
    1. Hook the audience instantly using the Hook concept, stating exactly how the S&P 500 closed today and why.
    2. Deep Dive on Sectors: Clearly tell the audience which sectors saw a jump and which ones took a dip. Give a simple, beginner-friendly explanation of WHY this rotation happened (e.g., cooling inflation sparking a tech run, or money moving out of energy due to oil fluctuation).
    3. The Low-Anxiety Lesson: Teach beginners that these daily jumps and dips are completely normal market breathing cycles. Explain why panic-selling the dips or chasing the green jumps is a wealth-killing trap.
    4. Transition cleanly to the anchor fund: Tell them to ignore the day-to-day chaos and auto-compound their cash in {anchor_asset} instead. Explicitly pronounce the letters of the ticker: {anchor_asset}.
    5. Close with the exact call to action: "Head over to the link in my bio, grab my free Low-Anxiety Investing Blueprint, and let's automate your wealth building today."
    
    CRITICAL RULES:
    - Focus heavily on the sector trends (e.g., Tech, Energy, Financials) rather than individual stocks. DO NOT mention stock symbols like NVDA or AAPL.
    - Write smoothly as one continuous voiceover—no scene tags, speaker blocks, brackets, or notes. Only output the spoken text.
    - Keep it under 165 words so it remains punchy and fits a short-form video perfectly.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return None

# ==========================================
# 3. MASTER PIPELINE
# ==========================================
def main():
    print("🚀 Starting Data Engine Pipeline...")
    
    market_data = fetch_live_market_data()
    ai_script = generate_daily_voiceover(market_data)
    
    if ai_script:
        print(f"✅ Dynamic sector-focused script compiled for anchor: {market_data['top_etf']}!")
        market_data["daily_voiceover_script"] = ai_script
    else:
        print("🔄 Deploying structural fallback template...")
        ticker = market_data.get("top_etf", "V-O-O")
        market_data["daily_voiceover_script"] = (
            f"The stock market saw some major moves today. While certain growth sectors surged ahead, "
            f"defensive areas saw a brief dip as investors rotated capital. As a beginner, chasing these "
            f"daily jumps is a trap. Instead of trying to time the market, rely on consistent, broad-market "
            f"anchors like {ticker} to build secure, long-term wealth. Grab my free Low-Anxiety Investing "
            f"Blueprint at the link in my bio and let's automate your strategy today."
        )
    
    output_filename = "business_bundle.json"
    with open(output_filename, "w") as f:
        json.dump(market_data, f, indent=4)
        
    print(f"🎉 Success! Fresh live data package saved to {output_filename}.\n")

if __name__ == "__main__":
    main()
