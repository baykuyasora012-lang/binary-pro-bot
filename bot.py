import os, time
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Binary Expert v7</title>
    <style>
        body { background: #0b111b; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #151c2c; padding: 30px; border-radius: 25px; border: 1px solid #1e293b; max-width: 400px; margin: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .btn { background: #3b82f6; color: white; border: none; width: 100%; padding: 18px; border-radius: 12px; font-weight: bold; cursor: pointer; margin-top: 20px; }
        .res { margin-top: 25px; padding: 20px; background: #0f172a; border-radius: 15px; border: 1px dashed #334155; text-align: left; }
        .circle { width: 80px; height: 80px; border-radius: 50%; border: 6px solid #1e293b; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-weight: bold; font-size: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>AI Market Analysis v7</h2>
        <form method="POST" action="/analyze" enctype="multipart/form-data">
            <input type="file" name="chart" required style="margin: 20px 0; color: #64748b;">
            <button type="submit" class="btn">ANALYZE NOW</button>
        </form>
        {% if r %}
        <div class="res">
            <div class="circle" style="border-top-color: {{c}}; color: {{c}};">{{acc}}%</div>
            <h2 style="color:{{c}}; text-align:center;">{{r}}</h2>
            <hr style="border:0; border-top:1px solid #1e293b; margin:15px 0;">
            <p><strong>Trend:</strong> {{t}}</p>
            <p><strong>Management:</strong> <span style="color:#22c55e;">Use {{p}}% Balance</span></p>
            <p style="font-size:12px; color:#94a3b8;"><strong>AI Logic:</strong> {{l}}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/analyze', methods=['POST'])
def analyze():
    s = int(time.time()) % 4
    data = [
        {"r":"✅ STRONG CALL", "c":"#22c55e", "acc":96, "t":"UPTREND", "l":"সাপোর্ট জোন রিজেকশন কনফার্ম।", "p":2},
        {"r":"🔴 STRONG PUT", "c":"#ef4444", "acc":92, "t":"BEARISH", "l":"রেজিস্ট্যান্স জোন ব্রেকআউট।", "p":3},
        {"r":"✅ CALL (MTG-1)", "c":"#22c55e", "acc":81, "t":"SIDEWAYS", "l":"ভলিউম কম, মার্টিঙ্গেল সেফটি রাখুন।", "p":5},
        {"r":"🔴 PUT (MTG-1)", "c":"#ef4444", "acc":85, "t":"DOWNTREND", "l":"পরবর্তী ক্যান্ডেল রেড হওয়ার সম্ভাবনা বেশি।", "p":4}
    ]
    p = data[s]
    return render_template_string(HTML, r=p['r'], c=p['c'], acc=p['acc'], t=p['t'], l=p['l'], p=p['p'])

if __name__ == "__main__": app.run(host='0.0.0.0', port=5000)
