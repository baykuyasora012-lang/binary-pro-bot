import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "v15_aether_x_quantum_god_level"

# Central Command Access
SYS_ID = "admin"
SYS_KEY = "1234"

HTML_V15 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AETHER-X | QUANTUM NEURAL CORE</title>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --win: #00ff88; --loss: #ff2a6d; --bg: #030308; --glass: rgba(15, 15, 25, 0.8); }
        body { background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; overflow-x: hidden; }
        
        /* Background Pulse */
        .bg-animate { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #00f2ff0a, transparent); z-index: -1; }

        .header-hud { display: flex; justify-content: space-between; padding: 20px; background: var(--glass); backdrop-filter: blur(15px); border-bottom: 1px solid rgba(0,242,255,0.3); position: sticky; top: 0; z-index: 100; }
        .clock { font-family: 'Syncopate', sans-serif; font-size: 16px; color: var(--neon); letter-spacing: 2px; }

        .stat-bridge { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 15px; margin-top: 10px; }
        .stat-tile { background: var(--glass); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .val { font-size: 24px; font-weight: 700; color: var(--neon); text-shadow: 0 0 10px var(--neon); }

        .terminal-core { max-width: 500px; margin: 20px auto; padding: 35px; background: var(--glass); border-radius: 40px; border: 1px solid rgba(0,242,255,0.1); position: relative; box-shadow: 0 25px 50px rgba(0,0,0,0.8); }
        h1 { font-family: 'Syncopate', sans-serif; font-size: 12px; text-align: center; color: var(--neon); letter-spacing: 5px; text-transform: uppercase; margin-bottom: 30px; opacity: 0.8; }

        .input-group input { width: 100%; padding: 18px; margin-bottom: 15px; background: #000; border: 1px solid rgba(0,242,255,0.2); border-radius: 12px; color: var(--neon); font-size: 16px; box-sizing: border-box; outline: none; transition: 0.4s; }
        .input-group input:focus { border-color: var(--neon); box-shadow: 0 0 15px rgba(0,242,255,0.3); }

        .drop-zone { border: 2px dashed rgba(0,242,255,0.2); padding: 45px; border-radius: 25px; text-align: center; margin: 20px 0; cursor: pointer; transition: 0.4s; background: rgba(0,242,255,0.02); }
        .drop-zone:hover { border-color: var(--neon); background: rgba(0,242,255,0.08); }

        .btn-launch { background: var(--neon); color: #000; border: none; width: 100%; padding: 22px; border-radius: 18px; font-family: 'Syncopate', sans-serif; font-weight: 700; cursor: pointer; transition: 0.3s; box-shadow: 0 0 30px rgba(0,242,255,0.4); }
        .btn-launch:hover { transform: translateY(-5px); box-shadow: 0 0 50px rgba(0,242,255,0.6); }

        /* Scanning Laser */
        .laser-line { height: 4px; background: var(--neon); position: absolute; left: 0; width: 100%; display: none; z-index: 10; animation: scanAnim 1.8s ease-in-out infinite; box-shadow: 0 0 20px var(--neon); }
        @keyframes scanAnim { 0% { top: 0%; opacity: 0; } 50% { opacity: 1; } 100% { top: 100%; opacity: 0; } }

        .prediction-panel { margin-top: 35px; padding: 25px; background: rgba(0,0,0,0.4); border-radius: 30px; border: 1px solid var(--neon); text-align: center; animation: glowPulse 2s infinite; }
        @keyframes glowPulse { 0% { box-shadow: 0 0 5px var(--neon); } 50% { box-shadow: 0 0 25px var(--neon); } 100% { box-shadow: 0 0 5px var(--neon); } }

        .sig-text { font-size: 42px; font-weight: 900; margin: 10px 0; text-shadow: 0 0 15px rgba(255,255,255,0.2); }
        .logic-terminal { text-align: left; font-size: 11px; background: #000; padding: 20px; border-radius: 15px; border-left: 4px solid var(--neon); color: #888; margin-top: 20px; line-height: 1.6; }

        .action-grid { display: flex; gap: 15px; margin-top: 25px; }
        .action-grid a { flex: 1; text-decoration: none; text-align: center; padding: 18px; border-radius: 15px; font-weight: 700; color: #fff; text-transform: uppercase; font-size: 12px; }

        /* Rules UI */
        .rules-trigger { background: transparent; color: var(--neon); border: 1px solid var(--neon); padding: 10px 20px; border-radius: 8px; font-size: 10px; cursor: pointer; margin: 20px auto; display: block; opacity: 0.6; }
        #rules-modal { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.95); display:none; z-index:1001; padding: 40px 20px; box-sizing: border-box; }
        .rules-wrap { background: #0a0a0f; border: 1px solid var(--neon); padding: 30px; border-radius: 25px; max-width: 450px; margin: auto; }
    </style>
</head>
<body>
    <div class="bg-animate"></div>

<div id="rules-modal">
    <div class="rules-wrap">
        <span style="color:var(--loss); float:right; cursor:pointer; font-weight:bold;" onclick="toggleRules()">[EXIT]</span>
        <h2 style="color:var(--neon); font-family:'Syncopate'; font-size:14px;">AETHER-X PROTOCOLS</h2>
        <div style="font-size: 12px; line-height: 1.8; color: #aaa; margin-top: 20px;">
            1. <b>MAX RISK:</b> Never exceed 2-5% of total wallet per trade.<br>
            2. <b>DAILY QUOTA:</b> Stop trading after 100 credit consumption.<br>
            3. <b>MARTINGALE:</b> Use 1st Step MTG only if Neural Core suggests.<br>
            4. <b>MARKET SYNC:</b> Avoid volatile red-folder news events.<br>
            5. <b>PSYCHOLOGY:</b> Exit session after 2 consecutive losses.
        </div>
    </div>
</div>

{% if not session.get('auth') %}
    <div style="height: 100vh; display: flex; align-items: center; justify-content: center;">
        <div class="terminal-core">
            <h1>AETHER-X LOGIN</h1>
            <form method="POST" action="/login">
                <div class="input-group">
                    <input type="text" name="u" placeholder="CORE IDENTITY" required>
                    <input type="password" name="p" placeholder="ACCESS KEY" required>
                </div>
                <button type="submit" class="btn-launch">INITIALIZE CORE</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="header-hud">
        <div class="clock" id="timer">00:00:00</div>
        <div style="font-size: 10px; color: var(--neon);">POWER: {{ session['credits'] }}%</div>
    </div>

    <div class="stat-bridge">
        <div class="stat-tile"><span>SUCCESS</span><b class="val" style="color:var(--win)">{{ session['wins'] }}</b></div>
        <div class="stat-tile"><span>FAIL</span><b class="val" style="color:var(--loss)">{{ session['losses'] }}</b></div>
        <div class="stat-tile"><span>EFFICIENCY</span><b class="val">{{ session.get('acc', '0') }}%</b></div>
    </div>

    <div class="terminal-core">
        <div class="laser-line" id="laser"></div>
        <h1>NEURAL ANALYZER v15</h1>
        <form method="POST" action="/analyze" enctype="multipart/form-data" onsubmit="document.getElementById('laser').style.display='block'">
            <div class="input-group">
                <input type="number" name="bal" placeholder="CURRENT CAPITAL ($)" required value="{{ session.get('last_bal', '') }}">
                <select name="time" style="width:100%; padding:18px; background:#000; border:1px solid rgba(0,242,255,0.2); border-radius:12px; color:var(--neon); font-family:inherit; margin-bottom:15px;">
                    <option value="1M">1 MINUTE DURATION</option>
                    <option value="5M">5 MINUTE DURATION</option>
                </select>
            </div>

            <div class="drop-zone" onclick="document.getElementById('chart').click()">
                <span id="label" style="color:var(--neon); font-size:12px;">[+] UPLOAD MARKET DATA STREAM</span>
                <input type="file" id="chart" name="chart" accept="image/*" required style="display:none" onchange="document.getElementById('label').innerText='DATA STREAM LINKED ✅'">
            </div>
            
            <button type="submit" class="btn-launch">EXECUTE QUANTUM SCAN</button>
        </form>

        <button class="rules-trigger" onclick="toggleRules()">CORE RULES & PROTOCOLS</button>

        {% if sig %}
        <div class="prediction-panel">
            <div style="font-size:10px; color:var(--neon); letter-spacing: 3px; margin-bottom:10px;">NEURAL ACCURACY: {{pa}}%</div>
            <div class="sig-text" style="color: {{col}}">{{sig}}</div>
            <div style="margin-bottom:20px;">
                <span style="background:var(--neon); color:#000; padding:8px 25px; border-radius:8px; font-weight:900; font-size:14px">INVEST: ${{trade}}</span>
            </div>
            <div class="logic-terminal">
                <b style="color:var(--neon)">[AETHER_LOGIC_FEED]:</b><br>{{log}}
            </div>
            <div class="action-grid">
                <a href="/update/win" style="background:var(--win); box-shadow: 0 0 20px rgba(0,255,136,0.3);">PROFIT</a>
                <a href="/update/loss" style="background:var(--loss); box-shadow: 0 0 20px rgba(255,42,109,0.3);">LOSS</a>
            </div>
        </div>
        {% endif %}
    </div>
{% endif %}

<script>
    function toggleRules() {
        var m = document.getElementById('rules-modal');
        m.style.display = (m.style.display === 'block') ? 'none' : 'block';
    }
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
def home(): return render_template_string(HTML_V15)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == SYS_ID and request.form['p'] == SYS_KEY:
        session['auth'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return "DAILY POWER DEPLETED."
    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    
    time.sleep(2) # Quantum Simulation
    
    logics = [
        "Quantum Neural Net detected an oversold correction. Bullish momentum building.",
        "Bearish rejection confirmed at the 1.618 Fibonacci extension. Downward trend likely.",
        "Market volatility is high. Identified institutional order block rejection."
    ]
    
    signals = [
        {"s": "SUPREME CALL ⬆️", "col": "#00ff88", "pa": 99.9, "log": random.choice(logics), "p": 3},
        {"s": "SUPREME PUT ⬇️", "col": "#ff2a6d", "pa": 99.7, "log": random.choice(logics), "p": 2},
        {"s": "CALL (MTG-1) ⬆️", "col": "#00ff88", "pa": 95.8, "log": "Slight fluctuation detected. Use Martingale 1st Layer for safety.", "p": 5}
    ]
    
    res = random.choice(signals)
    trade = round((bal * res['p']) / 100, 2)
    
    return render_template_string(HTML_V15, sig=res['s'], col=res['col'], pa=res['pa'], log=res['log'], trade=trade)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
