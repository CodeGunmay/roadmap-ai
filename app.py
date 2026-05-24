from flask import Flask, render_template_string, request
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

import os
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RoadmapAI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            color: #e0e0e0;
            min-height: 100vh;
        }
        .bg-grid {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-image:
                linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }
        .glow {
            position: fixed;
            top: -200px; left: 50%;
            transform: translateX(-50%);
            width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }
        .container {
            position: relative;
            z-index: 1;
            max-width: 720px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        .badge {
            display: inline-block;
            background: rgba(99,102,241,0.15);
            border: 1px solid rgba(99,102,241,0.3);
            color: #818cf8;
            font-size: 12px;
            font-weight: 500;
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 20px;
            letter-spacing: 0.5px;
        }
        h1 {
            font-size: 48px;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
            margin-bottom: 12px;
        }
        .subtitle {
            color: #6b7280;
            font-size: 16px;
            margin-bottom: 48px;
            font-weight: 400;
        }
        .card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            transition: opacity 0.3s;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        .form-group { margin-bottom: 20px; }
        .form-group.full { grid-column: 1 / -1; }
        label {
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: #9ca3af;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        input {
            width: 100%;
            padding: 12px 16px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: #e0e0e0;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s;
            outline: none;
        }
        input:focus {
            border-color: rgba(99,102,241,0.6);
            background: rgba(99,102,241,0.05);
            box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
        }
        input::placeholder { color: #4b5563; }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 8px;
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.3px;
            transition: all 0.2s;
        }
        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 25px rgba(99,102,241,0.4);
        }
        button:active { transform: translateY(0); }
        .loader {
            display: none;
            text-align: center;
            padding: 40px;
            color: #818cf8;
        }
        .loader-dots span {
            display: inline-block;
            width: 8px; height: 8px;
            background: #6366f1;
            border-radius: 50%;
            margin: 0 4px;
            animation: bounce 1.2s infinite;
        }
        .loader-dots span:nth-child(2) { animation-delay: 0.2s; }
        .loader-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
        }
        .result-card {
            margin-top: 32px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(99,102,241,0.2);
            border-radius: 20px;
            padding: 40px;
        }
        .result-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .result-dot {
            width: 8px; height: 8px;
            background: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 8px #22c55e;
        }
        .result-title {
            font-size: 14px;
            font-weight: 600;
            color: #9ca3af;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .result-body {
            line-height: 1.8;
            font-size: 14px;
            color: #d1d5db;
        }
        .result-body h2, .result-body h3 {
            color: #818cf8;
            margin: 20px 0 10px;
        }
        .result-body strong, .result-body b {
            color: #ffffff;
            font-weight: 600;
        }
        .result-body ul, .result-body ol {
            padding-left: 20px;
            margin: 8px 0;
        }
        .result-body li {
            margin: 6px 0;
            color: #d1d5db;
        }
        .result-body p { margin: 10px 0; }
        .week-block {
            background: rgba(99,102,241,0.05);
            border: 1px solid rgba(99,102,241,0.15);
            border-radius: 12px;
            padding: 16px 20px;
            margin: 12px 0;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #374151;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="glow"></div>
    <div class="container">
        <div class="badge">✦ AI-Powered Career Planner</div>
        <h1>Build Your<br>Learning Roadmap</h1>
        <p class="subtitle">Personalized week-by-week plan based on your skills and goals</p>

        <div class="card" id="formcard">
            <form method="POST" onsubmit="showLoading()">
                <div class="grid-2">
                    <div class="form-group">
                        <label>Your Name</label>
                        <input type="text" name="name" placeholder="e.g. Gunmay" required>
                    </div>
                    <div class="form-group">
                        <label>Branch</label>
                        <input type="text" name="branch" placeholder="e.g. AI/ML CSE" required>
                    </div>
                    <div class="form-group">
                        <label>Year Completed</label>
                        <input type="number" name="year" placeholder="1" required>
                    </div>
                    <div class="form-group">
                        <label>Goal</label>
                        <input type="text" name="goal" placeholder="internship / placement" required>
                    </div>
                    <div class="form-group">
                        <label>Hours Per Day</label>
                        <input type="number" name="hours" placeholder="2" required>
                    </div>
                    <div class="form-group">
                        <label>Timeline (months)</label>
                        <input type="number" name="months" placeholder="3" required>
                    </div>
                    <div class="form-group full">
                        <label>Current Skills</label>
                        <input type="text" name="skills" placeholder="e.g. Python, ML basics, NumPy" required>
                    </div>
                </div>
                <button type="submit">Generate My Roadmap →</button>
            </form>
        </div>

        <div class="loader" id="loader">
            <div class="loader-dots">
                <span></span><span></span><span></span>
            </div>
            <p style="margin-top:16px;font-size:14px">Generating your personalized roadmap...</p>
        </div>

        {% if roadmap %}
        <div class="result-card">
            <div class="result-header">
                <div class="result-dot"></div>
                <span class="result-title">Your Personalized Roadmap</span>
            </div>
            <div class="result-body">{{ roadmap | safe }}</div>
        </div>
        {% endif %}

        <div class="footer">Built with RoadmapAI — your personal tech career guide</div>
    </div>
    <script>
        function showLoading() {
            document.getElementById('loader').style.display = 'block';
            document.getElementById('formcard').style.opacity = '0.4';
        }
    </script>
</body>
</html>
"""

import re

def format_roadmap(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    lines = text.split('\n')
    html = ''
    in_ul = False
    for line in lines:
        line = line.strip()
        if not line:
            if in_ul:
                html += '</ul>'
                in_ul = False
            html += '<br>'
        elif line.startswith('### '):
            html += f'<h3>{line[4:]}</h3>'
        elif line.startswith('## '):
            html += f'<h2>{line[3:]}</h2>'
        elif line.startswith('# '):
            html += f'<h2>{line[2:]}</h2>'
        elif line.startswith('* ') or line.startswith('+ ') or line.startswith('- '):
            if not in_ul:
                html += '<ul>'
                in_ul = True
            html += f'<li>{line[2:]}</li>'
        elif line.startswith('**Week') or line.startswith('Week'):
            if in_ul:
                html += '</ul>'
                in_ul = False
            html += f'<div class="week-block"><strong>{line}</strong></div>'
        else:
            if in_ul:
                html += '</ul>'
                in_ul = False
            html += f'<p>{line}</p>'
    if in_ul:
        html += '</ul>'
    return html

def generate_roadmap(profile):
    prompt = f"""
You are an expert tech career coach for Indian students.

Based on this student profile, generate a detailed week by week learning roadmap:

Name: {profile['name']}
Branch: {profile['branch']}
Year completed: {profile['year']}
Current skills: {', '.join(profile['current_skills'])}
Goal: {profile['goal']}
Hours available per day: {profile['hours_per_day']}
Target timeline: {profile['target_months']} months

Generate a roadmap with:
1. Week by week topics to learn
2. One small project to build every 2 weeks
3. Resources (YouTube channels, free courses)
4. Skills that are currently in demand for {profile['goal']} in India

Be specific, practical, and motivating. Format it clearly week by week.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return format_roadmap(response.choices[0].message.content)

@app.route("/", methods=["GET", "POST"])
def index():
    roadmap = None
    if request.method == "POST":
        profile = {
            "name": request.form["name"],
            "branch": request.form["branch"],
            "year": int(request.form["year"]),
            "current_skills": [s.strip() for s in request.form["skills"].split(",")],
            "goal": request.form["goal"],
            "hours_per_day": int(request.form["hours"]),
            "target_months": int(request.form["months"])
        }
        roadmap = generate_roadmap(profile)
    return render_template_string(HTML, roadmap=roadmap)

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
