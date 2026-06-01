import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template_string
import json
import requests

import DB11_engine as db11
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
EMAIL_USER = os.environ.get("EMAIL_USER", "")
EMAIL_PASS = os.environ.get("EMAIL_PASS", "")
DEEPSEEK_MODEL = "deepseek-v4-pro"

def send_email_notification(name, mobile, email, dob, tob, pob, gender="male"):
    """Client details మీకు email లో పంపడం"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        msg['Subject'] = f"🔱 దివ్య బ్రహ్మ — కొత్త జాతక Request: {mobile}"

        gender_te = "పురుషుడు" if gender == "male" else "స్త్రీ"
        body = f"""
🔱 దివ్య బ్రహ్మ జ్యోతిష్యం — కొత్త Request

👤 పేరు: {name}
⚧ లింగం: {gender_te}
📱 Mobile: {mobile}
📧 Email: {email}
📅 DOB: {dob}
🕐 TOB: {tob}
📍 Place: {pob}

🔱 divyabrahma.onrender.com
"""
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def get_coords(pob):
    """City name లేదా Lat,Lon format support చేయడం"""
    # Lat,Lon directly enter చేశారా check చేయడం
    pob_stripped = pob.strip()
    if "," in pob_stripped:
        parts = pob_stripped.split(",")
        if len(parts) == 2:
            try:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    return lat, lon
            except ValueError:
                pass  # City name తో continue చేయాలి

    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": pob, "format": "json", "limit": 1}
        headers = {"User-Agent": "DivyaBrahmaJyotish/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code != 200:
            raise ValueError("Location service unavailable — మళ్ళీ try చేయండి")
        text = resp.text.strip()
        if not text or text[0] not in ("[", "{"):
            raise ValueError("Location service error — మళ్ళీ try చేయండి")
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        raise ValueError(
            f"'{pob}' స్థలం కనుగొనలేదు.\n"
            "దయచేసి:\n"
            "1. దగ్గరలో పెద్ద city పేరు enter చేయండి (ఉదా: Hyderabad, Telangana, India)\n"
            "2. లేదా Latitude,Longitude enter చేయండి (ఉదా: 17.2473,80.1514)"
        )
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Location error: {str(e)[:100]} — మళ్ళీ try చేయండి")

def call_deepseek_free_report(full_analysis_prompt):
    """
    build_analysis_prompt() నుండి వచ్చే full prompt Deepseek కి పంపడం
    Tab లో manually చేసినట్టే — V27 + KB1 + KB2 + JSON అన్నీ included
    """
    # Full prompt లో STAGE 7 మాత్రమే return చేయమని instruction add చేయడం
    # V27 లో ECHO + confirmation rules override చేయడం
    overrides = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 WEB APP FINAL INSTRUCTIONS — అన్నిటికంటే PRIORITY:
① ECHO చేయకూడదు — completely skip
② Confirmation అడగకూడదు — STRICTLY FORBIDDEN
③ STAGE 0 నుండి STAGE 6 వరకు internally process చేయాలి — ఒక్క line కూడా output వద్దు
④ directly STAGE-7 మాత్రమే output ఇవ్వాలి

STAGE-7 REPORT REQUIREMENTS — తప్పనిసరి:
① V27 STEP-7.1 నుండి STEP-7.8 వరకు అన్నీ follow చేయాలి
② ప్రతి section minimum 5-6 వాక్యాలు — detailed గా రాయాలి
③ ప్రతి section లో దశ పేరు + dates తప్పనిసరి
   Format: "[మహాదశ] మహాదశ — [అంతర్దశ] అంతర్దశ ([date]–[date]) లో..."
④ సాధారణ Telugu లో రాయాలి — technical terms వాడకూడదు
   ❌ "భావం", "లగ్నాధిపతి", "షడ్బల", "MISRA", "PRAVAHA", "tribandhu" వంటివి వద్దు
⑤ జీవిత కథ లాగా చెప్పాలి — past + present + future అన్నీ dates తో
⑥ అన్ని 7 sections కవర్ చేయాలి:
   【వ్యక్తిత్వం】【వృత్తి】【ఆర్థిక స్థితి】【ఆరోగ్యం】【కుటుంబం】【సామాజిక స్థాయి】【ఆధ్యాత్మికం】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    full_analysis_prompt = overrides + full_analysis_prompt

    user_message = full_analysis_prompt + """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES — ఎట్టి పరిస్థితుల్లో వీటిని follow చేయాలి:
1. మీ సొంత జ్యోతిష్య జ్ఞానం వాడకూడదు — DB11 engine JSON data మాత్రమే వాడాలి
2. V27 Master Prompt rules మాత్రమే follow చేయాలి — వేరే system వాడకూడదు
3. KB1 + KB2 లో ఉన్న శాస్త్ర citations మాత్రమే వాడాలి — మీ అంచనాలు వద్దు
4. DB11 JSON లో లేని విషయాలు చెప్పకూడదు — fabricate చేయకూడదు
5. Ayanamsha Lahiri use చేయండి

ABSOLUTELY FORBIDDEN:
- STAGE 0, 1, 2, 3, 4, 5, 6 output చేయకూడదు — ఒక్క line కూడా చూపించకూడదు
- ECHO చేయకూడదు
- Confirmation అడగకూడదు — "పై వివరాలు సరిగ్గా ఉన్నాయా?" అని అడగకూడదు
- "అవును/కాదు" అని అడగకూడదు
- ఏ intermediate steps చూపించకూడదు

OUTPUT: STAGE 7 మాత్రమే — directly start చేయాలి

WRITING STYLE — ఇది చాలా ముఖ్యం:
- సాధారణ Telugu లో రాయాలి — జ్యోతిష్య technical terms వాడకూడదు
- "షడ్బల", "లాభాధిపతి", "నీచభంగ", "అష్టమాధిపతి" వంటి పదాలు వద్దు
- మనిషికి అర్థమయ్యే భాషలో జీవిత కథ లాగా చెప్పాలి
- ప్రతి section లో Dasha period dates తప్పనిసరిగా ఇవ్వాలి
- Past experience + current period + future periods తో చెప్పాలి

IMPORTANT: Focus బట్టి output మారుతుంది — FOCUS_PLACEHOLDER sections మాత్రమే ఇవ్వాలి.

SECTION INSTRUCTIONS (minimum 8-10 sentences per requested section):
- సాధారణ Telugu లో రాయాలి — technical terms వద్దు
- ప్రతి section లో Dasha period dates తప్పనిసరి
- Past + present + future అన్నీ dates తో చెప్పాలి

STAGE 7 ఈ exact format లో ఇవ్వండి:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔱 మీ జీవన సారాంశం
వయస్సు: [వయస్సు] సంవత్సరాలు | TIER-[1/2/3]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTIONS_PLACEHOLDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ గమనిక: ఇవి సంభావ్యతలు మాత్రమే. వ్యక్తిగత విషయాల కోసం అనుభవజ్ఞుడైన జ్యోతిష్యుడిని సంప్రదించండి.
🔱 దివ్య బ్రహ్మ ప్రవాహ V27.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

తెలుగులో మాత్రమే సమాధానం ఇవ్వండి."""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 32768,
        "temperature": 0.3
    }

    resp = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=180
    )
    result = resp.json()
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    elif "error" in result:
        return f"Deepseek Error: {result['error'].get('message', str(result['error']))}"
    return f"Analysis రాలేదు — Response: {str(result)[:500]}"


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
        .contact { text-align: center; color: #aaa; font-size: 13px; margin-bottom: 16px; }
    </style>
</head>
<body>
    <h1>🔱 దివ్య బ్రహ్మ జ్యోతిష్యం</h1>
    <p class="subtitle">DB11 Engine V27 — శాస్త్ర ఆధారిత Telugu Jyotish Report</p>
    <p class="contact">📞 సంప్రదించండి: <a href="tel:9381394456" style="color:#ffd700;">9381394456</a></p>

    <label>మీ పూర్తి పేరు <span style="color:#ff6b6b;">*</span></label>
    <input type="text" id="fullname" placeholder="మీ పేరు enter చేయండి" required />

    <label>లింగం <span style="color:#ff6b6b;">*</span></label>
    <div style="margin-top:8px; display:flex; gap:20px;">
        <label style="margin:0; display:flex; align-items:center; gap:8px; cursor:pointer;">
            <input type="radio" name="gender" value="male" id="gender_male" required />
            <span>పురుషుడు (Male)</span>
        </label>
        <label style="margin:0; display:flex; align-items:center; gap:8px; cursor:pointer;">
            <input type="radio" name="gender" value="female" id="gender_female" />
            <span>స్త్రీ (Female)</span>
        </label>
    </div>

    <label>మీ మొబైల్ నంబర్ <span style="color:#ff6b6b;">*</span></label>
    <input type="tel" id="mobile" placeholder="దేశ కోడ్ తో enter చేయండి (ఉదా: +91XXXXXXXXXX లేదా 10 digit)" maxlength="15" required />

    <label>మీ Email ID <span style="color:#ff6b6b;">*</span></label>
    <input type="email" id="email_id" placeholder="yourname@gmail.com" required />

    <label>జన్మ తేదీ <span style="color:#ff6b6b;">*</span> <span style="color:#aaa; font-size:12px;">(DD/MM/YYYY format)</span></label>
    <input type="text" id="dob" placeholder="DD/MM/YYYY" maxlength="10" />

    <label>జన్మ సమయం <span style="color:#ff6b6b;">*</span> <span style="color:#aaa; font-size:12px;">(24 గంటల format లో — ఉదా: సాయంత్రం 6:19 అంటే 18:19)</span></label>
    <input type="text" id="tob" placeholder="HH:MM (ఉదా: 06:19 లేదా 18:19)" maxlength="8" />

    <label>జన్మ స్థలం <span style="color:#ff6b6b;">*</span> <span style="color:#aaa; font-size:12px;">(City, State, Country — English లో)</span></label>
    <input type="text" id="pob" placeholder="ఉదా: Hyderabad, Telangana, India" />
    <p style="color:#aaa; font-size:12px; margin-top:4px;">⚠️ చిన్న town అయితే దగ్గరలో పెద్ద city పేరు enter చేయండి. లేదా Latitude,Longitude enter చేయండి (ఉదా: 17.2473,80.1514)</p>

    <label>విచారణ విషయం <span style="color:#ff6b6b;">*</span></label>
    <select id="focus">
        <option value="" disabled selected>-- select చేయండి --</option>
        <option value="General">అ) సంపూర్ణ పూర్తి జాతకము</option>
        <option value="Career">ఆ) వృత్తి / వ్యాపారం</option>
        <option value="Finance">ఇ) ఆర్థికం</option>
        <option value="Marriage">ఈ) వివాహం</option>
        <option value="Health">ఉ) ఆరోగ్యం</option>
        <option value="Personality">ఊ) వ్యక్తిత్వం</option>
        <option value="Education">ఎ) విద్య / చదువు</option>
        <option value="Family">ఏ) కుటుంబం</option>
        <option value="Social">ఐ) సామాజిక స్థాయి</option>
        <option value="Spiritual">ఒ) ఆధ్యాత్మికం</option>
    </select>

    <button id="btn" onclick="submitForm()">జాతకం విశ్లేషించండి →</button>

    <div id="loading">
        <!-- Layer 1: Title -->
        <p style="font-size:20px; color:#ffd700; text-align:center; margin-bottom:16px;">
            🔱 మీ జాతకాన్ని విశ్లేషిస్తున్నాము...
        </p>

        <!-- Layer 2: Progress stages -->
        <div id="progress-stage" style="text-align:center; color:#7eb8f7; font-size:14px; margin-bottom:20px; min-height:24px;"></div>

        <!-- Layer 3: Animated planets -->
        <div style="text-align:center; font-size:28px; margin-bottom:20px;" id="planet-anim">
            🌞 🌙 ♂ ☿ ♃ ♀ ♄
        </div>

        <!-- Layer 1: Rotating Shlokas -->
        <div style="background:#0d1b3e; border:1px solid #ffd700; border-radius:10px; padding:16px; margin-bottom:20px; text-align:center;">
            <p style="color:#ffd700; font-size:13px; margin-bottom:8px;">📜 మహర్షుల వాక్కు</p>
            <p id="shloka-te" style="color:#fff; font-size:15px; font-style:italic; margin-bottom:6px;"></p>
            <p id="shloka-hi" style="color:#aaa; font-size:13px; margin-bottom:6px;"></p>
            <p id="shloka-en" style="color:#7eb8f7; font-size:12px;"></p>
            <p id="shloka-src" style="color:#ffd700; font-size:11px; margin-top:6px;"></p>
        </div>

        <!-- Layer 4: Did you know -->
        <div style="background:#16213e; border-radius:8px; padding:12px; text-align:center;">
            <p style="color:#ffd700; font-size:12px; margin-bottom:6px;">💡 తెలుసా?</p>
            <p id="did-you-know" style="color:#ccc; font-size:13px; line-height:1.6;"></p>
        </div>
    </div>

    <script>
    const shlokas = [
        {
            te: "జన్మ లగ్నం మహాభాగ్యం, గ్రహాః కాలస్య సూచకాః",
            hi: "जन्म लग्नं महाभाग्यं, ग्रहाः कालस्य सूचकाः",
            en: "The birth ascendant is the greatest fortune; planets are the indicators of time",
            src: "— పరాశర మహర్షి, బృహత్ పరాశర హోరా శాస్త్రం"
        },
        {
            te: "గ్రహాణాం చేష్టితం సర్వం ఫలదం జన్మ కాలతః",
            hi: "ग्रहाणां चेष्टितं सर्वं फलदं जन्म कालतः",
            en: "All planetary movements bear fruit from the moment of birth",
            src: "— వరాహమిహిర, బృహత్ జాతకం"
        },
        {
            te: "యద్భావం తద్భవేత్ సత్యం, గ్రహదృష్ట్యా న సంశయః",
            hi: "यद्भावं तद्भवेत् सत्यं, ग्रहदृष्ट्या न संशयः",
            en: "What is indicated by the houses comes true through planetary aspects, without doubt",
            src: "— కళ్యాణ వర్మ, సారావళి"
        },
        {
            te: "లగ్నాధిపో బలీ యస్య, తస్య సర్వం శుభం భవేత్",
            hi: "लग्नाधिपो बली यस्य, तस्य सर्वं शुभं भवेत्",
            en: "One whose ascendant lord is strong — for them, everything becomes auspicious",
            src: "— మంత్రేశ్వర, ఫలదీపిక"
        }
    ];

    const stages = [
        "🔍 గ్రహ స్థానాలు calculate అవుతున్నాయి...",
        "📊 17 వర్గ చక్రాలు తయారవుతున్నాయి...",
        "⚡ మహాదశ కాలాలు నిర్ణయిస్తున్నాయి...",
        "📚 శాస్త్ర గ్రంథాలు పరిశీలిస్తున్నాయి...",
        "🔱 షడ్బల, యోగాలు విశ్లేషిస్తున్నాయి...",
        "✨ మీ జాతక సారాంశం తయారవుతోంది..."
    ];

    const facts = [
        "జ్యోతిష్య శాస్త్రం 5000+ సంవత్సరాల పురాతన భారతీయ విజ్ఞానం — వేదాంగాలలో ఒకటి.",
        "వరాహమిహిర క్రీ.శ. 505-587 లో జీవించారు — బృహత్ జాతకం రాశారు. ఇది నేటికీ జ్యోతిష్య మూల గ్రంథం.",
        "మీ జన్మ సమయంలో ఉన్న 9 గ్రహాల స్థానాలు — మీ జీవిత పాఠ్యాంశాన్ని నిర్ణయిస్తాయని శాస్త్రం చెప్తుంది.",
        "లాహిరి అయనాంశం భారత ప్రభుత్వం officially adopt చేసిన ayanamsha — DB11 engine ఇదే వాడుతుంది.",
        "వింశోత్తరి దశా పద్ధతి 120 సంవత్సరాల జీవిత చక్రాన్ని 9 గ్రహాలకు విభజిస్తుంది.",
        "మీ జన్మ నక్షత్రం బట్టి మీ మహాదశ మొదలవుతుంది — ఇది పరాశరుడు నిర్ణయించిన పద్ధతి."
    ];

    const planets = ["🌞","🌙","♂","☿","♃","♀","♄","☊","☋"];
    let sloka_i = 0, stage_i = 0, fact_i = 0, planet_i = 0;

    function updateShloka() {
        const s = shlokas[sloka_i % shlokas.length];
        document.getElementById('shloka-te').textContent = s.te;
        document.getElementById('shloka-hi').textContent = s.hi;
        document.getElementById('shloka-en').textContent = '"' + s.en + '"';
        document.getElementById('shloka-src').textContent = s.src;
        sloka_i++;
    }

    function updateStage() {
        document.getElementById('progress-stage').textContent = stages[stage_i % stages.length];
        stage_i++;
    }

    function updateFact() {
        document.getElementById('did-you-know').textContent = facts[fact_i % facts.length];
        fact_i++;
    }

    function updatePlanets() {
        const p = planets[planet_i % planets.length];
        document.getElementById('planet-anim').textContent = 
            planets.map((pl, i) => i === planet_i % planets.length ? '✨' + pl + '✨' : pl).join(' ');
        planet_i++;
    }

    let loadingIntervals = [];

    function startLoadingAnimation() {
        updateShloka(); updateStage(); updateFact(); updatePlanets();
        loadingIntervals.push(setInterval(updateShloka, 4000));
        loadingIntervals.push(setInterval(updateStage, 2500));
        loadingIntervals.push(setInterval(updateFact, 5000));
        loadingIntervals.push(setInterval(updatePlanets, 800));
    }

    function stopLoadingAnimation() {
        loadingIntervals.forEach(clearInterval);
        loadingIntervals = [];
    }
    </script>
    <div id="result"></div>
    <div id="footer-contact" style="display:none; text-align:center; margin-top:24px; padding:16px; background:#16213e; border-radius:8px; border:1px solid #333;">
        <p style="color:#ffd700; font-size:15px;">🔱 దివ్య బ్రహ్మ జ్యోతిష్యం</p>
        <p style="color:#aaa; font-size:14px;">మరిన్ని వివరాలకు సంప్రదించండి: <a href="tel:9381394456" style="color:#ffd700;">📞 9381394456</a></p>
    </div>

    <script>
        async function submitForm() {
            const dob = document.getElementById('dob').value.trim();
            const tob = document.getElementById('tob').value.trim();
            const pob = document.getElementById('pob').value.trim();
            const focus = document.getElementById('focus').value;

            const fullname = document.getElementById('fullname').value.trim();
            const gender_el = document.querySelector('input[name="gender"]:checked');
            const gender = gender_el ? gender_el.value : '';
            const mobile = document.getElementById('mobile').value.trim();
            const email_id = document.getElementById('email_id').value.trim();

            if (!fullname) {
                alert('మీ పేరు enter చేయండి');
                return;
            }
            if (!focus) {
                alert('విచారణ విషయం select చేయండి');
                return;
            }
            if (!gender) {
                alert('లింగం select చేయండి');
                return;
            }
            if (!mobile || !email_id || !dob || !tob || !pob) {
                alert('అన్ని వివరాలు తప్పనిసరిగా enter చేయండి');
                return;
            }
            if (mobile.length < 10) {
                alert('సరైన మొబైల్ నంబర్ enter చేయండి');
                return;
            }

            let tobFull = tob;
            if (tob.length === 5) tobFull = tob + ':00';

            document.getElementById('btn').disabled = true;
            document.getElementById('loading').style.display = 'block';
            startLoadingAnimation();
            document.getElementById('result').style.display = 'none';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ dob, tob: tobFull, pob, focus, mobile, email_id, fullname, gender })
                });
                const data = await response.json();
                document.getElementById('loading').style.display = 'none';
                stopLoadingAnimation();
                document.getElementById('btn').disabled = false;
                document.getElementById('result').style.display = 'block';
                if (data.success) {
                    document.getElementById('result').className = '';
                    document.getElementById('result').innerText = data.analysis;
                    document.getElementById('footer-contact').style.display = 'block';
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
        mobile = data.get('mobile', '').strip()
        email_id = data.get('email_id', '').strip()
        fullname = data.get('fullname', '').strip()
        gender = data.get('gender', 'male').strip()

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

        # Step 3: build_analysis_prompt() — V27 + KB1 + KB2 + JSON full prompt
        full_prompt = db11.build_analysis_prompt(result_data, BASE_DIR)


        # Step 5: Deepseek కి full prompt పంపడం
        # Focus specific instruction add చేయడం
        # Focus బట్టి sections నిర్ణయించడం
        focus_sections_map = {
            "General":     "V27 STEP-7.0 నుండి STEP-7.8 వరకు అన్నీ — వ్యక్తిత్వం, చదువు, వృత్తి, ఆర్థికం, ఆరోగ్యం, కుటుంబం, సామాజిక స్థాయి, ఆధ్యాత్మికం అన్నీ TIER బట్టి వివరంగా",
            "Career":      "【వృత్తి / వ్యాపారం】 — వివరంగా, అన్ని dashas తో",
            "Finance":     "【ఆర్థిక స్థితి】 — వివరంగా, అన్ని dashas తో",
            "Marriage":    "V27 STEP-7.6 ప్రకారం కుటుంబం section లో వివాహం భాగం వివరంగా చెప్పాలి — జీవిత భాగస్వామి, వివాహ timing, దాంపత్య జీవితం dates తో",
            "Health":      "【ఆరోగ్యం】 — వివరంగా, అన్ని dashas తో",
            "Personality": "【వ్యక్తిత్వం】 — వివరంగా",
            "Education":   "【చదువు / విద్య】 — V27 STEP-7.2 ప్రకారం వివరంగా",
            "Family":      "【కుటుంబం】 — తల్లిదండ్రులు, పిల్లలు, సోదరులు విడిగా, అన్ని dashas తో",
            "Social":      "【సామాజిక స్థాయి / నాయకత్వం】 — వివరంగా, అన్ని dashas తో",
            "Spiritual":   "【ఆధ్యాత్మికం】 — వివరంగా, అన్ని dashas తో",
        }
        focus_sections = focus_sections_map.get(focus, focus_sections_map["General"])
        focus_instruction = f"కేవలం ఈ section(s) మాత్రమే ఇవ్వాలి — మిగతావి వద్దు:\n{focus_sections}"
        full_prompt = full_prompt.replace("SECTIONS_PLACEHOLDER", focus_sections)
        full_prompt = full_prompt.replace("FOCUS_PLACEHOLDER", focus_sections)
        full_prompt = full_prompt + f"\n\n⚠️ STRICT FOCUS: {focus_instruction}"

        # Gender context prompt కి add చేయడం
        gender_context = ""
        if gender == "female":
            gender_context = "\n\n⚠️ GENDER CONTEXT: ఈ జాతకం స్త్రీది. విశ్లేషణలో 'మీ భర్త', 'వివాహ జీవితం' వంటి స్త్రీకి సంబంధించిన పదాలు వాడాలి. సంతాన విషయంలో తల్లి దృక్కోణం నుండి చెప్పాలి."
        else:
            gender_context = "\n\n⚠️ GENDER CONTEXT: ఈ జాతకం పురుషుడిది. విశ్లేషణలో 'మీ భార్య', 'వివాహ జీవితం' వంటి పురుషుడికి సంబంధించిన పదాలు వాడాలి."
        full_prompt = full_prompt + gender_context

        analysis = call_deepseek_free_report(full_prompt)

        # Step 5: JSON save
        out_name = f"DB11_{dob.replace('/', '')}"
        json_path = os.path.join(BASE_DIR, f"{out_name}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)

        # Email notification పంపడం
        send_email_notification(fullname, mobile, email_id, dob, tob, pob, gender)

        return jsonify({'success': True, 'analysis': analysis})

    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e) + '\n' + traceback.format_exc()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
