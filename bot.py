import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "v11_titan_quantum_ai_final_core"

# Access Control
CREDENTIALS = {"user": "admin", "pass": "1234"}

HTML_V11 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITAN AI - QUANTUM TRADING CORE</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ff9d; --bg: #010409; --panel: #0d1117; --loss: #ff4d4d; --win: #00e676; }
        body { background: var(--bg); color: #c9d1d9; font-family: 'Share Tech Mono', monospace; margin: 0; padding: 10px; }
        
        /* Neon HUD Interface */
        .hud-header { display: flex; justify-content: space-between; align-items: center; background: var(--panel); padding: 15px; border-bottom: 2px solid var(--neon); box-shadow: 0 0 20px rgba(0,255,157,0.2); margin-bottom: 15px; border-radius: 10px; }
        .clock { font-size: 24px; color: var(--neon); text-shadow: 0 0 10px var(--neon); }
        .power-meter { font-size: 12px; background: #161b22; padding: 5px 10px; border: 1px solid #30363d; border-radius: 5px; }

        .grid-system { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        .box { background: var(--panel); padding: 15px; border-radius: 12px; border: 1px solid #30363d; text-align: center; }
        .box b { font-size: 22px; display: block; margin-top: 5px; }

        .terminal-core { background: linear-gradient(180deg, #0d1117 0%, #010409 100%); padding: 30px; border-radius: 30px; border: 1px solid #30363d; max-width: 480px; margin: auto; position: relative; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
        .terminal-core::after { content: "TITAN CORE ACTIVE"; position: absolute; top: 10px; right: 20px; font-size: 8px; color: var(--neon); opacity: 0.5; }

        h1 { font-size: 16px; text-align: center; color: var(--neon); letter-spacing: 4px; margin-bottom: 30px; }

        input, select { width: 100%; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #30363d; background: #010409; color: var(--neon); font-family: inherit; font-size: 16px; outline: none; box-sizing: border-box; }
        input:focus { border-color: var(--neon); box-shadow: 0 0 10px rgba(0,255,157,0.2); }

        .upload-area { border: 2px dashed #30363d; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0; cursor: pointer; transition: 0.3s; background: rgba(0,255,157,0.02); }
        .upload-area:hover { border-color: var(--neon); background: rgba(0,255,157,0.05); }

        .execute-btn { background: var(--neon); color: #000; border: none; width: 100%; padding: 20px; border-radius: 12px; font-weight: 900; font-size: 18px; cursor: pointer; box-shadow: 0 5px 25px rgba(0,255,157,0.3); transition: 0.3s; }
        .execute-btn:active { transform: scale(0.98); }

        /* Scanning Laser */
        .laser { width: 100%; height: 3px; background: var(--neon); position: absolute; left: 0; display: none; z-index: 100; box-shadow: 0 0 15px var(--neon); animation: scanMove 1.5s infinite; }
        @keyframes scanMove { 0% { top: 0; } 100% { top: 100%; } }

        .result-hud { margin-top: 30px; padding: 20px; background: #161b22; border-radius: 20px; border-left: 5px solid var(--neon); animation: slideUp 0.5s ease; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        .sig-display { font-size: 36px; font-weight: 900; text-align: center; margin: 10px 0; text-shadow: 0 0 20px rgba(255,255,255,0.2); }
        .logic-terminal { font-size: 12px; background: #010409; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-top: 15px; color: #8b949e; line-height: 1.6; }

        .footer-btns { display: flex; gap: 10px; margin-top: 20px; }
        .footer-btns a { flex: 1; text-decoration: none; text-align: center; padding: 15px; border-radius: 8px; font-weight: bold; color: white; transition: 0.3s; }
    </style>
</head>
<body>

{% if not session.get('titan_auth') %}
    <div style="height: 100vh; display: flex; align-items: center; justify-content: center;">
        <div class="terminal-core">
            <h1>AUTHENTICATION REQUIRED</h1>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="TITAN ID" required>
                <input type="password" name="p" placeholder="SECURITY KEY" required>
                <button type="submit" class="execute-btn">INITIATE SYSTEM</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="hud-header">
        <div class="clock" id="clock">00:00:00</div>
        <div class="power-meter">⚡ SYSTEM POWER: {{ session['credits'] }}%</div>
    </div>

    <div class="grid-system">
        <div class="box"><small>WINS</small><b style="color:var(--win)">{{ session['wins'] }}</b></div>
        <div class="box"><small>LOSSES</small><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
    </div>

    <div class="terminal-core">
        <div class="laser" id="laser"></div>
        <h1>QUANTUM ANALYZER V11</h1>
        <form method="POST" action="/analyze" enctype="multipart/form-data" onsubmit="document.getElementById('laser').style.display='block'">
            <input type="number" name="bal" placeholder="TOTAL BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
            
            <select name="mode">
                <option value="1M">1 MIN (ULTRA SCALPER)</option>
                <option value="5M">5 MIN (TREND SCANNER)</option>
                <option value="15M">15 MIN (STABLE CORE)</option>
            </select>

            <div class="upload-area" onclick="document.getElementById('fileIn').click()">
                <span id="fileTxt">📂 ATTACH MARKET DATA</span>
                <input type="file" id="fileIn" name="chart" accept="image/*" required style="display:none" onchange="document.getElementById('fileTxt').innerText='CHART CONNECTED ✅'">
            </div>
            
            <button type="submit" class="execute-btn">EXECUTE TITAN SCAN</button>
        </form>

        {% if sig %}
        <div class="result-hud">
            <div style="text-align:center; font-size:10px; color:var(--neon); letter-spacing: 2px;">PROBABILITY: {{acc}}%</div>
            <div class="sig-display" style="color: {{col}}">{{sig}}</div>
            <div style="text-align:center; margin-bottom:15px;">
                <span style="background:var(--neon); color:#000; padding:6px 15px; border-radius:4px; font-weight:bold; font-size:12px">INVEST: ${{trade}}</span>
            </div>
            <div class="logic-terminal">
                <b style="color:var(--neon)">[TITAN_LOGIC]:</b><br>{{log}}
            </div>
            <div class="footer-btns">
                <a href="/update/win" style="background:var(--win)">SUCCESS</a>
                <a href="/update/loss" style="background:var(--loss)">FAIL</a>
            </div>
        </div>
        {% endif %}
    </div>
    <div style="text-align:center; margin-top:20px; opacity: 0.3;"><a href="/logout" style="color:#fff; text-decoration:none; font-size:10px">SHUTDOWN CORE</a></div>
{% endif %}

<script>
    setInterval(() => {
        const d = new Date();
        document.getElementById('clock').innerText = d.toLocaleTimeString('en-GB');
    }, 1000);
</script>
</body>
</html>
'''

@app.before_request
def daily_sync():
    today = datetime.date.today().isoformat()
    if session.get('day') != today:
        session.update({'day': today, 'credits': 100, 'wins': 0, 'losses': 0})

@app.route('/')
def index(): return render_template_string(HTML_V11)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == CREDENTIALS['user'] and request.form['p'] == CREDENTIALS['pass']:
        session['titan_auth'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return "SYSTEM DEPLETED. WAIT FOR AUTOMATIC MIDNIGHT RECHARGE."
    
    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    mode = request.form.get('mode')
    
    # Simulating Deep AI Computation
    time.sleep(2) 
    
    patterns = ["Bullish Pin Bar", "Evening Star Pattern", "W-Shape Breakout", "V-Reversal Rejection"]
    logic_data = [
        f"AI Neural Net detected a '{random.choice(patterns)}' on the {mode} timeframe. Institutional buy-orders identified.",
        f"Significant divergence found on RSI and MACD. The market is reaching a critical {mode} exhaustion point.",
        f"Bollinger Band squeeze detected. High-velocity breakout expected in the next few candles."
    ]
    
    signals = [
        {"s": "TITAN CALL ⬆️", "c": "#00e676", "a": 99.2, "l": random.choice(logic_data), "p": 3},
        {"s": "TITAN PUT ⬇️", "c": "#ff4d4d", "a": 98.5, "l": random.choice(logic_data), "p": 2},
        {"s": "MTG-1 RECOVERY ⬆️", "c": "#00e676", "a": 94.7, "l": "Trend is slightly volatile. 1-step Martingale is active for safety.", "p": 5}
    ]
    
    res = random.choice(signals)
    trade_val = round((bal * res['p']) / 100, 2)
    
    return render_template_string(HTML_V11, sig=res['s'], col=res['c'], acc=res['a'], log=res['l'], trade=trade_val)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
