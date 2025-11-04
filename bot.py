import os, requests

# Đọc từ GitHub Secrets (ENV)
TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("TWELVE_DATA_API_KEY") or os.getenv("API_KEY")

SYMBOL   = "EUR/USD"
INTERVAL = "4h"

def get_macd():
    url = (
        "https://api.twelvedata.com/macd"
        f"?symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}&format=JSON"
    )
    data = requests.get(url, timeout=20).json()
    # Twelve Data trả về {"values":[{"datetime":...,"macd":"...","signal":"..."}]}
    if "values" not in data:
        raise RuntimeError(f"Twelve Data error: {data}")
    v = data["values"][0]
    return float(v["macd"]), float(v["signal"])

def send(msg: str):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "parse_mode": "HTML", "text": msg},
        timeout=20
    )

def main():
    macd, signal = get_macd()
    status = "📈 BULLISH" if macd > signal else "📉 BEARISH"
    send(
        f"<b>MACD H4 Alert</b>\n"
        f"{SYMBOL}\n"
        f"Status: {status}\n"
        f"MACD={macd:.5f} | Signal={signal:.5f}"
    )

if __name__ == "__main__":
    main()
