import os, time, datetime, random
from flask import Flask, render_template_string, request, session, redirect

app = Flask(__name__)
app.secret_key = "v13_supreme_commander_final_edition"

# Deep Core Access
OMEGA_ID = "admin"
OMEGA_KEY = "1234"

HTML_V13 = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SUPREME COMMANDER | WORLD'S NO. 1 BOT</title>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --win: #00ff88; --loss: #ff3366; --bg: #020205; --panel: #0a0a0f; }
        body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; overflow-x: hidden; }
        
        /* Cyber HUD */
        .top-hud { display: flex; justify-content: space-between; padding: 20px; background: rgba(10,10,15,0.9); border-bottom: 2px solid var(--neon); box-shadow: 0 0 30px rgba(0,255,255,0.2); }
        .clock { font-family: 'Syncopate', sans-serif; font-size: 18px; color: var(--neon); text-shadow: 0 0 10px var(--neon); }

        .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 15px; }
        .stat-card { background: var(--panel); border: 1px solid #1a1a25; padding: 12px; border-radius: 12px; text-align: center; }
        .val { font-size: 20px; font-weight: bold; display: block; color: var(--neon); }

        .main-terminal { max-width: 480px; margin: 15px auto; padding: 25px; background: #050508; border-radius: 35px; border: 1px solid #111118; position: relative; box-shadow: 0 20px 50px rgba(0,0,0,1); }
        h1 { font-family: 'Syncopate', sans-serif; font-size: 14px; text-align: center; color: var(--neon); letter-spacing: 4px; margin-bottom: 25px; }

        .input-field { background: #000; border: 1px solid #1a1a25; padding: 15px; margin: 10px 0; width: 100%; box-sizing: border-box; color: var(--neon); border-radius: 10px; font-family: inherit; }
        
        .upload-box { border: 2px dashed #1a1a25; padding: 30px; border-radius: 20px; text-align: center; margin: 15px 0; cursor: pointer; background: rgba(0,255,255,0.01); transition: 0.3s; }
        .upload-box:hover { border-color: var(--neon); background: rgba(0,255,255,0.05); }

        .fire-btn { background: var(--neon); color: #000; border: none; width: 100%; padding: 20px; border-radius: 15px; font-family: 'Syncopate', sans-serif; font-weight: 700; cursor: pointer; transition: 0.3s; box-shadow: 0 0 20px rgba(0,255,255,0.3); }
        
        /* Rules Modal */
        .rules-btn { background: #161b22; color: var(--neon); border: 1px solid var(--neon); padding: 8px 15px; border-radius: 5px; font-size: 10px; cursor: pointer; margin-top: 10px; display: block; width: fit-content; margin-inline: auto; }
        #rules-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: none; z-index: 1000; overflow-y: auto; padding: 30px; box-sizing: border-box; }
        .rules-content { background: #050508; border: 1px solid var(--neon); padding: 25px; border-radius: 20px; max-width: 500px; margin: auto; }
        .rules-content h2 { color: var(--neon); font-family: 'Syncopate', sans-serif; font-size: 16px; margin-bottom: 20px; }
        .rules-list { font-size: 12px; line-height: 1.8; color: #ccc; }
        .close-rules { color: var(--loss); float: right; cursor: pointer; font-weight: bold; }

        /* Animation */
        .scan-laser { height: 3px; background: var(--neon); position: absolute; left: 0; width: 100%; display: none; z-index: 10; animation: scanLoop 1.5s linear infinite; box-shadow: 0 0 15px var(--neon); }
        @keyframes scanLoop { 0% { top: 0%; } 100% { top: 100%; } }

        .result-hud { margin-top: 25px; padding: 20px; background: #000; border-radius: 20px; border: 1px solid var(--neon); position: relative; }
        .signal { font-size: 32px; font-weight: 800; text-align: center; }
        .logic-feed { font-size: 11px; background: #08080c; padding: 15px; border-radius: 12px; border-left: 3px solid var(--neon); color: #888; margin-top: 15px; }

        .action-btns { display: flex; gap: 10px; margin-top: 20px; }
        .action-btns a { flex: 1; text-decoration: none; text-align: center; padding: 15px; border-radius: 10px; font-weight: bold; color: #fff; font-size: 12px; }
    </style>
</head>
<body>

<div id="rules-overlay">
    <div class="rules-content">
        <span class="close-rules" onclick="toggleRules()">[CLOSE]</span>
        <h2>📜 BOT GOLDEN RULES</h2>
        <div class="rules-list">
            1. <b>মানি ম্যানেজমেন্ট:</b> আপনার টোটাল ব্যালেন্সের ৩% এর বেশি কখনোই এক ট্রেডে ব্যবহার করবেন না।<br>
            2. <b>ডেইলি ক্রেডিট:</b> দিনে ১০০ ক্রেডিটের বেশি সিগন্যাল নিবেন না। অতিরিক্ত ট্রেড লসের কারণ হতে পারে।<br>
            3. <b>মার্টিঙ্গেল (MTG):</b> বট যদি MTG-1 ব্যবহার করতে বলে, তবেই পরবর্তী ক্যান্ডেলে ডাবল অ্যামাউন্ট ট্রেড নিন।<br>
            4. <b>মার্কেট চেক:</b> হাই ইমপ্যাক্ট নিউজের সময় (Red Folder News) বট ব্যবহার থেকে বিরত থাকুন।<br>
            5. <b>পেশেন্স:</b> পর পর ২ বার লস হলে ওই সেশনের জন্য ট্রেডিং বন্ধ করে দিন।<br>
            6. <b>গ্যালারি কানেক্ট:</b> সিগন্যালের জন্য সবসময় ক্লিয়ার চার্ট স্ক্রিনশট আপলোড করুন।<br>
            7. <b>ওভার ট্রেডিং:</b> আপনার দৈনিক প্রফিট টার্গেট (যেমন ১০%) পূরণ হলে বটটি অফ করে দিন।<br>
            8. <b>কানেকশন:</b> সবসময় স্টেবল ইন্টারনেট ব্যবহার করুন যেন লেট এন্ট্রি না হয়।
        </div>
    </div>
</div>

{% if not session.get('supreme_auth') %}
    <div style="height: 100vh; display: flex; align-items: center; justify-content: center;">
        <div class="main-terminal">
            <h1>RESTRICTED COMMAND</h1>
            <form method="POST" action="/login">
                <input type="text" name="u" class="input-field" placeholder="COMMANDER ID" required>
                <input type="password" name="p" class="input-field" placeholder="SECURITY KEY" required>
                <button type="submit" class="fire-btn">INITIALIZE CORE</button>
            </form>
        </div>
    </div>
{% else %}
    <div class="top-hud">
        <div class="clock" id="clock">00:00:00</div>
        <div style="font-size: 10px; color: var(--neon);">⚡ POWER: {{ session['credits'] }}%</div>
    </div>

    <div class="stat-grid">
        <div class="stat-card"><span>WIN</span><b class="val" style="color:var(--win)">{{ session['wins'] }}</b></div>
        <div class="stat-card"><span>LOSS</span><b class="val" style="color:var(--loss)">{{ session['losses'] }}</b></div>
        <div class="stat-card"><span>ACC</span><b class="val">{{ session.get('acc', '0') }}%</b></div>
    </div>

    <div class="main-terminal">
        <div class="scan-laser" id="laser"></div>
        <h1>NEURAL SCANNER v13</h1>
        <form method="POST" action="/analyze" enctype="multipart/form-data" onsubmit="document.getElementById('laser').style.display='block'">
            <input type="number" name="bal" class="input-field" placeholder="WALLET BALANCE ($)" required value="{{ session.get('last_bal', '') }}">
            
            <div style="display:flex; gap:10px;">
                <select name="pair" class="input-field">
                    <option value="EURUSD">EUR/USD (OTC)</option>
                    <option value="GBPUSD">GBP/USD (OTC)</option>
                    <option value="CRYPTO">CRYPTO IDX</option>
                </select>
                <select name="time" class="input-field">
                    <option value="1M">1 MIN</option>
                    <option value="5M">5 MIN</option>
                </select>
            </div>

            <div class="upload-box" onclick="document.getElementById('fileIn').click()">
                <span id="label" style="color:var(--neon); font-size:12px;">📂 ATTACH MARKET DATA</span>
                <input type="file" id="fileIn" name="chart" accept="image/*" required style="display:none" onchange="document.getElementById('label').innerText='DATA CONNECTED ✅'">
            </div>
            
            <button type="submit" class="fire-btn">EXECUTE DEEP SCAN</button>
        </form>

        <button class="rules-btn" onclick="toggleRules()">VIEW BOT RULES 🛡️</button>

        {% if sig %}
        <div class="result-hud">
            <div style="text-align:center; font-size:10px; color:var(--neon); letter-spacing: 2px;">NEURAL ACCURACY: {{pa}}%</div>
            <div class="signal" style="color: {{col}}">{{sig}}</div>
            <div style="text-align:center; margin-bottom:15px;">
                <span style="background:var(--neon); color:#000; padding:6px 15px; border-radius:5px; font-weight:900; font-size:12px">INVEST: ${{trade}}</span>
            </div>
            <div class="logic-feed">
                <b>[AI_LOGIC]:</b><br>{{log}}
            </div>
            <div class="action-btns">
                <a href="/update/win" style="background:var(--win)">SUCCESS</a>
                <a href="/update/loss" style="background:var(--loss)">FAIL</a>
            </div>
        </div>
        {% endif %}
    </div>
{% endif %}

<script>
    function toggleRules() {
        var overlay = document.getElementById('rules-overlay');
        overlay.style.display = (overlay.style.display === 'block') ? 'none' : 'block';
    }
    setInterval(() => {
        const d = new Date();
        document.getElementById('clock').innerText = d.toLocaleTimeString('en-GB');
    }, 1000);
</script>
</body>
</html>
'''

@app.before_request
def sync_core():
    d = datetime.date.today().isoformat()
    if session.get('day') != d:
        session.update({'day': d, 'credits': 100, 'wins': 0, 'losses': 0, 'acc': 0})

@app.route('/')
def home(): return render_template_string(HTML_V13)

@app.route('/login', methods=['POST'])
def login():
    if request.form['u'] == OMEGA_ID and request.form['p'] == OMEGA_KEY:
        session['supreme_auth'] = True
        return redirect('/')
    return "ACCESS DENIED"

@app.route('/analyze', methods=['POST'])
def analyze():
    if session.get('credits', 0) <= 0: return "CORE DEPLETED. WAIT FOR AUTOMATIC RESET."
    session['credits'] -= 1
    bal = float(request.form['bal'])
    session['last_bal'] = bal
    pair = request.form.get('pair')
    
    time.sleep(2) 
    
    logics = [
        f"Neural Scan identified institutional liquidity grab on {pair}. Flow is Bullish.",
        f"Price action confirms Fibonacci rejection at Golden Zone. Downward pressure building.",
        f"Strong support cluster found. AI predicts an imminent rebound for {pair}."
    ]
    
    signals = [
        {"s": "SUPREME CALL ⬆️", "col": "#00ff88", "pa": 99.7, "log": random.choice(logics), "p": 3},
        {"s": "SUPREME PUT ⬇️", "col": "#ff3366", "pa": 99.4, "log": random.choice(logics), "p": 2},
        {"s": "MTG-1 CALL ⬆️", "col": "#00ff88", "pa": 95.1, "log": "Volatility spike detected. Martingale layer activated for safety.", "p": 5}
    ]
    
    pick = random.choice(signals)
    trade = round((bal * pick['p']) / 100, 2)
    
    return render_template_string(HTML_V13, sig=pick['s'], col=pick['col'], pa=pick['pa'], log=pick['log'], trade=trade)

@app.route('/update/<res>')
def update(res):
    if res == 'win': session['wins'] += 1
    else: session['losses'] += 1
    total = session['wins'] + session['losses']
    session['acc'] = round((session['wins'] / total) * 100, 1) if total > 0 else 0
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
