import sys
import os
sys.path.insert(0, os.path.expanduser("~"))

from flask import Flask, request, jsonify, render_template_string
import json

# DB11_engine import
import DB11_engine as db11

app = Flask(__name__)

HOME = os.path.expanduser("~")

HTML_FORM = """
<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>దివ్య బ్రహ్మ జ్యోతిష్యం</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; max-width: 620px; margin: 40px auto; padding: 20px; background: #1a1a2e; color: #eee; }
        h1 { color: #ffd700; text-align: center; margin-bottom: 6px; font-size: 24px; }
        .subtitle { text-align: center; color: #aaa; font-size: 14px; margin-bottom: 24px; }
        label { display: block; margin-top: 16px; color: #ccc; font-size: 14px; }
        input, select {
            width: 100%; padding: 10px 12px; margin-top: 6px;
            border-radius: 6px; border: 1px solid #444;
            background: #16213e; color: #eee; font-size: 15px;
        }
        button {
            width: 100%; padding: 14px; margin-top: 28px;
            background: #ffd700; color: #000; font-size: 17px;
            font-weight: bold; border: none; border-radius: 8px; cursor: pointer;
        }
        button:disabled { background: #888; cursor: not-allowed; }
        #loading { display: none; text-align: center; color: #ffd700; margin-top: 20px; font-size: 15px; }
        #result {
            display: none; margin-top: 20px; padding: 16px;
            background: #16213e; border-radius: 8px;
            white-space: pre-wrap; font-size: 13px; line-height: 1.6;
            max-height: 500px; overflow-y: auto;
        }
        .error { color: #ff6b6b; }
    </style>
</head>
<body>
    <h1>🔱 దివ్య బ్రహ్మ జ్యోతిష్యం</h1>
    <p class="subtitle">DB11 Engine V27 — శాస్త్ర ఆధారిత Telugu Jyotish Report</p>

    <label>జన్మ తేదీ (DD/MM/YYYY)</label>
    <input type="text" id="dob" placeholder="25/11/1966" maxlength="10" />

    <label>జన్మ సమయం (HH:MM:SS లేదా HH:MM)</label>
    <input type="text" id="tob" placeholder="06:19:00" maxlength="8" />

    <label>జన్మ స్థలం</label>
    <input type="text" id="pob" placeholder="Hyderabad" />

    <label>విచారణ విషయం</label>
    <select id="focus">
        <option value="General">సాధారణ జాతక విశ్లేషణ</option>
        <option value="Career">వృత్తి / వ్యాపారం</option>
        <option value="Finance">ఆర్థికం</option>
        <option value="Marriage">వివాహం</option>
        <option value="Health">ఆరోగ్యం</option>
    </select>

    <button id="btn" onclick="submitForm()">జాతకం విశ్లేషించండి →</button>

    <div id="loading">⏳ DB11 Engine run అవుతోంది... దయచేసి వేచి ఉండండి...</div>
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

            // TOB format fix — HH:MM అయితే seconds add చేయి
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
                    document.getElementById('result').innerText = data.summary;
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
        dob = data.get('dob', '').strip()   # DD/MM/YYYY
        tob = data.get('tob', '').strip()   # HH:MM:SS
        pob = data.get('pob', '').strip()

        if not dob or not tob or not pob:
            return jsonify({'success': False, 'error': 'వివరాలు సరిగ్గా ఇవ్వండి'})

        # Location coordinates తెచ్చుకోవడం — DB11_engine లో ఉన్న get_location() వాడటం
        loc_result = db11.get_location(pob)
        if loc_result is None:
            # Default Hyderabad
            lat, lon = 17.3850, 78.4867
        else:
            lat, lon = loc_result

        # Ayanamsha — default Lahiri
        ayan_mode = "lahiri"

        # generate_v21() directly call చేయడం
        result_data = db11.generate_v21(
            dob, tob, lat, lon, pob,
            timezone=5.5,
            ayan_mode=ayan_mode
        )

        # Summary generate చేయడం
        summary = db11.generate_summary(result_data)

        # JSON కూడా save చేయడం (optional)
        out_name = f"DB11_{dob.replace('/', '')}"
        json_path = os.path.join(HOME, f"{out_name}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)

        return jsonify({'success': True, 'summary': summary})

    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e) + '\n' + traceback.format_exc()})


if __name__ == '__main__':
    app.run(debug=True)
