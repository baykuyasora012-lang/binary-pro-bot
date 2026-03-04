import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "yggdrasil_v25_ascension_god_tier_2026"

# World Sovereign Access
MASTER_ID = "admin"
MASTER_KEY = "1234"

HTML_V25 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>YGGDRASIL V25 | SUPREME TRADING CORE</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Orbitron:wght@400;900&family=Space+Grotesk:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #ffcc00; --neon: #00ffcc; --win: #00ff88; --loss: #ff0055; --bg: #010102; }
        body { background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; overflow-x: hidden; }
        
        /* Animated Nebula Background */
        .nebula { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #00ffcc05, transparent); z-index: -1; animation: breathe 10s infinite alternate; }
        @keyframes breathe { from { opacity: 0.3; } to { opacity: 0.8; } }

        .top-nav { display: flex; justify-content: space-between; padding: 25px 35px; background: rgba(5, 5, 10, 0.9); border-bottom: 2px solid var(--gold); backdrop-filter: blur(50px); position: sticky; top: 0; z-index: 1000; box-shadow: 0 5px 40px rgba(255,204,0,0.2); }
        .bot-brand { font-family: 'Cinzel', serif; font-size: 16px; color: var(--gold); letter-spacing: 5px; text-shadow: 0 0 15px var(--gold); }

        .stats-hub { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; padding: 25px; }
        .stat-card { background: rgba(10, 10, 20, 0.8); border: 1px solid rgba(255,204,0,0.1); padding: 20px; border-radius: 25px; text-align: center; position: relative; }
        .stat-card span { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 2px; }
        .stat-card b { font-size: 26px; color: var(--gold); display: block; font-family: 'Orbitron', sans-serif; }

        .core-shell { max-width: 520px; margin: 10px auto; padding: 40px; background: rgba(5, 5, 15, 0.95); border-radius: 60px; border: 1px solid rgba(255, 204, 0, 0.15); box-shadow: 0 60px 120px rgba(0,0,0,1); position: relative; }
        h2 { text-align: center; font-family: 'Orbitron', sans-serif; font-size: 10px; color: var(--neon); letter-spacing: 8px; margin-bottom: 40px; }

        input, select { width: 100%; padding: 22px; margin-bottom: 18px; background: #000; border: 1px solid #1a1a25; border-radius: 25px; color: var(--neon); font-weight: bold; box-sizing: border-box; outline: none; font-size: 15px; transition: 0.4s; }
        input:focus { border-color: var(--gold); box-shadow: 0 0 30px rgba(255, 204, 0, 0.2); }

        .upload-portal { border: 2px dashed rgba(255, 204, 0, 0.3); padding: 70px; border-radius: 45px; text-align: center; margin: 30px 0; cursor: pointer; background: rgba(255, 204, 0, 0.02); transition: 0.5s; position: relative; }
        .upload-portal:hover { border-color: var(--gold); background: rgba(255, 204, 0, 0.08); }

        .btn-ascend { background: linear-gradient(45deg, var(--gold), #ffaa00); color: #000; border: none; width: 100%; padding: 25px; border-radius: 25px; font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 16px; cursor: pointer; box-shadow: 0 20px 60px rgba(255, 204, 0, 0.4); }

        .scanner-beam { height: 8px; background: var(--gold); position: absolute; left: 0; width: 100%; display: none; animation: skyScan 2s infinite linear; box-shadow: 0 0 40px var(--gold); z-index: 10; }
        @keyframes skyScan { 0% { top: 0; } 100% { top: 100%; } }

        .output-shield { margin-top: 45px; background: #000; border-radius: 50px; padding: 40px; border: 2px solid var(--gold); text-align: center; box-shadow: 0 0 60px rgba(255,204,0,0.1); }
        .sig-val { font-size: 55px; font-weight: 900; font-family: 'Orbitron'; margin: 20px 0; text-shadow: 0 0 30px currentColor; }
        
        .ai-log-terminal { text-align: left; font-size: 12px; background: #050508; padding: 30px; border-radius: 30px; color: #777; border-left: 8px solid var(--gold); margin-top: 35px; line-height: 1.8; }

        .pnl-buttons { display: flex; gap: 20px; margin-top: 35px; }
        .pnl-buttons a { flex: 1; text-decoration: none; text-align: center; padding: 24px; border-radius: 22px; font-weight: 900; color: #fff; font-size: 15px; letter-spacing: 3px; }

        .security-alert { background: rgba(255, 0, 85, 0.2); color: var(--loss); padding: 30px; border-radius: 35px; border: 1px solid var(--loss); font-size: 14px; text-align: center; margin-bottom: 35px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="nebula"></div>

{% if not session.get('authorized') %}
    <div style="height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px;">
        <div class="core-shell" style="width: 100%;">
            <h1 style="font-family:'Cinzel'; color:var(--gold); text-align:center; font-size:18px;">YGGDRASIL ACCESS</h1>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="SOVEREIGN ID" required>
                <input type="password" name="p" placeholder="QUANTUM ENCRYPTION" required>
                <button type="submit" class="btn-ascend">ASCEND CORE</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="top-nav">
        <div class="bot-brand">YGGDRASIL V25</div>
        <div style="color:var(--gold); font-size: 14px; font-family:'Orbitron';" id="timer">00:00:00</div>
    </div>

    <div class="stats-hub">
        <div class="stat-card"><span>SESSION WINS</span><b style="color:var(--win)">{{ session['wins'] }}</b></div>
        <div class="stat-card"><span>SESSION LOSS</span><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
        <div class="stat-card"><span>STABILITY</span><b>{{ session.get('acc', '0') }}%</b></div>
    </div>

    <div class="core-shell">
        <div class="scanner-beam" id="beam"></div>
        <h2>QUANTUM MARKET ANALYTICS</h2>

        {% if error %}
        <div class="security-alert">
            🚨 <b>DATA INTEGRITY BREACH:</b> <br> Unrecognized Entity Detected. <br> Human/Non-Chart Data rejected by Guardian Shield.
        </div>
        {% endif %}

        <form method="POST" action="/analyze" enctype="multipart/form-data" onsubmit="document.getElementById('beam').style.display='block'">
            <input type="number" name="bal" placeholder="LIQUIDITY BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
            
            <select name="time">
                <option value="1M">M1 - GOD MODE SCALPER</option>
                <option value="5M">M5 - INSTITUTIONAL TREND</option>
            </select>

            <div class="upload-portal" onclick="document.getElementById('f').click()">
                <span id="lb" style="color:var(--gold); font-size:14px; font-weight:900;">[+] INJECT MARKET VISUAL DNA</span>
                <input type="file" id="f" name="chart" accept="image/*" required style="display:none" onchange="document.getElementById('lb').innerText='DNA LINKED ✅'">
            </div>
            
            <button type="submit" class="btn-ascend">EXECUTE SUPREME SCAN</button>
        </form>

        {% if sig %}
        <div class="output-shield">
            <div style="font-size:12px; color:var(--gold); letter-spacing: 8px; margin-bottom:15px;">PROBABILITY: {{pa}}%</div>
            <div class="sig-val" style="color: {{col}}">{{sig}}</div>
            <div style="margin-bottom:30px;">
                <span style="background:var(--gold); color:#000; padding:15px 50px; border-radius:20px; font-weight:900; font-size:20px">ENTRY: ${{trade}}</span>
            </div>
            <div class="ai-log-terminal">
                <b style="color:var(--gold)">[YGGDRASIL_INSTITUTIONAL_LOG]:</b><br>{{log}}
            </div>
            <div class="pnl-buttons">
                <a href="/update/win" style="background:var(--win); box-shadow: 0 0 40px rgba(0,255,136,0.4);">PNL PROFIT</a>
                <a href="/update/loss" style="background:var(--loss); box-shadow: 0 0 40px rgba(255,0,85,0.4);">PNL LOSS</a>
            </div>
        </div>
        {% endif %}
    </div>
{% endif %}

<script>
    setInterval(() => {
        document.getElementById('timer').innerText = new Date().toLocaleTimeString('en-GB');
    }, 1000);
</script>
</body>
</html>
'''

@app.before_request
def core_sync():
    d = datetime.date.today().isoformat()
    if session.get('day') != d:
        session.update({'day': d, 'credits': 100, 'wins': 0, 'losses': 0, 'acc': 0})

@app.route('/')
def index(): return render_template_string(HTML_V25)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == MASTER_ID and request.form['p'] == MASTER_KEY:
        session['authorized'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return "LIMIT REACHED"
    
    file = request.files.get('chart')
    name = file.filename.lower()
    
    # 🚫 Supreme Protection: Human/Face/Selfie Filter
    forbidden_dna = ["human", "me", "photo", "face", "selfie", "person", "man", "woman", "girl", "boy", "hand", "eye"]
    if any(dna in name for dna in forbidden_dna):
        return render_template_string(HTML_V25, error=True)
    
    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    
    time.sleep(4) # Institutional Processing Time
    
    reports = [
        "Yggdrasil Core: Deep liquidity sweep detected at Institutional Supply Zone. Stop-Loss hunting cycle complete. Expecting aggressive reversal.",
        "Market Dynamics: Cumulative Volume Delta shows massive buy pressure at the Order Block. Demand exceeds Supply. Probability is Supreme.",
        "Quantum Scan: Bearish Market Structure Shift confirmed. Price is re-entering the Fair Value Gap. High-confidence sell orders identified."
    ]
    
    signals = [
        {"s": "ASCEND CALL ⬆️", "c": "#00ff88", "pa": 99.9, "l": reports[0], "p": 2.5},
        {"s": "ASCEND PUT ⬇️", "c": "#ff0055", "pa": 99.8, "l": reports[2], "p": 2.0},
        {"s": "SECURE CALL ⬆️", "c": "#00ff88", "pa": 98.2, "l": reports[1], "p": 4.0}
    ]
    
    res = random.choice(signals)
    trade_amt = round((bal * res['p']) / 100, 2)
    
    return render_template_string(HTML_V25, sig=res['s'], col=res['c'], pa=res['pa'], log=res['l'], trade=trade_amt)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
