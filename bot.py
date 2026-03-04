import os, time, datetime
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "v8_ultra_advanced_pro_final"

# Default Credentials
USER_LOGIN = "admin"
PASS_LOGIN = "1234"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI TRADING BOT V8 - ULTRA PRO</title>
    <style>
        :root { --bg: #020617; --card: #0f172a; --accent: #38bdf8; --green: #22c55e; --red: #ef4444; }
        body { background: var(--bg); color: #f1f5f9; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; overflow-x: hidden; }
        
        /* Header & Stats */
        .top-nav { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #1e293b, #0f172a); padding: 15px; border-radius: 20px; border: 1px solid #334155; margin-bottom: 12px; }
        .clock { font-family: 'Courier New', monospace; font-size: 20px; color: var(--accent); text-shadow: 0 0 10px var(--accent); }
        .credit-badge { background: #1e293b; padding: 6px 12px; border-radius: 50px; border: 1px solid #38bdf8; font-size: 13px; }

        .stat-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .stat-card { background: var(--card); padding: 15px; border-radius: 18px; text-align: center; border: 1px solid #1e293b; position: relative; }
        .win-count { color: var(--green); font-size: 24px; font-weight: 800; }
        .loss-count { color: var(--red); font-size: 24px; font-weight: 800; }

        /* Main Form */
        .glass-panel { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(10px); padding: 25px; border-radius: 30px; border: 1px solid #334155; max-width: 450px; margin: auto; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        h2 { text-align: center; font-size: 22px; margin-bottom: 20px; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; }
        
        input { width: 100%; padding: 14px; margin: 10px 0; border-radius: 12px; border: 1px solid #334155; background: #020617; color: white; outline: none; transition: 0.3s; box-sizing: border-box; }
        input:focus { border-color: var(--accent); box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }

        /* Mode Selector */
        .mode-selector { display: flex; gap: 10px; margin: 15px 0; }
        .mode-selector label { flex: 1; text-align: center; padding: 12px; border-radius: 12px; border: 1px solid #334155; cursor: pointer; transition: 0.3s; font-weight: bold; font-size: 13px; }
        .mode-selector input[type="radio"]:checked + span { background: var(--accent); color: #000; display: block; width: 100%; height: 100%; border-radius: 8px; margin-top: -8px; padding-top: 8px; }

        /* Buttons */
        .upload-area { position: relative; background: #1e293b; border: 2px dashed #38bdf8; border-radius: 15px; padding: 20px; text-align: center; margin: 15px 0; cursor: pointer; }
        .scan-btn { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white; border: none; width: 100%; padding: 18px; border-radius: 15px; font-weight: 800; font-size: 16px; cursor: pointer; transition: 0.4s; }
        .scan-btn:active { transform: scale(0.95); }

        /* Result Area */
        .result-box { margin-top: 25px; padding: 20px; background: #020617; border-radius: 20px; border: 1px solid #334155; animation: fadeIn 0.5s ease; }
        .signal { font-size: 28px; font-weight: 900; margin: 10px 0; text-align: center; }
        .logic { font-size: 13px; color: #94a3b8; background: #0f172a; padding: 12px; border-radius: 12px; border-left: 4px solid var(--accent); }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .wl-btns { display: flex; gap: 10px; margin-top: 15px; }
        .wl-btns a { flex: 1; text-decoration: none; text-align: center; padding: 10px; border-radius: 10px; color: white; font-weight: bold; }
    </style>
</head>
<body>

{% if not session.get('logged_in') %}
    <div style="height: 100vh; display: flex; align-items: center; justify-content: center;">
        <div class="glass-panel">
            <h2>🔒 AI BOT LOGIN</h2>
            <form method="POST" action="/login">
                <input type="text" name="user" placeholder="ব্যবহারকারীর নাম" required>
                <input type="password" name="pass" placeholder="পাসওয়ার্ড" required>
                <button type="submit" class="scan-btn">লগইন করুন</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="top-nav">
        <div class="clock" id="clock">00:00:00</div>
        <div class="credit-badge">⚡ ক্রেডিট: <span id="cr">{{ session['credits'] }}</span>/100</div>
    </div>

    <div class="stat-container">
        <div class="stat-card">
            <span style="font-size: 12px; color: #94a3b8;">বিজয় (WIN)</span><br>
            <span class="win-count">{{ session['wins'] }}</span>
        </div>
        <div class="stat-card">
            <span style="font-size: 12px; color: #94a3b8;">পরাজয় (LOSS)</span><br>
            <span class="loss-count">{{ session['losses'] }}</span>
        </div>
    </div>

    <div class="glass-panel">
        <h2>Market Scanner V8</h2>
        <form method="POST" action="/analyze" enctype="multipart/form-data">
            <input type="number" name="balance" placeholder="আপনার ব্যালেন্স লিখুন ($)" required value="{{ session.get('last_bal', '') }}">
            
            <div class="mode-selector">
                <label><input type="radio" name="tm" value="1m" checked style="display:none"><span>1 MIN</span></label>
                <label><input type="radio" name="tm" value="5m" style="display:none"><span>5 MIN</span></label>
            </div>

            <div class="upload-area" onclick="document.getElementById('f').click()">
                <span id="fn">📁 গ্যালারি থেকে চার্ট নিন</span>
                <input type="file" id="f" name="chart" accept="image/*" required style="display:none" onchange="document.getElementById('fn').innerText='Chart Selected ✅'">
            </div>
            
            <button type="submit" class="scan-btn">AI এনালাইসিস শুরু করুন</button>
        </form>

        {% if sig %}
        <div class="result-box">
            <div style="text-align: center; font-size: 12px; color: var(--accent);">AI একুরেসি: {{acc}}%</div>
            <div class="signal" style="color: {{col}}">{{sig}}</div>
            <p style="text-align: center;">💰 ব্যালেন্স থেকে <b>{{perc}}%</b> ব্যবহার করুন</p>
            <div class="logic"><b>AI লজিক:</b> {{log}}</div>
            
            <div class="wl-btns">
                <a href="/stat/win" style="background: var(--green);">WIN ✅</a>
                <a href="/stat/loss" style="background: var(--red);">LOSS ❌</a>
            </div>
        </div>
        {% endif %}
    </div>
    <p style="text-align: center;"><a href="/logout" style="color: #475569; font-size: 12px; text-decoration: none;">Logout System</a></p>
{% endif %}

<script>
    function clock() {
        const d = new Date();
        document.getElementById('clock').innerText = d.getHours().toString().padStart(2,'0') + ":" + 
            d.getMinutes().toString().padStart(2,'0') + ":" + d.getSeconds().toString().padStart(2,'0');
    }
    setInterval(clock, 1000); clock();
</script>
</body>
</html>
'''

@app.before_request
def check_reset():
    today = datetime.date.today().isoformat()
    if session.get('last_day') != today:
        session['last_day'] = today
        session['credits'] = 100
        session['wins'] = 0
        session['losses'] = 0

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    if request.form['user'] == USER_LOGIN and request.form['pass'] == PASS_LOGIN:
        session['logged_in'] = True
        return redirect('/')
    return "ভুল পাসওয়ার্ড!"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return "আজকের লিমিট শেষ! রাত ১২টার পর আবার আসুন।"
    
    session['credits'] -= 1
    session['last_bal'] = request.form['balance']
    mode = request.form.get('tm')
    
    # Advanced AI Logic Simulation
    import random
    options = [
        {"sig": "STRONG CALL ⬆️", "col": "#22c55e", "acc": 98.2, "log": f"মার্কেট {mode} চার্টে সাপোর্ট জোন থেকে রিজেকশন নিয়েছে। RSI ইনডিকেটর বুলিশ মোডে আছে।", "p": 2},
        {"sig": "STRONG PUT ⬇️", "col": "#ef4444", "acc": 97.5, "log": f"রেজিস্ট্যান্স লেভেলে সেলিং প্রেসার বেশি। {mode} ক্যান্ডেলস্টিক প্যাটার্ন অনুযায়ী মার্কেট নিচে নামবে।", "p": 3},
        {"sig": "CALL (MTG-1) ⬆️", "col": "#22c55e", "acc": 88.4, "log": "মার্কেট কিছুটা সাইডওয়ে। প্রথম ট্রেড লস হলে ১-ধাপ মার্টিঙ্গেল ব্যবহার করুন।", "p": 5}
    ]
    res = random.choice(options)
    return render_template_string(HTML_TEMPLATE, sig=res['sig'], col=res['col'], acc=res['acc'], log=res['log'], perc=res['p'])

@app.route('/stat/<res>')
def stat(res):
    if res == 'win': session['wins'] = session.get('wins', 0) + 1
    else: session['losses'] = session.get('losses', 0) + 1
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
