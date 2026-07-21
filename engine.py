import os
from dotenv import load_dotenv
load_dotenv()

import json
from datetime import datetime
import yfinance as yf
from google import genai

def fetch_market_data():
    """Fetches daily prices and percentage changes for key assets."""
    print("📈 Fetching today's market data...")
    # S&P 500 (SPY), Nasdaq (QQQ), and XRP (XRP-USD)
    tickers = {
        "S&P 500": "SPY",
        "Nasdaq": "QQQ",
        "XRP": "XRP-USD"
    }
    
    data_summary = {}
    for name, ticker in tickers.items():
        try:
            asset = yf.Ticker(ticker)
            # Fetch today's history (1 day interval)
            hist = asset.history(period="2d")
            if len(hist) >= 2:
                close_today = hist['Close'].iloc[-1]
                close_yesterday = hist['Close'].iloc[-2]
                pct_change = ((close_today - close_yesterday) / close_yesterday) * 100
                
                data_summary[name] = {
                    "ticker": ticker,
                    "price": round(close_today, 2),
                    "change": round(pct_change, 2)
                }
            else:
                # Fallback if 2 days of history aren't available
                info = asset.info
                price = info.get("regularMarketPrice") or info.get("previousClose") or 0.0
                change = info.get("regularMarketChangePercent", 0.0) * 100
                data_summary[name] = {
                    "ticker": ticker,
                    "price": round(price, 2),
                    "change": round(change, 2)
                }
        except Exception as e:
            print(f"⚠️ Failed to fetch data for {name}: {e}")
            data_summary[name] = {"ticker": ticker, "price": 0.0, "change": 0.0}
            
    return data_summary

def generate_video_script(market_data):
    """Generates a high-retention video script with a built-in terminal CTA."""
    print("🤖 Prompting Gemini for today's video script...")
    
    # Format market data into a clean text block for the prompt
    data_text = ""
    for asset, details in market_data.items():
        data_text += f"- {asset} ({details['ticker']}): ${details['price']} ({details['change']}% today)\n"
        
    # Initialize the correct Google GenAI client (picks up GEMINI_API_KEY automatically)
    client = genai.Client()
    
    prompt = f"""
You are an expert sports and finance creator. Write a highly engaging, fast-paced, 60-second video script analyzing today's market performance based on this data:

{data_text}

TONE & STYLE RULES:
1. Energetic, punchy, conversational, and completely low-anxiety. 
2. Speak directly to regular people trying to build long-term bags.
3. No complex jargon or dry financial reporting. Explain the "vibe" of the market today.
4. Keep the script under 130 words total so it comfortably fits a 60-second runtime.

CRITICAL RULE FOR THE OUTRO (MANDATORY CTA):
You must end the script with a very quick, natural, low-friction call-to-action (CTA) directing viewers to check out our free Streamlit market terminal (https://low-anxiety-terminal.streamlit.app/). Keep the CTA under 15 words.

Example Outro styles to adapt:
- "Check today's vibe and run your compound growth numbers on our free terminal—link is pinned!"
- "I updated today's numbers on our free, zero-panic market terminal. Tap the pinned link to calculate your bag."
- "Want to track this stress-free? Hit the pinned link for our free, no-nonsense market terminal."
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    return response.text.strip()

def main():
    # 1. Fetch live stock/crypto data
    market_data = fetch_market_data()
    
    # 2. Use Gemini to write the video script with the new CTA
    script = generate_video_script(market_data)
    
    # 3. Structure the data payload for the Streamlit App
    payload = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %I:%M %p EST"),
        "market_vibe": "Bullish" if any(details["change"] > 0 for details in market_data.values()) else "Bearish",
        "market_data": market_data,
        "daily_script": script
    }
    
    # 4. Save to business_bundle.json (Streamlit frontend pulls from this)
    print("💾 Saving updated bundle to business_bundle.json...")
    with open("business_bundle.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    # 5. Save script separately to daily_script.txt (for maker.py)
    print("📝 Saving daily video script to daily_script.txt...")
    with open("daily_script.txt", "w") as f:
        f.write(script)
        
    print("🚀 All pipeline jobs completed successfully!")

if __name__ == "__main__":
    main()
