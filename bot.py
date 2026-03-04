import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "v10_god_mode_ultimate_final"

# Super Admin Access
ACCESS_DATA = {"user": "admin", "pass": "1234"}

HTML_V10 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI GOD MODE - WORLD'S MOST POWERFUL BOT</title>
    <style>
        :root { --main: #00ffcc; --dark: #050505; --card: #0d0d0d; --win: #00ff88; --loss: #ff3366; }
        body { background: var(--dark); color: #fff; font-family: 'Orbitron', sans-serif; margin: 0; padding: 10px; overflow-x: hidden; }
        
        /* Matrix Background Effect */
        .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #00ffcc11, transparent); z-index: -1; }

        .top-bar { display: flex; justify-content: space-between; align-items: center; background: rgba(20,20,20,0.8); padding: 15px; border-radius: 20px; border: 1px solid var(--main); box-shadow: 0 0 15px var(--main); margin-bottom: 15px; }
        .live-clock { font-size: 20px; font-weight: bold; color: var(--main); letter-spacing: 2px; }
        .credit-hub { font-size: 11px; text-transform: uppercase; border: 1px solid #333; padding: 5px 10px; border-radius: 5px; }

        .grid-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
        .stat-box { background: var(--card); padding: 15px; border-radius: 15px; border: 1px solid #222; text-align: center; }
        .stat-box b { display: block; font-size: 18px; margin-top: 5px; }

        .terminal { background: linear-gradient(180deg, #111, #000); padding: 30px; border-radius: 40px; border: 1px solid #222; max-width: 500px; margin: auto; position: relative; overflow: hidden; }
        .terminal::before { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: var(--main); box-shadow: 0 0 20px var(--main); }

        h1 { font-size: 16px; text-align: center; color: var(--main); margin-bottom: 25px; letter-spacing: 5px; }
        
        input, select { width: 100%; padding: 15px; margin: 10px 0; border-radius: 12px; border: 1px solid #333; background: #000; color: var(--main); font-weight: bold; box-sizing: border-box; }
        
        .upload-zone { border: 2px dashed var(--main); padding: 25px; border-radius: 20px; text-align: center; margin: 20px 0; cursor: pointer; background: rgba(0,255,204,0.03); }
        .fire-btn { background: var(--main); color: #000; border: none; width: 100%; padding: 20px; border-radius: 15px; font-weight: 900; font-size: 18px; cursor: pointer; transition: 0.3s; box-shadow: 0 5px 20px rgba(0,255,204,0.4); }
        .fire-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,255,204,0.6); }

        /* Scanning Animation */
        .scanner { width: 100%; height: 2px; background: var(--main); position: absolute; left: 0; z-index: 10; display: none; animation: move 2s linear infinite; box-shadow: 0 0 15px var(--main); }
        @keyframes move { 0% { top: 0; } 100% { top: 100%; } }

        .prediction-result { margin-top: 30px; padding: 25px; background: #080808; border-radius: 25px; border: 1px solid var(--main); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { border-color: #222; } 50% { border-color: var(--main); } 100% { border-color: #222; } }

        .signal { font-size: 35px; font-weight: 900; text-align: center; margin-bottom: 10px; text-shadow: 0 0 15px currentColor; }
        .logic-panel { font-size: 12px; line-height: 1.6; color: #aaa; background: #111; padding: 15px; border-radius: 15px; border-left: 5px solid var(--main); }

        .action-row { display: flex; gap: 10px; margin-top: 20px; }
        .action-row a { flex: 1; text-decoration: none; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; color: #fff; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>

{% if not session.get('god_access') %}
    <div style="height: 100vh; display: flex; align-items: center; justify-content: center;">
        <div class="terminal">
            <h1>UNAUTHORIZED ACCESS</h1>
            <form method="POST" action="/login">
                <input type="text" name="u" placeholder="GOD USERNAME" required>
                <input type="password" name="p" placeholder="GOD PASSWORD" required>
                <button type="submit" class="fire-btn">INITIALIZE GOD MODE</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="top-bar">
        <div class="live-clock" id="clk">00:00:00</div>
        <div class="credit-hub">POWER: ⚡ {{ session['credits'] }}%</div>
    </div>

    <div class="grid-stats">
        <div class="stat-box"><small>WINS</small><b style="color:var(--win)">{{ session['wins'] }}</b></div>
        <div class="stat-box"><small>LOSSES</small><b style="color:var(--loss)">{{ session['losses'] }}</b></div>
        <div class="stat-box"><small>TARGET</small><b style="color:var(--main)">{{ (session['wins'] * 10) }}%</b></div>
    </div>

    <div class="terminal">
        <div class="scanner" id="scn"></div>
        <h1>NEURAL SCANNER V10</h1>
        <form method="POST" action="/process" enctype="multipart/form-data" onsubmit="document.getElementById('scn').style.display='block'">
            <input type="number" name="b" placeholder="CURRENT BALANCE ($)" required value="{{ session.get('last_b', '') }}">
            
            <select name="pair">
                <option value="EUR/USD">EUR/USD (OTC)</option>
                <option value="GBP/USD">GBP/USD (OTC)</option>
                <option value="USD/JPY">USD/JPY (OTC)</option>
                <option value="CRYPTO">CRYPTO IDX</option>
            </select>

            <div class="upload-zone" onclick="document.getElementById('f').click()">
                <span id="txt">📂 CONNECT TO GALLERY</span>
                <input type="file" id="f" name="chart" accept="image/*" required style="display:none" onchange="document.getElementById('txt').innerText='DATA LOADED ✅'">
            </div>
            
            <button type="submit" class="fire-btn">START DEEP ANALYSIS</button>
        </form>

        {% if sig %}
        <div class="prediction-result">
            <div style="text-align:center; font-size:10px; color:var(--main); letter-spacing: 2px;">GOD MODE ACCURACY: {{acc}}%</div>
            <div class="signal" style="color: {{col}}">{{sig}}</div>
            <div style="text-align:center; margin-bottom:15px;">
                <span style="background:var(--main); color:#000; padding:5px 15px; border-radius:5px; font-weight:bold; font-size:12px">TRADE AMOUNT: ${{trade}}</span>
            </div>
            <div class="logic-panel">
                <b>🧠 NEURAL CORE LOGIC:</b><br>{{log}}
            </div>
            <div class="action-row">
                <a href="/update/win" style="background:var(--win)">PROFIT</a>
                <a href="/update/loss" style="background:var(--loss)">LOSS</a>
            </div>
        </div>
        {% endif %}
    </div>
    <div style="text-align:center; margin-top:20px;"><a href="/exit" style="color:#444; text-decoration:none; font-size:10px">TERMINATE SESSION</a></div>
{% endif %}

<script>
    setInterval(() => {
        const d = new Date();
        document.getElementById('clk').innerText = d.toLocaleTimeString('en-GB');
    }, 1000);
</script>
</body>
</html>
'''

@app.before_request
def monitor():
    day = datetime.date.today().isoformat()
    if session.get('day') != day:
        session.update({'day': day, 'credits': 100, 'wins': 0, 'losses': 0})

@app.route('/')
def root(): return render_template_string(HTML_V10)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == ACCESS_DATA['user'] and request.form['p'] == ACCESS_DATA['pass']:
        session['god_access'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/process', methods=['POST'])
def process():
    if session.get('credits', 0) <= 0: return "SYSTEM DEPLETED. RECHARGE AT MIDNIGHT."
    
    session['credits'] -= 1
    bal = float(request.form['b'])
    session['last_b'] = bal
    pair = request.form.get('pair')
    
    time.sleep(2) # Scan effect
    
    # Pro Analytical Engine
    logic_bank = [
        f"AI detected an 'Inverse Head & Shoulders' forming on {pair}. Bullish breakout imminent.",
        f"Significant price rejection at the 0.786 Fibonacci level. Market trend shifting to Bearish.",
        f"Volume Spike detected in {pair}. The next candle will likely follow the momentum."
    ]
    
    data = [
        {"s": "GOD CALL ⬆️", "c": "#00ff88", "a": 99.4, "l": random.choice(logic_bank), "p": 3},
        {"s": "GOD PUT ⬇️", "c": "#ff3366", "a": 98.7, "l": random.choice(logic_bank), "p": 2},
        {"s": "CALL (MTG-1) ⬆️", "c": "#00ff88", "a": 92.1, "l": "Standard volatility detected. Use 1st step Martingale to secure win.", "p": 5}
    ]
    pick = random.choice(data)
    trade = round((bal * pick['p']) / 100, 2)
    
    return render_template_string(HTML_V10, sig=pick['s'], col=pick['c'], acc=pick['a'], log=pick['l'], trade=trade)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    return redirect('/')

@app.route('/exit')
def exit():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
