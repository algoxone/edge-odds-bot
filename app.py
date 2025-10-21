from flask import Flask, request, jsonify
import os, requests, math

app = Flask(__name__)
TOKEN = os.environ["TG_TOKEN"]  # we set this in Render dashboard

def ev(back, lay, comm=0.02):
    bp, lp = 1/back, 1/lay
    edge = (bp - lp)*100 - comm
    kelly = max(0, (bp - lp)/(1 - lp))/10
    return {"edge%": round(edge,2), "stake%": round(kelly,2)}

def send_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    msg_data = data.get("message", {})
    txt = msg_data.get("text", "").strip().split()
    chat_id = msg_data["chat"]["id"]
    if txt[0] == "/start":
        send_msg(chat_id, "Send me two odds: back_odds lay_odds  (e.g. 2.1 1.9)")
        return "ok"
    try:
        back, lay = map(float, txt)
        out = ev(back, lay)
        reply = f"Edge: {out['edge%']}%\nKelly stake: {out['stake%']}% of bank"
    except Exception:
        reply = "Format: back_odds lay_odds  (e.g. 2.5 2.3)"
    send_msg(chat_id, reply)
    return "ok"
