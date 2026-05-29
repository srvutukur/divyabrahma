import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template_string
import json
import requests

import DB11_engine as db11

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

def get_coords(pob):
    """Nominatim API వాడి city coordinates తెచ్చుకోవడం"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": pob, "format": "json", "limit": 1}
        headers = {"User-Agent": "DivyaBrahmaJyotish/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return (17.3850, 78.4867)

def load_v27_prompt():
    """V27MasterPrompt.txt load చేయడం"""
    path = os.path.join(BASE_DIR, "V27MasterPrompt.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_kb2_lagna(lagna_te):
    """లగ్నం KB file load చేయడం"""
    path = os.path.join(BASE_DIR, f"KB_{lagna_te}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def load_kb2():
    """KB2.txt load చేయడం — first 6000 chars"""
    path = os.path.join(BASE_DIR, "KB2.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:6000]
    return ""

def call_groq_analysis(summary_text, lagna_te, dasha_info):
    """Groq API కి పంపి Telugu analysis తెచ్చుకోవడం"""
    v27 = load_v27_prompt()
    kb2_lagna = load_kb2_lagna(lagna_te)
    kb2_common = load_kb2()

    # Confirmation block తీసేసి directly analysis అడగడం
    system_prompt = f"""మీరు దివ్య బ్రహ్మ ప్రవాహ జ్యోతిష్య నిపుణులు. 
V27 Master Prompt ప్రకారం జాతక విశ్లేషణ Telugu లో ఇవ్వాలి.
Confirmation అడగకూడదు. Echo చేసిన తర్వాత directly analysis ఇవ్వాలి.
శాస్త్ర citations తో — BPHS, Brihat Jataka, Saravali, Phaladeepika — వివరణ ఇవ్వాలి.

V27 MASTER PROMPT (సంక్షిప్తం):
{v27[:3000]}

LAGNA KB DATA ({lagna_te}):
{kb2_lagna[:2000]}

KB2 COMMON:
{kb2_common[:2000]}"""

    user_prompt = f"""ఈ జాతకం విశ్లేషించండి:

{summary_text}

ప్రస్తుత దశ: {dasha_info}

IMPORTANT INSTRUCTIONS:
- Confirmation అడగకూడదు
- Ayanamsha selection అడగకూడదు — Lahiri use చేయండి
- STAGE 1 నుండి STAGE 6 వరకు internally process చేయండి — client కి చూపించకూడదు
- STAGE 7 సారాంశం మాత్రమే Telugu లో ఇవ్వాలి

STAGE 7 లో ఇవ్వాల్సింది:
1. జాతక సంక్షిప్తం — లగ్నం, ముఖ్య గ్రహ స్థానాలు
2. ప్రస్తుత మహాదశ/అంతర్దశ ఫలాలు
3. Career మరియు Finance స్థితి
4. Health విచారణ
5. వివాహ/కుటుంబ స్థితి
6. వచ్చే 2 సంవత్సరాల శుభ/అశుభ కాలాలు
7. పరిహారాలు (Remedies)

తెలుగులో మాత్రమే సమాధానం ఇవ్వండి. శాస్త్ర citations తప్పనిసరి."""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.3
    }

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=120
    )
    result = resp.json()
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    elif "error" in result:
        return f"Groq Error: {result['error'].get('message', 'Unknown error')}"
    return "Analysis రాలేదు — మళ్ళీ try చేయండి"


HTML_FORM = """
<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>దివ్య బ్రహ్మ జ్యోతిష్యం</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Arial, sans-serif;
            max-width: 660px;
            margin: 40px auto;
            padding: 24px;
            background: #1a1a2e;
            color: #eee;
        }
        h1 { color: #ffd700; text-align: center; margin-bottom: 6px; font-size: 26px; }
        .subtitle { text-align: center; color: #aaa; font-size: 14px; margin-bottom: 28px; }
        label { display: block; margin-top: 18px; color: #ccc; font-size: 14px; }
        input, select {
            width: 100%; padding: 11px 13px; margin-top: 6px;
            border-radius: 7px; border: 1px solid #444;
            background: #16213e; color: #eee; font-size: 15px;
        }
        button {
            width: 100%; padding: 14px; margin-top: 30px;
            background: #ffd700; color: #000; font-size: 17px;
            font-weight: bold; border: none; border-radius: 8px; cursor: pointer;
        }
        button:hover { background: #ffe44d; }
        button:disabled { background: #555; color: #aaa; cursor: not-allowed; }
        #loading { display: none; text-align: center; color: #ffd700; margin-top: 22px; font-size: 15px; }
        #result {
            display: none; margin-top: 22px; padding: 20px;
            background: #16213e; border-radius: 8px;
            white-space: pre-wrap; font-size: 14px; line-height: 1.8;
            max-height: 600px; overflow-y: auto; border: 1px solid #333;
        }
        .error { color: #ff6b6b; }
    </style>
</head>
<body>
    <h1>🔱 దివ్య బ్రహ్మ జ్యోతిష్యం</h1>
    <p class="subtitle">DB11 Engine V27 — శాస్త్ర ఆధారిత Telugu Jyotish Report</p>

    <label>జన్మ తేదీ (DD/MM/YYYY)</label>
    <input type="text" id="dob" placeholder="25/11/1966" maxlength="10" />

    <label>జన్మ సమయం (HH:MM లేదా HH:MM:SS)</label>
    <input type="text" id="tob" placeholder="06:19" maxlength="8" />

    <label>జన్మ స్థలం (ఏ city అయినా, ఏ country అయినా)</label>
    <input type="text" id="pob" placeholder="Hyderabad, New York, London..." />

    <label>విచారణ విషయం</label>
    <select id="focus">
        <option value="General">సాధారణ జాతక విశ్లేషణ</option>
        <option value="Career">వృత్తి / వ్యాపారం</option>
        <option value="Finance">ఆర్థికం</option>
        <option value="Marriage">వివాహం</option>
        <option value="Health">ఆరోగ్యం</option>
    </select>

    <button id="btn" onclick="submitForm()">జాతకం విశ్లేషించండి →</button>

    <div id="loading">⏳ DB11 Engine + AI Analysis run అవుతోంది...<br>దయచేసి 2-3 నిమిషాలు వేచి ఉండండి...</div>
    <div id="result"></div>

    <script>
        async function submitForm() {
            const dob = document.getElementById('dob').value.trim();
            const tob = document.getElementById('tob').value.trim();
            const pob = document.getElementById('pob').value.trim();
            const focus = document.getElementById('focus').value;

            if (!dob || !tob || !pob) {
                alert('అన్ని వివరాలు enter చేయండి');
                return;
            }

            let tobFull = tob;
            if (tob.length === 5) tobFull = tob + ':00';

            document.getElementById('btn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ dob, tob: tobFull, pob, focus })
                });
                const data = await response.json();
                document.getElementById('loading').style.display = 'none';
                document.getElementById('btn').disabled = false;
                document.getElementById('result').style.display = 'block';
                if (data.success) {
                    document.getElementById('result').className = '';
                    document.getElementById('result').innerText = data.analysis;
                } else {
                    document.getElementById('result').className = 'error';
                    document.getElementById('result').innerText = 'Error: ' + data.error;
                }
            } catch (e) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('btn').disabled = false;
                document.getElementById('result').style.display = 'block';
                document.getElementById('result').className = 'error';
                document.getElementById('result').innerText = 'Network Error: ' + e.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FORM)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        dob = data.get('dob', '').strip()
        tob = data.get('tob', '').strip()
        pob = data.get('pob', '').strip()
        focus = data.get('focus', 'General')

        if not dob or not tob or not pob:
            return jsonify({'success': False, 'error': 'వివరాలు సరిగ్గా ఇవ్వండి'})

        # Step 1: Coordinates
        lat, lon = get_coords(pob)

        # Step 2: DB11 engine run
        result_data = db11.generate_v21(
            dob, tob, lat, lon, pob,
            timezone=5.5,
            ayan_mode="lahiri"
        )

        # Step 3: Summary generate
        summary = db11.generate_summary(result_data)

        # Step 4: Lagna + Dasha info
        lagna_te = result_data.get("d1", {}).get("lagna", {}).get("rashi_te", "వృశ్చికం")
        dasha = result_data.get("dasha", {})
        maha = dasha.get("mahadasha", {})
        antar = dasha.get("antardasha", {})
        dasha_info = f"మహాదశ: {maha.get('planet_te','')} ({maha.get('start_date','')} – {maha.get('end_date','')}), అంతర్దశ: {antar.get('planet_te','')} ({antar.get('start_date','')} – {antar.get('end_date','')})"

        # Step 5: Groq Telugu analysis
        analysis = call_groq_analysis(summary, lagna_te, dasha_info)

        # Step 6: JSON save
        out_name = f"DB11_{dob.replace('/', '')}"
        json_path = os.path.join(BASE_DIR, f"{out_name}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)

        return jsonify({'success': True, 'analysis': analysis})

    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e) + '\n' + traceback.format_exc()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
