"""
DB11-DIVYA BRAHMA ENGINE v11.0
Pure Calculation Engine — Classical Sources Only (BPHS + Brihat Jataka + Jataka Martanda)

DB10 నుండి DB11 కి additions (V27 Calibration Notes నుండి — Universal fields మాత్రమే):
  CAL-NOTE-4:  rikta_flag_scope — "health_timing_only" (ఆర్థిక ఫలాలకు వర్తించదు)
  CAL-NOTE-8:  health_risk_flag — 12వ bhava + Avrohi గ్రహం antardasha లో TRUE
  CAL-NOTE-9:  pratyantar.lord_info.bindu_phala — pratyantara lord bindu value
  CAL-NOTE-13: exaltation_aarohi_flag — ఉచ్చం + Aarohi రెండూ TRUE అయినప్పుడు
  CAL-NOTE-14: rahu.delivery_mechanism — "unexpected_network" (అన్ని lagna లకు universal)

DB9 నుండి DB10 కి additions:
  ADD-10: లఘు స్ఫుటము & భావ స్ఫుటము — Jataka Martanda PDF
  ADD-11: Bridge Layer — KB2 lagna section + V27 combine → analysis prompt

PRECEDENCE: Brihat Jataka (Varahamihira) > BPHS (Parashara)
EXCEPTION : Shadbala = BPHS only (Abda/Masa/Hora/Ayana/Chesta/Saptavargaja)

DB11 Calibration Notes (V27 validation — 25/11/1966 ground truth):
  అన్ని DB10 logic intact — 5 universal fields మాత్రమే add చేయబడ్డాయి

DB8 నుండి DB9 కి 8 కొత్త Additions (DB8 logic ఏదీ మార్చలేదు):
  ADD-1: మాంది/గులిక longitude — BPHS Ch.13-14 (వారవారీ దిన/రాత్రి ghati table)
  ADD-2: విశేష లగ్నాలు — హోరా లగ్నం, భావ లగ్నం, ఘటి లగ్నం — BPHS Ch.25
  ADD-3: తాత్కాలిక మైత్రి + పంచధా మైత్రి — Brihat Jataka Ch.2 Sl.18, BPHS
  ADD-4: పిండాయుర్దాయ పూర్తి calculation — Brihat Jataka Ch.7 Sl.1-4
  ADD-5: కాల సర్ప యోగం detection — Brihat Jataka Ch.12 (Sarpa yoga)
  ADD-6: జైమిని చర కారకాలు (Atmakaraka etc) — BPHS Jaimini section
  ADD-7: గ్రహ అవస్థ (బాల/కుమార/యువ/వృద్ధ/మృత) — BPHS Ch.45 degree-based
  ADD-8: గోచర (Transit) current positions — Brihat Jataka Ch.22 Sl.6 timing rules

Jataka Martanda నుండి 9 కొత్త Additions (DB9 Step additions):
  STEP-1: అధిపత్య శుభ/పాప — లగ్నం బట్టి 12 లగ్నాల table — Jataka Martanda PDFs
  STEP-2: ఆరూఢ లగ్నం calculation — Rajayogadyayamu PDF pages 7-8
  STEP-3: భావ బల (స్థాన+అధిపతి+కారక) — Yogas PDF pages 110-115
  STEP-4: రాజ యోగ flags (పంచ గ్రహ మాలిక, అధి యోగ) — Rajayogadyayamu PDF
  STEP-5: గ్రహ యుద్ధ — కుజుడు always wins rule — Jataka Martanda 81-82 PDF
  STEP-6: అష్టకవర్గ బిందు ఫలాలు Telugu names — Jataka Martanda 297-310 PDF
  STEP-7: Navamsha quality — No change (DB9 decanate_quality sufficient)
  STEP-8: ఆరూఢ లగ్న రాజ యోగ — Rajayogadyayamu PDF pages 7-8
  STEP-9: భాగ్య+రాజ్య అధిపతి యోగ — Rajayogadyayamu PDF pages 1-2

DB8 లో ఉన్న 7 Fixes అన్నీ intact:
  FIX-A: R4  check_lagna_bala_triple function implemented + called + special_flags
  FIX-B: R9  dhatu/dosha fields added to planet JSON output
  FIX-C: R16 Aarohi/Avrohi actual arc calculation (not hardcoded Neutral)
  FIX-D: R18 get_combust_exit_timing function integrated
  FIX-E: R23 opposite_results_flag via NATURAL_ENEMIES (not hardcoded False)
  FIX-F: R30 dasha_roga field in mahadasha + antardasha JSON
  FIX-G: R4  lagna_bala_triple in special_flags output

Shadbala restored from DB7 (BPHS Ch.27 exact):
  FIX-13 Saptavargaja, FIX-14 Abda/Masa, FIX-15 Hora, FIX-16 Ayana, FIX-17 Chesta

Installation: pip install ephem pyswisseph
Usage: python DB11_engine.py
"""

import ephem, math, datetime, json

try:
    import swisseph as swe
    SWE_OK = True
except ImportError:
    SWE_OK = False
    print("pip install pyswisseph చేయండి.")

# ═══════════════════════════════════════════════════════════
# DB8 CONSTANTS — అన్నీ intact (ఏదీ మార్చలేదు)
# ═══════════════════════════════════════════════════════════
RASHI_TE={1:"మేషం",2:"వృషభం",3:"మిథునం",4:"కర్కాటకం",5:"సింహం",6:"కన్య",7:"తులం",8:"వృశ్చికం",9:"ధనుస్సు",10:"మకరం",11:"కుంభం",12:"మీనం"}
NAKSHATRA_TE=["అశ్విని","భరణి","కృత్తిక","రోహిణి","మృగశిర","ఆర్ద్ర","పునర్వసు","పుష్యమి","ఆశ్లేష","మఖ","పూర్వఫల్గుని","ఉత్తరఫల్గుని","హస్త","చిత్త","స్వాతి","విశాఖ","అనురాధ","జ్యేష్ఠ","మూల","పూర్వాషాఢ","ఉత్తరాషాఢ","శ్రవణం","ధనిష్ఠ","శతభిష","పూర్వాభాద్ర","ఉత్తరాభాద్ర","రేవతి"]
PLANET_TE={"sun":"సూర్యుడు","moon":"చంద్రుడు","mars":"కుజుడు","mercury":"బుధుడు","jupiter":"గురువు","venus":"శుక్రుడు","saturn":"శని","rahu":"రాహు","ketu":"కేతు"}
PLANET_EMOJI={"sun":"🌞","moon":"🌙","mars":"♂","mercury":"☿","jupiter":"♃","venus":"♀","saturn":"♄","rahu":"☊","ketu":"☋"}
DASHA_ORDER=["ketu","venus","sun","moon","mars","rahu","jupiter","saturn","mercury"]
DASHA_YEARS={"ketu":7,"venus":20,"sun":6,"moon":10,"mars":7,"rahu":18,"jupiter":16,"saturn":19,"mercury":17}
UCCHA_LON={"sun":10.0,"moon":33.0,"mars":298.0,"mercury":165.0,"jupiter":95.0,"venus":357.0,"saturn":200.0}
UCCHA_RASHI={"sun":1,"moon":2,"mars":10,"mercury":6,"jupiter":4,"venus":12,"saturn":7}
NEECHA_RASHI={"sun":7,"moon":8,"mars":4,"mercury":12,"jupiter":10,"venus":6,"saturn":1}
STRENGTH_PERCENT={"ఉచ్చం":100,"మూల త్రికోణం":75,"స్వరాశి":50,"మిత్ర":25,"శత్రు":12.5,"నీచం":0,"దగ్ధం":0}
SWARASHI={"sun":[5],"moon":[4],"mars":[1,8],"mercury":[3,6],"jupiter":[9,12],"venus":[2,7],"saturn":[10,11]}
MOOL_TRIKONA={"sun":5,"moon":2,"mars":1,"mercury":6,"jupiter":9,"venus":7,"saturn":11}
DAY_PLANETS=["sun","jupiter","saturn"]
NIGHT_PLANETS=["moon","mars","venus"]
NAISARGIKA_ORDER={"saturn":1,"mars":2,"mercury":3,"jupiter":4,"venus":5,"moon":6,"sun":7}
NAISARGIKA_VIRUPA={"sun":60.0,"moon":51.43,"venus":42.86,"jupiter":34.29,"mercury":25.71,"mars":17.14,"saturn":8.57}
DHATU_MAP={"sun":"ఎముకలు","moon":"రక్తం","mars":"మజ్జ","mercury":"చర్మం","jupiter":"మెదడు","venus":"శుక్లం","saturn":"నరాలు"}
DOSHA_MAP={"sun":"పిత్త","moon":"వాత+కఫ","mars":"పిత్త","mercury":"త్రిదోషం","jupiter":"కఫ","venus":"వాత+కఫ","saturn":"వాత"}
DASHA_ROGA={"sun":"జ్వరం/గుండె/పిత్త","moon":"దగ్గు/వాత/రక్తం","mars":"రక్తం/వ్రణం","mercury":"నాడీ/త్రిదోషం","jupiter":"చెవులు/కఫం","venus":"మూత్ర/గుహ్యం","saturn":"వాత/కీళ్లు"}
KENDRA={1,4,7,10}; PANAPHAR={2,5,8,11}; APOKLIMA={3,6,9,12}; UPACHAYA={3,6,10,11}
BHAVA_LORDS={1:"mars",2:"venus",3:"mercury",4:"moon",5:"sun",6:"mercury",7:"venus",8:"mars",9:"jupiter",10:"saturn",11:"saturn",12:"jupiter"}
DIV_DESC={"D1":"లగ్న చక్రం","D2":"హోర","D3":"ద్రేష్కాణ","D4":"చతుర్థాంశ","D7":"సప్తాంశ","D8":"అష్టమాంశ","D9":"నవాంశ","D10":"దశాంశ","D12":"ద్వాదశాంశ","D16":"షోడశాంశ","D20":"వింశాంశ","D24":"చతుర్వింశాంశ","D27":"భాంశ","D30":"త్రింశాంశ","D40":"ఖవేదాంశ","D45":"అక్షవేదాంశ","D60":"షష్టాంశ"}
NATURAL_FRIENDS={"sun":{"moon","mars","jupiter"},"moon":{"sun","mercury"},"mars":{"sun","moon","jupiter"},"mercury":{"sun","venus"},"jupiter":{"sun","moon","mars"},"venus":{"mercury","saturn"},"saturn":{"mercury","venus"}}
NATURAL_ENEMIES={"sun":{"venus","saturn"},"moon":set(),"mars":{"mercury"},"mercury":{"moon"},"jupiter":{"mercury","venus"},"venus":{"sun","moon"},"saturn":{"sun","moon","mars"}}
SHADBALA_MIN={"sun":390,"moon":360,"mars":300,"mercury":420,"jupiter":390,"venus":330,"saturn":300}
CONFIRM_WORDS={"అవును","సరే","సరి","అవు","ఓకే","yes","y","ok","okay","confirm","correct","✅"}
WRONG_WORDS={"కాదు","తప్పు","లేదు","no","n","wrong","incorrect","❌"}

# ═══════════════════════════════════════════════════════════
# STEP-1: అధిపత్య శుభ/పాప lookup — Jataka Martanda PDFs
# Source: 89-95, 215-217, 212-214 PDFs
# రాహు/కేతులకు ఆధిపత్యం లేదు (BPHS) — వారు ఈ పట్టికలో లేరు
# Planet names Telugu లో — PLANET_TE_SHORT మ్యాప్ తో match చేయాలి
# ═══════════════════════════════════════════════════════════
PLANET_TE_SHORT = {
    "sun":"రవి","moon":"చంద్ర","mars":"కుజ","mercury":"బుధ",
    "jupiter":"గురు","venus":"శుక్ర","saturn":"శని"
}

LAGNA_SHUBHA_PAPA_LOOKUP = {
    "మేషం":     {"శుభులు":["రవి","కుజ","గురు","శని"],    "పాపులు":["చంద్ర","శుక్ర","బుధ"],           "సములు":[]},
    "వృషభం":    {"శుభులు":["రవి","శని","బుధ","శుక్ర"],   "పాపులు":["చంద్ర","గురు"],                  "సములు":["కుజ"]},
    "మిథునం":   {"శుభులు":["శుక్ర","శని"],               "పాపులు":["రవి","కుజ","గురు"],              "సములు":["చంద్ర","బుధ"]},
    "కర్కాటకం": {"శుభులు":["చంద్ర","శుక్ర"],             "పాపులు":["కుజ","శని"],                     "సములు":["రవి","బుధ","గురు"]},
    "సింహం":    {"శుభులు":["రవి","కుజ","గురు"],          "పాపులు":["బుధ","శుక్ర"],                   "సములు":["చంద్ర","శని"]},
    "కన్య":     {"శుభులు":["శుక్ర","శని"],               "పాపులు":["చంద్ర","కుజ","గురు"],            "సములు":["రవి","బుధ"]},
    "తులం":     {"శుభులు":["కుజ","బుధ","శని"],           "పాపులు":["రవి","చంద్ర","గురు"],            "సములు":["శుక్ర"]},
    "వృశ్చికం": {"శుభులు":["రవి","చంద్ర","గురు","శని"],  "పాపులు":["బుధ","శుక్ర"],                   "సములు":["కుజ"]},
    "ధనుస్సు":  {"శుభులు":["రవి","కుజ"],                 "పాపులు":["చంద్ర","బుధ","శుక్ర","శని"],     "సములు":["గురు"]},
    "మకరం":     {"శుభులు":["కుజ","బుధ","శుక్ర"],         "పాపులు":["రవి","చంద్ర"],                   "సములు":["శని"]},
    "కుంభం":    {"శుభులు":["రవి","కుజ","బుధ","శుక్ర"],   "పాపులు":["చంద్ర","గురు"],                  "సములు":["శని"]},
    "మీనం":     {"శుభులు":["చంద్ర","కుజ","గురు"],        "పాపులు":["రవి","బుధ","శుక్ర","శని"],       "సములు":[]}
}

# STEP-5: కుజుడు always wins in yuddha — Jataka Martanda 81-82 PDF
# PDF: "అంగారకునితో బుధ, గురు, శుక్ర, శనులు కలిసిన యెడల గ్రహాయుద్ధమందు పరాజితులగుదురు. కుజుడు విజేత."
MARS_ALWAYS_WINS_OVER = {"mercury","jupiter","venus","saturn"}

# STEP-6: అష్టకవర్గ బిందు ఫలాలు — Jataka Martanda 297-310 PDF
# PDF exact: "1 ఏందువువ్ని యెడల మహారోగము, 2=మనోవ్యాపనము, 3=ప్రకాశము,
# 4=స్వల్పధనము, 5=పోఖ్యము, 6=మిక్కిలి పోఖ్యము, 7=భాగ్యము, 8=చైభుతము"
ASHTAKA_PHALA = {
    0:"శూన్యం",1:"మహారోగము",2:"మనోవ్యాపనము",3:"ప్రకాశము",
    4:"స్వల్పధనము",5:"పోఖ్యము",6:"మిక్కిలి పోఖ్యము",7:"భాగ్యము",8:"చైభుతము"
}

# ═══════════════════════════════════════════════════════════
# DB11 CAL-NOTE-4: rikta_flag_scope
# V27 Calibration: Rikta flag = health/timing only — NOT ఆర్థిక suppress
# ═══════════════════════════════════════════════════════════
RIKTA_FLAG_SCOPE = "health_timing_only"
RIKTA_FLAG_NOTE  = "Rikta దశ = health/timing జాగ్రత్త మాత్రమే. ఆర్థిక ఫలాలు suppress చేయదు."

# ═══════════════════════════════════════════════════════════
# DB11 CAL-NOTE-13: exaltation_aarohi_flag per planet
# ఉచ్చం + Aarohi రెండూ = bindu_phala override సంభావ్యత
# ═══════════════════════════════════════════════════════════
def calc_exaltation_aarohi_flag(planet, strength, aarohi_avrohi):
    """
    CAL-NOTE-13: నైసర్గిక శుభ గ్రహం ఉచ్చం + Aarohi = bindu_phala override
    TRUE అయితే: bindu తక్కువ అయినా ఆ గ్రహం ఫలాలు స్పష్టంగా వస్తాయి
    """
    is_exalted  = (strength == "ఉచ్చం")
    is_aarohi   = ("Aarohi" in str(aarohi_avrohi))
    return is_exalted and is_aarohi

# ═══════════════════════════════════════════════════════════
# DB11 CAL-NOTE-14: rahu delivery_mechanism
# రాహు ఏ భావంలో ఉన్నా delivery = unexpected, network ద్వారా
# ═══════════════════════════════════════════════════════════
RAHU_DELIVERY_MECHANISM = "unexpected_network"
RAHU_DELIVERY_NOTE = (
    "రాహు dasha/antardasha ఫలాలు = unexpected, sudden, నెట్వర్క్/unconventional మార్గంలో వస్తాయి. "
    "KB2 classical phala text literal గా కాదు — రాహు స్వభావం ద్వారా delivery జరుగుతుంది."
)

# రాహు భావం వారీగా unexpected ఫలాల mapping (CAL-NOTE-14 table)
RAHU_BHAVA_UNEXPECTED = {
    1:  "వ్యక్తిత్వంలో sudden మార్పు, జీవన దిశ unexpected గా మారుతుంది",
    2:  "ధనం unexpected గా వస్తుంది లేదా పోతుంది, వాక్కులో unusual power",
    3:  "సోదర సంబంధిత unexpected సంఘటనలు, sudden ప్రయాణాలు, media గుర్తింపు",
    4:  "గృహంలో sudden మార్పులు, ఆస్తి unexpected గా వస్తుంది లేదా వివాదం",
    5:  "సంతానం unexpected, speculation లో sudden లాభ/నష్టం, unconventional బుద్ధి",
    6:  "శత్రు జయం unexpected, వ్యాధి unexpected గా వస్తుంది/నయమవుతుంది, ఆర్థిక లాభం",
    7:  "వివాహం/భాగస్వామి unexpected మార్గంలో, విదేశీయులతో సంబంధాలు",
    8:  "sudden health crisis కానీ unexpected గా బయటపడడం, వారసత్వ/insurance లాభం",
    9:  "భాగ్యం unexpected గా తెరుచుకుంటుంది, unconventional spiritual path",
    10: "వృత్తిలో sudden opportunity లేదా sudden పతనం, unexpected కీర్తి",
    11: "నెట్వర్క్ ద్వారా sudden large gains, unexpected వ్యక్తుల ద్వారా లాభం",
    12: "unexpected విదేశ అవకాశం, sudden పెద్ద ఖర్చులు, hospital unexpected గా"
}

# ═══════════════════════════════════════════════════════════
# DB11 CAL-NOTE-8: health_risk_flag for antardasha
# 12వ bhava + Avrohi గ్రహం antardasha = health risk flag
# ═══════════════════════════════════════════════════════════
def calc_health_risk_flag(planet, d1p, aarohi_avrohi):
    """
    CAL-NOTE-8: 12వ bhava + Avrohi గ్రహం antardasha లో health risk
    TRUE = hospitalization/surgery possibility అని separately flag చేయాలి
    """
    bhava    = d1p.get(planet, {}).get("bhava", 0)
    is_avrohi = ("Avrohi" in str(aarohi_avrohi))
    return (bhava == 12) and is_avrohi

# ═══════════════════════════════════════════════════════════
# DB11 CAL-NOTE-9: pratyantar bindu_phala helper
# shadbala_v19_practical నుండి pratyantar lord bindu value
# ═══════════════════════════════════════════════════════════
def get_pratyantar_bindu_phala(pratyantar_planet, ashtaka_data):
    """
    CAL-NOTE-9: Pratyantara lord bindu_phala = short-term ఆర్థిక స్థితి indicator
    ashtaka_data = shadbala_v19_practical dict
    """
    if pratyantar_planet in ("rahu", "ketu"):
        return None  # రాహు/కేతులకు bindu_phala లేదు
    planet_data  = ashtaka_data.get(pratyantar_planet, {})
    bindus       = planet_data.get("bindus_in_rashi", 0)
    bindu_phala  = planet_data.get("bindu_phala", "")
    return {
        "planet_en":   pratyantar_planet,
        "planet_te":   PLANET_TE.get(pratyantar_planet, "?"),
        "bindus":      bindus,
        "bindu_phala": bindu_phala,
        "note":        "CAL-NOTE-9: short-term ఆర్థిక స్థితి indicator"
    }



# ═══════════════════════════════════════════════════════════
# CAL-NOTE-18: TRIBANDHU SIDDHANTA
# Source: Brihat Jataka Ch.2 + BPHS panchadha_maitri
# ═══════════════════════════════════════════════════════════
TRIBANDHU_KARAKA = {
    "sun":"ఆత్మ/తండ్రి","moon":"మనస్సు/తల్లి","mars":"శక్తి/సోదరుడు",
    "mercury":"వాక్కు/విద్య","jupiter":"జ్ఞానం/సంతానం","venus":"కామం/భార్య",
    "saturn":"దుఃఖం/సేవ","rahu":"unexpected/నెట్వర్క్","ketu":"మోక్షం/ఆధ్యాత్మికత"
}

def calc_tribandhu_status(planet, d1p, pm):
    res = {"layer_a":"","layer_b":"","layer_c":"","status":"","note":"","karaka":""}
    res["karaka"] = TRIBANDHU_KARAKA.get(planet,"")
    adh = d1p.get(planet,{}).get("adhipatya_note","సముడు")
    la = "శుభ" if adh in ("శుభుడు","సముడు") else "అశుభ"
    res["layer_a"] = la
    st = d1p.get(planet,{}).get("strength","సాధారణం")
    if st in ("ఉచ్చం","స్వరాశి","మూల త్రికోణం"):
        bandhu="స్వబంధు"; lb="శుభ"
    else:
        pmd = pm.get(planet,{})
        mc = sum(1 for v in pmd.values() if isinstance(v,dict) and "Mitra" in v.get("panchadha",""))
        sc2 = sum(1 for v in pmd.values() if isinstance(v,dict) and "Shatru" in v.get("panchadha",""))
        if mc >= sc2: bandhu="మిత్రబంధు"; lb="శుభ"
        else: bandhu="శత్రుబంధు"; lb="అశుభ"
    res["layer_b"] = lb + " (" + bandhu + ")"
    ist = d1p.get(planet,{}).get("is_strong",False)
    aa = str(d1p.get(planet,{}).get("aarohi_avrohi",""))
    lc = "శుభ" if (ist and "Aarohi" in aa) else "అశుభ"
    res["layer_c"] = lc
    sh = [la,lb,lc].count("శుభ")
    if sh==3: res["status"]="PRAVAHA"; res["note"]="మూడు layers శుభం — అత్యంత శుభ ఫలితాలు"
    elif sh==2: res["status"]="MISRA"; res["note"]="రెండు layers శుభం — మిశ్రమ ఫలితాలు"
    elif sh==1: res["status"]="VIGHNA"; res["note"]="ఒక్క layer శుభం — తీవ్రమైన సవాళ్లు"
    else: res["status"]="YAMALA"; res["note"]="మూడు layers అశుభం — అత్యంత క్లిష్టమైన కాలం"
    return res

# STEP-3: భావ కారకులు — Yogas PDF pages 110-115
BHAVA_KARAKA = {
    1:"sun",2:"jupiter",3:"mars",4:"moon",5:"jupiter",6:"mars",
    7:"venus",8:"saturn",9:"sun",10:"mercury",11:"jupiter",12:"saturn"
}

# ═══════════════════════════════════════════════════════════
# ADD-3: పంచధా మైత్రి constants — Brihat Jataka Ch.2 Sl.18, BPHS
# నైసర్గిక + తాత్కాలిక కలిపి 5 స్థాయిల మైత్రి
# ═══════════════════════════════════════════════════════════
# తాత్కాలిక మైత్రి: 2,3,4,10,11,12 భావాల్లో ఉన్న గ్రహాలు మిత్రులు
# మిగిలిన స్థానాల్లో శత్రువులు — Brihat Jataka Ch.2 Sl.18
TATKALIKA_FRIEND_BHAVAS = {2,3,4,10,11,12}

# ADD-7: గ్రహ అవస్థ constants — BPHS Ch.45
# 0-6° = బాల, 6-12° = కుమార, 12-18° = యువ, 18-24° = వృద్ధ, 24-30° = మృత
AVASTHA_NAMES = {1:"బాల (బలహీనం)",2:"కుమార (మధ్యమం)",3:"యువ (బలిష్టం)",4:"వృద్ధ (క్షీణం)",5:"మృత (నిర్వీర్యం)"}
AVASTHA_PHALAM = {1:"అల్ప ఫలం","బాల":True, 2:"మధ్యమ ఫలం",3:"పూర్ణ ఫలం",4:"అర్ధ ఫలం",5:"శూన్య ఫలం"}

# ═══════════════════════════════════════════════════════════
# DB8 UTILITY FUNCTIONS — అన్నీ intact (ఏదీ మార్చలేదు)
# ═══════════════════════════════════════════════════════════
def norm(x): return x%360
def degrees_to_rashi(lon):
    lon=lon%360; r=int(lon//30)+1; d=lon%30; ni=int(lon/(360/27)); p=int((lon%(360/27))/(360/108))+1
    return r,round(d,4),ni,p
def bhava_of(pr,lr): return ((int(pr)-int(lr))%12)+1
def graha_strength(planet,rashi):
    if UCCHA_RASHI.get(planet)==rashi: return "ఉచ్చం"
    if NEECHA_RASHI.get(planet)==rashi: return "నీచం"
    if rashi in SWARASHI.get(planet,[]): return "స్వరాశి"
    if MOOL_TRIKONA.get(planet)==rashi: return "మూల త్రికోణం"
    return "సాధారణం"
def get_strength_percent(s): return STRENGTH_PERCENT.get(s,25)
def parse_time(t):
    t=t.strip().lower().replace(" ",""); pm="pm" in t; am="am" in t
    t=t.replace("am","").replace("pm","").replace(".",":").replace("-",":")
    p=t.split(":")
    h=int(p[0]) if p[0] else 0; m=int(p[1]) if len(p)>1 and p[1] else 0; s=int(p[2]) if len(p)>2 and p[2] else 0
    if pm and h!=12: h+=12
    if am and h==12: h=0
    return f"{h:02d}:{m:02d}:{s:02d}"
def get_location(city):
    try:
        import urllib.request,urllib.parse
        q=urllib.parse.quote(city.strip())
        req=urllib.request.Request(f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1",headers={"User-Agent":"DB9/1.0"})
        with urllib.request.urlopen(req,timeout=15) as r: data=json.loads(r.read().decode())
        if data:
            lat=round(float(data[0]["lat"]),4); lon=round(float(data[0]["lon"]),4)
            print(f"  ✅ {data[0].get('display_name','').split(',')[0]} → {lat},{lon}"); return lat,lon
        try:
            return get_location(input("  English city: ").strip())
        except EOFError:
            return None
    except: print("  Internet error. Hyderabad default."); return 17.385,78.4867
def get_lahiri(jd):
    if SWE_OK: swe.set_sid_mode(1,0,0); return swe.get_ayanamsa_ut(jd)
    return 22.46+((jd-2415020.0)/365.25)*(50.2564/3600)

def get_ayanamsha(jd, mode="lahiri"):
    """
    Ayanamsha selector — user choice at runtime
    lahiri      = standard (most common)
    pushyapaksha = Narasimha Rao preference (~Lahiri - 0.9814°)
    """
    lahiri = get_lahiri(jd)
    if mode == "pushyapaksha":
        return lahiri - 0.9814
    return lahiri  # default: lahiri

def select_ayanamsha():
    """User prompt to select ayanamsha"""
    print("\n" + "─"*42)
    print("అయనాంశం ఎంచుకోండి:")
    print("  1. Lahiri (default — most common)")
    print("  2. Pushyapaksha (Narasimha Rao preference)")
    print("─"*42)
    while True:
        c = input("మీ choice (1/2, default=1): ").strip()
        if c == "" or c == "1":
            print("  ✅ Lahiri అయనాంశం selected")
            return "lahiri"
        elif c == "2":
            print("  ✅ Pushyapaksha అయనాంశం selected (~Lahiri − 0.9814°)")
            return "pushyapaksha"
        else:
            print("  1 లేదా 2 enter చేయండి")

def get_positions(dob,tob,lat,lon,tz=5.5):
    d,m,y=map(int,dob.split("/")); h,mi,s=map(int,tob.split(":"))
    bd=datetime.datetime(y,m,d,h,mi,s); utc=bd-datetime.timedelta(hours=tz)
    ep=utc.strftime("%Y/%m/%d %H:%M:%S")
    obs=ephem.Observer(); obs.lat=str(lat); obs.lon=str(lon); obs.date=ep; obs.epoch=ep; obs.pressure=0
    bodies={"sun":ephem.Sun(),"moon":ephem.Moon(),"mercury":ephem.Mercury(),"venus":ephem.Venus(),"mars":ephem.Mars(),"jupiter":ephem.Jupiter(),"saturn":ephem.Saturn()}
    trop={}
    for k,b in bodies.items():
        b.compute(obs); ecl=ephem.Ecliptic(b,epoch=ep); trop[k]=math.degrees(ecl.lon)%360
    jd=ephem.julian_date(obs.date); T=(jd-2451545.0)/36525.0
    rahu=norm(125.04452-1934.136261*T+0.0020708*T**2+T**3/450000)
    trop["rahu"]=rahu; trop["ketu"]=norm(rahu+180)
    SP={"sun":0,"moon":1,"mercury":2,"venus":3,"mars":4,"jupiter":5,"saturn":6}
    spd={}; mlon={}; lat_p={}; tlon=dict(trop)
    if SWE_OK:
        for k,si in SP.items():
            xx,_=swe.calc_ut(jd,si,256); spd[k]=round(xx[3],6); lat_p[k]=round(xx[1],6); mlon[k]=round(xx[0],6)
        sx,_=swe.calc_ut(jd,0,256); mlon["sun_mean"]=round(sx[0],6)
        xr,_=swe.calc_ut(jd,10,256); spd["rahu"]=round(xr[3],6); spd["ketu"]=round(-xr[3],6); lat_p["rahu"]=round(xr[1],6); lat_p["ketu"]=round(-xr[1],6)
    else:
        spd={"sun":0.9856,"moon":13.1764,"mercury":1.3833,"venus":1.2,"mars":0.524,"jupiter":0.0831,"saturn":0.0335,"rahu":-0.053,"ketu":0.053}
        lat_p={k:0.0 for k in PLANET_TE}; mlon={k:trop.get(k,0) for k in PLANET_TE}; mlon["sun_mean"]=trop.get("sun",0)
    return trop,obs,jd,T,spd,mlon,lat_p,tlon

def calc_lagna(obs,lat,lon,ayan):
    jd=ephem.julian_date(obs.date)
    if SWE_OK:
        cusps,ascmc=swe.houses(jd,lat,lon,b'P'); at=ascmc[0]
    else:
        T=(jd-2451545.0)/36525.0; GMST=norm(280.46061837+360.98564736629*(jd-2451545.0)+0.000387933*T**2-T**3/38710000)
        LST=norm(GMST+lon); eps=23.439291-0.013004*T
        lr=math.radians(LST); er=math.radians(eps); latr=math.radians(lat)
        den=math.sin(er)*math.tan(latr)+math.cos(er)*math.sin(lr); raw=math.degrees(math.atan(-math.cos(lr)/den))
        at=((raw+180)%360) if math.cos(lr)<0 else (raw%360)
    return (at-ayan)%360

def calc_div_planet(sl,d): return int(((sl*d)%360)//30)+1
def calc_div_lagna(sl,d): return int((((sl*d)%360))//30)+1
def build_div_chart(sid,ls,div):
    dl=calc_div_lagna(ls,div); chart={"lagna_rashi":dl,"lagna_te":RASHI_TE.get(dl,"?")}; bh={i:[] for i in range(1,13)}
    for k in PLANET_TE:
        dr=calc_div_planet(sid[k],div); db=bhava_of(dr,dl)
        chart[k]={"name_te":PLANET_TE[k],"rashi_num":dr,"rashi_te":RASHI_TE.get(dr,"?"),"bhava":db,"strength":graha_strength(k,dr)}; bh[db].append(PLANET_TE[k])
    chart["bhava_chart"]=bh; return chart

# FIX-A: R4 check_lagna_bala_triple (Brihat Jataka Ch.1, Sl.19) — DB8 intact
def check_lagna_bala_triple(d1p,llk,asp):
    mal=["sun","mars","saturn","rahu","ketu"]
    ll_in=(d1p.get(llk,{}).get("bhava",0)==1)
    ll_asp=any(a.get("planet_en")==llk for a in asp.get(llk,{}).get("aspects_to",[]) if a.get("bhava")==1)
    ll=ll_in or ll_asp
    jg=(d1p.get("jupiter",{}).get("bhava",0)==1 or any(a.get("planet_en")=="jupiter" for a in asp.get(llk,{}).get("aspected_by",[])))
    mg=(d1p.get("mercury",{}).get("bhava",0)==1 or any(a.get("planet_en")=="mercury" for a in asp.get(llk,{}).get("aspected_by",[])))
    nm=not any(d1p.get(p,{}).get("bhava",0)==1 for p in mal)
    nma=not any(a.get("planet_en") in mal for a in asp.get(llk,{}).get("aspected_by",[]))
    return ll and jg and mg and nm and nma

def calc_ayurdaya_combust_loss(planet,is_c,spd=None):
    """R13: Ch.7 Sl.2 — Venus/Saturn exception"""
    if not is_c: return 0
    if planet in ["venus","saturn"]: return 0
    return 50

def calc_lagna_malefic_reduction(d1p,asp):
    """R14: Ch.7 Sl.4"""
    mal=["sun","mars","saturn","rahu","ketu"]; ben=["jupiter","venus","mercury","moon"]
    lm=any(d1p.get(p,{}).get("bhava",0)==1 for p in mal)
    bon=(any(d1p.get(p,{}).get("bhava",0)==1 for p in ben) or any(a.get("planet_en") in ben and a.get("aspect",0)==7 for a in asp.get("sun",{}).get("aspected_by",[])))
    return 50 if lm and bon else 0

def calc_satyacharya_multiplier(planet,strength,ir,iv,d1r,d9r,dc):
    """R15: Ch.7 Sl.11"""
    if strength=="ఉచ్చం" or ir: return 3
    if iv or d1r==d9r or strength=="స్వరాశి": return 2
    return 1

# FIX-C: R16 Aarohi/Avrohi actual arc (Ch.8 Sl.6) — DB8 intact
def calc_aarohi_avrohi(planet,strength,ir,pd,sid):
    if planet in ("rahu","ketu"): return "వర్తించదు"
    if strength=="ఉచ్చం": return "Aarohi (ఉచ్చ శిఖరం)"
    if strength=="నీచం": return "Avrohi (నీచ అడుగు)"
    ul=UCCHA_LON.get(planet,0); nl=(ul+180)%360; cl=sid.get(planet,0) if sid else 0
    aa=(cl>=nl and cl<ul) if nl<ul else (cl>=nl or cl<ul)
    return "Aarohi (ఉచ్చం వైపు — శుభ)" if aa else "Avrohi (నీచం వైపు — అశుభ)"

# FIX-D: R18 combustion exit timing (Ch.8 Sl.2) — DB8 intact
def get_combust_exit_timing(planet,bd,sid,spd):
    ORB={"moon":12.0,"mars":17.0,"mercury":14.0,"jupiter":11.0,"venus":10.0,"saturn":15.0}
    if planet in ("sun","rahu","ketu"): return 999999
    sl=sid.get("sun",0); pl=sid.get(planet,0); orb=ORB.get(planet,12.0)
    diff=abs(pl-sl)
    if diff>180: diff=360-diff
    if diff>orb: return 0
    sd=abs(spd.get(planet,1.0)-spd.get("sun",1.0))
    return (orb-diff)/sd if sd>0.1 else 30

def get_decanate_quality(lr,ld):
    """R20: Ch.8 Sl.8"""
    M={1,4,7,10}; F={2,5,8,11}; MU={3,6,9,12}; dc=int(ld/10)+1
    if lr in M: q="best" if dc==1 else "medium" if dc==2 else "low"
    elif lr in F: q="best" if dc==2 else "medium" if dc==1 else "low"
    elif lr in MU: q="best" if dc==3 else "medium" if dc==2 else "low"
    else: q="medium"
    return {"decanate":dc,"quality":q,"description":f"{dc}వ ద్రేష్కాణ — {q}"}

def calc_profession_lord(d1p,d10,sid,lr):
    """R25: Ch.10 Sl.1"""
    p10=[p for p,d in d1p.items() if d.get("bhava")==10 and p not in ["rahu","ketu"]]
    if p10: return {"source":"10th direct","planet":PLANET_TE[p10[0]],"planet_en":p10[0]}
    tr=((lr+8)%12)+1; tl=BHAVA_LORDS.get(tr,"sun")
    if tl in sid:
        d9r=int(((sid[tl]*9)%360)//30)+1; nl=BHAVA_LORDS.get(d9r,"sun")
        return {"source":"10th lord navamsha (R25)","planet":PLANET_TE[nl],"planet_en":nl,"tenth_lord":PLANET_TE[tl],"navamsha_rashi":RASHI_TE.get(d9r,"?")}
    return {"source":"unknown","planet":"?","planet_en":"?"}

def calc_conception_difficulty(d1p):
    """R10: Ch.4 Sl.22"""
    mal=["sun","mars","saturn","rahu","ketu"]
    mb=d1p.get("moon",{}).get("bhava",0); jb=d1p.get("jupiter",{}).get("bhava",0)
    if mb==1 and jb==1: return "EASY (చంద్ర+గురువు లగ్నంలో)"
    if any(d1p.get(p,{}).get("bhava",0)==8 for p in mal): return "DIFFICULT (8వ పాపం)"
    prev=((mb-2)%12)+1; nxt=(mb%12)+1
    if any(d1p.get(p,{}).get("bhava",0)==prev for p in mal) and any(d1p.get(p,{}).get("bhava",0)==nxt for p in mal): return "DIFFICULT (చంద్రుడు పాప మధ్యలో)"
    return "NORMAL"

# ═══════════════════════════════════════════════════════════
# DB8 DASHA FUNCTION — intact
# ═══════════════════════════════════════════════════════════
def compute_dasha(moon_sid,birth_dt,planets_data=None,sid=None,planet_speeds=None):
    ns=360/27; ni=int(moon_sid/ns); din=moon_sid%ns; nf=din/ns
    lord=DASHA_ORDER[ni%9]; ye=DASHA_YEARS[lord]*nf
    tl=[]; st=birth_dt-datetime.timedelta(days=ye*365.25); idx=DASHA_ORDER.index(lord)
    for i in range(9):
        p=DASHA_ORDER[(idx+i)%9]; en=st+datetime.timedelta(days=DASHA_YEARS[p]*365.25)
        tl.append({"planet":p,"start":st,"end":en,"years":DASHA_YEARS[p]}); st=en
    today=datetime.datetime.now(); ci=next((i for i,d in enumerate(tl) if d["start"]<=today<d["end"]),0); maha=tl[ci]
    rikta=False
    if planets_data:
        md=planets_data.get(maha["planet"],{})
        if md.get("strength") in ["నీచం","సాధారణం"] and not md.get("vargottama",False): rikta=True
    md_days=(maha["end"]-maha["start"]).days; ss=maha["start"]; mi=DASHA_ORDER.index(maha["planet"]); ants=[]
    for i in range(9):
        sp=DASHA_ORDER[(mi+i)%9]; sd=(DASHA_YEARS[sp]/120)*md_days; se=ss+datetime.timedelta(days=sd)
        ants.append({"planet":sp,"start":ss,"end":se}); ss=se
    antar=next((a for a in ants if a["start"]<=today<a["end"]),ants[0])
    mq="unknown"
    if planets_data:
        mb=planets_data.get("moon",{}).get("bhava",0); mdb=planets_data.get(maha["planet"],{}).get("bhava",0)
        db=((mb-mdb)%12)+1; mq="good (శుభ)" if db in [3,5,6,7,9,10,11] else "bad (అశుభ)" if db in [1,2,4,8] else "neutral"
    ps=antar["start"]; ai=DASHA_ORDER.index(antar["planet"]); pts=[]
    for i in range(9):
        sp=DASHA_ORDER[(ai+i)%9]; sd=(DASHA_YEARS[sp]/1200)*md_days; se=ps+datetime.timedelta(days=sd)
        pts.append({"planet":sp,"start":ps,"end":se}); ps=se
    prat=next((p for p in pts if p["start"]<=today<p["end"]),pts[0])
    future=[{"planet_te":PLANET_TE[tl[(ci+i)%9]["planet"]],"planet_en":tl[(ci+i)%9]["planet"],"start_date":tl[(ci+i)%9]["start"].strftime("%d/%m/%Y"),"end_date":tl[(ci+i)%9]["end"].strftime("%d/%m/%Y"),"duration_years":tl[(ci+i)%9]["years"]} for i in range(1,4)]
    ftl=[{"planet_te":PLANET_TE[d["planet"]],"planet_en":d["planet"],"start_date":d["start"].strftime("%d/%m/%Y"),"end_date":d["end"].strftime("%d/%m/%Y"),"years":d["years"]} for d in tl]
    fadm={}
    for t in tl:
        mp=t["planet"]; ms=t["start"]; me=t["end"]; mdd=(me-ms).days; mi2=DASHA_ORDER.index(mp); ss2=ms; a2=[]
        for i in range(9):
            sp2=DASHA_ORDER[(mi2+i)%9]; sd2=(DASHA_YEARS[sp2]/120)*mdd; se2=ss2+datetime.timedelta(days=sd2)
            ps2=ss2; ai2=DASHA_ORDER.index(sp2); pt2=[]
            for j in range(9):
                sp3=DASHA_ORDER[(ai2+j)%9]; sd3=(DASHA_YEARS[sp3]/1200)*mdd; se3=ps2+datetime.timedelta(days=sd3)
                pt2.append({"planet_te":PLANET_TE[sp3],"planet_en":sp3,"start_date":ps2.strftime("%d/%m/%Y"),"end_date":se3.strftime("%d/%m/%Y")}); ps2=se3
            a2.append({"planet_te":PLANET_TE[sp2],"planet_en":sp2,"start_date":ss2.strftime("%d/%m/%Y"),"end_date":se2.strftime("%d/%m/%Y"),"pratyantars":pt2}); ss2=se2
        fadm[mp]={"mahadasha_te":PLANET_TE[mp],"start_date":ms.strftime("%d/%m/%Y"),"end_date":me.strftime("%d/%m/%Y"),"antardashas":a2}
    return {
        "mahadasha":{"planet_te":PLANET_TE[maha["planet"]],"planet_en":maha["planet"],"start_date":maha["start"].strftime("%d/%m/%Y"),"end_date":maha["end"].strftime("%d/%m/%Y"),"years":maha["years"],"rikta_flag":rikta,"dasha_roga":DASHA_ROGA.get(maha["planet"],"")},
        "antardasha":{"planet_te":PLANET_TE[antar["planet"]],"planet_en":antar["planet"],"start_date":antar["start"].strftime("%d/%m/%Y"),"end_date":antar["end"].strftime("%d/%m/%Y"),"moon_position_quality":mq,"rikta_flag":False,"dasha_roga":DASHA_ROGA.get(antar["planet"],"")},
        "pratyantar":{"planet_te":PLANET_TE[prat["planet"]],"planet_en":prat["planet"],"start_date":prat["start"].strftime("%d/%m/%Y"),"end_date":prat["end"].strftime("%d/%m/%Y")},
        "future_dashas":future,"full_timeline":ftl,"full_antardasha_map":fadm
    }

# ═══════════════════════════════════════════════════════════
# DB8 PANCHANGA FUNCTION — intact
# ═══════════════════════════════════════════════════════════
def calc_panchanga(sid,bd,_ss=None):
    VA={0:"సోమ",1:"మంగళ",2:"బుధ",3:"గురు",4:"శుక్ర",5:"శని",6:"ఆది"}; VL={0:"moon",1:"mars",2:"mercury",3:"jupiter",4:"venus",5:"saturn",6:"sun"}
    ml=sid["moon"]; sl=sid["sun"]; td=(ml-sl)%360; tn=int(td/12)+1
    TN=["పాడ్యమి","విదియ","తదియ","చవితి","పంచమి","షష్ఠి","సప్తమి","అష్టమి","నవమి","దశమి","ఏకాదశి","ద్వాదశి","త్రయోదశి","చతుర్దశి","పౌర్ణమి / అమావాస్య"]
    is_s=td<180; mni=int(ml/(360/27))%27; mnp=int((ml%(360/27))/(360/108))+1
    yln=(sl+ml)%360; yn=int(yln/(360/27))+1
    YN=["విష్కంభ","ప్రీతి","ఆయుష్మాన్","సౌభాగ్య","శోభన","అతిగండ","సుకర్మ","ధృతి","శూల","గండ","వృద్ధి","ధ్రువ","వ్యాఘాత","హర్షణ","వజ్ర","సిద్ధి","వ్యతీపాత","వరీయాన్","పరిఘ","శివ","సిద్ధ","సాధ్య","శుభ","శుక్ల","బ్రహ్మ","ఇంద్ర","వైధృతి"]
    YQ={1:"అశుభం",2:"శుభం",3:"శుభం",4:"శుభం",5:"శుభం",6:"అశుభం",7:"శుభం",8:"శుభం",9:"అశుభం",10:"అశుభం",11:"శుభం",12:"శుభం",13:"అశుభం",14:"శుభం",15:"అశుభం",16:"శుభం",17:"అశుభం",18:"శుభం",19:"అశుభం",20:"శుభం",21:"శుభం",22:"శుభం",23:"శుభం",24:"శుభం",25:"శుభం",26:"శుభం",27:"అశుభం"}
    kn=int(td/6)%60+1; KN=["బవ","బాలవ","కౌలవ","తైతిల","గర","వణిజ","విష్టి","శకుని","చతుష్పాద","నాగ","కింస్తుఘ్న"]; ki=((kn-1)%7) if kn<=56 else (7+(kn-57))
    nf=(ml%(360/27))/(360/27)
    return {"vaara":VA.get(bd.weekday(),"?"),"vaara_lord_en":VL.get(bd.weekday(),"sun"),"tithi_num":tn,"tithi_name":TN[min((tn-1)%15,14)],"paksha":"శుక్ల పక్షం" if is_s else "కృష్ణ పక్షం","nakshatra":NAKSHATRA_TE[mni],"nakshatra_idx":mni,"nakshatra_pada":mnp,"yoga_num":yn,"yoga_name":YN[yn-1],"yoga_quality":YQ.get(yn,"సాధారణం"),"karana":KN[min(ki,len(KN)-1)],"varjyam_approximate":nf>0.85}

# ═══════════════════════════════════════════════════════════
# DB8 SPECIAL LAGNAS FUNCTION — intact (surya/chandra lagna)
# ADD-2 కొత్త విశేష లగ్నాలు దీని తర్వాత వేరే function లో add చేశాం
# ═══════════════════════════════════════════════════════════
def calc_special_lagnas(sid,ls,lr):
    cr=int(sid["moon"]//30)+1; sr=int(sid["sun"]//30)+1; bm={}
    for i in range(1,13): r=((lr+i-2)%12)+1; bm[i]={"rashi":r,"rashi_te":RASHI_TE.get(r,"?")}
    return {"chandra_lagna_rashi":cr,"chandra_lagna_te":RASHI_TE.get(cr,"?"),"surya_lagna_rashi":sr,"surya_lagna_te":RASHI_TE.get(sr,"?"),"bhava_rashi_map":bm}

# ═══════════════════════════════════════════════════════════
# DB8 GRAHA ASPECTS — intact
# ═══════════════════════════════════════════════════════════
def calc_graha_aspects(pd,lr):
    asp={p:{"aspects_to":[],"aspected_by":[]} for p in pd}
    # Raman Factor (b): bhava-level aspect tracking
    # ప్రతి bhava కి ఆ bhavanu చూసే గ్రహాల list — ఖాళీ bhava అయినా
    bhava_aspected_by={i:[] for i in range(1,13)}
    SP={"mars":[4,7,8],"jupiter":[5,7,9],"saturn":[3,7,10]}
    for p1k,p1 in pd.items():
        b1=p1["bhava"]; aa=[7]
        if p1k in SP: aa.extend(SP[p1k])
        for an in aa:
            tb=((b1+an-2)%12)+1
            if an==7: fr="పూర్తి (1/1)"
            elif an in [3,10]: fr="పూర్తి (1/1)" if p1k=="saturn" else "1/4"
            elif an in [5,9]:  fr="పూర్తి (1/1)" if p1k=="jupiter" else "1/2"
            elif an in [4,8]:  fr="పూర్తి (1/1)" if p1k=="mars" else "3/4"
            else: fr="పూర్తి (1/1)"
            # Bhava-level: ఖాళీ అయినా record చేయి
            bhava_aspected_by[tb].append({"planet_en":p1k,"planet_te":PLANET_TE.get(p1k,"?"),"aspect":an,"fraction":fr})
            # Planet-level: target bhava లో planet ఉంటేనే
            for p2k,p2 in pd.items():
                if p2k==p1k: continue
                if p2["bhava"]==tb:
                    asp[p1k]["aspects_to"].append({"planet":PLANET_TE[p2k],"planet_en":p2k,"bhava":tb,"aspect":an,"fraction":fr})
                    asp[p2k]["aspected_by"].append({"planet":PLANET_TE[p1k],"planet_en":p1k,"aspect":an,"fraction":fr})
    return asp, bhava_aspected_by

# ═══════════════════════════════════════════════════════════
# DB8 DISPOSITOR CHAIN — intact
# ═══════════════════════════════════════════════════════════
def calc_dispositor_chain(pd,lr):
    ch={}
    for pk in PLANET_TE:
        chain=[pk]; cur=pk; vis=set([pk]); lt="terminal"
        for _ in range(9):
            pr=pd[cur]["rashi_num"]; d=BHAVA_LORDS.get(pr,"sun")
            if d in vis: lt="cyclic" if d==pk else "convergent"; chain.append(d); break
            chain.append(d); vis.add(d); cur=d
        ch[pk]={"chain":[PLANET_TE[p] for p in chain],"chain_en":chain,"loop_type":lt,"length":len(chain)}
    ll=BHAVA_LORDS[lr]; mc=ch.get(ll,{})
    return {"all_chains":ch,"lagna_lord":PLANET_TE[ll],"master_chain":mc,"master_loop":mc.get("loop_type","terminal")}

# ═══════════════════════════════════════════════════════════
# DB8 ASHTAKAVARGA — intact (full bindus already calculated)
# ═══════════════════════════════════════════════════════════
def calc_ashtakavarga_approx(sid,lr):
    BH={"sun":{"sun":{1,2,4,7,8,9,10,11},"moon":{3,6,10,11},"mars":{1,2,4,7,8,9,10,11},"mercury":{3,5,6,9,10,11,12},"jupiter":{5,6,9,11},"venus":{6,7,12},"saturn":{1,2,4,7,8,9,10,11},"lagna":{3,4,6,10,11,12}},"moon":{"sun":{3,6,7,8,10,11},"moon":{1,3,6,7,10,11},"mars":{2,3,5,6,9,10,11},"mercury":{1,3,4,5,7,8,10,11},"jupiter":{1,4,7,8,10,11,12},"venus":{3,4,5,7,9,10,11},"saturn":{3,5,6,11},"lagna":{3,6,10,11}},"mars":{"sun":{3,5,6,10,11},"moon":{3,6,11},"mars":{1,2,4,7,8,10,11},"mercury":{3,5,6,11},"jupiter":{6,10,11,12},"venus":{6,8,11,12},"saturn":{1,4,7,8,9,10,11},"lagna":{1,4,7,8,9,10,11}},"mercury":{"sun":{5,6,9,11,12},"moon":{2,4,6,8,10,11},"mars":{1,2,4,7,8,9,10,11},"mercury":{1,3,5,6,9,10,11,12},"jupiter":{6,8,11,12},"venus":{1,2,3,4,5,8,9,11},"saturn":{1,2,4,7,8,9,10,11},"lagna":{1,2,4,6,8,10,11}},"jupiter":{"sun":{1,2,3,4,7,8,9,10,11},"moon":{2,5,7,9,11},"mars":{1,2,4,7,8,10,11},"mercury":{1,2,4,5,6,9,10,11},"jupiter":{1,2,3,4,7,8,10,11},"venus":{2,5,6,9,10,11},"saturn":{3,5,6,12},"lagna":{1,2,4,5,6,7,9,10,11}},"venus":{"sun":{8,11,12},"moon":{1,2,3,4,5,8,9,11,12},"mars":{3,4,6,9,11,12},"mercury":{3,5,6,9,11},"jupiter":{5,8,9,10,11},"venus":{1,2,3,4,5,8,9,10,11},"saturn":{3,4,5,8,9,10,11},"lagna":{1,2,3,4,5,8,9,11}},"saturn":{"sun":{1,2,4,7,8,10,11},"moon":{3,6,11},"mars":{3,5,6,10,11,12},"mercury":{6,8,9,10,11,12},"jupiter":{5,6,11,12},"venus":{6,11,12},"saturn":{3,5,6,11},"lagna":{1,3,4,6,10,11}}}
    CO={k:["sun","moon","mars","mercury","jupiter","venus","saturn","lagna"] for k in ["sun","moon","mars","mercury","jupiter","venus","saturn"]}
    pos={k:int(sid[k]//30)+1 for k in ["sun","moon","mars","mercury","jupiter","venus","saturn"]}; pos["lagna"]=lr
    pb={}; sarva=[0]*12
    for target in ["sun","moon","mars","mercury","jupiter","venus","saturn"]:
        hb=[0]*12; ct=BH.get(target,{})
        for contrib in CO[target]:
            bs=ct.get(contrib,set()); cp=pos[contrib]
            for hi in range(12):
                hn=hi+1; dist=((hn-cp)%12); dist=12 if dist==0 else dist
                if dist in bs: hb[hi]+=1
        total=sum(hb); pr=pos[target]; pbi=hb[pr-1]
        for i in range(12): sarva[i]+=hb[i]
        bc=pbi; rp="100% (పూర్తి)" if bc>=8 else "75%" if bc>=6 else "50% (సగం)" if bc>=4 else "25% (పాదం)" if bc>=2 else "0%"
        pb[target]={"rashi":pr,"rashi_te":RASHI_TE.get(pr,"?"),"bindus_in_rashi":pbi,"total_bindus":total,"house_bindus":hb,"result_proportion":rp,"bindu_phala":ASHTAKA_PHALA.get(pbi,"మహారోగము")}
    pb["sarvashtakavarga"]={"house_totals":sarva,"total":sum(sarva)}; return pb

# ═══════════════════════════════════════════════════════════
# DB8 GRAHA YUDDHA — STEP-5 patch: కుజుడు always wins
# Source: Jataka Martanda 81-82 PDF
# "అంగారకునితో బుధ, గురు, శుక్ర, శనులు కలిసిన యెడల పరాజితులగుదురు. కుజుడు విజేత."
# "బుధునకు అస్తంగత్వ దోషముండదు" — Mercury combust note added
# ═══════════════════════════════════════════════════════════
def calc_graha_yuddha(sid,pd,lat_p=None):
    YP=["mars","mercury","jupiter","venus","saturn"]; pairs=[]; ck=set()
    for i,p1 in enumerate(YP):
        for p2 in YP[i+1:]:
            pk=f"{p1}_{p2}"
            if pk in ck: continue
            ck.add(pk); l1=sid.get(p1,0); l2=sid.get(p2,0); diff=abs(l1-l2)
            if diff>180: diff=360-diff
            if diff>1.0: continue
            # STEP-5: కుజుడు vs ఇతర గ్రహాలు — Mars always wins (Jataka Martanda 81-82)
            if p1=="mars" and p2 in MARS_ALWAYS_WINS_OVER:
                w,lo=p1,p2; mars_rule=True
            elif p2=="mars" and p1 in MARS_ALWAYS_WINS_OVER:
                w,lo=p2,p1; mars_rule=True
            else:
                mars_rule=False
                if lat_p: la1=lat_p.get(p1,0.0); la2=lat_p.get(p2,0.0)
                else: la1=-(l1%30); la2=-(l2%30)
                if la1>la2: w,lo=p1,p2
                elif la2>la1: w,lo=p2,p1
                else: w,lo=(p1,p2) if NAISARGIKA_ORDER.get(p1,9)<NAISARGIKA_ORDER.get(p2,9) else (p2,p1)
            pairs.append({"planet1_en":p1,"planet1_te":PLANET_TE[p1],"planet2_en":p2,"planet2_te":PLANET_TE[p2],"lon_diff_deg":round(diff,4),"winner_en":w,"winner_te":PLANET_TE[w],"loser_en":lo,"loser_te":PLANET_TE[lo],"mars_rule_applied":mars_rule})
    return {"yuddha_present":len(pairs)>0,"pairs":pairs,"defeated_planets":[p["loser_en"] for p in pairs],"winning_planets":[p["winner_en"] for p in pairs],"note":"బుధునకు అస్తంగత్వ దోషముండదు (Jataka Martanda)"}

# ═══════════════════════════════════════════════════════════
# DB8 VARGOTTAMA — intact
# ═══════════════════════════════════════════════════════════
def calc_vargottama(sid):
    vg={}
    for k in PLANET_TE:
        d1r=int(sid[k]//30)+1; d9r=int(((sid[k]*9)%360)//30)+1
        vg[k]={"is_vargottama":d1r==d9r,"d1_rashi_te":RASHI_TE.get(d1r,"?"),"d9_rashi_te":RASHI_TE.get(d9r,"?")}
    return vg

# ═══════════════════════════════════════════════════════════
# PARIVARTANA (Mutual Reception) detection
# Source: B.V. Raman "How to Judge a Horoscope Vol 2"
# రెండు గ్రహాలు ఒకదాని రాశిలో మరొకటి ఉండటం
# శుభ parivartana: రెండూ శుభ స్థానాల్లో → "mutually benefiting each other"
# అశుభ parivartana: dusthana lords మధ్య → weakens both bhavas
# ═══════════════════════════════════════════════════════════
def calc_parivartana(d1p, lr):
    """
    Parivartana = Planet A in rashi of Planet B AND Planet B in rashi of Planet A
    Source: B.V. Raman "How to Judge a Horoscope Vol 2" — extensively used
    Returns: list of parivartana pairs with quality assessment
    """
    planets = ["sun","moon","mars","mercury","jupiter","venus","saturn"]
    DUSTHANA = {6, 8, 12}
    pairs = []
    checked = set()

    for p1 in planets:
        for p2 in planets:
            if p1 == p2: continue
            key = tuple(sorted([p1, p2]))
            if key in checked: continue
            checked.add(key)

            r1 = d1p[p1].get("rashi_num", 0)  # p1 ఉన్న రాశి
            r2 = d1p[p2].get("rashi_num", 0)  # p2 ఉన్న రాశి

            # p1 యొక్క swarashi లో p2 ఉందా?
            p1_owns = SWARASHI.get(p1, [])
            p2_owns = SWARASHI.get(p2, [])

            if r1 in p2_owns and r2 in p1_owns:
                # Parivartana confirmed
                b1 = d1p[p1].get("bhava", 0)
                b2 = d1p[p2].get("bhava", 0)

                # Quality assessment
                both_dusthana = (b1 in DUSTHANA) and (b2 in DUSTHANA)
                one_dusthana  = (b1 in DUSTHANA) or  (b2 in DUSTHANA)
                both_shubha   = (b1 not in DUSTHANA) and (b2 not in DUSTHANA)

                if both_shubha:
                    quality = "శుభ"
                    note = "రెండూ శుభ స్థానాల్లో — పరస్పర బలవర్ధనం"
                elif both_dusthana:
                    quality = "విపరీత"
                    note = "రెండూ దుష్టస్థానాల్లో — Viparita Parivartana"
                else:
                    quality = "మిశ్రమ"
                    note = "ఒకటి శుభ, ఒకటి దుష్ట — మిశ్రమ ఫలితాలు"

                pairs.append({
                    "planet1_en": p1,
                    "planet1_te": PLANET_TE.get(p1, "?"),
                    "planet1_bhava": b1,
                    "planet1_rashi_te": RASHI_TE.get(r1, "?"),
                    "planet2_en": p2,
                    "planet2_te": PLANET_TE.get(p2, "?"),
                    "planet2_bhava": b2,
                    "planet2_rashi_te": RASHI_TE.get(r2, "?"),
                    "quality": quality,
                    "note": note,
                    "source": "B.V. Raman How to Judge a Horoscope Vol 2"
                })

    return {
        "present": len(pairs) > 0,
        "pairs": pairs,
        "count": len(pairs),
        "shubha_count":  sum(1 for p in pairs if p["quality"] == "శుభ"),
        "misra_count":   sum(1 for p in pairs if p["quality"] == "మిశ్రమ"),
        "viparita_count":sum(1 for p in pairs if p["quality"] == "విపరీత"),
    }

# ═══════════════════════════════════════════════════════════
# PAPAKARTARI YOGA detection
# Source: B.V. Raman "How to Judge a Horoscope Vol 2"
# భావం/గ్రహం రెండు వైపులా malefics = Papakartari
# "hemmed in between malefics" — bhava ఫలాలు బలహీనపడతాయి
# ═══════════════════════════════════════════════════════════
def calc_papakartari(d1p):
    """
    Papakartari = Planet/Bhava కి ముందు + వెనక bhavas రెండింటిలో malefics ఉంటే
    Source: B.V. Raman "How to Judge a Horoscope Vol 2" — extensively used
    """
    MALEFICS = {"sun","mars","saturn","rahu","ketu"}

    # Planet-level papakartari
    planet_pk = {}
    for pk, pd in d1p.items():
        pb = pd.get("bhava", 0)
        if pb == 0: continue
        prev_b = ((pb - 2) % 12) + 1
        next_b = (pb % 12) + 1
        prev_mal = [p for p,d in d1p.items() if d.get("bhava")==prev_b and p in MALEFICS]
        next_mal = [p for p,d in d1p.items() if d.get("bhava")==next_b and p in MALEFICS]
        present = bool(prev_mal and next_mal)
        planet_pk[pk] = {
            "planet_te": PLANET_TE.get(pk,"?"),
            "bhava": pb,
            "prev_bhava": prev_b,
            "next_bhava": next_b,
            "prev_malefics": [PLANET_TE.get(p,"?") for p in prev_mal],
            "next_malefics": [PLANET_TE.get(p,"?") for p in next_mal],
            "papakartari": present,
            "note": "రెండు వైపులా పాప గ్రహాలు — ఫలాలు బలహీనపడతాయి" if present else ""
        }

    # Bhava-level papakartari
    bhava_pk = {}
    for bh in range(1, 13):
        prev_b = ((bh - 2) % 12) + 1
        next_b = (bh % 12) + 1
        prev_mal = [p for p,d in d1p.items() if d.get("bhava")==prev_b and p in MALEFICS]
        next_mal = [p for p,d in d1p.items() if d.get("bhava")==next_b and p in MALEFICS]
        present = bool(prev_mal and next_mal)
        bhava_pk[bh] = {
            "prev_malefics": [PLANET_TE.get(p,"?") for p in prev_mal],
            "next_malefics": [PLANET_TE.get(p,"?") for p in next_mal],
            "papakartari": present,
            "note": f"{bh}వ భావం రెండు వైపులా పాప గ్రహాలు — bhava ఫలాలు బలహీనం" if present else ""
        }

    affected_planets = [pk for pk,v in planet_pk.items() if v["papakartari"]]
    affected_bhavas  = [bh for bh,v in bhava_pk.items()  if v["papakartari"]]

    return {
        "planet_papakartari": planet_pk,
        "bhava_papakartari":  bhava_pk,
        "affected_planets_te": [PLANET_TE.get(p,"?") for p in affected_planets],
        "affected_bhavas": affected_bhavas,
        "source": "B.V. Raman How to Judge a Horoscope Vol 2"
    }

# ═══════════════════════════════════════════════════════════
# RAHU/KETU SIGN DISPOSITOR
# Source: B.V. Raman "How to Judge a Horoscope Vol 2"
# "Ketu should give the results of sign dispositor Saturn"
# "Rahu gives results similar to the Sun, his sign-dispositor"
# ═══════════════════════════════════════════════════════════
def calc_rahu_ketu_dispositor(d1p):
    """
    రాహు/కేతు తమ sign lord (dispositor) ఫలాలు reflect చేస్తాయి
    Source: B.V. Raman Vol 2 — dasha timing లో వాడాలి
    """
    result = {}
    for node in ("rahu", "ketu"):
        rashi = d1p.get(node, {}).get("rashi_num", 0)
        disp = BHAVA_LORDS.get(rashi)
        if not disp:
            result[node] = {"dispositor_en": None, "dispositor_te": None}
            continue
        disp_data = d1p.get(disp, {})
        result[node] = {
            "node_te": PLANET_TE.get(node, "?"),
            "rashi_te": RASHI_TE.get(rashi, "?"),
            "dispositor_en": disp,
            "dispositor_te": PLANET_TE.get(disp, "?"),
            "dispositor_bhava": disp_data.get("bhava", 0),
            "dispositor_strength": disp_data.get("strength", "సాధారణం"),
            "dispositor_is_strong": disp_data.get("is_strong", False),
            "note": f"{PLANET_TE.get(node,'?')} దశలో {PLANET_TE.get(disp,'?')} (sign dispositor) ఫలాలు reflect అవుతాయి",
            "source": "B.V. Raman How to Judge a Horoscope Vol 2"
        }
    return result

# ═══════════════════════════════════════════════════════════
# NEECHABHANGA DETECTION
# Source: B.V. Raman Vol 2 + BPHS (V27 PART-2 existing conditions)
# Condition-A: నీచ గ్రహం sign lord (dispositor) kendra లో ఉంటే
# Condition-B: నీచ గ్రహం exaltation lord kendra లో ఉంటే
# Condition-C: నీచ lord లేదా exaltation lord kendra లో (lagna/chandra నుండి)
# ═══════════════════════════════════════════════════════════
def calc_neechabhanga(d1p, lr):
    """
    నీచ గ్రహాలకు Neechabhanga conditions detect చేయడం
    Source: B.V. Raman Vol 2 + BPHS
    """
    KENDRA = {1, 4, 7, 10}
    moon_bhava = d1p.get("moon", {}).get("bhava", 1)
    moon_kendras = {moon_bhava, ((moon_bhava+2)%12)+1, ((moon_bhava+5)%12)+1, ((moon_bhava+8)%12)+1}

    result = {}
    for planet, neecha_rashi in NEECHA_RASHI.items():
        if planet not in d1p: continue
        p_rashi = d1p[planet].get("rashi_num", 0)
        if p_rashi != neecha_rashi:
            result[planet] = {"is_neecha": False, "neechabhanga": False}
            continue

        conditions_met = []

        # Condition-A: sign dispositor (neecha rashi lord) kendra లో
        sign_lord = BHAVA_LORDS.get(neecha_rashi)
        if sign_lord and sign_lord in d1p:
            sl_bhava = d1p[sign_lord].get("bhava", 0)
            if sl_bhava in KENDRA:
                conditions_met.append(f"A: sign dispositor {PLANET_TE.get(sign_lord,'?')} కేంద్రంలో ({sl_bhava}వ)")
            if sl_bhava in moon_kendras:
                conditions_met.append(f"A2: sign dispositor {PLANET_TE.get(sign_lord,'?')} చంద్ర కేంద్రంలో")

        # Condition-B: exaltation lord kendra లో
        uccha_rashi = UCCHA_RASHI.get(planet)
        if uccha_rashi:
            uccha_lord = BHAVA_LORDS.get(uccha_rashi)
            if uccha_lord and uccha_lord in d1p:
                ul_bhava = d1p[uccha_lord].get("bhava", 0)
                if ul_bhava in KENDRA:
                    conditions_met.append(f"B: exaltation lord {PLANET_TE.get(uccha_lord,'?')} కేంద్రంలో ({ul_bhava}వ)")

        # Condition-C: neecha planet itself exaltation sign lord tho conjunction
        if uccha_rashi:
            uccha_lord = BHAVA_LORDS.get(uccha_rashi)
            p_bhava = d1p[planet].get("bhava", 0)
            if uccha_lord and uccha_lord in d1p:
                if d1p[uccha_lord].get("bhava") == p_bhava:
                    conditions_met.append(f"C: ఉచ్చ lord {PLANET_TE.get(uccha_lord,'?')} తో సంయోగం")

        nb = len(conditions_met) > 0
        result[planet] = {
            "planet_te": PLANET_TE.get(planet, "?"),
            "is_neecha": True,
            "neecha_rashi_te": RASHI_TE.get(neecha_rashi, "?"),
            "neechabhanga": nb,
            "conditions_met": conditions_met,
            "note": "నీచభంగ రాజయోగం — నీచ ఫలాలు రద్దు, రాజయోగ ఫలాలు" if nb else "నీచం — బలహీనం",
            "source": "B.V. Raman Vol 2 + BPHS"
        }
    return result

# ═══════════════════════════════════════════════════════════
# MULTI-FACTOR DOMAIN ANALYSIS
# Source: Saravali Ch.8,34 (కళ్యాణ వర్మ) + Phaladeepika Ch.10,12,13 (మంత్రేశ్వరుడు)
# ఒక్క factor చూసి wrong conclusion రాకుండా multi-factor fields
# AI తప్పు conclusion చేయకుండా protection
# ═══════════════════════════════════════════════════════════
def calc_domain_analysis(d1p, lr, asp, dc_data, shad):
    """
    10 domains కి multi-factor analysis fields
    Source: Saravali Ch.8,34 + Phaladeepika Ch.10,12,13,15,16
    """
    KENDRA   = {1,4,7,10}
    TRIKONA  = {1,5,9}
    DUSTHANA = {6,8,12}
    SHUBHA   = {1,4,5,7,9,10}
    BENEFICS = ["jupiter","venus","mercury","moon"]
    MALEFICS = ["sun","mars","saturn","rahu","ketu"]
    ODD_RASHI  = {1,3,5,7,9,11}
    EVEN_RASHI = {2,4,6,8,10,12}

    def bhava_from_lr(n):
        return ((lr-1+n-1)%12)+1

    def is_shubha_bhava(b): return b in SHUBHA
    def is_dusthana(b): return b in DUSTHANA

    def bhava_has_benefic(bh):
        return any(d1p.get(p,{}).get("bhava")==bh for p in BENEFICS)
    def bhava_has_malefic(bh):
        return any(d1p.get(p,{}).get("bhava")==bh for p in MALEFICS if p not in ["rahu","ketu"])
    def bhava_aspected_by_benefic(bh, asp):
        return any(a.get("planet_en") in BENEFICS
                   for p in BENEFICS
                   for a in asp.get(p,{}).get("aspects_to",[])
                   if a.get("bhava")==bh)
    def planet_strong(p):
        return shad.get(p,{}).get("is_strong", False) or \
               d1p.get(p,{}).get("strength","") in ["ఉచ్చం","స్వరాశి","మూల త్రికోణం"]

    def overall_yoga(factors_positive, factors_total):
        ratio = factors_positive/factors_total if factors_total else 0
        if ratio >= 0.75: return "STRONG"
        if ratio >= 0.50: return "MODERATE"
        if ratio >= 0.25: return "WEAK"
        return "DELAY"

    result = {}

    # ══════════════════════════════════════════════
    # 1. సంతానం — Saravali Ch.34 St.25-27 + Phaladeepika Ch.12 St.1
    # ══════════════════════════════════════════════
    b5 = bhava_from_lr(5)
    lord5 = BHAVA_LORDS.get(b5)
    l5_bhava = d1p.get(lord5,{}).get("bhava",0)
    l5_rashi = d1p.get(lord5,{}).get("rashi_num",0)
    jup_b = d1p.get("jupiter",{}).get("bhava",0)
    jup_r = d1p.get("jupiter",{}).get("rashi_num",0)

    # D9 5th bhava
    d9_data = dc_data.get("D9",{}).get("planets",{})
    d9_5th_rashi = bhava_from_lr(5)
    d9_5th_planets = [p for p,v in d9_data.items() if v.get("bhava")==d9_5th_rashi] if d9_data else []

    # D7 5th bhava
    d7_data = dc_data.get("D7",{}).get("planets",{})
    d7_5th_planets = [p for p,v in d7_data.items() if v.get("bhava")==d9_5th_rashi] if d7_data else []

    # f1: Saravali Ch.34 St.25 — "If the 5th House contains a benefic,
    #     the native will surely beget children."
    f1 = bhava_has_benefic(b5)

    # f2: Saravali Ch.34 St.25 — "or is aspected by a benefic,
    #     the native will surely beget children."
    f2 = bhava_aspected_by_benefic(b5, asp)

    # f3: BPHS Ch.15 — 5th lord strong/well-placed = strong santana yoga
    #     "The lord of the 5th in own/exaltation/moolatrikona = progeny blessed"
    f3 = planet_strong(lord5) if lord5 else False

    # f4: Phaladeepika Ch.12 St.1 — "If Jupiter and lords of the 5th with
    #     reference to the Lagna and the Moon be well placed..."
    #     Jupiter well placed = shubha bhava లో
    f4 = jup_b in SHUBHA

    # f5: Saravali Ch.34 St.27 — "If the Navansa of the 5th falls in a benefics
    #     Rasi the number of children equals the number of Navansas past"
    #     D9 5th bhava లో strong planet = partial classical support
    f5 = any(planet_strong(p) for p in d9_5th_planets) if d9_5th_planets else False

    sant_positive = sum([f1,f2,f3,f4,f5])

    # Son/Daughter — Saravali Ch.8 St.14-17 (కళ్యాణ వర్మ)
    # FIX-30: St.14 individual scoring — ప్రతి గ్రహానికి వేర్వేరుగా score
    # St.14: Lagna+Moon+Jupiter+Sun — ప్రతి గ్రహం odd=male+1, even=female+1
    # St.15a: Jupiter+Sun రెండూ odd → male+1
    # St.15b: Venus+Moon+Mars అన్నీ even → female+1
    # St.17: TIEBREAKER ONLY — Tie వచ్చినప్పుడు మాత్రమే
    #         Saturn odd house (lagna కాదు) → male+1, even house → female+1
    moon_r = d1p.get("moon",{}).get("rashi_num",0)
    sun_r  = d1p.get("sun",{}).get("rashi_num",0)
    ven_r  = d1p.get("venus",{}).get("rashi_num",0)
    mars_r = d1p.get("mars",{}).get("rashi_num",0)
    sat_b  = d1p.get("saturn",{}).get("bhava",0)

    # St.14 FIX-30: ప్రతి గ్రహానికి individual score
    # odd rashi → male+1 | even rashi → female+1
    st14_male_count   = sum(1 for r in [lr, moon_r, jup_r, sun_r] if r in ODD_RASHI)
    st14_female_count = sum(1 for r in [lr, moon_r, jup_r, sun_r] if r in EVEN_RASHI)

    # St.15a male: Jupiter+Sun రెండూ odd rashi → male+1
    st15a_male = (jup_r in ODD_RASHI and sun_r in ODD_RASHI)

    # St.15b female: Venus+Moon+Mars అన్నీ even rashi → female+1
    st15b_female = all(r in EVEN_RASHI for r in [ven_r, moon_r, mars_r])

    # Total before tiebreaker
    male_count   = st14_male_count   + (1 if st15a_male   else 0)
    female_count = st14_female_count + (1 if st15b_female else 0)

    # St.17 TIEBREAKER ONLY — Tie వచ్చినప్పుడు మాత్రమే apply చేయి
    st17_applied = False
    if male_count == female_count:
        if sat_b in {3,5,7,9,11}:          # odd house → male
            male_count  += 1
            st17_applied = True
        elif sat_b in {2,4,6,8,10,12}:     # even house → female
            female_count += 1
            st17_applied  = True

    # Result
    gender_rules = []
    if male_count > female_count:
        child_gender = "పుత్రుడు సంభావ్యత"
        if st14_male_count > st14_female_count:
            gender_rules.append("St.14_male_score")
        if st15a_male:
            gender_rules.append("St.15a")
        if st17_applied and sat_b in {3,5,7,9,11}:
            gender_rules.append("St.17_tiebreaker")
    elif female_count > male_count:
        child_gender = "పుత్రిక సంభావ్యత"
        if st14_female_count > st14_male_count:
            gender_rules.append("St.14_female_score")
        if st15b_female:
            gender_rules.append("St.15b")
        if st17_applied and sat_b in {2,4,6,8,10,12}:
            gender_rules.append("St.17_tiebreaker")
    else:
        child_gender = "నిర్ణయించలేదు"
        gender_rules = []

    # Build classical_rule text based on active rules
    CT_SANTANA = {
        "St.14_male_score":   "Saravali Ch.8 St.14 (FIX-30): Lagna+Moon+Jupiter+Sun — odd rashi majority → పుత్రుడు",
        "St.14_female_score": "Saravali Ch.8 St.14 (FIX-30): Lagna+Moon+Jupiter+Sun — even rashi majority → పుత్రిక",
        "St.15a":             "Saravali Ch.8 St.15a: Jupiter+Sun odd rashi లో → పుత్రుడు",
        "St.15b":             "Saravali Ch.8 St.15b: Venus+Moon+Mars అన్నీ even rashi → పుత్రిక",
        "St.17_tiebreaker":   "Saravali Ch.8 St.17 (tiebreaker): Saturn odd/even house → లింగ నిర్ధారణ",
    }
    classical_rule_santana = " | ".join([CT_SANTANA[r] for r in gender_rules if r in CT_SANTANA])

    result["santana"] = {
        "d1_5th_bhava": b5,
        "d1_5th_has_benefic": f1,
        "d1_5th_aspected_by_benefic": f2,
        "d1_5th_lord_strong": f3,
        "guru_in_shubha_bhava": f4,
        "d9_5th_strong_planet": f5,
        "d7_5th_planets": [PLANET_TE.get(p,"?") for p in d7_5th_planets],
        "positive_factors": sant_positive,
        "total_factors": 5,
        "overall_yoga": overall_yoga(sant_positive, 5),
        "child_gender_indicator": child_gender,
        "child_gender_male_count": male_count,
        "child_gender_female_count": female_count,
        "child_gender_rules_applied": gender_rules,
        "classical_rule": classical_rule_santana if classical_rule_santana else "Saravali Ch.8 St.14-17 (కళ్యాణ వర్మ)",
        "source": "Saravali Ch.8 St.14-17 + Ch.34 St.25-27 + Phaladeepika Ch.12 St.1"
    }

    # ══════════════════════════════════════════════
    # 2. వివాహం — Saravali Ch.34 St.45-47 + Phaladeepika Ch.10 St.1
    # ══════════════════════════════════════════════
    b7 = bhava_from_lr(7)
    lord7 = BHAVA_LORDS.get(b7)
    l7_bhava = d1p.get(lord7,{}).get("bhava",0)
    ven_b = d1p.get("venus",{}).get("bhava",0)
    moon_b = d1p.get("moon",{}).get("bhava",0)

    # g1: Saravali Ch.34 St.45 — "If the 7th house has benefics the native
    #     has a faithful and beautiful wife"
    g1 = bhava_has_benefic(b7)

    # g2: Saravali Ch.34 St.45 — "or is aspected by benefics — good marriage"
    g2 = bhava_aspected_by_benefic(b7, asp)

    # g3: Phaladeepika Ch.10 St.1 — "The lord of the 7th house well placed
    #     = marriage yoga strong"
    g3 = planet_strong(lord7) if lord7 else False

    # g4: Phaladeepika Ch.10 — "Find out who amongst Venus and Moon is stronger —
    #     marriage in that dasha." Venus = vivaha karaka.
    #     Venus NOT in dusthana (6/8/12) = karaka not afflicted = vivaha yoga intact
    #     Saravali Ch.34 St.45: "Venus in good position = beautiful spouse"
    g4 = ven_b not in DUSTHANA

    # g5: BPHS Ch.7 — "7th lord in dusthana = marital difficulties"
    #     Contrapositive: 7th lord NOT in dusthana = normal marriage
    g5 = not (l7_bhava in DUSTHANA)

    viv_positive = sum([g1,g2,g3,g4,g5])

    # vivaha classical rules based on active factors
    viv_rules = []
    if g1: viv_rules.append("Saravali Ch.34 St.45: 7వ bhava లో శుభ గ్రహం → మంచి వివాహం")
    if g2: viv_rules.append("Saravali Ch.34 St.45: 7వ bhava శుభ దృష్టి → వివాహ యోగం")
    if g3: viv_rules.append("Phaladeepika Ch.10 St.1: 7వ lord బలిష్టం → వివాహ యోగం")
    if g4: viv_rules.append("Phaladeepika Ch.10: శుక్రుడు (వివాహ కారకుడు) దుష్థానంలో లేడు")
    if g5: viv_rules.append("BPHS Ch.7: 7వ lord దుష్థానంలో లేడు → వివాహ యోగం intact")

    result["vivaha"] = {
        "d1_7th_bhava": b7,
        "d1_7th_has_benefic": g1,
        "d1_7th_aspected_by_benefic": g2,
        "d1_7th_lord_strong": g3,
        "shukra_not_dusthana": g4,
        "7th_lord_not_dusthana": g5,
        "positive_factors": viv_positive,
        "total_factors": 5,
        "overall_yoga": overall_yoga(viv_positive, 5),
        "classical_rule": " | ".join(viv_rules) if viv_rules else "Saravali Ch.34 St.45-47",
        "source": "Saravali Ch.34 St.45-47 + Phaladeepika Ch.10 St.1"
    }

    # ══════════════════════════════════════════════
    # 3. వృత్తి — Saravali Ch.7 + Ch.30 St.11 + Phaladeepika Ch.5
    # ══════════════════════════════════════════════
    b10 = bhava_from_lr(10)
    lord10 = BHAVA_LORDS.get(b10)
    l10_bhava = d1p.get(lord10,{}).get("bhava",0)

    # h1: Saravali Ch.34 — "Malefics in bhavas destroy the significations of
    #     those bhavas." Contrapositive: 10th malefic-free = vritti intact
    h1 = bhava_has_benefic(b10) or not bhava_has_malefic(b10)

    # h2: Phaladeepika Ch.5 — "10th lord strong = vritti/karma bhava strong"
    h2 = planet_strong(lord10) if lord10 else False

    # h3: BPHS Ch.15 — "Lord of 10th in shubha bhava = karma phala good"
    h3 = l10_bhava in SHUBHA

    # h4: Saravali Ch.30 St.11 — "Sun in 10th = succeed in undertakings, great"
    #     Saravali Ch.30 St.1 — "Sun in 1st = intelligent, healthy"
    #     Saravali Ch.30 St.9 — "Sun in 9th = fortunate, righteous"
    sun_b = d1p.get("sun",{}).get("bhava",0)
    h4 = sun_b in {1,9,10}

    vru_positive = sum([h1,h2,h3,h4])

    result["vritti"] = {
        "d1_10th_bhava": b10,
        "d1_10th_shubha": h1,
        "10th_lord_strong": h2,
        "10th_lord_in_shubha": h3,
        "sun_in_shubha": h4,
        "positive_factors": vru_positive,
        "total_factors": 4,
        "overall_yoga": overall_yoga(vru_positive, 4),
        "source": "Saravali Ch.7 + Phaladeepika Ch.5"
    }

    # ══════════════════════════════════════════════
    # 4. ఆర్థికం — Saravali Ch.34 St.15-20, St.58-67
    # ══════════════════════════════════════════════
    b2 = bhava_from_lr(2)
    b9 = bhava_from_lr(9)
    b11 = bhava_from_lr(11)
    lord2 = BHAVA_LORDS.get(b2)
    lord11 = BHAVA_LORDS.get(b11)

    # i1: Saravali Ch.34 St.15-16 — "If the 2nd house has benefic/aspected
    #     by benefic — dhana yoga strong"
    i1 = bhava_has_benefic(b2) or bhava_aspected_by_benefic(b2, asp)

    # i2: Saravali Ch.34 St.58 — "Planets in 11th = source of gains"
    #     Benefic in 11th = strong gain yoga
    i2 = bhava_has_benefic(b11) or bhava_aspected_by_benefic(b11, asp)

    # i3: BPHS Ch.15 — "2nd lord strong = dhana bhava strong"
    i3 = planet_strong(lord2) if lord2 else False

    # i4: BPHS Ch.15 — "11th lord strong = labha bhava strong"
    i4 = planet_strong(lord11) if lord11 else False

    # i5: Saravali Ch.34 St.58-66 — planet-wise gain source from 11th bhava
    #     Jupiter = naisargika dhana karaka (BPHS Ch.7 — "Jupiter rules wealth,
    #     gold, learning, religion, sons")
    #     Saravali Ch.6 St.2 — "Jupiter rules wealth, sons, learning"
    i5 = planet_strong("jupiter")

    arth_positive = sum([i1,i2,i3,i4,i5])

    # 11th bhava planet → gain source (Saravali Ch.34 St.58-66)
    GAIN_SOURCE = {
        "sun":    "రాజు/సర్కార్ ద్వారా లాభం",
        "moon":   "స్త్రీలు/వ్యాపారం ద్వారా లాభం",
        "mars":   "స్వర్ణం/ఆయుధాలు/ధైర్యం ద్వారా",
        "mercury":"రచన/కళలు/వాదం ద్వారా",
        "jupiter":"నగర నాయకత్వం/యజ్ఞాలు ద్వారా",
        "venus":  "వేశ్యలు/ముత్యాలు/వెండి ద్వారా",
        "saturn": "నగరాలు/ఇనుము/గేదెలు ద్వారా"
    }
    b11_planets = [p for p in d1p if d1p[p].get("bhava")==b11 and p not in ["rahu","ketu"]]
    gain_sources = [GAIN_SOURCE.get(p,"") for p in b11_planets if GAIN_SOURCE.get(p)]

    result["arthika"] = {
        "d1_2nd_shubha": i1,
        "d1_11th_shubha": i2,
        "2nd_lord_strong": i3,
        "11th_lord_strong": i4,
        "jupiter_strong": i5,
        "gain_source_te": gain_sources if gain_sources else ["11వ bhava ఖాళీ"],
        "positive_factors": arth_positive,
        "total_factors": 5,
        "overall_yoga": overall_yoga(arth_positive, 5),
        "source": "Saravali Ch.34 St.58-66"
    }

    # ══════════════════════════════════════════════
    # 5. ఆరోగ్యం — Saravali Ch.34 St.74-78 + Phaladeepika Ch.14
    # ══════════════════════════════════════════════
    b1 = lr
    b6 = bhava_from_lr(6)
    b8 = bhava_from_lr(8)

    # j1: Saravali Ch.34 St.74 — "Malefics in Ascendant = diseases/weak body"
    #     Contrapositive: Lagna malefic-free = healthy body
    j1 = not bhava_has_malefic(b1)

    # j2: Saravali Ch.34 + BPHS Ch.3 — Moon = body/mind health karaka
    #     "Moon strong = healthy mind and body"
    j2 = planet_strong("moon")

    # j3: Phaladeepika Ch.14 — "malefic occupying or aspecting 8th house —
    #     death caused through diseases"
    #     Saravali Ch.30 St.33 — "If Mars in 8th — suffer from diseases, short-lived"
    #     Contrapositive: 8th malefic-free = healthier, longer life
    j3 = not bhava_has_malefic(b8)

    # j4: REMOVED — "6th benefic = health good" rule
    #     No classical source found. Saravali Ch.30 St.19 only says
    #     "Moon in 6th = stomachial diseases" — negative rule, not positive.
    #     Brihat Jataka Ashtakavarga: "benefic places of Saturn are 3rd,5th,6th,11th"
    #     — Ashtakavarga context, not health rule.
    #     Therefore j4 removed from arogya calculation.

    # arogya classical rules
    aro_rules = []
    if j1: aro_rules.append("Saravali Ch.34 St.74: లగ్నంలో పాప గ్రహాలు లేవు → శరీరం బలిష్టం")
    if j2: aro_rules.append("BPHS Ch.3: చంద్రుడు బలిష్టం → మంచి ఆరోగ్యం")
    if j3: aro_rules.append("Phaladeepika Ch.14 + Saravali Ch.30 St.33: 8వ bhava పాప గ్రహాలు లేవు → దీర్ఘాయువు")
    aro_positive = sum([j1,j2,j3])

    result["arogya"] = {
        "lagna_malefic_free": j1,
        "moon_strong": j2,
        "8th_malefic_free": j3,
        "positive_factors": aro_positive,
        "total_factors": 3,
        "overall_yoga": overall_yoga(aro_positive, 3),
        "classical_rule": " | ".join(aro_rules) if aro_rules else "Phaladeepika Ch.14",
        "source": "Phaladeepika Ch.14 + Saravali Ch.30 St.33 + Ch.34 St.74"
    }

    # ══════════════════════════════════════════════
    # 6. తల్లి — Saravali Ch.34 St.55-58 + Phaladeepika Ch.16
    # ══════════════════════════════════════════════
    b4 = bhava_from_lr(4)
    lord4 = BHAVA_LORDS.get(b4)

    # k1: Saravali Ch.34 — "4th bhava = mother, happiness, home"
    #     Phaladeepika Ch.16 — "4th house + benefic = mother's wellbeing"
    #     BPHS Ch.7 — "Moon = mother's karaka"
    k1 = bhava_has_benefic(b4) or bhava_aspected_by_benefic(b4, asp)

    # k2: BPHS Ch.15 — "4th lord well placed = 4th bhava strong = mother protected"
    k2 = planet_strong(lord4) if lord4 else False

    # k3: BPHS Ch.7 — "Moon is the karaka of mother"
    #     Saravali Ch.34 — "Moon strong = mother's wellbeing"
    k3 = planet_strong("moon")

    talli_positive = sum([k1,k2,k3])
    talli_rules = []
    if k1: talli_rules.append("Saravali Ch.34 + Phaladeepika Ch.16: 4వ bhava శుభం → తల్లి క్షేమంగా ఉంటారు")
    if k2: talli_rules.append("BPHS Ch.15: 4వ lord బలిష్టం → తల్లి రక్షణ")
    if k3: talli_rules.append("BPHS Ch.7: చంద్రుడు (తల్లి కారకుడు) బలిష్టం")

    result["talli"] = {
        "d1_4th_shubha": k1,
        "4th_lord_strong": k2,
        "moon_strong": k3,
        "positive_factors": talli_positive,
        "total_factors": 3,
        "overall_yoga": overall_yoga(talli_positive, 3),
        "classical_rule": " | ".join(talli_rules) if talli_rules else "Saravali Ch.34",
        "source": "Saravali Ch.34 + Phaladeepika Ch.16 + BPHS Ch.7"
    }

    # ══════════════════════════════════════════════
    # 7. తండ్రి — Saravali Ch.34 St.27-28 + Phaladeepika Ch.16
    # ══════════════════════════════════════════════
    lord9 = BHAVA_LORDS.get(b9)

    # l1: Saravali Ch.34 — "9th bhava = father, fortune, righteousness"
    #     Phaladeepika Ch.16 — "9th house benefic = father's wellbeing"
    l1 = bhava_has_benefic(b9) or bhava_aspected_by_benefic(b9, asp)

    # l2: BPHS Ch.15 — "9th lord well placed = bhagya bhava strong = father strong"
    l2 = planet_strong(lord9) if lord9 else False

    # l3: BPHS Ch.7 — "Sun is the karaka of father"
    #     Saravali Ch.34 — "Sun strong = father's wellbeing, authority"
    l3 = planet_strong("sun")

    tandri_positive = sum([l1,l2,l3])
    tandri_rules = []
    if l1: tandri_rules.append("Saravali Ch.34 + Phaladeepika Ch.16: 9వ bhava శుభం → తండ్రి క్షేమంగా ఉంటారు")
    if l2: tandri_rules.append("BPHS Ch.15: 9వ lord బలిష్టం → భాగ్య భావం బలం")
    if l3: tandri_rules.append("BPHS Ch.7: సూర్యుడు (తండ్రి కారకుడు) బలిష్టం")

    result["tandri"] = {
        "d1_9th_shubha": l1,
        "9th_lord_strong": l2,
        "sun_strong": l3,
        "positive_factors": tandri_positive,
        "total_factors": 3,
        "overall_yoga": overall_yoga(tandri_positive, 3),
        "classical_rule": " | ".join(tandri_rules) if tandri_rules else "Saravali Ch.34",
        "source": "Saravali Ch.34 + Phaladeepika Ch.16 + BPHS Ch.7"
    }

    # ══════════════════════════════════════════════
    # 8. విదేశం — BPHS + Saravali Ch.34 St.69-70
    # ══════════════════════════════════════════════
    b12 = bhava_from_lr(12)
    b9  = bhava_from_lr(9)
    lord12 = BHAVA_LORDS.get(b12)
    lord9_v = BHAVA_LORDS.get(b9)
    rahu_b = d1p.get("rahu",{}).get("bhava",0)

    # m1: Saravali Ch.34 St.69-70 — "12th bhava = foreign lands, bed pleasures,
    #     expenses abroad" — 12th bhava favorable = positive foreign experience
    #     BPHS Ch.12 — "12th bhava = vyaya, foreign residence, moksha"
    m1 = bhava_has_benefic(b12) or not bhava_has_malefic(b12)

    # m2: REMOVED — "Rahu 3/6/9/12 = foreign" — No classical source found.
    #     Rahu = foreign dasha timing (Raman Vol 2) but NOT bhava-specific rule.

    # m3: REMOVED — "Saturn 3/12 = foreign" — No classical source found.
    #     Phaladeepika: Sun+Saturn in 10th = foreign service only (conjunction rule).

    # m2_new: BPHS Ch.11 — "4th house = homeland, birthplace"
    #     "Rahu afflicting 4th = separation from birthplace = foreign tendency"
    b4_v = bhava_from_lr(4)
    m2_new = rahu_b == b4_v or any(
        a.get("planet_en")=="rahu"
        for a in asp.get("rahu",{}).get("aspects_to",[])
        if a.get("bhava")==b4_v
    )

    # m3_new: BPHS Ch.7 — 12th = foreign residence | 9th = long journeys/fortune
    #     Classical standard — "9th and 12th houses primary for foreign travel"
    #     "12th lord or 9th lord well-placed = foreign yoga active"
    l12_bhava = d1p.get(lord12,{}).get("bhava",0) if lord12 else 0
    l9v_bhava = d1p.get(lord9_v,{}).get("bhava",0) if lord9_v else 0
    m3_new = (l12_bhava in {1,9,10,12}) or (l9v_bhava in {1,9,12})

    # m4: BPHS Ch.15 — "12th lord strong = 12th bhava significations active"
    #     12th lord strong = foreign bhava activated
    m4 = planet_strong(lord12) if lord12 else False

    vid_positive = sum([m1, m2_new, m3_new, m4])
    vid_rules = []
    if m1: vid_rules.append("Saravali Ch.34 St.69-70 + BPHS Ch.12: 12వ bhava అనుకూలం → విదేశ అనుభవం")
    if m2_new: vid_rules.append("BPHS Ch.11: రాహు 4వ bhava afflict చేస్తున్నాడు → స్వస్థలం నుండి వేర్పాటు")
    if m3_new: vid_rules.append("BPHS Ch.7: 12వ/9వ lord అనుకూలంగా ఉన్నారు → విదేశ యోగం")
    if m4: vid_rules.append("BPHS Ch.15: 12వ lord బలిష్టం → విదేశ భావం active")

    result["videsha"] = {
        "d1_12th_favorable": m1,
        "rahu_afflicts_4th": m2_new,
        "12th_9th_lord_connected": m3_new,
        "12th_lord_strong": m4,
        "positive_factors": vid_positive,
        "total_factors": 4,
        "overall_yoga": overall_yoga(vid_positive, 4),
        "classical_rule": " | ".join(vid_rules) if vid_rules else "Saravali Ch.34 St.69-70",
        "source": "Saravali Ch.34 St.69-70 + BPHS Ch.11,12,15"
    }

    # ══════════════════════════════════════════════
    # 9. ఆయుర్దాయం — Phaladeepika Ch.13 + Brihat Jataka Ch.7
    # ══════════════════════════════════════════════
    lagna_lord = BHAVA_LORDS.get(lr)

    # n1: Phaladeepika Ch.13 — "Lagna lord strong = long life"
    #     BPHS Ch.15 — "Lagna lord in shubha = ayur strong"
    n1 = planet_strong(lagna_lord) if lagna_lord else False

    # n2: Saravali Ch.34 St.74 — "Malefics in Ascendant = weak body/short life"
    #     Contrapositive: Lagna malefic-free = better longevity foundation
    n2 = not bhava_has_malefic(b1)

    # n3: Phaladeepika Ch.13 + BPHS Ch.3 — "Moon = body/mind/constitution karaka"
    #     "Moon strong = strong constitution = better longevity"
    n3 = planet_strong("moon")

    # n4: REMOVED — "Saturn in 1st/7th = ayur weak"
    #     Phaladeepika Ch.7 St.7 says "Saturn rules longevity" as karaka only.
    #     "Saturn in 7th" specific effect (Phaladeepika Ch.7 St.3) relates to
    #     spouse, not directly longevity reduction. No direct classical rule found.

    ayu_positive = sum([n1,n2,n3])
    ayu_rules = []
    if n1: ayu_rules.append("Phaladeepika Ch.13 + BPHS Ch.15: లగ్నాధిపతి బలిష్టం → దీర్ఘాయువు")
    if n2: ayu_rules.append("Saravali Ch.34 St.74: లగ్నంలో పాప గ్రహాలు లేవు → ఆయుర్దాయం అనుకూలం")
    if n3: ayu_rules.append("Phaladeepika Ch.13 + BPHS Ch.3: చంద్రుడు బలిష్టం → మంచి రాజ్యాంగం")

    result["ayurdaya"] = {
        "lagna_lord_strong": n1,
        "lagna_malefic_free": n2,
        "moon_strong": n3,
        "positive_factors": ayu_positive,
        "total_factors": 3,
        "overall_yoga": overall_yoga(ayu_positive, 3),
        "note": "ఆయుర్దాయం range మాత్రమే — exact year చెప్పకూడదు",
        "classical_rule": " | ".join(ayu_rules) if ayu_rules else "Phaladeepika Ch.13",
        "source": "Phaladeepika Ch.13 + Brihat Jataka Ch.7 Sl.1-4"
    }

    # ══════════════════════════════════════════════
    # 10. యోగ + దశా timing — Multi-factor confirm
    # ══════════════════════════════════════════════
    result["yoga_dasha_timing"] = {
        "note": "MD+AD+Pratyantar మూడూ align అయినప్పుడే timing confirm చేయాలి",
        "rule": "ఒక్క MD చూసి exact year చెప్పకూడదు — Phaladeepika Ch.19-21",
        "source": "Phaladeepika Ch.19-21 + Brihat Jataka Ch.8"
    }

    return result

# ═══════════════════════════════════════════════════════════
# PANCHA MAHAPURUSHA YOGA detection
# Source: BPHS Ch.75 (పరాశరుడు) + Brihat Jataka (వరాహమిహిర)
# ═══════════════════════════════════════════════════════════
def calc_pancha_mahapurusha(d1p, lr):
    KENDRA = {1,4,7,10}
    PM_PLANETS = {
        "mars":    {"yoga_te":"రుచక యోగం",   "yoga_en":"Ruchaka"},
        "mercury": {"yoga_te":"భద్ర యోగం",    "yoga_en":"Bhadra"},
        "jupiter": {"yoga_te":"హంస యోగం",     "yoga_en":"Hamsa"},
        "venus":   {"yoga_te":"మాళవ్య యోగం",  "yoga_en":"Malavya"},
        "saturn":  {"yoga_te":"శశ యోగం",      "yoga_en":"Sasa"},
    }
    PM_RESULTS = {
        "mars":    "శూరుడు, క్రూరుడు, సేనాపతి, ధనవంతుడు",
        "mercury": "తెలివైనవాడు, వక్త, వ్యాపారి, గణిత నిపుణుడు",
        "jupiter": "విద్వాంసుడు, ధర్మపరుడు, రాజ సమ్మానం, దీర్ఘాయువు",
        "venus":   "సౌందర్యవంతుడు, సంపన్నుడు, సుఖజీవి",
        "saturn":  "సేవకులు ఉంటారు, ధనవంతుడు, నాయకుడు, దీర్ఘాయువు",
    }
    result = {}; yogas_present = []
    for pk, info in PM_PLANETS.items():
        if pk not in d1p:
            result[pk] = {"present": False}; continue
        rashi = d1p[pk].get("rashi_num",0); bhava = d1p[pk].get("bhava",0)
        is_swa = rashi in SWARASHI.get(pk,[]); is_uccha = UCCHA_RASHI.get(pk)==rashi
        present = (is_swa or is_uccha) and bhava in KENDRA
        dignity = "ఉచ్చం" if is_uccha else ("స్వరాశి" if is_swa else "")
        result[pk] = {"planet_te":PLANET_TE.get(pk,"?"),"yoga_te":info["yoga_te"],
                      "yoga_en":info["yoga_en"],"present":present,"dignity":dignity,
                      "bhava":bhava,"note":f"{info['yoga_te']} — {PM_RESULTS[pk]}" if present else "",
                      "source":"BPHS Ch.75 (పరాశరుడు)"}
        if present:
            yogas_present.append({"planet_en":pk,"planet_te":PLANET_TE.get(pk,"?"),
                                   "yoga_te":info["yoga_te"],"yoga_en":info["yoga_en"],
                                   "dignity":dignity,"bhava":bhava,"result_te":PM_RESULTS[pk]})
    return {"any_present":len(yogas_present)>0,"count":len(yogas_present),
            "yogas_present":yogas_present,"planet_details":result,
            "source":"BPHS Ch.75 (పరాశరుడు) + Brihat Jataka (వరాహమిహిర)"}


# ═══════════════════════════════════════════════════════════
# SARAVALI Ch.13 — Planet-wise Sunapha/Anapha/Durudhura effects
# Source: Kalyana Varma Saravali Chapter 13
# ═══════════════════════════════════════════════════════════
def calc_saravali_ch13_lunar_yogas(d1p):
    moon_r = d1p.get("moon",{}).get("rashi_num",0)
    s2r = (moon_r%12)+1; s12r = ((moon_r-2)%12)+1
    PLANETS = ["mars","mercury","jupiter","venus","saturn"]
    SUNAPHA_EFFECTS = {
        "mars":    "శూరుడు, ధనవంతుడు, క్రూర వాక్కు, సేనాపతి, తీవ్ర స్వభావం",
        "mercury": "వేద-శాస్త్ర-సంగీత నిపుణుడు, కవి, సుందర దేహం, ఉన్నత మనస్సు",
        "jupiter": "అధిక విద్యావంతుడు, ప్రసిద్ధుడు, రాజు లేదా రాజ ప్రియుడు, ధనవంతుడు",
        "venus":   "భార్య-భూమి-ధన-శక్తి-పశువులు, రాజ సమ్మానం, శూరుడు",
        "saturn":  "నేర్పరి, గ్రామ-నగర జనుల పూజనీయుడు, ధనవంతుడు, కర్తవ్య నిష్ఠ"
    }
    ANAPHA_EFFECTS = {
        "mars":    "దొంగల నాయకుడు, అహంకారి, యుద్ధ ప్రియుడు, సుందర దేహం",
        "mercury": "సంగీత-నృత్య-లేఖన నిపుణుడు, కవి, వక్త, రాజ సమ్మానం",
        "jupiter": "మహిమాన్వితుడు, బలవంతుడు, తెలివైనవాడు, రాజ ప్రియ కవి",
        "venus":   "స్త్రీ ప్రియుడు, రాజ ప్రియుడు, సుఖజీవి, ప్రసిద్ధుడు, స్వర్ణ సంపన్నుడు",
        "saturn":  "విశాల భుజాలు, నాయకుడు, పశు సంపన్నుడు, ధర్మపరుడు"
    }
    DURUDHURA_EFFECTS = {
        ("mars","mercury"):   "అబద్ధాలకోరు, అత్యంత ధనవంతుడు, నేర్పరి",
        ("mars","jupiter"):   "కార్యనిష్ఠుడు, బలవంతుడు, రక్షకుడు, ధన సంచయం",
        ("mars","venus"):     "పుణ్యాత్మ భార్య, భాగ్యవంతుడు, శూరుడు",
        ("mars","saturn"):    "చెడు భార్య, ధన సంచయం, క్రోధి",
        ("mercury","jupiter"):"ధర్మపరుడు, శాస్త్ర విద్వాంసుడు, కవి, ధనవంతుడు",
        ("mercury","venus"):  "మధుర వక్త, భాగ్యవంతుడు, నృత్య-సంగీత ప్రియుడు, మంత్రి",
        ("mercury","saturn"): "దేశ దేశాలు తిరుగువాడు, పూజనీయుడు",
        ("jupiter","venus"):  "శూరుడు, తెలివైనవాడు, స్వర్ణ-రత్న సంపన్నుడు",
        ("jupiter","saturn"): "సుఖవంతుడు, మధుర వక్త, విద్వాంసుడు, శాంతి ప్రియుడు",
        ("venus","saturn"):   "పరిణతి గలవాడు, వంశ ముఖ్యుడు, నేర్పరి, ధనవంతుడు"
    }
    sunapha_planets = [p for p in PLANETS if d1p.get(p,{}).get("rashi_num")==s2r]
    anapha_planets  = [p for p in PLANETS if d1p.get(p,{}).get("rashi_num")==s12r]
    sunapha_results = [{"planet_en":p,"planet_te":PLANET_TE.get(p,"?"),
                        "effect_te":SUNAPHA_EFFECTS.get(p,""),
                        "source":"Saravali Ch.13 St.10-14"} for p in sunapha_planets]
    anapha_results  = [{"planet_en":p,"planet_te":PLANET_TE.get(p,"?"),
                        "effect_te":ANAPHA_EFFECTS.get(p,""),
                        "source":"Saravali Ch.13 St.15-19"} for p in anapha_planets]
    durudhura_results = []
    for sp in sunapha_planets:
        for ap in anapha_planets:
            key = tuple(sorted([sp,ap]))
            if key in DURUDHURA_EFFECTS:
                durudhura_results.append({"planets_te":[PLANET_TE.get(k,"?") for k in key],
                                          "effect_te":DURUDHURA_EFFECTS[key],
                                          "source":"Saravali Ch.13 St.20-29"})
    yoga_type = "DURUDHURA" if (sunapha_planets and anapha_planets) else \
                "SUNAPHA" if sunapha_planets else \
                "ANAPHA"  if anapha_planets else "KEMADRUMA"
    return {"yoga_type":yoga_type,
            "sunapha_planets":[PLANET_TE.get(p,"?") for p in sunapha_planets],
            "anapha_planets": [PLANET_TE.get(p,"?") for p in anapha_planets],
            "sunapha_results":sunapha_results,"anapha_results":anapha_results,
            "durudhura_results":durudhura_results,
            "source":"Kalyana Varma Saravali Chapter 13"}


# ═══════════════════════════════════════════════════════════
# SARAVALI Ch.14 — Vasi/Vesi/Ubhayachari Yogas
# Source: Kalyana Varma Saravali Chapter 14
# ═══════════════════════════════════════════════════════════
def calc_saravali_ch14_solar_yogas(d1p):
    sun_r  = d1p.get("sun",{}).get("rashi_num",0)
    vasi_r = ((sun_r-2)%12)+1; vesi_r = (sun_r%12)+1
    PLANETS = ["mars","mercury","jupiter","venus","saturn"]
    VASI_GENERAL  = "శ్రేష్ఠ వాక్కు, మంచి జ్ఞాపకశక్తి, ఉద్యోగం, రాజ తుల్యుడు, నిజాయితీపరుడు"
    VESI_GENERAL  = "బలహీన దృష్టి, వాగ్దానపాలన, కష్టజీవి"
    UBHAYA_GENERAL = "సహనం, అదృష్టవంతుడు, బలవంతుడు, విద్వాంసుడు, రాజ తుల్యుడు"
    VASI_EFFECTS = {
        "jupiter": "ధైర్యం, బలం, జ్ఞానం, వాగ్దానపాలన",
        "venus":   "శూరుడు, ప్రసిద్ధుడు, ధర్మపరుడు, కీర్తివంతుడు",
        "mercury": "మధుర వక్త, సుందరుడు, ఇతరుల ఆజ్ఞలు పాటించేవాడు",
        "mars":    "యుద్ధ విజేత, ప్రసిద్ధుడు, స్వశక్తితో జీవించేవాడు",
        "saturn":  "వ్యాపారి, పెద్దలను ద్వేషించేవాడు, పుణ్యాత్మ భార్య"
    }
    VESI_EFFECTS = {
        "jupiter": "ధన సంచయం, విద్వాంసుడు, సద్గుణవంతుడు",
        "venus":   "భీరువు, అడ్డంకులు, ఓటమి",
        "mercury": "సేవకుడు, మృదు వాక్కు, వినయం",
        "mars":    "నీచ మార్గాలు, ఇతరులకు సహాయం",
        "saturn":  "పరస్త్రీ ప్రియుడు, దుష్ట స్వభావం, ధనవంతుడు"
    }
    vasi_planets = [p for p in PLANETS if d1p.get(p,{}).get("rashi_num")==vasi_r]
    vesi_planets = [p for p in PLANETS if d1p.get(p,{}).get("rashi_num")==vesi_r]
    ubhaya = bool(vasi_planets and vesi_planets)
    yoga_type = "UBHAYACHARI" if ubhaya else "VASI" if vasi_planets else "VESI" if vesi_planets else "లేదు"
    vasi_results = [{"planet_en":p,"planet_te":PLANET_TE.get(p,"?"),
                     "general_te":VASI_GENERAL,"specific_te":VASI_EFFECTS.get(p,""),
                     "source":"Saravali Ch.14 St.6-9"} for p in vasi_planets]
    vesi_results = [{"planet_en":p,"planet_te":PLANET_TE.get(p,"?"),
                     "general_te":VESI_GENERAL,"specific_te":VESI_EFFECTS.get(p,""),
                     "source":"Saravali Ch.14 St.2-5"} for p in vesi_planets]
    return {"yoga_type":yoga_type,
            "vasi_planets":[PLANET_TE.get(p,"?") for p in vasi_planets],
            "vesi_planets":[PLANET_TE.get(p,"?") for p in vesi_planets],
            "ubhayachari":ubhaya,"ubhaya_general":UBHAYA_GENERAL if ubhaya else "",
            "vasi_results":vasi_results,"vesi_results":vesi_results,
            "source":"Kalyana Varma Saravali Chapter 14"}


# ═══════════════════════════════════════════════════════════
# EKADHIPATYA — Dual House Lordship Analysis
# Source: Phaladeepika Ch.15 (మంత్రేశ్వరుడు) Stanza 11, 29
# ═══════════════════════════════════════════════════════════
def calc_ekadhipatya(d1p, lr):
    SHUBHA   = {1,4,5,7,9,10}; DUSTHANA = {6,8,12}
    def bhava_type(b):
        if b in SHUBHA: return "శుభం"
        if b in DUSTHANA: return "దుష్టం"
        return "నపుంసకం"
    from collections import defaultdict
    planet_bhavas = defaultdict(list)
    for bh in range(1,13):
        bh_rashi = ((lr-1+bh-1)%12)+1
        lord = BHAVA_LORDS.get(bh_rashi)
        if lord: planet_bhavas[lord].append(bh)
    result = {}
    for pk in ["sun","moon","mars","mercury","jupiter","venus","saturn"]:
        bhavas = planet_bhavas.get(pk,[])
        if len(bhavas)<2:
            result[pk] = {"planet_te":PLANET_TE.get(pk,"?"),"ekadhipatya":False,
                          "bhavas":bhavas,"note":"ఒక్క భావానికి మాత్రమే lord — Ekadhipatya వర్తించదు"}
            continue
        b1,b2 = bhavas[0],bhavas[1]; t1=bhava_type(b1); t2=bhava_type(b2)
        mt_rashi = MOOL_TRIKONA.get(pk)
        mt_bhava = ((mt_rashi-lr)%12)+1 if mt_rashi else None
        dom = mt_bhava if mt_bhava in [b1,b2] else b1
        sec = b2 if dom==b1 else b1
        p_bhava = d1p.get(pk,{}).get("bhava",0)
        dom_type = bhava_type(dom); sec_type = bhava_type(sec)
        st29 = (p_bhava==dom and dom_type=="శుభం" and sec_type=="దుష్టం") or \
               (p_bhava==sec and sec_type=="శుభం" and dom_type=="దుష్టం")
        if st29: dasha_note=f"{PLANET_TE.get(pk,'?')} దశలో → శుభ bhava ఫలాలు మాత్రమే"
        elif dom_type=="శుభం" and sec_type=="దుష్టం":
            dasha_note=f"{PLANET_TE.get(pk,'?')} దశలో → {dom}వ శుభ ఫలాలు + {sec}వ దుష్ట ఫలాలు మిశ్రమం"
        elif dom_type=="దుష్టం" and sec_type=="శుభం":
            dasha_note=f"{PLANET_TE.get(pk,'?')} దశలో → {dom}వ దుష్ట ఫలాలు dominant + {sec}వ శుభ ఫలాలు half"
        elif dom_type=="శుభం" and sec_type=="శుభం":
            dasha_note=f"{PLANET_TE.get(pk,'?')} దశలో → రెండూ శుభ bhavas → పూర్తి శుభ ఫలాలు"
        else: dasha_note=f"{PLANET_TE.get(pk,'?')} దశలో → మిశ్రమ ఫలాలు"
        result[pk] = {"planet_te":PLANET_TE.get(pk,"?"),"ekadhipatya":True,
                      "bhavas":[b1,b2],"bhava_types":[t1,t2],
                      "dominant_bhava":dom,"dominant_type":dom_type,
                      "secondary_bhava":sec,"secondary_type":sec_type,
                      "planet_in_bhava":p_bhava,"moolatrikona_bhava":mt_bhava,
                      "stanza29_applies":st29,
                      "stanza29_note":f"Stanza 29: {PLANET_TE.get(pk,'?')} శుభ bhava లో — దుష్ట ఫలాలు రావు" if st29 else "",
                      "dasha_note":dasha_note,
                      "source":"Phaladeepika Ch.15 Stanza 11+29 (మంత్రేశ్వరుడు)"}
    return result

# ═══════════════════════════════════════════════════════════
# SARAVALI CH.44 — Antidotes for Evil Dashas
# Source: Kalyana Varma "Saravali" Chapter 44
# "దశాగమే" — జన్మ పట్టికలో planet uccha/swarashi/mitra రాశిలో ఉంటే
# ఆ planet మహాదశలో దుష్ఫలాలు నశిస్తాయి
# ═══════════════════════════════════════════════════════════
def calc_saravali_ch44_antidote(d1p):
    """
    Saravali Ch.44: Natal chart లో ప్రతి planet కి ch44_antidote flag
    ఆ planet మహాదశ వచ్చినప్పుడు దుష్ఫలాలు నశిస్తాయా లేదా అని
    Source: Kalyana Varma Saravali Chapter 44 — "దశాగమే శుభాంశే..."
    """
    BENEFICS = {"jupiter","venus","mercury","moon"}

    result = {}
    for pk in ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]:
        if pk not in d1p:
            result[pk] = {"planet_te": PLANET_TE.get(pk,"?"), "ch44_antidote": False, "reason": ""}
            continue

        pd = d1p[pk]
        rashi = pd.get("rashi_num", 0)

        # Condition check
        is_uccha   = UCCHA_RASHI.get(pk) == rashi
        is_swa     = rashi in SWARASHI.get(pk, [])
        is_moola   = MOOL_TRIKONA.get(pk) == rashi
        # Mitra rashi — friendly sign
        is_mitra   = pd.get("strength") in ("మిత్ర రాశి",)

        benefic_div = is_uccha or is_swa or is_moola or is_mitra

        # Aspected by benefic (from aspects already calculated — check done post-asp calc)
        # Here we store planet status; V27 will combine with asp data
        if is_uccha:
            div_tag = "ఉచ్చం"
        elif is_swa:
            div_tag = "స్వరాశి"
        elif is_moola:
            div_tag = "మూలత్రికోణం"
        elif is_mitra:
            div_tag = "మిత్ర రాశి"
        else:
            div_tag = ""

        result[pk] = {
            "planet_te":    PLANET_TE.get(pk, "?"),
            "ch44_antidote": benefic_div,
            "dignity":       div_tag,
            "note": f"{PLANET_TE.get(pk,'?')} దశలో దుష్ఫలాలు నశిస్తాయి (Saravali Ch.44)" if benefic_div else f"{PLANET_TE.get(pk,'?')} దశలో Ch.44 antidote లేదు",
            "source": "Kalyana Varma Saravali Chapter 44"
        }

    return result

# ═══════════════════════════════════════════════════════════
# CONJUNCTION DOMINANT PLANET ANALYSIS
# Source: Saravali Ch.4 St.40 (కళ్యాణ వర్మ) — "stronger planet prevails"
#         Saravali Ch.4 St.19-20 — "effects correspond to strength of Lords"
#         Phaladeepika — "Lagna lord stronger than 8th lord = native survives"
# ═══════════════════════════════════════════════════════════
def calc_conjunction_dominance(d1p, shad):
    """
    Conjunction లో ఏ planet dominant అనేది calculate చేయడం
    Source: Saravali Ch.4 St.40 — "Should two planets have identical strength,
            the one with higher Naisarga Bala will prevail."
    """
    # Group planets by bhava
    bhava_groups = {}
    for pk in ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]:
        if pk not in d1p: continue
        b = d1p[pk].get("bhava",0)
        if b not in bhava_groups: bhava_groups[b] = []
        bhava_groups[b].append(pk)

    result = {}

    for bhava, planets in bhava_groups.items():
        if len(planets) < 2:
            continue  # conjunction కాదు — skip

        # Step 1: Shadbala strength score
        def strength_score(pk):
            if pk in ["rahu","ketu"]:
                return NAISARGIKA_VIRUPA.get(pk, 15.0)
            shad_data = shad.get(pk, {})
            total = shad_data.get("total_virupa", NAISARGIKA_VIRUPA.get(pk, 25.71))
            return float(total)

        # Step 2: Sort by strength (highest first)
        scored = [(pk, strength_score(pk)) for pk in planets]
        scored.sort(key=lambda x: x[1], reverse=True)

        dominant = scored[0][0]
        subordinate = [p for p,s in scored[1:]]

        # Step 3: Naisargika tiebreaker (Saravali Ch.4 St.40)
        if len(scored) >= 2:
            if abs(scored[0][1] - scored[1][1]) < 5.0:  # scores close
                # Natural strength tiebreaker
                dom_nai = NAISARGIKA_ORDER.get(dominant, 5)
                sub_nai = NAISARGIKA_ORDER.get(scored[1][0], 5)
                if sub_nai > dom_nai:  # higher order = stronger naturally
                    dominant = scored[1][0]
                    subordinate = [p for p,s in scored if p != dominant]

        result[bhava] = {
            "bhava": bhava,
            "planets_te": [PLANET_TE.get(p,"?") for p in planets],
            "dominant_planet_en": dominant,
            "dominant_planet_te": PLANET_TE.get(dominant,"?"),
            "dominant_score": round(scored[0][1], 2),
            "subordinate_planets_te": [PLANET_TE.get(p,"?") for p in subordinate],
            "classical_rule": f"Saravali Ch.4 St.40: {PLANET_TE.get(dominant,'?')} బలిష్టం → వారి ఫలాలు predominate అవుతాయి",
            "source": "Saravali Ch.4 St.40 + St.19-20 (కళ్యాణ వర్మ)"
        }

    return result if result else {}

# ═══════════════════════════════════════════════════════════
# DB8 TARA BALA — intact
# ═══════════════════════════════════════════════════════════
def calc_tara_bala(jni,pd):
    TN={1:"జన్మ",2:"సంపత్",3:"విపత్",4:"క్షేమ",5:"ప్రత్యక్",6:"సాధన",7:"నైధన",8:"మిత్ర",9:"పరమ మిత్ర"}
    TP={1:"జన్మ బలపడతాయి",2:"ధన లాభం",3:"ప్రమాదం",4:"క్షేమం",5:"అడ్డంకులు",6:"సాధన",7:"నష్టం",8:"మిత్రత్వం",9:"అత్యుత్తమ"}
    AK={3,5,7}; tr={}
    for k,p in pd.items():
        if k in ("rahu","ketu"): continue
        pni=int(p["sid_longitude"]/(360/27))%27; c=((pni-jni)%27)+1; tn=c%9; tn=9 if tn==0 else tn
        tr[k]={"planet_te":p["name_te"],"planet_nakshatra":p["nakshatra"],"count_from_janma":c,"tara_num":tn,"tara_name_te":TN[tn],"tara_phalam":TP[tn],"is_ashubha":tn in AK}
    return tr

# ═══════════════════════════════════════════════════════════
# DB8 SHADBALA FUNCTIONS — అన్నీ intact
# ═══════════════════════════════════════════════════════════
def get_dignity_saptav(planet,rashi,rl):
    if UCCHA_RASHI.get(planet)==rashi: return 1.0
    if NEECHA_RASHI.get(planet)==rashi: return 0.0
    if rashi in SWARASHI.get(planet,[]): return 0.875
    fr=NATURAL_FRIENDS.get(planet,set()); en=NATURAL_ENEMIES.get(planet,set())
    if rl in fr and rl not in en: return 0.75
    if rl in en and rl not in fr: return 0.25
    return 0.5

def calc_sthana_bala(planet,sl,rn,pd,dc=None):
    male=["sun","mars","jupiter","saturn"]; female=["moon","venus"]; neuter=["mercury"]
    odd=[1,3,5,7,9,11]; even=[2,4,6,8,10,12]
    el=UCCHA_LON.get(planet,0); dist=abs(sl-el)
    if dist>180: dist=360-dist
    uchcha=max(0.0,(180-dist)/3.0)
    SW={"d1":45,"D2":30,"D3":15,"D7":15,"D9":60,"D10":30,"D12":30}
    if dc:
        sv=0.0
        for ck,w in SW.items():
            chart=dc.get(ck,{})
            if not chart or planet not in chart: sv+=w*0.5; continue
            pr=chart[planet].get("rashi_num",rn); prl=BHAVA_LORDS.get(pr,"sun"); sv+=w*get_dignity_saptav(planet,pr,prl)
    else:
        sm={"ఉచ్చం":45.0,"స్వరాశి":30.0,"సాధారణం":15.0,"నీచం":3.75}; sv=sm.get(pd[planet]["strength"],15.0)
    oja=15.0 if (planet in male and rn in odd) or (planet in female and rn in even) or planet in neuter else 0.0
    bh=pd[planet]["bhava"]; ke=60.0 if bh in [1,4,7,10] else 30.0 if bh in [2,5,8,11] else 15.0
    dr=sl%30; dcc=int(dr/10)+1
    drek=15.0 if (planet in male and dcc==1) or (planet in female and dcc==3) or (planet in neuter and dcc==2) else 0.0
    return uchcha+sv+oja+ke+drek

def calc_dig_bala(planet,bhava):
    sh={"sun":10,"mars":10,"moon":4,"venus":4,"mercury":1,"jupiter":1,"saturn":7}; s=sh.get(planet,1)
    diff=abs(bhava-s); diff=min(diff,12-diff); return max(0.0,60.0-(diff*10.0))

def calc_sunrise_sunset(bd,lat,lon,tz=5.5):
    obs=ephem.Observer(); obs.lat=str(lat); obs.lon=str(lon); obs.pressure=0; sun=ephem.Sun()
    try:
        obs.date=f"{bd.year}/{bd.month:02d}/{bd.day:02d} 00:00:00"
        sru=obs.next_rising(sun).datetime(); ssu=obs.next_setting(sun).datetime()
        obs.date=ssu.strftime("%Y/%m/%d %H:%M:%S"); sr2u=obs.next_rising(sun).datetime()
        sr=sru+datetime.timedelta(hours=tz); ss=ssu+datetime.timedelta(hours=tz); sr2=sr2u+datetime.timedelta(hours=tz)
        is_day=sr<=bd<ss
        if not is_day and bd<sr:
            obs2=ephem.Observer(); obs2.lat=obs.lat; obs2.lon=obs.lon; obs2.pressure=0
            prev=bd-datetime.timedelta(days=1); obs2.date=prev.strftime("%Y/%m/%d 12:00:00")
            ns=(obs2.next_setting(sun).datetime())+datetime.timedelta(hours=tz)
        else: ns=ss
        return {"sunrise_local":sr,"sunset_local":ss,"sunrise2_local":sr2,"night_start":ns,"is_day_birth":is_day,"ok":True}
    except:
        h=bd.hour; return {"sunrise_local":bd.replace(hour=6,minute=0,second=0),"sunset_local":bd.replace(hour=18,minute=0,second=0),"sunrise2_local":bd.replace(hour=6,minute=0,second=0)+datetime.timedelta(days=1),"night_start":bd.replace(hour=18,minute=0,second=0),"is_day_birth":6<=h<18,"ok":False}

def calc_tribhaga_lord(bd,lat,lon,tz=5.5,_ss=None):
    c=_ss or calc_sunrise_sunset(bd,lat,lon,tz); sr=c["sunrise_local"]; ss=c["sunset_local"]; sr2=c["sunrise2_local"]; ns=c["night_start"]; id=c["is_day_birth"]
    try:
        if id:
            dur=(ss-sr).total_seconds(); pd=dur/3.0; el=(bd-sr).total_seconds(); return ["jupiter","sun","saturn"][min(int(el/pd),2)]
        else:
            dur=(sr2-ns).total_seconds(); pd=dur/3.0; el=max(0,(bd-ns).total_seconds()); return ["moon","venus","mars"][min(int(el/pd),2)]
    except:
        h=bd.hour
        if 6<=h<18: return "jupiter" if h<10 else "sun" if h<14 else "saturn"
        return "moon" if h>=18 else "venus" if h<2 else "mars"

def calc_kala_bala(planet,sl,bd,is_day,tbl=None,stl=None,sc=None):
    """FIX-14,15,16: Abda/Masa/Hora/Ayana (BPHS Ch.27)"""
    mal=["sun","mars","saturn"]; ben=["moon","jupiter","venus","mercury"]
    day_p=["sun","jupiter","saturn"]; night_p=["moon","venus","mars"]
    nath=60.0 if (planet in day_p and is_day) or (planet in night_p and not is_day) or planet=="mercury" else 0.0
    trib=60.0 if planet==tbl else 0.0
    SEVEN=["sun","moon","mars","mercury","jupiter","venus","saturn"]; KALI=588465.5
    jdb=ephem.julian_date(bd); aha=jdb-KALI
    abda=15.0 if planet==SEVEN[int(aha/365.25636)%7] else 0.0
    masa=30.0 if planet==SEVEN[int(aha/29.530588)%7] else 0.0
    wl={0:"moon",1:"mars",2:"mercury",3:"jupiter",4:"venus",5:"saturn",6:"sun"}
    vara=45.0 if planet==wl.get(bd.weekday(),"sun") else 0.0
    HS=["sun","venus","mercury","moon","saturn","jupiter","mars"]; hora=0.0
    if sc and sc.get("ok"):
        sru=sc["sunrise_local"]; sec=(bd-sru).total_seconds()
        if sec<0: ns=sc.get("night_start",sru); sec=max(0,(bd-ns).total_seconds())
        hora=60.0 if planet==HS[int(sec//3600)%7] else 0.0
    utta=(stl%360>=270 or stl%360<90) if stl else (bd.month in [1,2,3,4,5,6])
    ayana=60.0 if (planet in ben and utta) or (planet in mal and not utta) else 30.0
    return nath+trib+abda+masa+vara+hora+ayana

def calc_chesta_bala(planet,ir,spd=None,ml=None,tl=None,sml=None):
    """FIX-17: BPHS exact Chesta Bala"""
    OUTER={"mars","jupiter","saturn"}; INNER={"mercury","venus"}
    if planet in ("rahu","ketu","sun","moon"): return 60.0
    if ml is not None and tl is not None and sml is not None:
        if planet in OUTER:
            avg=(ml+tl)/2.0; k=(sml-avg)%360
            if k>180: k=360-k
            return min(60.0,k/3.0)
        if planet in INNER:
            k=(tl-sml)%360
            if k>180: k=360-k
            return min(60.0,k/3.0)
    if spd is None: return 60.0 if ir else 30.0
    MS={"mars":0.524,"jupiter":0.0831,"saturn":0.0335,"mercury":1.3833,"venus":1.2}
    m=MS.get(planet,0.5)
    if spd<0: return 30.0 if abs(spd)<(m*0.2) else 60.0
    if abs(spd)<(m*0.05): return 15.0
    r=spd/m
    return 30.0 if r<0.5 else 15.0 if r<0.85 else 7.5 if r<=1.15 else 45.0 if r<=1.5 else 30.0

def calc_drik_bala(planet,pd,asp):
    B={"jupiter","venus","moon","mercury"}; ab=asp.get(planet,{}).get("aspected_by",[]); total=0.0
    for a in ab:
        ap=a.get("planet_en",""); an=int(a.get("aspect",7)); v=60.0 if an==7 else 45.0
        total+=v if ap in B else -v
    return round(max(-60.0,min(60.0,total)),2)

def calc_shadbala_virupa(pd,sid,ls,asp,bd,lat=17.385,lon=78.4867,tz=5.5,_ss=None,dc=None,mlon=None,stl=None):
    cache=_ss or calc_sunrise_sunset(bd,lat,lon,tz); is_day=cache["is_day_birth"]
    tbl=calc_tribhaga_lord(bd,lat,lon,tz,_ss=cache)
    ml=sid.get("moon",0); sl=sid.get("sun",0); diff=(ml-sl)%360; is_s=diff<180
    sm=mlon.get("sun_mean",mlon.get("sun",None)) if mlon else None
    mal=["sun","mars","saturn"]; ben=["moon","jupiter","venus","mercury"]; res={}
    for key in ["sun","moon","mars","mercury","jupiter","venus","saturn"]:
        p=pd[key]; sl2=sid[key]; rn=p["rashi_num"]
        sth=calc_sthana_bala(key,sl2,rn,pd,dc=dc)
        dig=calc_dig_bala(key,p["bhava"])
        kala=calc_kala_bala(key,sl2,bd,is_day,tbl=tbl,stl=stl,sc=cache)
        pak=60.0 if (is_s and key in ben) or (not is_s and key in mal) else 0.0; kala+=pak
        ml2=mlon.get(key) if mlon else None
        che=0.0 if key in ("sun","moon") else calc_chesta_bala(key,p.get("is_retrograde",False),p.get("speed_deg_per_day"),ml=ml2,tl=sl2,sml=sm)
        nai=NAISARGIKA_VIRUPA.get(key,25.71); drik=calc_drik_bala(key,pd,asp)
        total=sth+dig+kala+che+nai+drik; mr=SHADBALA_MIN.get(key,300); strong=total>=mr
        res[key]={"planet_te":PLANET_TE[key],"total_virupa":round(total,2),"rupa":round(total/60.0,3),"min_required":mr,"is_strong":strong,"strength_pct":round((total/mr)*100,1),"paksha":"శుక్ల" if is_s else "కృష్ణ","day_night":"పగలు" if is_day else "రాత్రి","components":{"sthana":round(sth,2),"dig":round(dig,2),"kala":round(kala,2),"chesta":round(che,2),"naisargika":round(nai,2),"drik":round(drik,2)}}
    return res

# ═══════════════════════════════════════════════════════════
# ADD-1: మాంది/గులిక longitude calculation
# Source: BPHS Ch.13-14
# వారవారీ దిన/రాత్రి ప్రారంభ ghati table (BPHS exact)
# పగలు: ఆది=26, సోమ=22, మంగళ=18, బుధ=14, గురు=10, శుక్ర=6, శని=2 (ghatis)
# రాత్రి: ఆది=10, సోమ=6, మంగళ=2, బుధ=26, గురు=22, శుక్ర=18, శని=14 (ghatis)
# 1 ghati = 24 minutes; మాంది = 8వ భావ కారకం
# ═══════════════════════════════════════════════════════════
def calc_mandi(bd, sc, lat, lon, tz=5.5):
    """
    ADD-1: మాంది/గులిక longitude — BPHS Ch.13-14
    Returns: {"longitude": float, "rashi_num": int, "rashi_te": str,
              "degrees": float, "nakshatra": str, "pada": int,
              "source": "BPHS Ch.13-14"}
    """
    # BPHS: మాంది ప్రారంభ ghatis — వారము (0=ఆది,...,6=శని) × పగలు/రాత్రి
    # weekday: 6=ఆది, 0=సోమ, 1=మంగళ, 2=బుధ, 3=గురు, 4=శుక్ర, 5=శని
    # Python weekday: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri,5=Sat,6=Sun
    # BPHS order: Sun=0,Mon=1,Tue=2,Wed=3,Thu=4,Fri=5,Sat=6
    # Python to BPHS: Python 6→BPHS 0(Sun), Python 0→BPHS 1(Mon) etc.
    py_to_bphs = {6:0, 0:1, 1:2, 2:3, 3:4, 4:5, 5:6}
    # పగలు మాంది ప్రారంభ ghatis (BPHS table)
    DAY_MANDI_GHATI   = {0:26, 1:22, 2:18, 3:14, 4:10, 5:6, 6:2}
    # రాత్రి మాంది ప్రారంభ ghatis (BPHS table)
    NIGHT_MANDI_GHATI = {0:10, 1:6,  2:2,  3:26, 4:22, 5:18, 6:14}

    is_day = sc.get("is_day_birth", True)
    sr = sc.get("sunrise_local", bd.replace(hour=6,minute=0,second=0))
    ss = sc.get("sunset_local",  bd.replace(hour=18,minute=0,second=0))
    sr2 = sc.get("sunrise2_local", sr + datetime.timedelta(days=1))

    bphs_day = py_to_bphs.get(bd.weekday(), 0)

    if is_day:
        ghati_start = DAY_MANDI_GHATI.get(bphs_day, 26)
        day_dur_sec = (ss - sr).total_seconds()
        # 1 ghati = day_duration / 30
        ghati_sec = day_dur_sec / 30.0
        mandi_time = sr + datetime.timedelta(seconds=ghati_start * ghati_sec)
    else:
        ghati_start = NIGHT_MANDI_GHATI.get(bphs_day, 10)
        ns = sc.get("night_start", ss)
        night_dur_sec = (sr2 - ns).total_seconds()
        ghati_sec = night_dur_sec / 30.0
        mandi_time = ns + datetime.timedelta(seconds=ghati_start * ghati_sec)

    # మాంది సమయంలో లగ్నం = మాంది longitude
    try:
        utc_mandi = mandi_time - datetime.timedelta(hours=tz)
        ep2 = utc_mandi.strftime("%Y/%m/%d %H:%M:%S")
        obs2 = ephem.Observer()
        obs2.lat = str(lat); obs2.lon = str(lon)
        obs2.date = ep2; obs2.epoch = ep2; obs2.pressure = 0
        jd2 = ephem.julian_date(obs2.date)
        ayan2 = get_ayanamsha(jd2, _ayan_mode if "_ayan_mode" in dir() else "lahiri")
        mandi_lon = calc_lagna(obs2, lat, lon, ayan2)
    except Exception:
        mandi_lon = 0.0

    r, d, ni, pada = degrees_to_rashi(mandi_lon)
    return {
        "longitude": round(mandi_lon, 4),
        "rashi_num": r,
        "rashi_te": RASHI_TE.get(r, "?"),
        "degrees": round(d, 4),
        "nakshatra": NAKSHATRA_TE[ni] if ni < 27 else "?",
        "pada": pada,
        "ghati_start": ghati_start,
        "is_day_calc": is_day,
        "source": "BPHS Ch.13-14"
    }

# ═══════════════════════════════════════════════════════════
# ADD-2: విశేష లగ్నాలు — హోరా లగ్నం, భావ లగ్నం, ఘటి లగ్నం
# Source: BPHS Ch.25 (విశేష లగ్న అధ్యాయం)
# హోరా లగ్నం: జన్మ సమయం నుండి గడిచిన ghatis × 30° — సింహం/కర్కాటకం నుండి
# భావ లగ్నం: జన్మ నుండి గడిచిన ghatis × 30° — మేషం నుండి
# ఘటి లగ్నం: జన్మ నుండి గడిచిన ghatis × 30° — మేషం నుండి (వేరే formula)
# ═══════════════════════════════════════════════════════════
def calc_vishesa_lagnas(sid, ls, lr, bd, sc, tz=5.5):
    """
    ADD-2: హోరా లగ్నం, భావ లగ్నం, ఘటి లగ్నం — BPHS Ch.25
    Returns dict with hora_lagna, bhava_lagna, ghati_lagna
    """
    sr = sc.get("sunrise_local", bd.replace(hour=6,minute=0,second=0))

    # జన్మ సమయం నుండి సూర్యోదయం వరకు గడిచిన seconds
    elapsed_sec = (bd - sr).total_seconds()
    if elapsed_sec < 0:
        # రాత్రి జన్మ — మునుపటి రోజు సూర్యోదయం నుండి లెక్క
        prev_sr = sr - datetime.timedelta(days=1)
        elapsed_sec = (bd - prev_sr).total_seconds()

    # 1 ghati = 24 minutes = 1440 seconds
    GHATI_SEC = 1440.0
    elapsed_ghatis = elapsed_sec / GHATI_SEC

    # హోరా లగ్నం: BPHS — సూర్యోదయ సమయంలో సూర్యుని రాశి నుండి
    # ప్రతి ghati కి 30° → ప్రతి రాశి = 1 ghati
    # జన్మ లగ్న రాశి నుండి elapsed ghatis × 30° కలపాలి
    sun_rashi = int(sid["sun"] // 30) + 1
    # సింహం (5) లేదా కర్కాటకం (4) ప్రారంభం — BPHS: సూర్యుని హోర నుండి
    # Simplified: HL = (sun_lon + elapsed_ghatis * 30) % 360
    hora_lon = (sid["sun"] + elapsed_ghatis * 30.0) % 360
    hr, hd, hni, hpada = degrees_to_rashi(hora_lon)

    # భావ లగ్నం: BPHS — మేషం (0°) నుండి ప్రారంభం
    # BL = (elapsed_ghatis * 30) % 360
    bhava_lon = (elapsed_ghatis * 30.0) % 360
    br, bd2, bni, bpada = degrees_to_rashi(bhava_lon)

    # ఘటి లగ్నం: BPHS — జన్మ లగ్నం నుండి
    # GL = (lagna_lon + elapsed_ghatis * 30) % 360
    ghati_lon = (ls + elapsed_ghatis * 30.0) % 360
    gr, gd, gni, gpada = degrees_to_rashi(ghati_lon)

    return {
        "hora_lagna": {
            "longitude": round(hora_lon, 4),
            "rashi_num": hr,
            "rashi_te": RASHI_TE.get(hr, "?"),
            "degrees": round(hd, 4),
            "nakshatra": NAKSHATRA_TE[hni] if hni < 27 else "?",
            "pada": hpada,
            "source": "BPHS Ch.25"
        },
        "bhava_lagna": {
            "longitude": round(bhava_lon, 4),
            "rashi_num": br,
            "rashi_te": RASHI_TE.get(br, "?"),
            "degrees": round(bd2, 4),
            "nakshatra": NAKSHATRA_TE[bni] if bni < 27 else "?",
            "pada": bpada,
            "source": "BPHS Ch.25"
        },
        "ghati_lagna": {
            "longitude": round(ghati_lon, 4),
            "rashi_num": gr,
            "rashi_te": RASHI_TE.get(gr, "?"),
            "degrees": round(gd, 4),
            "nakshatra": NAKSHATRA_TE[gni] if gni < 27 else "?",
            "pada": gpada,
            "source": "BPHS Ch.25"
        },
        "elapsed_ghatis": round(elapsed_ghatis, 4)
    }

# ═══════════════════════════════════════════════════════════
# ADD-3: తాత్కాలిక మైత్రి + పంచధా మైత్రి
# Source: Brihat Jataka Ch.2 Sl.18 + BPHS
# నైసర్గిక + తాత్కాలిక కలిపి 5-fold friendship నిర్ణయించడం
# ═══════════════════════════════════════════════════════════
def calc_tatkalika_maitri(d1p):
    """
    ADD-3: తాత్కాలిక మైత్రి — Brihat Jataka Ch.2 Sl.18
    గ్రహాలు 2,3,4,10,11,12 స్థానాల్లో ఉంటే తాత్కాలిక మిత్రులు
    మిగిలిన స్థానాల్లో తాత్కాలిక శత్రువులు
    Returns: dict of planet → tatkalika friends/enemies
    """
    planets = ["sun","moon","mars","mercury","jupiter","venus","saturn"]
    result = {}
    for p1 in planets:
        b1 = d1p.get(p1, {}).get("bhava", 0)
        tatka_friends = []
        tatka_enemies = []
        for p2 in planets:
            if p2 == p1: continue
            b2 = d1p.get(p2, {}).get("bhava", 0)
            if b1 == 0 or b2 == 0: continue
            # p1 నుండి p2 యొక్క bhava distance
            dist = ((b2 - b1) % 12) + 1
            if dist in TATKALIKA_FRIEND_BHAVAS:
                tatka_friends.append(p2)
            else:
                tatka_enemies.append(p2)
        result[p1] = {"tatkalika_friends": tatka_friends, "tatkalika_enemies": tatka_enemies}
    return result

def calc_panchadha_maitri(d1p):
    """
    ADD-3: పంచధా మైత్రి — Brihat Jataka Ch.2 Sl.18 + BPHS
    నైసర్గిక + తాత్కాలిక కలిపి 5 స్థాయిలు:
    Adhi Mitra (నైసర్గిక మిత్రుడు + తాత్కాలిక మిత్రుడు)
    Mitra     (నైసర్గిక మిత్రుడు + తాత్కాలిక శత్రువు) లేదా (న్యూట్రల్ + తాత్కాలిక మిత్రుడు)
    Sama      (న్యూట్రల్ + తాత్కాలిక న్యూట్రల్)
    Shatru    (నైసర్గిక శత్రువు + తాత్కాలిక మిత్రుడు) లేదా (న్యూట్రల్ + తాత్కాలిక శత్రువు)
    Adhi Shatru (నైసర్గిక శత్రువు + తాత్కాలిక శత్రువు)
    Returns: dict of planet → dict of other_planet → panchadha_level
    """
    tatka = calc_tatkalika_maitri(d1p)
    planets = ["sun","moon","mars","mercury","jupiter","venus","saturn"]
    result = {}
    for p1 in planets:
        result[p1] = {}
        nat_fr = NATURAL_FRIENDS.get(p1, set())
        nat_en = NATURAL_ENEMIES.get(p1, set())
        tk_fr  = set(tatka.get(p1, {}).get("tatkalika_friends", []))
        for p2 in planets:
            if p2 == p1: continue
            nat = "mitra" if p2 in nat_fr else "shatru" if p2 in nat_en else "sama"
            tatk = "mitra" if p2 in tk_fr else "shatru"
            if nat=="mitra" and tatk=="mitra":   level="Adhi Mitra (అధి మిత్ర)"
            elif nat=="mitra" and tatk=="shatru": level="Mitra (మిత్ర)"
            elif nat=="sama"  and tatk=="mitra":  level="Mitra (మిత్ర)"
            elif nat=="sama"  and tatk=="shatru": level="Shatru (శత్రు)"
            elif nat=="shatru" and tatk=="mitra": level="Shatru (శత్రు)"
            else:                                  level="Adhi Shatru (అధి శత్రు)"
            result[p1][p2] = {"nat_maitri":nat,"tatkalika":tatk,"panchadha":level}
    return result

# ═══════════════════════════════════════════════════════════
# ADD-4: పిండాయుర్దాయ పూర్తి calculation
# Source: Brihat Jataka Ch.7 Sl.1-4
# గ్రహం యొక్క ఉచ్చ degree నుండి proportional సంవత్సరాలు
# ═══════════════════════════════════════════════════════════
def calc_pindayu(d1p, sid, lr):
    """
    ADD-4: పిండాయుర్దాయ — Brihat Jataka Ch.7 Sl.1-4
    Maximum years: Sun=19, Moon=25, Mars=15, Mercury=12,
                   Jupiter=15, Venus=21, Saturn=20
    Reduction: 7-12th house (malefic loses full/half/third etc)
    Lagna also contributes years (navamsha based)
    Combust exception: Venus/Saturn lose nothing (Sl.2)
    Returns: {"total_years": float, "planet_years": dict, "lagna_years": float}
    """
    MAX_YEARS = {"sun":19.0,"moon":25.0,"mars":15.0,"mercury":12.0,
                 "jupiter":15.0,"venus":21.0,"saturn":20.0}
    # House 7-12 reduction fractions per Brihat Jataka Ch.7 Sl.3
    # malefic: h12=full, h11=1/2, h10=1/3, h9=1/4, h8=1/5, h7=1/6
    # benefic: h12=1/2, h11=1/4, h10=1/6, h9=1/8, h8=1/10, h7=1/12
    MAL_REDUCE = {12:1.0, 11:0.5, 10:1/3.0, 9:0.25, 8:0.2, 7:1/6.0}
    BEN_REDUCE = {12:0.5, 11:0.25, 10:1/6.0, 9:0.125, 8:0.1, 7:1/12.0}
    malefics = {"sun","mars","saturn","rahu","ketu"}
    benefics = {"jupiter","venus","mercury","moon"}

    planet_years = {}
    total = 0.0

    for key, max_yr in MAX_YEARS.items():
        p = d1p.get(key, {})
        rashi_num = p.get("rashi_num", 1)
        deg = p.get("degrees", 0.0)
        bhava = p.get("bhava", 1)
        is_combust = p.get("is_combust", False)
        strength = p.get("strength", "సాధారణం")

        # Step 1: uccha/neecha proportion (Sl.1-2)
        uccha_lon = UCCHA_LON.get(key, 0.0)
        neecha_lon = (uccha_lon + 180.0) % 360.0
        planet_lon = sid.get(key, 0.0)
        dist_from_uccha = abs(planet_lon - uccha_lon)
        if dist_from_uccha > 180: dist_from_uccha = 360 - dist_from_uccha
        # Proportion: 0° from uccha = max, 180° from uccha = max/2
        proportion = 1.0 - (dist_from_uccha / 360.0)
        proportion = max(0.5, min(1.0, proportion))
        yr = max_yr * proportion

        # Step 2: Inimical sign — loses 1/3 (Sl.2, except retrograde)
        is_retro = p.get("is_retrograde", False)
        if not is_retro:
            nat_fr = NATURAL_FRIENDS.get(key, set())
            nat_en = NATURAL_ENEMIES.get(key, set())
            rashi_lord = BHAVA_LORDS.get(rashi_num, "sun")
            if rashi_lord in nat_en and rashi_lord not in nat_fr:
                yr = yr * (2.0/3.0)

        # Step 3: Combust — loses half, except Venus/Saturn (Sl.2)
        if is_combust and key not in ("venus","saturn"):
            yr = yr * 0.5

        # Step 4: House 7-12 reduction (Sl.3)
        # Only strongest planet in house applies
        if bhava in MAL_REDUCE:
            if key in malefics:
                reduce_frac = MAL_REDUCE[bhava]
            else:
                reduce_frac = BEN_REDUCE[bhava]
            yr = yr * (1.0 - reduce_frac)

        planet_years[key] = round(yr, 4)
        total += yr

    # Lagna contribution (Sl.1-2): navamshas elapsed × 1 year
    # lagna degrees → navamsha count
    from_data = d1p  # use for reference
    lagna_lon_deg = 0.0
    # We need ls (lagna sidereal longitude) — passed via d1p lagna
    # Use rashi + degrees approximation
    lr_deg = (lr - 1) * 30.0  # start of lagna rashi
    lagna_years = round(lr_deg / (360.0/108.0), 4)  # navamshas elapsed

    total += lagna_years

    return {
        "total_years": round(total, 2),
        "planet_years": planet_years,
        "lagna_years": lagna_years,
        "source": "Brihat Jataka Ch.7 Sl.1-4"
    }

# ═══════════════════════════════════════════════════════════
# ADD-5: కాల సర్ప యోగం detection
# Source: Brihat Jataka Ch.12 (Sarpa yoga / Nabhasa yogas)
# Rahu-Ketu axis మధ్య అన్ని గ్రహాలు ఉన్నప్పుడు Kala Sarpa
# ═══════════════════════════════════════════════════════════
def calc_kala_sarpa(sid):
    """
    ADD-5: కాల సర్ప యోగం — Brihat Jataka Ch.12 Sarpa yoga
    అన్ని గ్రహాలు Rahu → Ketu మధ్య ఉంటే: Kala Sarpa
    అన్ని గ్రహాలు Ketu → Rahu మధ్య ఉంటే: Kala Amrita (అమృత)
    ఏదైనా గ్రహం బయట ఉంటే: లేదు
    Returns: {"present": bool, "type": str, "planets_outside": list, "source": str}
    """
    rahu_lon = sid.get("rahu", 0.0)
    ketu_lon = sid.get("ketu", 0.0)
    main_planets = ["sun","moon","mars","mercury","jupiter","venus","saturn"]

    # Rahu నుండి Ketu వరకు clockwise (Rahu → Rahu+180 = Ketu)
    # గ్రహం rahu నుండి ketu వైపు 180° arc లో ఉంటే Kala Sarpa arc
    def in_rahu_to_ketu(lon, rahu, ketu):
        """rahu నుండి ketu వరకు clockwise arc లో ఉందా?"""
        # Normalize
        arc = (ketu - rahu) % 360
        dist = (lon - rahu) % 360
        return dist <= arc

    in_rk = []  # Rahu→Ketu arc లో
    in_kr = []  # Ketu→Rahu arc లో
    outside = []

    for p in main_planets:
        lon = sid.get(p, 0.0)
        if in_rahu_to_ketu(lon, rahu_lon, ketu_lon):
            in_rk.append(p)
        else:
            in_kr.append(p)

    if len(in_rk) == len(main_planets):
        # అన్నీ Rahu→Ketu arc లో → Kala Sarpa
        return {"present": True, "type": "Kala Sarpa (కాల సర్ప — అశుభ)", "planets_outside": [], "source": "Brihat Jataka Ch.12"}
    elif len(in_kr) == len(main_planets):
        # అన్నీ Ketu→Rahu arc లో → Kala Amrita
        return {"present": True, "type": "Kala Amrita (కాల అమృత — శుభ)", "planets_outside": [], "source": "Brihat Jataka Ch.12"}
    else:
        out = [PLANET_TE[p] for p in main_planets if p not in in_rk and p not in in_kr]
        return {"present": False, "type": "లేదు", "planets_outside": [], "source": "Brihat Jataka Ch.12"}

# ═══════════════════════════════════════════════════════════
# ADD-6: జైమిని చర కారకాలు — Atmakaraka etc
# Source: BPHS Jaimini section
# Degrees (0-30° ignoring rashi) బట్టి rank చేయాలి
# Highest degree = Atmakaraka, next = Amatyakaraka etc
# ═══════════════════════════════════════════════════════════
def calc_chara_karakas(d1p):
    """
    ADD-6: జైమిని చర కారకాలు — BPHS Jaimini
    7 గ్రహాలు (Rahu/Ketu తప్ప) degree బట్టి rank
    Rahu కి: 30° - rahu_degree (reverse)
    1. Atmakaraka (AK)    — ఆత్మ కారకుడు
    2. Amatyakaraka (AmK) — మంత్రి కారకుడు
    3. Bhratrukaraka (BK) — సోదర కారకుడు
    4. Matrukaraka (MK)   — మాత కారకుడు
    5. Putrakaraka (PK)   — సంతాన కారకుడు
    6. Gnatikaraka (GK)   — బంధు కారకుడు
    7. Darakaraka (DK)    — దార కారకుడు
    """
    KARAKA_NAMES = {
        0: "Atmakaraka (ఆత్మ కారకుడు — AK)",
        1: "Amatyakaraka (అమాత్య కారకుడు — AmK)",
        2: "Bhratrukaraka (భ్రాతృ కారకుడు — BK)",
        3: "Matrukaraka (మాతృ కారకుడు — MK)",
        4: "Putrakaraka (పుత్ర కారకుడు — PK)",
        5: "Gnatikaraka (జ్ఞాతి కారకుడు — GK)",
        6: "Darakaraka (దార కారకుడు — DK)"
    }
    planets = ["sun","moon","mars","mercury","jupiter","venus","saturn"]
    deg_map = {}
    for p in planets:
        raw_deg = d1p.get(p, {}).get("degrees", 0.0)
        # Rahu: 30 - degrees (reverse)
        if p == "rahu":
            deg_map[p] = 30.0 - raw_deg
        else:
            deg_map[p] = raw_deg

    # Degree బట్టి descending sort
    sorted_planets = sorted(deg_map.keys(), key=lambda x: deg_map[x], reverse=True)
    result = {}
    for i, p in enumerate(sorted_planets[:7]):
        result[p] = {
            "planet_te": PLANET_TE[p],
            "degrees": round(deg_map[p], 4),
            "karaka_num": i+1,
            "karaka_name": KARAKA_NAMES[i],
            "karaka_short": ["AK","AmK","BK","MK","PK","GK","DK"][i]
        }
    # Atmakaraka ప్రత్యేకంగా
    ak_planet = sorted_planets[0] if sorted_planets else "sun"
    return {
        "karakas": result,
        "atmakaraka": ak_planet,
        "atmakaraka_te": PLANET_TE.get(ak_planet, "?"),
        "source": "BPHS Jaimini section"
    }

# ═══════════════════════════════════════════════════════════
# ADD-7: గ్రహ అవస్థ (Graha Avastha)
# Source: BPHS Ch.45 — degree-based 5 states
# 0-6° = బాల, 6-12° = కుమార, 12-18° = యువ,
# 18-24° = వృద్ధ, 24-30° = మృత
# ═══════════════════════════════════════════════════════════
def calc_graha_avastha(d1p):
    """
    ADD-7: గ్రహ అవస్థ — BPHS Ch.45
    ప్రతి రాశిలో degree బట్టి గ్రహ స్థితి
    బాల: అల్ప ఫలం | కుమార: మధ్యమం | యువ: పూర్ణ ఫలం
    వృద్ధ: క్షీణ ఫలం | మృత: శూన్య ఫలం
    """
    AVASTHA = [
        (6,  "బాల (0-6°)", "అల్ప ఫలం — బలహీనం"),
        (12, "కుమార (6-12°)", "మధ్యమ ఫలం"),
        (18, "యువ (12-18°)", "పూర్ణ ఫలం — బలిష్టం"),
        (24, "వృద్ధ (18-24°)", "క్షీణ ఫలం"),
        (30, "మృత (24-30°)", "శూన్య ఫలం — నిర్వీర్యం")
    ]
    result = {}
    for key in PLANET_TE:
        deg = d1p.get(key, {}).get("degrees", 0.0)
        avastha_name = "యువ (12-18°)"
        avastha_phalam = "పూర్ణ ఫలం — బలిష్టం"
        avastha_num = 3
        for i,(threshold, name, phalam) in enumerate(AVASTHA):
            if deg < threshold:
                avastha_name = name
                avastha_phalam = phalam
                avastha_num = i+1
                break
        result[key] = {
            "planet_te": PLANET_TE[key],
            "degrees_in_rashi": round(deg, 4),
            "avastha_num": avastha_num,
            "avastha": avastha_name,
            "phalam": avastha_phalam,
            "source": "BPHS Ch.45"
        }
    return result

# ═══════════════════════════════════════════════════════════
# ADD-8: గోచర (Transit) current positions
# Source: Brihat Jataka Ch.22 Sl.6 — transit timing rules
# Sun/Mars: sign entry లో ఫలితాలు
# Jupiter/Venus: sign middle లో ఫలితాలు
# Saturn/Moon: sign exit లో ఫలితాలు
# Mercury: throughout stay లో ఫలితాలు
# ═══════════════════════════════════════════════════════════
def calc_gochara(tz=5.5):
    """
    ADD-8: గోచర వర్తమాన స్థానాలు — Brihat Jataka Ch.22 Sl.6
    ప్రస్తుత తేదీకి గ్రహ స్థానాలు + transit timing stage
    Returns: dict with current positions + timing stage per planet
    """
    today = datetime.datetime.now()
    dob_str = today.strftime("%d/%m/%Y")
    tob_str = today.strftime("%H:%M:%S")

    try:
        trop, obs, jd, T, spd, mlon, lat_p, tlon = get_positions(dob_str, tob_str, 17.385, 78.4867, tz)
        ayan = get_lahiri(jd)
        sid_now = {k: (v - ayan) % 360 for k, v in trop.items()}
    except Exception as e:
        return {"error": str(e), "source": "Brihat Jataka Ch.22 Sl.6"}

    # Brihat Jataka Ch.22 Sl.6: transit result timing per planet
    # Sun/Mars: entry (0-10°), Jupiter/Venus: middle (10-20°), Saturn/Moon: exit (20-30°)
    # Mercury: throughout
    TRANSIT_STAGE = {
        "sun":     ("entry",   0, 10),
        "mars":    ("entry",   0, 10),
        "jupiter": ("middle", 10, 20),
        "venus":   ("middle", 10, 20),
        "saturn":  ("exit",   20, 30),
        "moon":    ("exit",   20, 30),
        "mercury": ("throughout", 0, 30),
        "rahu":    ("throughout", 0, 30),
        "ketu":    ("throughout", 0, 30),
    }

    result = {}
    for key in PLANET_TE:
        lon = sid_now.get(key, 0.0)
        r, d, ni, pada = degrees_to_rashi(lon)
        stage_info = TRANSIT_STAGE.get(key, ("throughout", 0, 30))
        stage_name, deg_start, deg_end = stage_info
        # ఈ గ్రహం తన ఫలిత దశలో ఉందా?
        in_result_zone = (deg_start <= d < deg_end)
        result[key] = {
            "planet_te": PLANET_TE[key],
            "current_lon": round(lon, 4),
            "current_rashi_num": r,
            "current_rashi_te": RASHI_TE.get(r, "?"),
            "current_degrees": round(d, 4),
            "current_nakshatra": NAKSHATRA_TE[ni] if ni < 27 else "?",
            "current_pada": pada,
            "transit_stage": stage_name,
            "result_zone": f"{deg_start}-{deg_end}°",
            "in_result_zone": in_result_zone,
            "result_note": f"ఫలితాలు {stage_name} లో — {'✅ ఇప్పుడు active' if in_result_zone else '⏳ వేచి ఉంది'}"
        }
    return {
        "date": today.strftime("%d/%m/%Y %H:%M"),
        "planets": result,
        "source": "Brihat Jataka Ch.22 Sl.6"
    }

# ═══════════════════════════════════════════════════════════
# STEP-1: అధిపత్య శుభ/పాప per planet per lagna
# Source: Jataka Martanda PDFs (89-95, 215-217, 212-214)
# ═══════════════════════════════════════════════════════════
def calc_adhipatya_shubha_papa(d1p, lagna_rashi_te):
    """
    లగ్నం బట్టి ప్రతి గ్రహానికి శుభ/పాప/సమ నిర్ణయం
    రాహు/కేతులకు ఆధిపత్యం లేదు — వారికి 'వర్తించదు' ఇస్తాం
    """
    lookup = LAGNA_SHUBHA_PAPA_LOOKUP.get(lagna_rashi_te, {})
    shubha_list = lookup.get("శుభులు", [])
    papa_list   = lookup.get("పాపులు", [])
    result = {}
    for key in PLANET_TE:
        if key in ("rahu","ketu"):
            result[key] = {"is_adhipatya_shubha":False,"is_adhipatya_papa":False,"adhipatya_note":"వర్తించదు (ఆధిపత్యం లేదు)"}
            continue
        short = PLANET_TE_SHORT.get(key,"")
        if short in shubha_list:
            result[key] = {"is_adhipatya_shubha":True,"is_adhipatya_papa":False,"adhipatya_note":"శుభుడు"}
        elif short in papa_list:
            result[key] = {"is_adhipatya_shubha":False,"is_adhipatya_papa":True,"adhipatya_note":"పాపి"}
        else:
            result[key] = {"is_adhipatya_shubha":False,"is_adhipatya_papa":False,"adhipatya_note":"సముడు"}
    return result

# ═══════════════════════════════════════════════════════════
# STEP-2: ఆరూఢ లగ్నం calculation
# Source: Rajayogadyayamu PDF pages 7-8
# ═══════════════════════════════════════════════════════════
def calc_arudha_lagna(lagna_rashi_num, lagna_lord_en, d1p):
    """
    PDF: ఆరూఢ లగ్నము = లగ్నాధిపతి ఉన్న రాశిని లగ్నం నుండి లెక్కించు
    Formula: lord_bhava నుండి అదే దూరం ముందుకు వేయాలి
    Arudha = lord_bhava + (lord_bhava - lagna) = 2*lord_bhava - lagna
    Exception: if result = lagna → 10th from lagna; if result = 7th → 4th from lagna
    """
    lord_bhava = d1p.get(lagna_lord_en, {}).get("bhava", 1)
    raw = ((2 * lord_bhava - lagna_rashi_num) % 12)
    arudha_bhava = raw if raw != 0 else 12
    # Exception rules (BPHS Jaimini)
    if arudha_bhava == 1: arudha_bhava = 10
    elif arudha_bhava == 7: arudha_bhava = 4
    # Convert bhava to rashi
    arudha_rashi = ((lagna_rashi_num + arudha_bhava - 2) % 12) + 1
    r,d,ni,pada = degrees_to_rashi((arudha_rashi-1)*30.0)
    return {
        "arudha_lagna_bhava": arudha_bhava,
        "arudha_lagna_rashi": arudha_rashi,
        "arudha_lagna_te": RASHI_TE.get(arudha_rashi,"?"),
        "source": "Rajayogadyayamu PDF pages 7-8"
    }

# ═══════════════════════════════════════════════════════════
# STEP-3: భావ బల (స్థాన + అధిపతి + కారక)
# Source: Yogas PDF pages 110-115
# PDF: "తనుభావమునకు స్థానము, స్థానాధిపతి, కారకుడు మూడు బలముగా నుండవలెను"
# ═══════════════════════════════════════════════════════════
def calc_bhava_bala(d1p, shad, lr):
    """
    ప్రతి భావానికి 3-factor strength:
    1. స్థాన బలం: శుభ/ఉచ్చ గ్రహం ఉంటే strong
    2. అధిపతి బలం: shadbala.is_strong
    3. కారక బలం: shadbala.is_strong of karaka
    """
    benf = {"jupiter","venus","mercury","moon"}
    mal  = {"sun","mars","saturn","rahu","ketu"}
    result = {}
    for bhava_num in range(1,13):
        # స్థాన బలం: ఈ భావంలో ఉన్న గ్రహాలు
        planets_in_bhava = [k for k,p in d1p.items() if p.get("bhava")==bhava_num]
        strong_in_bhava  = [k for k in planets_in_bhava if d1p[k].get("strength") in ["ఉచ్చం","స్వరాశి","మూల త్రికోణం"]]
        malefic_in_bhava = [k for k in planets_in_bhava if k in mal and d1p[k].get("strength") in ["నీచం","సాధారణం"]]
        if strong_in_bhava: sthana="బలంగా"
        elif malefic_in_bhava and not planets_in_bhava.__len__()>len(malefic_in_bhava): sthana="బలహీనంగా"
        elif not planets_in_bhava: sthana="ఖాళీ (తటస్థం)"
        else: sthana="మధ్యమంగా"

        # అధిపతి బలం
        bhava_lord_rashi = ((lr + bhava_num - 2) % 12) + 1
        adhipati_en = BHAVA_LORDS.get(bhava_lord_rashi,"sun")
        adhipati_strong = shad.get(adhipati_en,{}).get("is_strong",False) if adhipati_en not in ("rahu","ketu") else False
        adhipati_str = "బలంగా" if adhipati_strong else "బలహీనంగా"

        # కారక బలం
        karaka_en = BHAVA_KARAKA.get(bhava_num,"sun")
        karaka_strong = shad.get(karaka_en,{}).get("is_strong",False) if karaka_en not in ("rahu","ketu") else False
        karaka_str = "బలంగా" if karaka_strong else "బలహీనంగా"

        # Overall
        strong_count = sum([
            sthana in ("బలంగా","ఖాళీ (తటస్థం)"),
            adhipati_strong,
            karaka_strong
        ])
        overall = "ఉత్తమం (మూడూ బలం)" if strong_count==3 else "మధ్యమం" if strong_count==2 else "సాధారణం" if strong_count==1 else "బలహీనం"

        # Raman Factor (f): Lord from Moon
        # Source: B.V. Raman "How to Judge a Horoscope Vol 2"
        # ఆ bhava lord చంద్రుడి నుండి ఏ స్థానంలో ఉన్నాడు
        moon_bhava = d1p.get("moon",{}).get("bhava",1)
        adhipati_bhava = d1p.get(adhipati_en,{}).get("bhava",0)
        lord_from_moon = ((adhipati_bhava - moon_bhava) % 12) + 1 if adhipati_bhava else 0

        result[bhava_num] = {
            "bhava_num": bhava_num,
            "adhipati_en": adhipati_en,
            "adhipati_te": PLANET_TE.get(adhipati_en,"?"),
            "adhipati_bhava": adhipati_bhava,
            "lord_from_moon": lord_from_moon,
            "karaka_en": karaka_en,
            "karaka_te": PLANET_TE.get(karaka_en,"?"),
            "sthana_strength": sthana,
            "adhipati_strength": adhipati_str,
            "karaka_strength": karaka_str,
            "strong_factor_count": strong_count,
            "overall": overall,
            "note": "స్థానము, స్థానాధిపతి, కారకుడు మూడూ బలముగా నుండిన ఆ భావము అభివృద్ధిగా నుండును"
        }
    return result

# ═══════════════════════════════════════════════════════════
# FIX-25: Yoga Net Strength — B.V. Raman +/- unit system
# Source: "Three Hundred Important Combinations" (1947)
# Yogakaraka = benefic lord +1 | malefic lord -1
# With/aspected by benefic lord +1 | malefic lord -1
# Exaltation/friendly sign +1 | debilitation/inimical -1
# ═══════════════════════════════════════════════════════════
def calc_yoga_net_strength(yoga_planets, d1p, asp):
    score = 0
    for p in yoga_planets:
        if p not in d1p: continue
        adh = d1p[p].get("adhipatya_note","సముడు")
        if adh == "శుభుడు": score += 1
        elif adh == "పాపుడు": score -= 1
        st = d1p[p].get("strength","సాధారణం")
        if st in ("ఉచ్చం","స్వరాశి","మూల త్రికోణం"): score += 1
        elif st == "నీచం": score -= 1
        p_bhava = d1p[p].get("bhava",0)
        for p2,pd2 in d1p.items():
            if p2 == p: continue
            if pd2.get("bhava") == p_bhava:
                adh2 = pd2.get("adhipatya_note","సముడు")
                if adh2 == "శుభుడు": score += 1
                elif adh2 == "పాపుడు": score -= 1
        for asp_info in asp.get(p,{}).get("aspected_by",[]):
            asp_p = asp_info.get("planet_en","")
            if asp_p and asp_p in d1p:
                adh3 = d1p[asp_p].get("adhipatya_note","సముడు")
                if adh3 == "శుభుడు": score += 1
                elif adh3 == "పాపుడు": score -= 1
    if score >= 3: return score, "MAXIMUM"
    elif score >= 1: return score, "MODERATE"
    elif score == 0: return score, "NOMINAL"
    else: return score, "CANCELLED"

# ═══════════════════════════════════════════════════════════
# STEP-4: రాజ యోగ flags
# Source: Rajayogadyayamu PDF
# ═══════════════════════════════════════════════════════════
def check_pancha_graha_malika(d1p, lagna_rashi_num, arudha_rashi_num):
    """
    PDF: ఐదు రాశులలో వరుసగా గ్రహములుండుట = పంచగ్రహమాలిక యోగము
    Check from lagna and arudha lagna
    రాహు/కేతులు లెక్కలోకి తీసుకోకూడదు
    """
    main_p = [k for k in d1p if k not in ("rahu","ketu")]
    for base_name, base_rashi in [("lagna", lagna_rashi_num), ("arudha_lagna", arudha_rashi_num)]:
        count = 0
        for i in range(12):
            bhava = ((base_rashi - 1 + i) % 12) + 1
            if any(d1p[p].get("bhava")==bhava for p in main_p):
                count += 1
                if count >= 5:
                    return True, base_name
            else:
                count = 0
    return False, None

def check_adhi_yoga(moon_bhava, d1p):
    """
    PDF: చంద్రుడున్న రాశి లాగాయతు 6,7,8 స్థానములలో శుభగ్రహములున్న = అధియోగము
    1 శుభం = కీర్తి, 2 శుభాలు = రాజయోగం, 3 శుభాలు = మహారాజు
    """
    adhi_bhavas = {((moon_bhava+4)%12)+1, ((moon_bhava+5)%12)+1, ((moon_bhava+6)%12)+1}
    benf = {"jupiter","venus","mercury","moon"}
    count = sum(1 for k,p in d1p.items() if k in benf and p.get("bhava") in adhi_bhavas
                and p.get("strength") in ["ఉచ్చం","స్వరాశి","మూల త్రికోణం"])
    if count >= 3: tag="మహారాజు యోగం"
    elif count == 2: tag="రాజయోగం"
    elif count == 1: tag="కీర్తి యోగం"
    else: tag="లేదు"
    return count, tag

# ═══════════════════════════════════════════════════════════
# STEP-8: ఆరూఢ లగ్న రాజ యోగ
# Source: Rajayogadyayamu PDF pages 7-8
# ═══════════════════════════════════════════════════════════
def check_arudha_raja_yoga(arudha_bhava, d1p):
    """
    PDF: ఆరూఢలగ్నమందు ఎన్ని శుభగ్రహములు బలముగా నుండునో రాజయోగము అంత విశేషముగా నుండును
    """
    count = sum(1 for k,p in d1p.items()
                if p.get("bhava")==arudha_bhava
                and p.get("strength") in ["ఉచ్చం","స్వరాశి","మూల త్రికోణం"])
    if count >= 3: tag="ఉత్తమ రాజయోగం"
    elif count == 2: tag="మధ్యమ రాజయోగం"
    elif count == 1: tag="సామాన్య రాజయోగం"
    else: tag="రాజయోగం లేదు"
    return count, tag

# ═══════════════════════════════════════════════════════════
# FIX-29: Yoga Timing — దేని దశలో yoga manifest అవుతుంది
# Source: B.V. Raman "300 Combinations"
# "The planet whose shadbala strength is more will fulfil
#  the larger part of the yoga results in his Dasa"
# Brihat Jataka Ch.8: yoga results come in dasha of strongest yogakaraka
# ═══════════════════════════════════════════════════════════
def calc_yoga_timing(yoga_planets, d1p, shad, dasha_timeline):
    """
    Yoga ఫలాలు ఏ దశలో వస్తాయో నిర్ణయించడం
    Strongest yogakaraka dasha లో primary manifestation
    """
    if not yoga_planets:
        return {"primary_dasha": None, "secondary_dasha": None, "note": "yoga planets లేదు"}
    planet_scores = {}
    for p in yoga_planets:
        if p not in d1p: continue
        shad_data = shad.get(p, {})
        virupa = shad_data.get("total_virupa", 0)
        is_strong = shad_data.get("is_strong", False)
        st = d1p[p].get("strength", "సాధారణం")
        score = virupa
        if st == "ఉచ్చం": score *= 1.3
        elif st == "స్వరాశి": score *= 1.1
        elif st == "నీచం": score *= 0.5
        if is_strong: score *= 1.1
        planet_scores[p] = round(score, 2)
    if not planet_scores:
        return {"primary_dasha": None, "secondary_dasha": None, "note": "shadbala data లేదు"}
    sorted_p = sorted(planet_scores, key=lambda x: planet_scores[x], reverse=True)
    primary = sorted_p[0]
    secondary = sorted_p[1] if len(sorted_p) > 1 else None
    # Dasha timeline లో ఆ planet dasha dates తీసుకోవడం
    primary_dates = next(({"start": d["start_date"], "end": d["end_date"]}
                          for d in dasha_timeline if d["planet_en"] == primary), None)
    secondary_dates = next(({"start": d["start_date"], "end": d["end_date"]}
                            for d in dasha_timeline if d["planet_en"] == secondary), None) if secondary else None
    return {
        "primary_planet_en": primary,
        "primary_planet_te": PLANET_TE.get(primary, "?"),
        "primary_shadbala_score": planet_scores[primary],
        "primary_dasha_dates": primary_dates,
        "secondary_planet_en": secondary,
        "secondary_planet_te": PLANET_TE.get(secondary, "?") if secondary else None,
        "secondary_shadbala_score": planet_scores.get(secondary, 0),
        "secondary_dasha_dates": secondary_dates,
        "all_scores": {PLANET_TE.get(p,"?"): s for p,s in planet_scores.items()},
        "note": "అత్యధిక shadbala గ్రహం దశలో yoga ఫలాలు అత్యధికంగా వస్తాయి (B.V. Raman + Brihat Jataka Ch.8)"
    }

# ═══════════════════════════════════════════════════════════
# FIX-27: విపరీత రాజ యోగ detection
# Source: B.V. Raman "300 Combinations" — Harsha/Sarala/Vimala yogas
# 6వ lord 6/8/12లో = Harsha | 8వ lord 6/8/12లో = Sarala | 12వ lord 6/8/12లో = Vimala
# Parashara: "sting తగ్గుతుంది — పూర్తిగా పోదు" (partial negative intact)
# ═══════════════════════════════════════════════════════════
def check_viparita_raja_yoga(d1p, lr):
    DUSTHANA = {6, 8, 12}
    VIPARITA_NAMES = {6:"Harsha (హర్ష)", 8:"Sarala (సారళ)", 12:"Vimala (విమల)"}
    result = {}
    for bh in DUSTHANA:
        bh_rashi = ((lr - 1 + bh - 1) % 12) + 1
        lord = BHAVA_LORDS.get(bh_rashi)
        if not lord or lord not in d1p: continue
        lord_bhava = d1p[lord].get("bhava", 0)
        if lord_bhava in DUSTHANA:
            result[bh] = {
                "yoga_name": VIPARITA_NAMES[bh],
                "lord_en": lord,
                "lord_te": PLANET_TE.get(lord,"?"),
                "lord_bhava": lord_bhava,
                "parashara_note": "దుష్ఫలాలు తగ్గుతాయి — పూర్తిగా రద్దు కావు (పరాశరుడు)",
                "practical_result": "శత్రు నాశనం, రుణ విముక్తి, అకస్మాత్ రక్షణ సాధ్యం"
            }
    present = len(result) > 0
    yogas = [v["yoga_name"] for v in result.values()]
    return present, result, yogas

# ═══════════════════════════════════════════════════════════
# STEP-9: భాగ్య + రాజ్య అధిపతి యోగ
# Source: Rajayogadyayamu PDF pages 1-2
# PDF: "భాగ్యరాజ్యాధిపతులు కలిసినచో రాజయోగము"
# ═══════════════════════════════════════════════════════════
def check_bhagya_rajya_yoga(d1p, lr, asp):
    """
    9వ + 10వ భావాధిపతులు కలిసినా లేదా చూసినా = రాజయోగం
    """
    bhagya_rashi = ((lr - 1 + 8) % 12) + 1   # 9th rashi from lagna
    rajya_rashi  = ((lr - 1 + 9) % 12) + 1   # 10th rashi from lagna
    bhagya_lord  = BHAVA_LORDS.get(bhagya_rashi,"jupiter")
    rajya_lord   = BHAVA_LORDS.get(rajya_rashi,"saturn")
    bl_bhava = d1p.get(bhagya_lord,{}).get("bhava",0)
    rl_bhava = d1p.get(rajya_lord,{}).get("bhava",0)
    # Conjunction
    if bl_bhava == rl_bhava and bl_bhava != 0:
        return True, "conjunction", bhagya_lord, rajya_lord
    # Aspect check
    if bhagya_lord in asp and rajya_lord in asp:
        bl_aspects_to = [a["planet_en"] for a in asp[bhagya_lord].get("aspects_to",[])]
        rl_aspects_to = [a["planet_en"] for a in asp[rajya_lord].get("aspects_to",[])]
        if rajya_lord in bl_aspects_to or bhagya_lord in rl_aspects_to:
            return True, "aspect", bhagya_lord, rajya_lord
    return False, None, bhagya_lord, rajya_lord

# ═══════════════════════════════════════════════════════════
# DB9 MAIN GENERATE FUNCTION
# DB8 generate_v21 లో ఏ logic మార్చలేదు
# 8 కొత్త fields మాత్రమే return dict కి add చేశాం
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
# 7-STEP DASHA PHALA ENGINE
# Sources: BPHS + Brihat Jataka + Uttara Kalamrita (Sloka 24½-25½)
# ═══════════════════════════════════════════════════════════
def calc_dasha_phala_engine(dl_planet, d1p, shad, panchadha, lr=8):
    """
    7-Step Dasha Phala Engine — Final Version (All Fixes Applied)
    Fix-1: BL = actual lagna-based rashi lord
    Fix-2: DL bhava position score
    Fix-3: DL adhipatya_note score
    Fix-4: రాహు/కేతు bhava rules differentiated
    Fix-5: స్వరాశి/ఉచ్చం = HIGH
    Sources: BPHS + Brihat Jataka + Uttara Kalamrita (Sloka 24½-25½)
    """
    RASHI_LORD = {1:"mars",2:"venus",3:"mercury",4:"moon",5:"sun",6:"mercury",
                  7:"venus",8:"mars",9:"jupiter",10:"saturn",11:"saturn",12:"jupiter"}
    dl_data = d1p.get(dl_planet, {})
    dl_bhava = dl_data.get("bhava", 0)
    dl_strength_str = dl_data.get("strength", "సాధారణం")
    dl_aarohi = dl_data.get("aarohi_avrohi", "")
    shad_data = shad.get(dl_planet, {})
    dl_is_strong = shad_data.get("is_strong", False)

    # STEP-1: DL బలం — Fix-5: స్వరాశి/ఉచ్చం/మూల త్రికోణం = HIGH
    if dl_strength_str in ("ఉచ్చం","స్వరాశి","మూల త్రికోణం") and dl_is_strong:
        dl_strength = "HIGH"
    elif dl_strength_str == "నీచం" and not dl_is_strong:
        dl_strength = "LOW"
    else:
        dl_strength = "MEDIUM"

    # STEP-2: DL భావం → PRIMARY phala domain (BPHS)
    bhava_karaka_map = {1:"sun",2:"jupiter",3:"mars",4:"moon",5:"jupiter",
                        6:"mars",7:"venus",8:"saturn",9:"sun",10:"mercury",
                        11:"jupiter",12:"saturn"}
    karaka_en = bhava_karaka_map.get(dl_bhava, "sun")
    karaka_te = PLANET_TE.get(karaka_en, "?")

    # STEP-3: భావాధిపతి (BL) — Fix-1: actual lagna-based rashi lord
    bhava_rashi = ((lr - 1 + dl_bhava - 1) % 12) + 1
    bhava_lord_en = RASHI_LORD.get(bhava_rashi, "sun")
    bhava_lord_data = d1p.get(bhava_lord_en, {})
    bhava_lord_shad = shad.get(bhava_lord_en, {})
    bl_maitri = panchadha.get(dl_planet, {}).get(bhava_lord_en, {}).get("panchadha", "Sama") if dl_planet not in ("rahu","ketu") else "Sama"
    if ("Mitra" in bl_maitri) and (bhava_lord_shad.get("is_strong") or "Aarohi" in bhava_lord_data.get("aarohi_avrohi","")):
        bl_quality = "శుభ"
    elif "Shatru" in bl_maitri:
        bl_quality = "అశుభ"
    else:
        bl_quality = "మిశ్రమ"

    # STEP-3B: DL adhipatya quality — Fix-3
    adh_note = dl_data.get("adhipatya_note", "సముడు")
    if adh_note == "శుభుడు": adh_score = 1.0
    elif adh_note == "సముడు": adh_score = 0.5
    else: adh_score = 0.0

    # STEP-4: రాశ్యధిపతి (RL) — Fix-1: actual rashi lord
    dl_rashi = dl_data.get("rashi_num", 1)
    rashi_lord_en = RASHI_LORD.get(dl_rashi, "sun")
    rashi_lord_data = d1p.get(rashi_lord_en, {})
    rl_bhava = rashi_lord_data.get("bhava", 0)
    rl_maitri = panchadha.get(dl_planet, {}).get(rashi_lord_en, {}).get("panchadha", "Sama") if dl_planet not in ("rahu","ketu") else "Sama"
    if rl_bhava in [1,4,5,7,9,10,11] and "Mitra" in rl_maitri:
        rl_quality = "శుభ"
    elif rl_bhava in [6,8,12]:
        rl_quality = "అశుభ"
    else:
        rl_quality = "మిశ్రమ"

    # STEP-5: Conjunction విశ్లేషణ (Uttara Kalamrita Sloka 24½-25½)
    conjunct_planets = [p for p,pd in d1p.items() if p != dl_planet and pd.get("bhava") == dl_bhava]
    benefics = ["jupiter","venus","mercury","moon"]
    conjunct_benefics = [p for p in conjunct_planets if p in benefics]
    conjunct_malefics = [p for p in conjunct_planets if p not in benefics and p not in ("rahu","ketu")]
    rk_conj = [p for p in conjunct_planets if p in ("rahu","ketu")]
    if conjunct_benefics and not conjunct_malefics:
        conjunction_effect = "శుభ ప్రభావం — మహాదశ ఫలాలు శుభం వైపు మొగ్గు"
    elif conjunct_malefics and not conjunct_benefics:
        conjunction_effect = "అశుభ ప్రభావం — మహాదశ ఫలాలు తీవ్రమైన అశుభం"
    elif conjunct_benefics and conjunct_malefics:
        conjunction_effect = "మిశ్రమ ప్రభావం — శుభ+అశుభ కలిస్తాయి"
    else:
        conjunction_effect = "conjunction లేదు — స్వతంత్ర ఫలాలు"
    karaka_map2 = {"jupiter":"జ్ఞానం/సంతానం/భాగ్యం","venus":"కామం/సంపద/సంబంధాలు",
                   "mars":"శక్తి/సోదరుడు/యుద్ధం","saturn":"కర్మ/దీర్ఘకాలిక ఫలం",
                   "mercury":"వాక్కు/విద్య/వ్యాపారం","moon":"మనస్సు/తల్లి/ప్రయాణం",
                   "sun":"ఆత్మ/తండ్రి/ప్రభుత్వం","rahu":"unexpected/నెట్వర్క్/విదేశం",
                   "ketu":"మోక్షం/ఆధ్యాత్మికత/వియోగం"}
    conjunct_karakas = [karaka_map2.get(p,"") for p in conjunct_planets]

    # STEP-6: Final Score — All Fixes
    score = 0.0

    # DL strength
    if dl_strength == "HIGH": score += 1.0
    elif dl_strength == "MEDIUM": score += 0.5

    # DL bhava position — Fix-2 + Fix-4
    if dl_planet == "rahu":
        # రాహు కి 6వ భావం strength (upachaya) — వ్యయం వర్తించదు
        if dl_bhava in [1,4,5,7,9,10,11]: score += 0.5
        elif dl_bhava in [3,6,11]: score += 0.3
        elif dl_bhava in [8,12]: score -= 0.3
    elif dl_planet == "ketu":
        # కేతు కి 12వ భావం = వ్యయ స్థానం — penalty వర్తిస్తుంది
        if dl_bhava in [1,4,5,7,9,10,11]: score += 0.5
        elif dl_bhava in [3,6]: score += 0.2
        elif dl_bhava in [8,12]: score -= 0.4
    else:
        if dl_bhava in [1,4,7,10]: score += 0.5    # కేంద్ర
        elif dl_bhava in [5,9]: score += 0.5        # త్రికోణ
        elif dl_bhava == 11: score += 0.5           # లాభ
        elif dl_bhava in [6,8,12]: score -= 0.3     # దుష్ట

    # BL quality
    if bl_quality == "శుభ": score += 1.0
    elif bl_quality == "మిశ్రమ": score += 0.5

    # RL quality
    if rl_quality == "శుభ": score += 1.0
    elif rl_quality == "మిశ్రమ": score += 0.5

    # DL adhipatya — Fix-3
    score += adh_score * 0.5

    # Conjunction effect
    if conjunction_effect == "శుభ ప్రభావం": score += 0.5
    elif conjunction_effect == "అశుభ ప్రభావం": score -= 0.5
    # రాహు/కేతు conjunction = partial negative
    if rk_conj: score -= 0.2

    if score >= 2.5: final_status = "PRAVAHA"
    elif score >= 2.0: final_status = "MISRA"
    elif score >= 1.0: final_status = "VIGHNA"
    else: final_status = "YAMALA"

    # STEP-7: సంగ్రహ ఫలిత వాక్యం
    phala_summary = f"{PLANET_TE.get(dl_planet,'?')} దశ — {final_status} స్థితిలో ఉంది. "
    phala_summary += f"DL {dl_bhava}వ భావంలో ({karaka_te} కారకత్వం). "
    if conjunct_planets:
        phala_summary += f"{', '.join([PLANET_TE.get(p,'?') for p in conjunct_planets])} తో సంయోగం — {conjunction_effect}. "
    if bl_quality == "శుభ":
        phala_summary += f"భావాధిపతి ({PLANET_TE.get(bhava_lord_en,'?')}) శుభంగా ఉంది."
    elif bl_quality == "అశుభ":
        phala_summary += f"భావాధిపతి ({PLANET_TE.get(bhava_lord_en,'?')}) అశుభంగా ఉంది — సవాళ్లు ఉండొచ్చు."

    return {
        "dl_planet_en": dl_planet,
        "dl_planet_te": PLANET_TE.get(dl_planet,"?"),
        "dl_strength": dl_strength,
        "dl_bhava": dl_bhava,
        "dl_bhava_karaka": karaka_te,
        "bhava_lord": {"planet_en":bhava_lord_en,"planet_te":PLANET_TE.get(bhava_lord_en,"?"),
                       "strength":"HIGH" if bhava_lord_shad.get("is_strong") else "MEDIUM",
                       "maitri_with_dl":bl_maitri,"quality":bl_quality},
        "rashi_lord": {"planet_en":rashi_lord_en,"planet_te":PLANET_TE.get(rashi_lord_en,"?"),
                       "bhava":rl_bhava,"maitri_with_dl":rl_maitri,"quality":rl_quality},
        "adhipatya_note": adh_note,
        "adhipatya_score": adh_score,
        "conjunct_planets_te":[PLANET_TE.get(p,"?") for p in conjunct_planets],
        "conjunct_planets_en":conjunct_planets,
        "conjunction_effect":conjunction_effect,
        "conjunct_karakas":conjunct_karakas,
        "final_status":final_status,
        "score":round(score,2),
        "phala_summary":phala_summary
    }



# ═══════════════════════════════════════════════════════════
# DB11 UNIVERSAL CONTRADICTION RESOLUTION — 5 DOMAINS
# Source: BPHS Multi-Varga + Brihat Jataka Karaka theory
# ═══════════════════════════════════════════════════════════
DOMAIN_MAPPING = {
    "వివాహం":       {"special_varga":"D9",  "special_varga_bhava":7,  "karaka_type":"DK",    "karaka_planet":None},
    "సంతానం":       {"special_varga":"D7",  "special_varga_bhava":5,  "karaka_type":"PK",    "karaka_planet":"jupiter"},
    "ఆర్థికం":      {"special_varga":"D2",  "special_varga_bhava":2,  "karaka_type":"fixed", "karaka_planet":"jupiter"},
    "వృత్తి":        {"special_varga":"D10", "special_varga_bhava":10, "karaka_type":"fixed", "karaka_planet":"sun"},
    "సోషల్ స్టేటస్":{"special_varga":"D10", "special_varga_bhava":10, "karaka_type":"fixed", "karaka_planet":"sun", "secondary_check":"arudha_lagna"},
}

def _get_varga_bhava_strength(dc_data, varga_name, bhava_num):
    varga = dc_data.get(varga_name, {})
    if not varga: return "NEUTRAL"
    bhava_chart = varga.get("bhava_chart", {})
    planets_in_bhava = bhava_chart.get(bhava_num, [])
    if not planets_in_bhava: return "NEUTRAL"
    TE_PLANET = {v: k for k, v in PLANET_TE.items()}
    pos = neg = 0
    for p_te in planets_in_bhava:
        p_en = TE_PLANET.get(p_te, "")
        if not p_en or p_en not in varga: continue
        st = varga[p_en].get("strength", "సాధారణం")
        if st in ("ఉచ్చం","స్వరాశి","మూల త్రికోణం"): pos += 1
        elif st == "నీచం": neg += 1
    if pos > neg: return "POSITIVE"
    elif neg > pos: return "NEGATIVE"
    return "NEUTRAL"

def _get_karaka_result(config, d1p, shad, chara_karakas):
    karaka_type = config.get("karaka_type","fixed")
    karaka_planet = config.get("karaka_planet")
    if karaka_type in ("DK","PK","AK","AmK"):
        for p_en, kdata in chara_karakas.get("karakas",{}).items():
            if kdata.get("karaka_short") == karaka_type:
                karaka_planet = p_en; break
    if not karaka_planet or karaka_planet not in d1p: return "NEUTRAL"
    st = d1p[karaka_planet].get("strength","సాధారణం")
    is_s = shad.get(karaka_planet,{}).get("is_strong",False)
    if st in ("ఉచ్చం","స్వరాశి") and is_s: return "POSITIVE"
    elif st == "నీచం" and not is_s: return "NEGATIVE"
    return "NEUTRAL"

def resolve_contradiction(domain, kb2_base_result, d1p, shad, dc_data, chara_karakas, special_lagnas=None):
    """
    DB11 Universal Contradiction Resolution — 5 Domains
    వివాహం, సంతానం, ఆర్థికం, వృత్తి, సోషల్ స్టేటస్
    """
    if domain not in DOMAIN_MAPPING:
        return {"domain":domain,"error":f"Unsupported domain","final_result":kb2_base_result,"confidence":"LOW"}

    config = DOMAIN_MAPPING[domain]
    varga_name = config["special_varga"]
    varga_bhava = config["special_varga_bhava"]

    varga_result = _get_varga_bhava_strength(dc_data, varga_name, varga_bhava)

    # సోషల్ స్టేటస్ కి ఆరూఢ లగ్నం boost
    arudha_boost = False
    if domain == "సోషల్ స్టేటస్" and special_lagnas:
        ab = special_lagnas.get("arudha_lagna_bhava", 0)
        arudha_boost = any(
            pd.get("bhava")==ab and pd.get("strength") in ("ఉచ్చం","స్వరాశి")
            and p in ("jupiter","venus","mercury","moon")
            for p,pd in d1p.items()
        )

    contradiction = (
        (kb2_base_result=="NEGATIVE" and varga_result=="POSITIVE") or
        (kb2_base_result=="POSITIVE" and varga_result=="NEGATIVE")
    )

    if not contradiction:
        return {
            "domain":domain,"kb2_base_result":kb2_base_result,
            "varga_result":varga_result,"karaka_result":"NEUTRAL",
            "override_score":0,"final_result":kb2_base_result,
            "confidence":"HIGH","contradiction":False,
            "conclusion":f"{domain} విషయంలో KB2 మరియు {varga_name} ఏకాభిప్రాయంగా ఉన్నాయి — {kb2_base_result} ఫలితం నమ్మదగినది."
        }

    override_score = 0
    # CONDITION-A: Varga bhava లో ఉచ్చ/స్వరాశి గ్రహం
    varga = dc_data.get(varga_name,{})
    bc = varga.get("bhava_chart",{})
    TE_PLANET = {v:k for k,v in PLANET_TE.items()}
    for p_te in bc.get(varga_bhava,[]):
        p_en = TE_PLANET.get(p_te,"")
        if p_en and p_en in varga:
            if varga[p_en].get("strength") in ("ఉచ్చం","స్వరాశి","మూల త్రికోణం"):
                override_score += 1; break
    # CONDITION-B: Karaka strong
    karaka_result = _get_karaka_result(config, d1p, shad, chara_karakas)
    if karaka_result == "POSITIVE": override_score += 1
    # CONDITION-C: Arudha boost
    if arudha_boost: override_score += 1

    if override_score >= 2:
        final_result = "POSITIVE" if kb2_base_result=="NEGATIVE" else "NEGATIVE"
        confidence = "HIGH"
        note = f"KB2 నియమం override అయింది. {varga_name} మరియు కారకుడు బలంగా ఉన్నారు."
    elif override_score == 1:
        final_result = "MIXED"; confidence = "MEDIUM"
        note = f"KB2 మరియు {varga_name} మధ్య మిశ్రమ ఫలితం."
    else:
        final_result = kb2_base_result; confidence = "LOW"
        note = "Override conditions లేవు. KB2 నియమమే ప్రాధాన్యం."

    if final_result=="POSITIVE": conc = f"{domain} విషయంలో శుభ ఫలితాలు సంభావ్యత ఎక్కువ. {note}"
    elif final_result=="NEGATIVE": conc = f"{domain} విషయంలో సవాళ్లు ఉండే సంభావ్యత. {note}"
    else: conc = f"{domain} విషయంలో మిశ్రమ ఫలితాలు. {note}"

    return {
        "domain":domain,"kb2_base_result":kb2_base_result,
        "varga_result":varga_result,"karaka_result":karaka_result,
        "override_score":override_score,"final_result":final_result,
        "confidence":confidence,"contradiction":True,"conclusion":conc
    }

def calc_all_domain_contradictions(d1p, shad, dc_data, chara_karakas, special_lagnas=None):
    """అన్ని 5 domains కి contradiction check"""
    results = {}
    def d1_bhava_quality(bhava_num):
        planets_in = [p for p,pd in d1p.items() if pd.get("bhava")==bhava_num]
        strong = [p for p in planets_in if d1p[p].get("strength") in ("ఉచ్చం","స్వరాశి","మూల త్రికోణం")]
        weak_mal = [p for p in planets_in if p in ("saturn","mars","rahu","ketu") and d1p[p].get("strength")=="నీచం"]
        if strong: return "POSITIVE"
        if weak_mal: return "NEGATIVE"
        return "NEUTRAL"

    domain_bhava_map = {"వివాహం":7,"సంతానం":5,"ఆర్థికం":2,"వృత్తి":10,"సోషల్ స్టేటస్":10}
    for domain, bhava in domain_bhava_map.items():
        kb2_base = d1_bhava_quality(bhava)
        if kb2_base == "NEUTRAL":
            results[domain] = {"domain":domain,"kb2_base_result":"NEUTRAL","final_result":"NEUTRAL",
                               "confidence":"LOW","contradiction":False,
                               "conclusion":f"{domain} — D1 లో neutral స్థితి. వర్గ చక్రం ముఖ్యం."}
        else:
            results[domain] = resolve_contradiction(domain, kb2_base, d1p, shad, dc_data, chara_karakas, special_lagnas)
    return results


def calc_bhava_assessment(d1p, lagna_rashi_num, shad=None):
    """
    Chapter 15 Phaladeepika — Bhava Assessment
    ప్రతి bhava కి STRONG/WEAK/DESTROYED/MIXED calculate చేయి
    """
    MALEFICS = {"sun","mars","saturn","rahu","ketu"}
    BENEFICS = {"moon","mercury","jupiter","venus"}
    DUSTHANA = {6, 8, 12}
    SHUBHA   = {1, 2, 4, 5, 7, 9, 10, 11}

    # Rashi lord map
    RASHI_LORD = {1:"mars",2:"venus",3:"mercury",4:"moon",5:"sun",6:"mercury",
                  7:"venus",8:"mars",9:"jupiter",10:"saturn",11:"saturn",12:"jupiter"}

    # Bhava lord map (lagna rashi based)
    def bhava_lord(bhava_num):
        rashi = ((lagna_rashi_num - 1 + bhava_num - 1) % 12) + 1
        return RASHI_LORD.get(rashi, "")

    # Get planet bhava
    def get_bhava(p_en):
        return d1p.get(p_en, {}).get("bhava", 0)

    # Get planet strength
    def get_strength(p_en):
        return d1p.get(p_en, {}).get("graha_strength",
               d1p.get(p_en, {}).get("strength", ""))

    # Is combust
    def is_combust(p_en):
        return d1p.get(p_en, {}).get("is_combust", False)

    result = {}
    for bhava_num in range(1, 13):
        lord = bhava_lord(bhava_num)
        if not lord:
            result[f"bhava{bhava_num}"] = {"status": "UNKNOWN"}
            continue

        lord_bhava = get_bhava(lord)
        lord_strength = get_strength(lord)
        lord_combust = is_combust(lord)
        reasons = []
        score = 0

        # RULE_BHAVA_ASSESS_3: Lord in 8th, combust, neecha, shatru → DESTROYED
        destroyed = False
        if lord_bhava == 8:
            destroyed = True
            reasons.append("lord_in_8th")
        if lord_combust:
            destroyed = True
            reasons.append("lord_combust")
        if lord_strength in ("నీచం", "శత్రు రాశి"):
            destroyed = True
            reasons.append("lord_neecha_or_shatru")

        # RULE_BHAVA_ASSESS_5: Lord in 6/8/12 from lagna
        if lord_bhava in DUSTHANA:
            reasons.append("lord_in_dusthana")
            score -= 2

        # RULE_BHAVA_ASSESS_1: Lord in own/exalted/friendly
        if lord_strength in ("ఉచ్చం", "స్వరాశి", "మూల త్రికోణం"):
            score += 3
            reasons.append("lord_strong")
        elif lord_strength in ("మిత్ర రాశి",):
            score += 1
            reasons.append("lord_friendly")

        # Planets in this bhava
        planets_in_bhava = [p for p, pd in d1p.items() if pd.get("bhava") == bhava_num]
        benefics_in = [p for p in planets_in_bhava if p in BENEFICS]
        malefics_in = [p for p in planets_in_bhava if p in MALEFICS]

        if benefics_in:
            score += len(benefics_in)
            reasons.append(f"benefics_present:{','.join(benefics_in)}")
        if malefics_in:
            score -= len(malefics_in)
            reasons.append(f"malefics_present:{','.join(malefics_in)}")

        # RULE_BHAVA_ASSESS_6: Karaka check
        KARAKA_MAP = {1:"sun",2:"jupiter",3:"mars",4:"moon",5:"jupiter",
                      6:"venus",7:"saturn",8:"sun",9:"jupiter",10:"jupiter",11:"saturn",12:"saturn"}
        karaka = KARAKA_MAP.get(bhava_num, "")
        if karaka:
            k_strength = get_strength(karaka)
            k_bhava = get_bhava(karaka)
            if k_strength in ("ఉచ్చం", "స్వరాశి", "మూల త్రికోణం"):
                score += 2
                reasons.append("karaka_strong")
            elif k_bhava in DUSTHANA:
                score -= 1
                reasons.append("karaka_in_dusthana")

        # Final status
        if destroyed and score <= 0:
            status = "DESTROYED"
        elif score >= 3:
            status = "STRONG"
        elif score >= 1:
            status = "MODERATE"
        elif score == 0:
            status = "MIXED"
        else:
            status = "WEAK"

        result[f"bhava{bhava_num}"] = {
            "status": status,
            "lord": lord,
            "lord_bhava": lord_bhava,
            "lord_strength": lord_strength,
            "score": score,
            "reasons": reasons
        }

    return result

def generate_v21(dob,tob,lat,lon,place,timezone=5.5,ayan_mode="lahiri"):
    # ─── DB8 logic intact — అక్షరం మార్చలేదు ───
    d,m,y=map(int,dob.split("/")); h,mi,s=map(int,tob.split(":"))
    bd=datetime.datetime(y,m,d,h,mi,s)
    trop,obs,jd,T,spd,mlon,lat_p,tlon=get_positions(dob,tob,lat,lon,timezone)
    ayan=get_ayanamsha(jd,ayan_mode); sid={k:(v-ayan)%360 for k,v in trop.items()}
    stl=tlon.get("sun",trop.get("sun",0)); sc=calc_sunrise_sunset(bd,lat,lon,timezone)
    ls=calc_lagna(obs,lat,lon,ayan); lr,ld,lni,lp=degrees_to_rashi(ls)
    dq=get_decanate_quality(lr,ld)
    CORB={"moon":12.0,"mars":17.0,"mercury":14.0,"jupiter":11.0,"venus":10.0,"saturn":15.0}
    ss=sid["sun"]; MSP={"sun":0.9856,"moon":13.1764,"mercury":1.3833,"venus":1.2,"mars":0.524,"jupiter":0.0831,"saturn":0.0335,"rahu":0.053,"ketu":0.053}
    d1p={}
    for key in PLANET_TE:
        rashi,deg,ni,pada=degrees_to_rashi(sid[key]); bhava=bhava_of(rashi,lr); strength=graha_strength(key,rashi)
        d9r=int(((sid[key]*9)%360)//30)+1; vargo=(rashi==d9r); sp=spd.get(key,0.0); mn=MSP.get(key,0.5)
        if key in ("rahu","ketu"): ct="వక్ర (నిత్యం)"
        elif sp<0: ct="అనువక్ర" if abs(sp)<(mn*0.2) else "వక్ర"
        elif abs(sp)<(mn*0.05): ct="వికల"
        else:
            r=sp/mn; ct="మంద" if r<0.5 else "మందతర" if r<0.85 else "సమ" if r<=1.15 else "చర" if r<=1.5 else "అతిచర"
        if key in ("sun","rahu","ketu"): ic=False; cs="వర్తించదు"
        else:
            orb=CORB.get(key,12.0)
            if key=="mercury" and sp<0: orb=12.0
            elif key=="venus" and sp<0: orb=8.0
            dc2=abs(sid[key]-ss)
            if dc2>180: dc2=360-dc2
            ic=(dc2<=orb); cs="దగ్ధం" if ic else "సాధారణం"
        acl=calc_ayurdaya_combust_loss(key,ic,sp); sm2=calc_satyacharya_multiplier(key,strength,sp<0,vargo,rashi,d9r,int(deg/10)+1); aa=calc_aarohi_avrohi(key,strength,sp<0,None,sid)
        # DB11 CAL-NOTE-13: exaltation_aarohi_flag
        eaf = calc_exaltation_aarohi_flag(key, strength, aa)
        d1p[key]={"name_te":PLANET_TE[key],"emoji":PLANET_EMOJI[key],"rashi_te":RASHI_TE.get(rashi,"?"),"rashi_num":rashi,"bhava":bhava,"degrees":deg,"sid_longitude":round(sid[key],4),"trop_longitude":round(trop[key],4),"nakshatra":NAKSHATRA_TE[ni] if ni<27 else "?","pada":pada,"strength":strength,"strength_percent":get_strength_percent(strength),"d9_rashi_num":d9r,"d9_rashi_te":RASHI_TE.get(d9r,"?"),"d9_strength":graha_strength(key,d9r),"vargottama":vargo,"is_retrograde":key in ("rahu","ketu") or sp<0,"speed_deg_per_day":round(sp,6),"chesta_type":ct,"is_combust":ic,"combust_status":cs,"dhatu":DHATU_MAP.get(key,"వర్తించదు"),"dosha":DOSHA_MAP.get(key,"వర్తించదు"),"ayurdaya_combust_loss":acl,"satyacharya_multiplier":sm2,"aarohi_avrohi":aa,"exaltation_aarohi_flag":eaf}
    d1bh={i:[] for i in range(1,13)}
    for k,p in d1p.items(): d1bh[p["bhava"]].append(p["name_te"])
    dmap={"D2":2,"D3":3,"D4":4,"D7":7,"D8":8,"D9":9,"D10":10,"D12":12,"D16":16,"D20":20,"D24":24,"D27":27,"D30":30,"D40":40,"D45":45,"D60":60}
    dc_data={dn:build_div_chart(sid,ls,dv) for dn,dv in dmap.items()}
    asp,bhava_aspected_by=calc_graha_aspects(d1p,lr); lmr=calc_lagna_malefic_reduction(d1p,asp)
    llk=BHAVA_LORDS[lr]; lbt=check_lagna_bala_triple(d1p,llk,asp)
    dasha=compute_dasha(sid["moon"],bd,planets_data=d1p,sid=sid,planet_speeds=spd)
    mdp=dasha["mahadasha"]["planet_en"]; adp=dasha["antardasha"]["planet_en"]
    opp=(adp in NATURAL_ENEMIES.get(mdp,set())) or (mdp in NATURAL_ENEMIES.get(adp,set()))
    on=f"{PLANET_TE.get(mdp,'?')}+{PLANET_TE.get(adp,'?')} సహజ శత్రువులు — వ్యతిరేక ఫలాలు" if opp else ""
    dasha["mahadasha"]["opposite_results_flag"]=opp; dasha["mahadasha"]["opposite_results_note"]=on
    dasha["antardasha"]["opposite_results_flag"]=opp; dasha["antardasha"]["opposite_results_note"]=on
    dasha["mahadasha"]["dasha_4factor"]={"natural_signification":DASHA_ROGA.get(mdp,""),"house":f"భావం {d1p[mdp]['bhava']}","sign":d1p[mdp]["rashi_te"],"yoga":"V23 లో నిర్ణయించాలి"}
    add=d1p.get(adp,{}); dasha["antardasha"]["rikta_flag"]=add.get("strength") in ["నీచం","సాధారణం"] and not add.get("vargottama",False)
    dc_chain=calc_dispositor_chain(d1p,lr); av=calc_ashtakavarga_approx(sid,lr); vg=calc_vargottama(sid)
    gy=calc_graha_yuddha(sid,d1p,lat_p=lat_p); mni=int(sid["moon"]/(360/27))%27; tb=calc_tara_bala(mni,d1p)
    parivartana_data    = calc_parivartana(d1p, lr)
    papakartari_data    = calc_papakartari(d1p)
    rk_dispositor_data  = calc_rahu_ketu_dispositor(d1p)
    neechabhanga_data   = calc_neechabhanga(d1p, lr)
    ch44_antidote_data  = calc_saravali_ch44_antidote(d1p)
    ch13_lunar_data     = calc_saravali_ch13_lunar_yogas(d1p)
    ch14_solar_data     = calc_saravali_ch14_solar_yogas(d1p)
    pancha_maha_data    = calc_pancha_mahapurusha(d1p, lr)
    ekadhipatya_data    = calc_ekadhipatya(d1p, lr)
    pc=calc_panchanga(sid,bd,_ss=sc); sl2=calc_special_lagnas(sid,ls,lr)
    dcs2={"d1":{"lagna":lr,**{k:{"rashi_num":d1p[k]["rashi_num"]} for k in PLANET_TE}},"D2":dc_data.get("D2",{}),"D3":dc_data.get("D3",{}),"D7":dc_data.get("D7",{}),"D9":dc_data.get("D9",{}),"D10":dc_data.get("D10",{}),"D12":dc_data.get("D12",{})}
    shad=calc_shadbala_virupa(d1p,sid,ls,asp,bd,lat,lon,timezone,_ss=sc,dc=dcs2,mlon=mlon,stl=stl)
    domain_analysis     = calc_domain_analysis(d1p, lr, asp, dc_data, shad)
    conjunction_dom     = calc_conjunction_dominance(d1p, shad)
    pi=calc_profession_lord(d1p,dc_data.get("D10",{}),sid,lr)
    mb=d1p["moon"]["bhava"]; benf=["jupiter","venus","mercury","moon"]
    s6=((mb+4)%12)+1; s7=((mb+5)%12)+1; s8=((mb+6)%12)+1
    sb6=[p for p in benf if d1p.get(p,{}).get("bhava",0)==s6]; sb7=[p for p in benf if d1p.get(p,{}).get("bhava",0)==s7]; sb8=[p for p in benf if d1p.get(p,{}).get("bhava",0)==s8]
    cdh=bool(sb6 and sb7 and sb8); jb=d1p.get("jupiter",{}).get("bhava",0); sh_y=(jb==s6 or jb==s8) and not cdh
    pex=[k for k in d1p if k not in ["sun","rahu","ketu"]]; s2h=(mb%12)+1; s12h=((mb-2)%12)+1
    s2=any(d1p.get(p,{}).get("bhava",0)==s2h for p in pex); s12=any(d1p.get(p,{}).get("bhava",0)==s12h for p in pex)
    if s2 and s12: sy="DURUDHARA"
    elif s2: sy="SUNAPHA"
    elif s12: sy="ANAPHA"
    else:
        sy="KEMADURMA"
        # FIX-26: B.V. Raman "300 Combinations" — రెండు cancellation conditions
        # Condition (a): Moon నుండి kendras లో planets ఉంటే cancel
        # Condition (b): Lagna నుండి kendras లో planets ఉంటే cancel
        # Source: "there is distinct cancellation of the Kemadruma because
        #          (a) kendras from the Moon are occupied and
        #          (b) kendras from the Lagna are also occupied"
        # DB11 పాత code: KENDRA = {1,4,7,10} — ఇవి Lagna నుండి kendras మాత్రమే
        # FIX-26: Moon నుండి kendras వేరే గా calculate చేయాలి
        moon_bhava = d1p["moon"]["bhava"]
        moon_kendras = {moon_bhava, ((moon_bhava+2)%12)+1, ((moon_bhava+5)%12)+1, ((moon_bhava+8)%12)+1}
        cond_a = any(d1p.get(p,{}).get("bhava",0) in moon_kendras for p in pex)  # Moon నుండి kendra
        cond_b = any(d1p.get(p,{}).get("bhava",0) in KENDRA for p in pex)         # Lagna నుండి kendra
        if cond_a or cond_b:
            cancel_reason = []
            if cond_a: cancel_reason.append("చంద్ర కేంద్రం")
            if cond_b: cancel_reason.append("లగ్న కేంద్రం")
            sy = "KEMADURMA (CANCELLED:" + "+".join(cancel_reason) + ")"
    today=datetime.datetime.now(); age=(today-bd).days/365.25
    NA=[(1,"moon"),(3,"mars"),(12,"mercury"),(32,"venus"),(50,"jupiter"),(70,"sun"),(120,"saturn")]
    nc=any(age<=ma and mdp==mp for ma,mp in NA); dasha["mahadasha"]["naisargika_confirmed"]=nc
    con=calc_conception_difficulty(d1p); ar=shad.get("jupiter",{}).get("is_strong",False)
    def dli(pen):
        if pen not in d1p: return {}
        p=d1p[pen]; return {"bhava":p["bhava"],"rashi_te":p["rashi_te"],"strength":p["strength"],"is_combust":p["is_combust"],"combust_status":p["combust_status"],"chesta_type":p["chesta_type"]}
    dasha["antardasha"]["lord_info"]=dli(adp); dasha["pratyantar"]["lord_info"]=dli(dasha["pratyantar"]["planet_en"]); dasha["mahadasha"]["lord_info"]=dli(mdp)
    # ─── DB11 CAL-NOTE-9: pratyantar lord bindu_phala ───
    prat_planet = dasha["pratyantar"]["planet_en"]
    prat_bp = get_pratyantar_bindu_phala(prat_planet, av)
    dasha["pratyantar"]["lord_info"]["bindu_phala"] = prat_bp
    # ─── DB11 CAL-NOTE-8: health_risk_flag for antardasha lord ───
    ad_aa = d1p.get(adp, {}).get("aarohi_avrohi", "")
    dasha["antardasha"]["health_risk_flag"] = calc_health_risk_flag(adp, d1p, ad_aa)
    dasha["antardasha"]["health_risk_note"] = (
        "12వ bhava + Avrohi antardasha lord — hospitalization/surgery possibility వేరే report చేయాలి (CAL-NOTE-8)"
        if dasha["antardasha"]["health_risk_flag"] else ""
    )
    # ─── DB11 CAL-NOTE-4: rikta_flag_scope ───
    dasha["mahadasha"]["rikta_flag_scope"]  = RIKTA_FLAG_SCOPE
    dasha["mahadasha"]["rikta_flag_note"]   = RIKTA_FLAG_NOTE if dasha["mahadasha"].get("rikta_flag") else ""
    dasha["antardasha"]["rikta_flag_scope"] = RIKTA_FLAG_SCOPE
    dasha["antardasha"]["rikta_flag_note"]  = RIKTA_FLAG_NOTE if dasha["antardasha"].get("rikta_flag") else ""
    # ─── DB8 return dict intact ───

    # ─── ADD-1 through ADD-8: కొత్త calculations ───
    mandi_data       = calc_mandi(bd, sc, lat, lon, timezone)
    vishesa_data     = calc_vishesa_lagnas(sid, ls, lr, bd, sc, timezone)
    panchadha_data   = calc_panchadha_maitri(d1p)
    tatkalika_data   = calc_tatkalika_maitri(d1p)
    pindayu_data     = calc_pindayu(d1p, sid, lr)
    kala_sarpa_data  = calc_kala_sarpa(sid)
    chara_karaka_data= calc_chara_karakas(d1p)
    avastha_data     = calc_graha_avastha(d1p)
    gochara_data     = calc_gochara(timezone)

    # ─── CAL-NOTE-18: tribandhu ───
    for _pk, _sd in shad.items():
        if _pk in d1p: d1p[_pk]["is_strong"] = _sd.get("is_strong",False)
    dasha["mahadasha"]["tribandhu"] = calc_tribandhu_status(mdp, d1p, panchadha_data)
    dasha["antardasha"]["tribandhu"] = calc_tribandhu_status(adp, d1p, panchadha_data)
    dasha["pratyantar"]["tribandhu"] = calc_tribandhu_status(dasha["pratyantar"]["planet_en"], d1p, panchadha_data)
    # ─── 7-Step Dasha Phala Engine ───
    dasha["mahadasha"]["phala_engine"] = calc_dasha_phala_engine(mdp, d1p, shad, panchadha_data, lr)
    dasha["antardasha"]["phala_engine"] = calc_dasha_phala_engine(adp, d1p, shad, panchadha_data, lr)
    dasha["pratyantar"]["phala_engine"] = calc_dasha_phala_engine(prat_planet, d1p, shad, panchadha_data, lr)

    # ─── STEP-1: అధిపత్య శుభ/పాప ───
    lagna_rashi_te = RASHI_TE.get(lr,"మేషం")
    adhipatya_data = calc_adhipatya_shubha_papa(d1p, lagna_rashi_te)
    # Planet JSON లో adhipatya fields merge చేయడం
    for key in PLANET_TE:
        d1p[key].update(adhipatya_data.get(key,{}))

    # ─── DB11 CAL-NOTE-14: rahu delivery_mechanism ───
    rahu_bhava = d1p.get("rahu", {}).get("bhava", 6)
    d1p["rahu"]["delivery_mechanism"] = RAHU_DELIVERY_MECHANISM
    d1p["rahu"]["delivery_note"]      = RAHU_BHAVA_UNEXPECTED.get(rahu_bhava, RAHU_DELIVERY_MECHANISM)
    d1p["rahu"]["delivery_source"]    = "V27 CAL-NOTE-14 (Universal)"

    # ─── STEP-2: ఆరూఢ లగ్నం ───
    arudha_data = calc_arudha_lagna(lr, llk, d1p)
    arudha_bhava = arudha_data.get("arudha_lagna_bhava",10)
    arudha_rashi = arudha_data.get("arudha_lagna_rashi",lr)
    # special_lagnas కి add చేయడం
    sl2["arudha_lagna_rashi"] = arudha_data["arudha_lagna_rashi"]
    sl2["arudha_lagna_te"]    = arudha_data["arudha_lagna_te"]
    sl2["arudha_lagna_bhava"] = arudha_data["arudha_lagna_bhava"]

    # ─── STEP-3: భావ బల ───
    bhava_bala_data = calc_bhava_bala(d1p, shad, lr)

    # ─── STEP-4: రాజ యోగ flags ───
    pgm_present, pgm_base = check_pancha_graha_malika(d1p, lr, arudha_rashi)
    adhi_count, adhi_tag  = check_adhi_yoga(d1p["moon"]["bhava"], d1p)

    # ─── STEP-8: ఆరూఢ రాజ యోగ ───
    ar_count, ar_tag = check_arudha_raja_yoga(arudha_bhava, d1p)

    # ─── STEP-9: భాగ్య + రాజ్య యోగ ───
    bry_present, bry_type, bry_bl, bry_rl = check_bhagya_rajya_yoga(d1p, lr, asp)

    # ─── FIX-27: విపరీత రాజ యోగ ───
    vip_present, vip_detail, vip_yogas = check_viparita_raja_yoga(d1p, lr)

    # ─── FIX-25 (partial): gaja_present, adhi_planets, bry_planets ముందే define చేయాలి — FIX-29 కి అవసరం ───
    gaja_present = (jb in KENDRA) and (mb in KENDRA)
    adhi_planets = [p for p in ["jupiter","venus","mercury","moon"] if d1p.get(p,{}).get("bhava",0) in {s6,s7,s8}]
    bry_planets = [bry_bl, bry_rl] if bry_present else []

    # ─── FIX-29: Yoga Timing ───
    ftl = dasha.get("full_timeline", [])
    gaja_timing   = calc_yoga_timing(["jupiter","moon"], d1p, shad, ftl) if gaja_present else None
    bry_timing    = calc_yoga_timing(bry_planets, d1p, shad, ftl) if bry_present else None
    adhi_timing   = calc_yoga_timing(adhi_planets, d1p, shad, ftl) if adhi_planets else None
    vip_planets_list = [v["lord_en"] for v in vip_detail.values()]
    vip_timing    = calc_yoga_timing(vip_planets_list, d1p, shad, ftl) if vip_present else None

    # ─── FIX-25: Yoga Net Strength — అన్ని yogas ───
    adhi_score, adhi_strength = calc_yoga_net_strength(adhi_planets, d1p, asp) if adhi_planets else (0,"NOMINAL")
    bry_score, bry_strength = calc_yoga_net_strength(bry_planets, d1p, asp) if bry_planets else (0,"NOMINAL")
    gaja_score, gaja_strength = calc_yoga_net_strength(["jupiter","moon"], d1p, asp) if gaja_present else (0,"NOMINAL")
    sunapha_planets = [p for p in pex if d1p.get(p,{}).get("bhava",0) in {s2h, s12h}]
    sunapha_score, sunapha_strength = calc_yoga_net_strength(["moon"]+sunapha_planets, d1p, asp) if sunapha_planets else (0,"NOMINAL")
    cdh_planets = sb6+sb7+sb8
    cdh_score, cdh_strength = calc_yoga_net_strength(cdh_planets, d1p, asp) if cdh else (0,"NOMINAL")
    shakata_score, shakata_strength = calc_yoga_net_strength(["jupiter","moon"], d1p, asp) if sh_y else (0,"NOMINAL")
    pgm_planets = [k for k in d1p if k not in ("rahu","ketu")] if pgm_present else []
    pgm_score, pgm_strength = calc_yoga_net_strength(pgm_planets, d1p, asp) if pgm_present else (0,"NOMINAL")
    ar_planets = [p for p in d1p if d1p[p].get("bhava")==arudha_bhava and p not in ("rahu","ketu")]
    ar_score, ar_strength = calc_yoga_net_strength(ar_planets, d1p, asp) if ar_planets else (0,"NOMINAL")

    # special_flags కి ADD-5, ADD-6 + STEP flags కలపడం
    sf_extra = {
        "kala_sarpa_present": kala_sarpa_data["present"],
        "kala_sarpa_type": kala_sarpa_data["type"],
        "atmakaraka": chara_karaka_data["atmakaraka_te"],
        "atmakaraka_en": chara_karaka_data["atmakaraka"],
        "pancha_graha_malika_yoga": pgm_present,
        "pancha_graha_malika_base": pgm_base or "లేదు",
        "pancha_graha_malika_net_strength": pgm_strength,
        "pancha_graha_malika_net_score": pgm_score,
        "adhi_yoga_shubha_count": adhi_count,
        "adhi_yoga_tag": adhi_tag,
        "adhi_yoga_net_strength": adhi_strength,
        "adhi_yoga_net_score": adhi_score,
        "bhagya_rajya_adhipati_yoga": bry_present,
        "bhagya_rajya_yoga_type": bry_type or "లేదు",
        "bhagya_rajya_net_strength": bry_strength,
        "bhagya_rajya_net_score": bry_score,
        "bhagya_lord_en": bry_bl,
        "rajya_lord_en": bry_rl,
        "arudha_shubha_count": ar_count,
        "arudha_raja_yoga_tag": ar_tag,
        "arudha_raja_yoga_net_strength": ar_strength,
        "arudha_raja_yoga_net_score": ar_score,
        "gajakesari_yoga_present": gaja_present,
        "gajakesari_net_strength": gaja_strength,
        "gajakesari_net_score": gaja_score,
        "sunapha_anapha_yoga": sy,
        "sunapha_anapha_net_strength": sunapha_strength,
        "sunapha_anapha_net_score": sunapha_score,
        "chandradhiyoga_net_strength": cdh_strength,
        "chandradhiyoga_net_score": cdh_score,
        "shakata_yoga_net_strength": shakata_strength,
        "shakata_yoga_net_score": shakata_score,
        "viparita_raja_yoga_present": vip_present,
        "viparita_raja_yogas": vip_yogas,
        "viparita_raja_yoga_detail": vip_detail,
        "yoga_timing_gajakesari": gaja_timing,
        "yoga_timing_bhagya_rajya": bry_timing,
        "yoga_timing_adhi": adhi_timing,
        "yoga_timing_viparita": vip_timing,
    }


    # ─── Domain Contradiction Resolution ───
    domain_contradictions = calc_all_domain_contradictions(d1p, shad, dc_data, chara_karaka_data, sl2)

    # ── DB10 ADD-10: భావ స్ఫుటము ────────────────────────────────────────────
    try:
        _dparts = dob.split('/')
        _tparts = tob.split(':')
        bd_dt = datetime.datetime(int(_dparts[2]),int(_dparts[1]),int(_dparts[0]),
                                  int(_tparts[0]),int(_tparts[1]),
                                  int(_tparts[2]) if len(_tparts)>2 else 0)
        bhava_sputamu = calc_bhava_sputamu(ls, sid["sun"], bd_dt)
        planet_bhava_assignment = assign_planets_bhava_sputamu(bhava_sputamu, sid)
    except Exception as _e:
        print(f"  ⚠️  bhava_sputamu error: {_e}")
        bhava_sputamu = {}
        planet_bhava_assignment = {}
    # ─────────────────────────────────────────────────────────────────────────

    return {
        # ─── DB8 fields (అన్నీ intact) ───
        "meta":{
            "system":"DB11-DIVYA BRAHMA ENGINE","version":"11.0",
            "engine":"pyephem+swisseph","source":"Brihat Jataka+BPHS+Jataka Martanda",
            "precedence":"Brihat Jataka>BPHS (except Shadbala)",
            "ayanamsha":f"{ayan_mode.capitalize()} {ayan:.4f}°","ayanamsha_val":round(ayan,4),"ayanamsha_mode":ayan_mode,
            "dob":dob,"tob":tob,"place":place,"lat":lat,"lon":lon,
            "timezone":timezone,"jd":round(jd,4),
            "generated":datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "calibration_notes":"V27 Rules + Tribandhu Siddhanta (CAL-NOTE-18)"
        },
        "d1":{"lagna":{"rashi_te":RASHI_TE.get(lr,"?"),"rashi_num":lr,"degrees":ld,"sid_longitude":round(ls,4),"nakshatra":NAKSHATRA_TE[lni] if lni<27 else "?","pada":lp,"lord_en":llk,"lord_te":PLANET_TE.get(llk,"?"),"lagna_malefic_reduction":lmr,"decanate_quality":dq},"planets":d1p,"bhava_chart":d1bh,"desc":DIV_DESC["D1"]},
        **{k:{**v,"desc":DIV_DESC.get(k,"")} for k,v in dc_data.items()},
        "dasha":dasha,"special_lagnas":sl2,"aspects":asp,"bhava_aspected_by":bhava_aspected_by,
        "dispositor_chain":dc_chain,"shadbala_v19_practical":av,
        "vargottama":vg,"graha_yuddha":gy,"tara_bala":tb,
        "parivartana":parivartana_data,"papakartari":papakartari_data,
        "rahu_ketu_dispositor":rk_dispositor_data,"neechabhanga":neechabhanga_data,
        "saravali_ch44_antidote":ch44_antidote_data,
        "saravali_ch13_lunar_yogas":ch13_lunar_data,
        "saravali_ch14_solar_yogas":ch14_solar_data,
        "pancha_mahapurusha":pancha_maha_data,
        "ekadhipatya":ekadhipatya_data,
        "domain_analysis":domain_analysis,
        "conjunction_dominance":conjunction_dom,
        "panchanga":pc,"shadbala_virupa":shad,
        "sidereal_longitudes":{k:round(v,4) for k,v in sid.items()},
        "lagna_sid":round(ls,4),
        "metadata_enhancement":{
            "analysis_ready":True,"upgrade_version":"DB11-11.0",
            "source":"Brihat Jataka 30 rules + BPHS Shadbala + 8 DB9 additions + 9 Jataka Martanda steps + 5 V27 Calibration fields",
            "precedence_note":"Brihat Jataka > BPHS. Shadbala = BPHS only.",
            "brihat_jataka_rules":["R4 Lagna Bala","R9 Dhatu/Dosha","R16 Aarohi/Avrohi","R18 Combust","R23 Opposite","R30 Dasha Roga"],
            "classical_additions":["Mandi","Vishesa Lagnas","Panchadha Maitri","Pindayu","Kala Sarpa","Chara Karakas","Graha Avastha","Gochara"],
            "jataka_martanda":["Adhipatya","Arudha Lagna","Bhava Bala","Raja Yoga","Mars Yuddha","Ashtaka Phala","Arudha Raja Yoga","Bhagya Rajya Yoga"],
            "db11_calibrations":{
                "CAL-NOTE-4": {"field":"rikta_flag_scope","scope":"health_timing_only","note":RIKTA_FLAG_NOTE},
                "CAL-NOTE-8": {"field":"health_risk_flag","location":"dasha.antardasha","note":"12వ bhava + Avrohi antardasha lord"},
                "CAL-NOTE-9": {"field":"pratyantar.lord_info.bindu_phala","note":"short-term ఆర్థిక స్థితి indicator"},
                "CAL-NOTE-13":{"field":"exaltation_aarohi_flag","location":"d1.planets.[planet]","note":"ఉచ్చం + Aarohi = bindu override"},
                "CAL-NOTE-14":{"field":"rahu.delivery_mechanism","value":RAHU_DELIVERY_MECHANISM,"bhava_table":RAHU_BHAVA_UNEXPECTED},
                "CAL-NOTE-18":{"field":"tribandhu","location":"dasha.mahadasha/antardasha/pratyantar","note":"Tribandhu Siddhanta"}
            },
            "special_flags":{
                **{"lagna_bala_triple":lbt,"lagna_malefic_reduction_pct":lmr,"chandradhiyoga":cdh,"shakata_yoga":sh_y,"sunapha_etc":sy,"conception_difficulty":con,"naisargika_dasha_confirmed":nc,"arishta_bhanga_jupiter_strong":ar,"profession_lord":pi.get("planet_en","?"),"profession_source":pi.get("source","?"),"md_ad_opposite_results":opp,"md_ad_opposite_note":on},
                **sf_extra
            }
        },
        # ─── DB9 ADD-1..8 fields ───
        "mandi":              mandi_data,
        "vishesa_lagnas":     vishesa_data,
        "panchadha_maitri":   panchadha_data,
        "tatkalika_maitri":   tatkalika_data,
        "pindayu":            pindayu_data,
        "kala_sarpa":         kala_sarpa_data,
        "chara_karakas":      chara_karaka_data,
        "graha_avastha":      avastha_data,
        "gochara":            gochara_data,
        # ─── Jataka Martanda STEP fields ───
        "bhava_bala":         bhava_bala_data,
        "bhava_sputamu":      bhava_sputamu,
        "planet_bhava_sputamu": planet_bhava_assignment,
        "domain_contradictions": domain_contradictions,
        "bhava_assessment": calc_bhava_assessment(d1p, lr, shad)
    }

# ═══════════════════════════════════════════════════════════
# DISPLAY FUNCTION — DB8 intact + DB9 additions display
# ═══════════════════════════════════════════════════════════
def step0_display(data):
    sep="─"*42; l=data["d1"]["lagna"]; pl=data["d1"]["planets"]; da=data["dasha"]
    print("\n"+"═"*42); print("🔱 DB11-DIVYA BRAHMA ENGINE v11.0"); print("   Brihat Jataka > BPHS > Jataka Martanda | Tribandhu Siddhanta"); print("═"*42)
    print(f"📅 {data['meta']['dob']} | 🕐 {data['meta']['tob']} | 📍 {data['meta']['place']}"); print(f"🌐 {data['meta']['ayanamsha']}"); print(sep)
    print(f"⬆️  లగ్నం: {l['rashi_te']} ({l['degrees']}°)"); print(f"✨ నక్షత్రం: {l['nakshatra']} పాద {l['pada']}"); print(f"👑 లగ్నాధిపతి: {l['lord_te']}"); print(f"🎯 ద్రేష్కాణ: {l['decanate_quality']['description']}"); print(f"🌞 సూర్య లగ్నం: {data['special_lagnas']['surya_lagna_te']}"); print(f"🌙 చంద్ర లగ్నం: {data['special_lagnas']['chandra_lagna_te']}")
    # ADD-2 display
    vl=data.get("vishesa_lagnas",{})
    print(f"⭐ హోరా లగ్నం: {vl.get('hora_lagna',{}).get('rashi_te','?')} | భావ లగ్నం: {vl.get('bhava_lagna',{}).get('rashi_te','?')} | ఘటి లగ్నం: {vl.get('ghati_lagna',{}).get('rashi_te','?')}")
    # ADD-1 display
    md=data.get("mandi",{})
    print(f"🌑 మాంది: {md.get('rashi_te','?')} {md.get('degrees',0):.2f}° | నక్షత్రం: {md.get('nakshatra','?')} పాద {md.get('pada','?')}")
    print(sep)
    print("🪐 గ్రహాలు:")
    for key in ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]:
        p=pl[key]; ret=" (వక్ర)" if p["is_retrograde"] else ""; vg=" ⭐" if p["vargottama"] else ""; cb=" 🔥" if p["is_combust"] else ""
        # ADD-7 avastha
        av=data.get("graha_avastha",{}).get(key,{}).get("avastha","")
        av_short = av.split("(")[0].strip() if av else ""
        print(f"  {p['emoji']} {p['name_te']:<10}: {p['rashi_te']}, భావం {p['bhava']:>2} | {p['nakshatra']} పాద{p['pada']} | {p['strength']}{ret}{vg}{cb} [{av_short}]")
    print(sep); print("🏠 భావ చక్రం:")
    for i in range(1,13): print(f"  భావం {i:>2}: {', '.join(data['d1']['bhava_chart'].get(i,[])) or 'ఖాళీ'}")
    print(sep); print(f"📊 D9: {data['D9']['lagna_te']} | D10: {data['D10']['lagna_te']}"); print(sep)
    maha=da["mahadasha"]; antar=da["antardasha"]; prat=da["pratyantar"]
    rik=" [RIKTA⚠️]" if maha.get("rikta_flag") else ""; opp=" [వ్యతిరేక⚠️]" if maha.get("opposite_results_flag") else ""
    print(f"⏳ మహాదశ: {maha['planet_te']} ({maha['start_date']} – {maha['end_date']}){rik}{opp}"); print(f"   🏥 దశ రోగ: {maha.get('dasha_roga','')} (R30)")
    print(f"⏳ అంతర్దశ: {antar['planet_te']} ({antar['start_date']} – {antar['end_date']})")
    print(f"   🌙 Moon quality: {antar.get('moon_position_quality','')} (R21)"); print(f"⏳ ప్రత్యంతర: {prat['planet_te']} ({prat['start_date']} – {prat['end_date']})")
    print(sep); print("🔮 వచ్చే మహాదశలు:")
    for fd in da["future_dashas"]: print(f"  ▶ {fd['planet_te']:<10}: {fd['start_date']} – {fd['end_date']} ({fd['duration_years']} సం.)")
    print(sep)
    fl=data["metadata_enhancement"].get("special_flags",{})
    if fl.get("lagna_bala_triple"): print("✅ R4: లగ్న బలం")
    if fl.get("chandradhiyoga"):    print("✅ R27: చంద్రాధియోగం")
    if fl.get("shakata_yoga"):      print("⚠️  R27: శకట యోగం")
    if fl.get("sunapha_etc"):       print(f"📊 R28: {fl['sunapha_etc']}")
    if fl.get("naisargika_dasha_confirmed"): print("✅ R19: Naisargika confirmed")
    if fl.get("arishta_bhanga_jupiter_strong"): print("✅ R11: అరిష్ట భంగం")
    if fl.get("md_ad_opposite_results"): print(f"⚠️  R23: {fl.get('md_ad_opposite_note','')}")
    # ADD-5 display
    ks=data.get("kala_sarpa",{})
    if ks.get("present"): print(f"🐍 ADD-5: {ks.get('type','')}")
    else: print("✅ ADD-5: కాల సర్ప యోగం లేదు")
    # ADD-6 display
    ck=data.get("chara_karakas",{})
    print(f"👑 ADD-6: Atmakaraka = {ck.get('atmakaraka_te','?')}")
    # ADD-4 display
    py=data.get("pindayu",{})
    print(f"📅 ADD-4: పిండాయు = {py.get('total_years','?')} సంవత్సరాలు (సూచన)")
    # STEP-2 display
    sl_d=data.get("special_lagnas",{})
    print(f"🏠 ఆరూఢ లగ్నం: {sl_d.get('arudha_lagna_te','?')} (భావం {sl_d.get('arudha_lagna_bhava','?')})")
    # STEP-4/8/9 display
    sf=data["metadata_enhancement"].get("special_flags",{})
    if sf.get("pancha_graha_malika_yoga"): print(f"✅ STEP-4: పంచగ్రహమాలిక యోగం ({sf.get('pancha_graha_malika_base','')})")
    print(f"🌟 STEP-4: అధియోగ — {sf.get('adhi_yoga_tag','లేదు')} ({sf.get('adhi_yoga_shubha_count',0)} శుభాలు)")
    if sf.get("bhagya_rajya_adhipati_yoga"): print(f"✅ STEP-9: భాగ్య+రాజ్య యోగం ({sf.get('bhagya_rajya_yoga_type','')})")
    print(f"🏅 STEP-8: ఆరూఢ రాజయోగం — {sf.get('arudha_raja_yoga_tag','?')}")
    print("═"*42)

# ═══════════════════════════════════════════════════════════
# GENERATE SUMMARY — DB8 intact + DB9 additions
# ═══════════════════════════════════════════════════════════
def generate_summary(data):
    lines=[]; sep="─"*42
    d1=data["d1"]; l=d1["lagna"]; pl=d1["planets"]; da=data["dasha"]
    dc=data["dispositor_chain"]; sl=data["special_lagnas"]; fl=data["metadata_enhancement"].get("special_flags",{})
    lines.append("════════════════════════════════════════")
    lines.append("🔱 DB11-DIVYA BRAHMA ENGINE v11.0 — SUMMARY")
    lines.append("Precedence: Brihat Jataka > BPHS (except Shadbala)")
    lines.append("Classical: Brihat Jataka + BPHS + Jataka Martanda")
    lines.append("════════════════════════════════════════")
    lines.append(f"DOB: {data['meta']['dob']} | TOB: {data['meta']['tob']} | Place: {data['meta']['place']}")
    lines.append(f"Ayanamsha: {data['meta']['ayanamsha']}"); lines.append(sep)
    lines.append(f"లగ్నం: {l['rashi_te']} ({l['degrees']}°) | {l['nakshatra']} పాద {l['pada']} | Lord: {l['lord_te']}")
    lines.append(f"ద్రేష్కాణ: {l['decanate_quality']['description']}")
    lines.append(f"సూర్య లగ్నం: {sl['surya_lagna_te']} | చంద్ర లగ్నం: {sl['chandra_lagna_te']}")
    # ADD-2
    vl=data.get("vishesa_lagnas",{})
    lines.append(f"హోరా లగ్నం: {vl.get('hora_lagna',{}).get('rashi_te','?')} | భావ లగ్నం: {vl.get('bhava_lagna',{}).get('rashi_te','?')} | ఘటి లగ్నం: {vl.get('ghati_lagna',{}).get('rashi_te','?')}")
    # ADD-1
    md=data.get("mandi",{})
    lines.append(f"మాంది: {md.get('rashi_te','?')} {md.get('degrees',0):.2f}° | {md.get('nakshatra','?')} పాద {md.get('pada','?')}")
    lines.append(sep); lines.append("గ్రహాలు (D1):")
    for key in ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]:
        p=pl[key]; ret="(వక్ర)" if p["is_retrograde"] else ""; vg="⭐" if p["vargottama"] else ""; cb="🔥" if p["is_combust"] else ""
        lines.append(f"  {p['emoji']} {p['name_te']:<10}: {p['rashi_te']:<12} భావం {p['bhava']:>2} | {p['strength']} {ret}{vg}{cb}")
        if key not in ("rahu","ketu"):
            av=data.get("graha_avastha",{}).get(key,{}).get("avastha","")
            lines.append(f"     ధాతు:{p.get('dhatu','')} | దోష:{p.get('dosha','')} | {p.get('aarohi_avrohi','')} | Satyacharya:{p.get('satyacharya_multiplier',1)}x | అవస్థ:{av}")
    lines.append(sep); lines.append("భావ చక్రం:")
    for i in range(1,13): lines.append(f"  భావం {i:>2}: {', '.join(d1['bhava_chart'].get(i,[])) or 'ఖాళీ'}")
    lines.append(sep); lines.append("వర్గ లగ్నాలు:")
    DM={"D2":"హోర","D3":"ద్రేష్కాణ","D4":"చతుర్థాంశ","D7":"సప్తాంశ","D8":"అష్టమాంశ","D9":"నవాంశ","D10":"దశాంశ","D12":"ద్వాదశాంశ","D16":"షోడశాంశ","D20":"వింశాంశ","D24":"చతుర్వింశాంశ","D27":"భాంశ","D30":"త్రింశాంశ","D40":"ఖవేదాంశ","D45":"అక్షవేదాంశ","D60":"షష్టాంశ"}
    for dn,desc in DM.items():
        dc2=data.get(dn,{})
        if dc2: lines.append(f"  {dn:<4} ({desc:<12}): {dc2.get('lagna_te','?')}")
    lines.append(sep)
    maha=da["mahadasha"]; antar=da["antardasha"]; prat=da["pratyantar"]
    rik=" [RIKTA]" if maha.get("rikta_flag") else ""; opp=" [వ్యతిరేక]" if maha.get("opposite_results_flag") else ""
    lines.append(f"మహాదశ: {maha['planet_te']} ({maha['start_date']} – {maha['end_date']}){rik}{opp}")
    lines.append(f"  దశ రోగ: {maha.get('dasha_roga','')} (R30)")
    f4=maha.get("dasha_4factor",{})
    if f4: lines.append(f"  4-factor: {f4.get('natural_signification','')} | {f4.get('house','')} | {f4.get('sign','')} (R22)")
    lines.append(f"అంతర్దశ: {antar['planet_te']} ({antar['start_date']} – {antar['end_date']})")
    lines.append(f"  Moon quality: {antar.get('moon_position_quality','')} (R21) | దశ రోగ: {antar.get('dasha_roga','')} (R30)")
    lines.append(f"ప్రత్యంతర: {prat['planet_te']} ({prat['start_date']} – {prat['end_date']})")
    lines.append("వచ్చే మహాదశలు:")
    for fd in da["future_dashas"]: lines.append(f"  ▶ {fd['planet_te']:<10}: {fd['start_date']} – {fd['end_date']} ({fd['duration_years']} సం.)")
    lines.append(sep)
    mc=dc.get("master_chain",{})
    lines.append(f"Dispositor Chain: {dc.get('lagna_lord','?')}")
    lines.append(f"  Chain: {' → '.join(mc.get('chain',[]))} | Loop: {mc.get('loop_type','?')}")
    lines.append(sep); lines.append("బృహత్ జాతక + BPHS నియమాలు:")
    if fl.get("lagna_bala_triple"): lines.append("  ✅ R4: లగ్న బలం")
    if fl.get("chandradhiyoga"): lines.append("  ✅ R27: చంద్రాధియోగం")
    if fl.get("shakata_yoga"): lines.append("  ⚠️  R27: శకట యోగం")
    if fl.get("sunapha_etc"): lines.append(f"  📌 R28: {fl['sunapha_etc']}")
    if fl.get("naisargika_dasha_confirmed"): lines.append("  ✅ R19: Naisargika confirmed")
    if fl.get("arishta_bhanga_jupiter_strong"): lines.append("  ✅ R11: అరిష్ట భంగం")
    if fl.get("md_ad_opposite_results"): lines.append(f"  ⚠️  R23: {fl.get('md_ad_opposite_note','')}")
    lines.append(f"  💼 R25: వృత్తి — {fl.get('profession_lord','?')} ({fl.get('profession_source','')})")
    lines.append(f"  🤰 R10: {fl.get('conception_difficulty','')}")
    # ADD-5
    ks=data.get("kala_sarpa",{})
    lines.append(f"  🐍 ADD-5 కాల సర్ప: {ks.get('type','లేదు')}")
    # ADD-6
    ck=data.get("chara_karakas",{})
    lines.append(f"  👑 ADD-6 Atmakaraka: {ck.get('atmakaraka_te','?')}")
    ak_karakas = ck.get("karakas",{})
    for p,kd in ak_karakas.items():
        lines.append(f"    {kd.get('karaka_short','')}: {kd.get('planet_te','')} ({kd.get('degrees',0):.2f}°)")
    # ADD-4
    py=data.get("pindayu",{})
    lines.append(f"  📅 ADD-4 పిండాయు: {py.get('total_years','?')} సంవత్సరాలు")
    # STEP-2
    sl_d=data.get("special_lagnas",{})
    lines.append(f"  🏠 STEP-2 ఆరూఢ లగ్నం: {sl_d.get('arudha_lagna_te','?')} (భావం {sl_d.get('arudha_lagna_bhava','?')})")
    # STEP-4/8/9
    sf2=data["metadata_enhancement"].get("special_flags",{})
    lines.append(f"  🌟 STEP-4 అధియోగ: {sf2.get('adhi_yoga_tag','లేదు')} ({sf2.get('adhi_yoga_shubha_count',0)} శుభాలు)")
    if sf2.get("pancha_graha_malika_yoga"): lines.append(f"  ✅ STEP-4 పంచగ్రహమాలిక: {sf2.get('pancha_graha_malika_base','')}")
    if sf2.get("bhagya_rajya_adhipati_yoga"): lines.append(f"  ✅ STEP-9 భాగ్య+రాజ్య యోగం: {sf2.get('bhagya_rajya_yoga_type','')}")
    lines.append(f"  🏅 STEP-8 ఆరూఢ రాజయోగం: {sf2.get('arudha_raja_yoga_tag','?')}")
    # STEP-3 bhava bala summary
    lines.append(sep); lines.append("STEP-3 భావ బల సంక్షిప్తం:")
    bb=data.get("bhava_bala",{})
    for bn in range(1,13):
        bbd=bb.get(bn,{})
        lines.append(f"  భావం {bn:>2}: {bbd.get('overall','?')} | అధిపతి:{bbd.get('adhipati_te','?')} {bbd.get('adhipati_strength','?')} | కారకుడు:{bbd.get('karaka_te','?')} {bbd.get('karaka_strength','?')}")
    # ADD-3
    lines.append(sep); lines.append("ADD-3 పంచధా మైత్రి (ముఖ్యమైన గ్రహాలు):")
    pm=data.get("panchadha_maitri",{})
    for p1 in ["sun","moon","mars","mercury","jupiter","venus","saturn"]:
        row = pm.get(p1,{})
        parts = [f"{PLANET_TE.get(p2,'?')}={v.get('panchadha','?').split('(')[0].strip()}" for p2,v in row.items()]
        lines.append(f"  {PLANET_TE.get(p1,'?')}: {' | '.join(parts[:3])}")
    # ADD-8 gochara summary
    lines.append(sep); lines.append("ADD-8 గోచర వర్తమాన స్థానాలు:")
    gc=data.get("gochara",{}).get("planets",{})
    for key in ["sun","moon","mars","mercury","jupiter","venus","saturn","rahu","ketu"]:
        gp=gc.get(key,{})
        active="✅" if gp.get("in_result_zone") else "  "
        lines.append(f"  {active} {PLANET_TE.get(key,'?'):<10}: {gp.get('current_rashi_te','?')} {gp.get('current_degrees',0):.1f}° | {gp.get('transit_stage','')}")
    lines.append("════════════════════════════════════════")
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════
# CONFIRMATION + MAIN — DB8 intact, version string updated
# ═══════════════════════════════════════════════════════════
def get_confirmation():
    print("\n"+"─"*42); print("✅ అవును / yes / ok  |  ❌ కాదు / no"); print("─"*42)
    while True:
        try:
            r=input("మీ జవాబు: ").strip().lower()
        except EOFError:
            r="అవును"
        if r in {w.lower() for w in CONFIRM_WORDS}: print("\n✅ నిర్ధారించబడింది\n"); return True
        if r in {w.lower() for w in WRONG_WORDS}:
            try:
                c=input("సరైన వివరాలు: ").strip(); print(f"✏️  {c}")
                if input("ఇప్పుడు సరిగ్గా? (అవును/కాదు): ").strip().lower() in {w.lower() for w in CONFIRM_WORDS}: return True
            except EOFError:
                return True
            continue
        print("  అవును / కాదు అని చెప్పండి")


# ═══════════════════════════════════════════════════════════
# DB10 ADD-10: లఘు స్ఫుటము & భావ స్ఫుటము
# Source: జాతక మార్తాండము Laghu Sputamu & Bhava Sputamu PDF
# ═══════════════════════════════════════════════════════════

def calc_bhava_sputamu(lagna_lon, sun_lon, birth_dt):
    """
    భావ స్ఫుటము calculation — Jataka Martanda method
    తను భావము = లగ్న స్ఫుటమే
    నాటము ద్వారా దశమ, చతుర్థ నిర్ణయించి
    వస్తాంశ ద్వారా 12 భావాలు + 12 సంధులు
    """
    # Step 1: తను భావము = లగ్న స్ఫుటమే
    tanu_bhava = lagna_lon

    # Step 2: నాట గణన
    birth_hour = birth_dt.hour + birth_dt.minute/60.0 + birth_dt.second/3600.0
    midday = 12.0
    if birth_hour < midday:
        nata_degrees = (midday - birth_hour) * 15.0
        is_purva = True  # పూర్వకపాల (AM)
    else:
        nata_degrees = (birth_hour - midday) * 15.0
        is_purva = False  # అపరకపాల (PM)

    # Step 3: దశమ భావము (RULE_NATA_4, RULE_NATA_5)
    if is_purva:
        dasham_bhava = (sun_lon - nata_degrees) % 360
    else:
        dasham_bhava = (sun_lon + nata_degrees) % 360

    # Step 4: చతుర్థ భావము (దశమ + 180°)
    chaturtha_bhava = (dasham_bhava + 180.0) % 360

    # Step 5: సప్తమ భావము (లగ్న + 180°)
    saptama_bhava = (tanu_bhava + 180.0) % 360

    # Step 6: వస్తాంశ (RULE_BHAVA_1)
    diff = (chaturtha_bhava - tanu_bhava) % 360
    vastamsha = diff / 6.0

    # Step 7: 12 భావ మధ్యాలు
    bhava_madhyas = [(tanu_bhava + i * vastamsha) % 360 for i in range(12)]

    # Step 8: 12 సంధులు (consecutive bhava midpoints)
    sandhis = []
    for i in range(12):
        a = bhava_madhyas[i]
        b = bhava_madhyas[(i+1) % 12]
        if abs(b - a) > 180:
            s = ((a + b + 360) / 2) % 360
        else:
            s = (a + b) / 2
        sandhis.append(round(s % 360, 4))

    bhava_names_te = {
        1:"తను (లగ్న)", 2:"ధన", 3:"భ్రాతృ", 4:"మాతృ",
        5:"పుత్ర", 6:"శత్రు", 7:"కళత్ర", 8:"రంధ్ర",
        9:"ధర్మ", 10:"కర్మ (దశమ)", 11:"లాభ", 12:"వ్యయ"
    }

    result = {
        "vastamsha_degrees": round(vastamsha, 4),
        "nata_degrees": round(nata_degrees, 4),
        "nata_type": "పూర్వకపాల (AM)" if is_purva else "అపరకపాల (PM)",
        "tanu_bhava_lon": round(tanu_bhava, 4),
        "dasham_bhava_lon": round(dasham_bhava, 4),
        "chaturtha_bhava_lon": round(chaturtha_bhava, 4),
        "saptama_bhava_lon": round(saptama_bhava, 4),
        "bhava_madhyas": {},
        "sandhis": {},
    }

    for i in range(12):
        bn = i + 1
        lon = bhava_madhyas[i]
        r = int(lon // 30) + 1
        result["bhava_madhyas"][str(bn)] = {
            "name_te": bhava_names_te[bn],
            "longitude": round(lon, 4),
            "rashi_num": r,
            "rashi_te": RASHI_TE.get(r, "?"),
            "degrees_in_rashi": round(lon % 30, 4)
        }
        s_lon = sandhis[i]
        sr = int(s_lon // 30) + 1
        result["sandhis"][str(bn)] = {
            "longitude": s_lon,
            "rashi_num": sr,
            "rashi_te": RASHI_TE.get(sr, "?"),
            "degrees_in_rashi": round(s_lon % 30, 4),
            "label": f"భావ {bn} → భావ {bn%12+1} మధ్య సంధి"
        }

    return result


def assign_planets_bhava_sputamu(bhava_sputamu, sid_positions):
    """
    RULE_SANDHI_6: భావ స్ఫుటము ప్రకారం గ్రహ భావ నిర్ణయం
    Method: nearest bhava madhya — angular distance minimum
    Jataka Martanda RULE_SANDHI_10: రాశిచక్రం ≠ భావచక్రం
    """
    bhava_madhyas = bhava_sputamu.get("bhava_madhyas", {})
    sandhis = bhava_sputamu.get("sandhis", {})
    assignments = {}

    def angular_diff(a, b):
        d = abs(a - b) % 360
        return min(d, 360 - d)

    def in_sandhi(p_lon, bhava_num):
        """RULE_SANDHI_3: గ్రహం సంధిలో ఉంటే ఫలం ఈయదు"""
        s_lon = sandhis.get(str(bhava_num), {}).get("longitude", -1)
        return angular_diff(p_lon, s_lon) < 1.0  # 1° sandhi zone

    for planet, p_lon_raw in sid_positions.items():
        p_lon = p_lon_raw % 360

        # Find nearest bhava madhya
        best_bhava = None
        best_diff = 999.0
        for i in range(1, 13):
            madhya_lon = bhava_madhyas.get(str(i), {}).get("longitude", -1)
            if madhya_lon < 0:
                continue
            diff = angular_diff(p_lon, madhya_lon)
            if diff < best_diff:
                best_diff = diff
                best_bhava = i

        # Check if in sandhi zone
        sandhi_flag = in_sandhi(p_lon, best_bhava) if best_bhava else False

        assignments[planet] = {
            "bhava_sputamu": best_bhava,
            "angular_diff_degrees": round(best_diff, 2),
            "in_sandhi_zone": sandhi_flag,
            "note": "సంధి — ఫలం స్వల్పం" if sandhi_flag else "భావ స్ఫుటము ప్రకారం"
        }

    return assignments


# ═══════════════════════════════════════════════════════════
# DB10 ADD-11: BRIDGE LAYER
# KB2 లగ్న section + KB1 common + V25.1 → combined prompt
# ═══════════════════════════════════════════════════════════

def _load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"# File not found: {path}"

# ─── BPHS_AD EMBEDDED DATA (BPHS Ch.52-60 Antardasha Phala) ───
# External file dependency లేకుండా engine లోనే embed చేయబడింది
# Source files: BPHS_AD_Surya/Chandra/Kuja/Rahu/Budha/Guru/Shani/Ketu/Shukra.txt
def _get_bphs_ad_embedded():
    import os as _os
    _base = _os.path.dirname(_os.path.abspath(__file__))
    _files = {
        "Surya":"BPHS_AD_Surya.txt","Chandra":"BPHS_AD_Chandra.txt",
        "Kuja":"BPHS_AD_Kuja.txt","Rahu":"BPHS_AD_Rahu.txt",
        "Budha":"BPHS_AD_Budha.txt","Guru":"BPHS_AD_Guru.txt",
        "Shani":"BPHS_AD_Shani.txt","Ketu":"BPHS_AD_Ketu.txt",
        "Shukra":"BPHS_AD_Shukra.txt",
    }
    _data = {}
    for _name, _fname in _files.items():
        _path = _os.path.join(_base, _fname)
        if _os.path.exists(_path):
            with open(_path, 'r', encoding='utf-8') as _f:
                _data[_name] = _f.read()
    return _data

# Module-level cache — engine start అయినప్పుడు ఒకసారే load అవుతుంది
_BPHS_AD_CACHE = None

def _bphs_ad_lookup(md_name, rule_key):
    """MD planet name (e.g. 'Rahu') + rule_key (e.g. 'RULE_RAHU_MD_KETU_AD')
    → matching rule text లేదా '' return చేస్తుంది."""
    global _BPHS_AD_CACHE
    if _BPHS_AD_CACHE is None:
        _BPHS_AD_CACHE = _get_bphs_ad_embedded()
    text = _BPHS_AD_CACHE.get(md_name, "")
    if not text:
        return ""
    rule_lines = []
    in_rule = False
    for line in text.splitlines():
        if line.startswith(rule_key):
            in_rule = True
        elif in_rule and line.startswith("RULE_") and not line.startswith(rule_key):
            break
        elif in_rule and line.startswith("\u2550" * 8):
            break
        elif in_rule and line.startswith("\u2500" * 8):
            break
        if in_rule:
            rule_lines.append(line)
    return "\n".join(rule_lines)

def extract_kb2_lagna(kb2_text, lagna_name):
    """
    KB2 నుండి [KB2.lagna] section extract
    
    PATH RECONCILIATION (WARN-3 fix):
    V26 pointer format  → KB2 actual format
    KB_Lagna/[lagna].json → [KB2.lagna_name] section
    
    V26 లో ఉన్న pointers:
      ⟹ KB_Lagna/[lagna_rashi].json → swabhavam    = KB2.[lagna].swabhavam
      ⟹ KB_Lagna/[lagna_rashi].json → yogakara_sthanas = KB2.[lagna].yogakara.*
      ⟹ KB_Lagna/[lagna_rashi].json → badhaka_maraka = KB2.[lagna].badhaka + maraka
    
    DB10 bridge layer ఈ mapping automatically handle చేస్తుంది —
    full lagna section extract చేస్తే అన్ని sub-keys included అవుతాయి.
    """
    import re
    tag = f"[KB2.{lagna_name}]"
    start = kb2_text.find(tag)
    if start == -1:
        return f"# KB2 లో {lagna_name} section లేదు"
    search = start + len(tag)
    ends = []
    n1 = kb2_text.find("\n[KB2.", search)
    n2 = kb2_text.find("\n════", search)
    if n1 != -1: ends.append(n1)
    if n2 != -1: ends.append(n2)
    end = min(ends) if ends else len(kb2_text)
    return kb2_text[start:end].strip()


def v26_pointer_to_kb2_key(pointer_path, lagna_name):
    """
    WARN-3 Fix: V26 pointer path → KB2 actual key mapping
    
    V26 pointer: "KB_Lagna/[lagna_rashi].json → swabhavam"
    KB2 key:     "KB2.[lagna_name].swabhavam"
    
    Usage: DB10 bridge layer లో V26 pointers resolve చేయడానికి
    """
    # Path mapping table
    PATH_MAP = {
        "KB_Lagna/[lagna_rashi].json":     f"KB2.{lagna_name}",
        "KB_Lagna/[lagna].json":           f"KB2.{lagna_name}",
        "KB1_common.swabhavam":            f"KB2.{lagna_name}.swabhavam",
        "KB1_common.bhava_karakatvam":     "KB1.bhava_karakatvam",
        "KB1_common.graha_karakatvam":     "KB1.graha_karakatvam",
        "KB1_common.adhipatya":            f"KB2.{lagna_name}.adhipatya_shubha",
        "KB1_common.anishta_yogas":        "KB1.anishta_yogas",
        "KB1_common.rajayoga_sutras":      "KB1.rajayoga_sutras",
        "KB1_common.gochara_phala":        "KB1.gochara_phala",
        "KB1_common.tara_bala_meanings":   "KB1.tara_bala_meanings",
        "KB1_common.sharira_bhava_map":    "KB1.sharira_bhava_map",
        "KB1_common.matru_pitru_ayush":    "KB1.matru_pitru_ayush",
        "KB1_common.vritti_navamsha":      "KB1.vritti_navamsha",
        "KB1_common.indu_lagna":           "KB1.indu_lagna",
        "KB_Yoga/yogamulu":                "KB_Yoga.yogamulu",
    }
    return PATH_MAP.get(pointer_path, f"# UNKNOWN: {pointer_path}")

def extract_kb1_common(kb2_text):
    """KB2 PART-1 (KB1) extract — common reference data"""
    start = kb2_text.find("PART-1:")
    end = kb2_text.find("PART-2:")
    if start != -1 and end != -1:
        return kb2_text[start:end].strip()
    return ""

def build_analysis_prompt(data, script_dir):
    """
    DB10 Bridge Layer:
    DB10 JSON + V26.0 + KB2 lagna → combined analysis prompt
    """
    import os, json
    lagna_name = data.get("d1",{}).get("lagna",{}).get("rashi_te") or data.get("lagna",{}).get("rashi_te","మేషం")

    kb2_path = os.path.join(script_dir, "KB2.txt")
    v25_path = os.path.join(script_dir, "V27MasterPrompt.txt")

    v25 = _load_file(v25_path)
    kb2_text = _load_file(kb2_path)
    kb1_common = extract_kb1_common(kb2_text)

    # Lagna file auto-pick — same folder లో KB_[lagna].txt ఉంటే వాడు
    # lagna_name లో space ఉండవచ్చు — strip చేయి
    lagna_name_clean = lagna_name.strip()
    lagna_kb_path = os.path.join(script_dir, f"KB_{lagna_name_clean}.txt")
    if os.path.exists(lagna_kb_path):
        kb2_lagna = _load_file(lagna_kb_path)
        lagna_source = f"KB_{lagna_name_clean}.txt"
    else:
        # Try without KB_ prefix also
        alt_path = os.path.join(script_dir, f"{lagna_name_clean}.txt")
        if os.path.exists(alt_path):
            kb2_lagna = _load_file(alt_path)
            lagna_source = f"{lagna_name_clean}.txt"
        else:
            kb2_lagna = extract_kb2_lagna(kb2_text, lagna_name)
            lagna_source = "KB2.txt"

    lines = []
    lines.append("═" * 72)
    lines.append(f"🔱 DIVYA BRAHMA PRAVAHA V27.0 + DB11 — {lagna_name} లగ్న విచారణ")
    lines.append("═" * 72)
    lines.append("")
    # PATH RECONCILIATION NOTE (WARN-3 fix)
    lines.append("## PATH MAPPING (V27 pointer → KB2 actual)")
    lines.append(f"# V27: ⟹ KB_Lagna/[lagna_rashi].json → [key]")
    lines.append(f"# KB2: [KB2.{lagna_name}].key (ఈ file లో PART-C లో ఉంది)")
    lines.append(f"# V26: ⟹ KB1_common.[section] → KB2 PART-B లో ఉంది")
    lines.append("")
    lines.append("## PART-A: ANALYSIS PROMPT (V27.0)")
    lines.append(v25)
    lines.append("")
    lines.append("## PART-B: KB1 COMMON REFERENCE DATA (సంక్షిప్తం)")
    lines.append(kb1_common[:8000])  # First 8000 chars
    lines.append("")
    lines.append(f"## PART-C: LAGNA DATA — {lagna_name} (Source: {lagna_source})")
    lines.append(kb2_lagna)
    lines.append("")

    # ─── PART-C2: Current Mahadasha file auto-pick ───
    md_planet_te = data.get("dasha", {}).get("mahadasha", {}).get("planet_te", "")
    if md_planet_te:
        md_file_path = os.path.join(script_dir, f"MD_{md_planet_te}.txt")
        if os.path.exists(md_file_path):
            md_content = _load_file(md_file_path)
            lines.append(f"## PART-C2: MAHADASHA DATA — {md_planet_te} మహాదశ (Source: MD_{md_planet_te}.txt)")
            lines.append(md_content)
            lines.append("")

    # PART-C3: Bhava Lord MD rule auto-pick (Phaladeepika Adhyaya XX)
    adh20_path = os.path.join(script_dir, "KB_Adh20_BhavaLord_MD.txt")
    if os.path.exists(adh20_path):
        adh20_text = _load_file(adh20_path)
        md_planet_en = data.get("dasha", {}).get("mahadasha", {}).get("planet_en", "")
        lr_num = data.get("d1", {}).get("lagna", {}).get("rashi_num", 1)
        d1p_local = data.get("d1", {}).get("planets", {})
        RLORD = {1:"mars",2:"venus",3:"mercury",4:"moon",5:"sun",6:"mercury",
                 7:"venus",8:"mars",9:"jupiter",10:"saturn",11:"saturn",12:"jupiter"}
        owned_bhava = 0
        if md_planet_en in ("rahu", "ketu"):
            # రాహు/కేతు = shadow planets
            # వారు ఏ రాశిలో ఉన్నారో → ఆ రాశి lord → ఆ lord ఏ bhava లో ఉన్నాడో
            rk_rashi = d1p_local.get(md_planet_en, {}).get("rashi_num", 1)
            rk_dispositor = RLORD.get(rk_rashi, "mars")
            # dispositor ఏ bhava లో ఉన్నాడో తీసుకో (lord అయిన bhava కాదు)
            owned_bhava = d1p_local.get(rk_dispositor, {}).get("bhava", 0)
        else:
            for b in range(1, 13):
                br = ((lr_num - 1 + b - 1) % 12) + 1
                if RLORD.get(br) == md_planet_en:
                    owned_bhava = b
                    break
        if owned_bhava > 0:
            rule_key = "RULE_BHAVA" + str(owned_bhava) + "_MD"
            rule_lines = []
            in_rule = False
            for line in adh20_text.splitlines():
                if line.startswith(rule_key):
                    in_rule = True
                elif in_rule and line.startswith("RULE_BHAVA") and not line.startswith(rule_key):
                    break
                elif in_rule and "=" * 10 in line:
                    break
                if in_rule:
                    rule_lines.append(line)
            if rule_lines:
                hdr = "## PART-C3: BHAVA LORD MD RULE — " + md_planet_te + " = " + str(owned_bhava) + "వ భావేశుడు (Phaladeepika Adh.XX)"
                lines.append(hdr)
                lines.append("\n".join(rule_lines))
                lines.append("")


    # PART-C4: AD lord analysis — MD_[AD].txt + Adh20 RULE_BHAVA[n]_MD
    ad_planet_te = data.get("dasha",{}).get("antardasha",{}).get("planet_te","")
    ad_planet_en = data.get("dasha",{}).get("antardasha",{}).get("planet_en","")
    if ad_planet_en and ad_planet_en != md_planet_en:
        # AD MD file pickup
        ad_md_path = os.path.join(script_dir, "MD_" + ad_planet_te + ".txt")
        if os.path.exists(ad_md_path):
            ad_md_content = _load_file(ad_md_path)
            lines.append("## PART-C4: ANTARDASHA DATA — " + ad_planet_te + " అంతర్దశ (Source: MD_" + ad_planet_te + ".txt)")
            lines.append(ad_md_content)
            lines.append("")

        # AD lord Adh20 rule
        if os.path.exists(adh20_path):
            # రాహు/కేతు కి dispositor logic
            RLORD2 = {1:"mars",2:"venus",3:"mercury",4:"moon",5:"sun",6:"mercury",
                      7:"venus",8:"mars",9:"jupiter",10:"saturn",11:"saturn",12:"jupiter"}
            if ad_planet_en in ("rahu","ketu"):
                ad_rashi = d1p_local.get(ad_planet_en,{}).get("rashi_num",1)
                ad_dispositor = RLORD2.get(ad_rashi,"mars")
                ad_owned_bhava = d1p_local.get(ad_dispositor,{}).get("bhava",0)
            else:
                ad_owned_bhava = 0
                for b in range(1,13):
                    br = ((lr_num-1+b-1)%12)+1
                    if RLORD2.get(br) == ad_planet_en:
                        ad_owned_bhava = b
                        break
            if ad_owned_bhava > 0:
                ad_rule_key = "RULE_BHAVA" + str(ad_owned_bhava) + "_MD"
                ad_rule_lines = []
                in_rule = False
                for line in adh20_text.splitlines():
                    if line.startswith(ad_rule_key):
                        in_rule = True
                    elif in_rule and line.startswith("RULE_BHAVA") and not line.startswith(ad_rule_key):
                        break
                    elif in_rule and "="*10 in line:
                        break
                    if in_rule:
                        ad_rule_lines.append(line)
                if ad_rule_lines:
                    hdr2 = "## PART-C4B: AD BHAVA LORD RULE — " + ad_planet_te + " = " + str(ad_owned_bhava) + "వ భావేశుడు (Phaladeepika Adh.XX)"
                    lines.append(hdr2)
                    lines.append("\n".join(ad_rule_lines))
                    lines.append("")


    # ─── PART-C4C: BPHS Antardasha Rules auto-pick ───
    # MD + AD combination → BPHS_AD embedded data నుండి RULE_[MD]_MD_[AD]_AD pickup
    # Source: BPHS Chapters 52-60 (Vimshottari Antardasha Phala)
    # External file అక్కర్లేదు — engine లోనే embedded (_bphs_ad_lookup)
    BPHS_MD_MAP = {
        "sun":     "Surya",
        "moon":    "Chandra",
        "mars":    "Kuja",
        "mercury": "Budha",
        "jupiter": "Guru",
        "venus":   "Shukra",
        "saturn":  "Shani",
        "rahu":    "Rahu",
        "ketu":    "Ketu",
    }
    BPHS_RULE_MAP = {
        "sun":     "SURYA",
        "moon":    "CHANDRA",
        "mars":    "KUJA",
        "mercury": "BUDHA",
        "jupiter": "GURU",
        "venus":   "SHUKRA",
        "saturn":  "SHANI",
        "rahu":    "RAHU",
        "ketu":    "KETU",
    }
    md_planet_en_c4c  = data.get("dasha", {}).get("mahadasha",  {}).get("planet_en", "")
    ad_planet_en_c4c  = data.get("dasha", {}).get("antardasha", {}).get("planet_en", "")
    md_planet_te_c4c  = data.get("dasha", {}).get("mahadasha",  {}).get("planet_te", "")
    ad_planet_te_c4c  = data.get("dasha", {}).get("antardasha", {}).get("planet_te", "")

    if md_planet_en_c4c and ad_planet_en_c4c:
        rule_key_c4c = (
            "RULE_"
            + BPHS_RULE_MAP.get(md_planet_en_c4c, "") + "_MD_"
            + BPHS_RULE_MAP.get(ad_planet_en_c4c, "") + "_AD"
        )
        md_name_c4c = BPHS_MD_MAP.get(md_planet_en_c4c, "")
        c4c_text = _bphs_ad_lookup(md_name_c4c, rule_key_c4c)
        if c4c_text:
            hdr_c4c = (
                "## PART-C4C: BPHS ANTARDASHA RULE — "
                + md_planet_te_c4c + " MD + " + ad_planet_te_c4c + " AD"
                + " (" + rule_key_c4c + ")"
                + " | Source: BPHS Ch.52-60"
            )
            lines.append(hdr_c4c)
            lines.append(c4c_text)
            lines.append("")

    # ─── PART-X: Adhyaya 8 Graha Bhava auto-pick ───
    # 9 గ్రహాలు × 12 bhavas — Phaladeepika Adhyaya VIII
    GRAHA_ADH8_MAP = {
        "sun":"Surya","moon":"Chandra","mars":"Kuja","mercury":"Budha",
        "jupiter":"Guru","venus":"Shukra","saturn":"Shani","rahu":"Rahu","ketu":"Ketu"
    }
    adh8_rules = []
    d1p_all = data.get("d1",{}).get("planets",{})
    for planet_en, file_suffix in GRAHA_ADH8_MAP.items():
        adh8_file = os.path.join(script_dir, f"KB_Adh8_{file_suffix}.txt")
        if not os.path.exists(adh8_file):
            continue
        adh8_text = _load_file(adh8_file)
        p_bhava = d1p_all.get(planet_en,{}).get("bhava",0)
        if p_bhava == 0:
            continue
        rule_key = f"RULE_{file_suffix.upper()}_BHAVA{p_bhava}"
        rule_lines = []
        in_rule = False
        for line in adh8_text.splitlines():
            if line.startswith(rule_key):
                in_rule = True
            elif in_rule and line.startswith("RULE_") and not line.startswith(rule_key):
                break
            elif in_rule and "="*10 in line:
                break
            if in_rule:
                rule_lines.append(line)
        if rule_lines:
            p_te = d1p_all.get(planet_en,{}).get("name_te", planet_en)
            adh8_rules.append(f"### {p_te} ({planet_en}) — {p_bhava}వ భావంలో")
            adh8_rules.extend(rule_lines)
            adh8_rules.append("")
    if adh8_rules:
        lines.append("## PART-X: GRAHA BHAVA PHALA (Phaladeepika Adh.VIII)")
        lines.append("\n".join(adh8_rules))
        lines.append("")

    # ─── PART-R: గ్రహములద్వాదశ రాసుల ఉండగా ఫలములు auto-pickup ───
    rashi_files = [
        "గ్రహములద్వాదశ _రాసుల ఉండగా _ఫలములు .txt",
        "గ్రహములద్వాదశ_రాసుల_ఉండగా_ఫలములు.txt",
    ]
    rashi_kb_text = None
    for rfname in rashi_files:
        rfpath = os.path.join(script_dir, rfname)
        if os.path.exists(rfpath):
            rashi_kb_text = _load_file(rfpath)
            break
    if rashi_kb_text:
        RASHI_SUFFIX = {
            "sun":"SURYA","moon":"CHANDRA","mars":"KUJA","mercury":"BUDHA",
            "jupiter":"GURU","venus":"SHUKRA","saturn":"SHANI","rahu":"RAHU","ketu":"KETU"
        }
        rashi_rules = []
        for p_en, suffix in RASHI_SUFFIX.items():
            p_rashi = d1p_all.get(p_en,{}).get("rashi_num",0)
            if not p_rashi:
                continue
            rule_key = f"RULE_{suffix}_{p_rashi}"
            for line in rashi_kb_text.splitlines():
                if line.startswith(rule_key):
                    p_te = d1p_all.get(p_en,{}).get("name_te",p_en)
                    rashi_rules.append(f"### {p_te} — {d1p_all.get(p_en,{}).get('rashi_te','')}")
                    rashi_rules.append(line)
                    rashi_rules.append("")
                    break
        if rashi_rules:
            lines.append("## PART-R: GRAHA RASHI PHALA (జాతక మార్తాండం — గ్రహ రాశి ఫలాలు)")
            lines.append("\n".join(rashi_rules))
            lines.append("")


    # ─── PART-Y: Adhyaya 18 Conjunction auto-pick ───
    adh18_path = os.path.join(script_dir, "KB_Adh18_Conjunctions.txt")
    if os.path.exists(adh18_path):
        adh18_text = _load_file(adh18_path)
        # Find all conjunctions in chart
        conj_rules = []
        SUFFIX_MAP = {
            "sun":"SURYA","moon":"CHANDRA","mars":"KUJA","mercury":"BUDHA",
            "jupiter":"GURU","venus":"SHUKRA","saturn":"SHANI","rahu":"RAHU","ketu":"KETU"
        }
        # Check each bhava for multiple planets
        bhava_planets = {}
        for p_en, p_data in d1p_all.items():
            b = p_data.get("bhava", 0)
            if b:
                bhava_planets.setdefault(b, []).append(p_en)

        # For each bhava with 2+ planets, find conjunction rules
        processed = set()
        for bhava, planets in bhava_planets.items():
            if len(planets) < 2:
                continue
            for i in range(len(planets)):
                for j in range(i+1, len(planets)):
                    p1, p2 = planets[i], planets[j]
                    # Try both orders
                    for pa, pb in [(p1,p2),(p2,p1)]:
                        key = "RULE_" + SUFFIX_MAP.get(pa,"") + "_" + SUFFIX_MAP.get(pb,"") + "_CONJ"
                        if key in processed:
                            continue
                        if key in adh18_text:
                            processed.add(key)
                            for line in adh18_text.splitlines():
                                if line.startswith(key):
                                    p1_te = d1p_all.get(pa,{}).get("name_te",pa)
                                    p2_te = d1p_all.get(pb,{}).get("name_te",pb)
                                    conj_rules.append(f"### {p1_te}+{p2_te} (bhava {bhava})")
                                    conj_rules.append(line)
                                    conj_rules.append("")
                                    break

        # Also add Moon aspect rule based on Moon's rashi
        moon_rashi_map = {
            1:"MESHA",2:"VRISHABHA",3:"MITHUNA",4:"KARKATAKA",
            5:"SIMHA",6:"KANYA",7:"TULA",8:"VRISHCHIKA",
            9:"DHANU",10:"MAKARA",11:"KUMBHA",12:"MEENA"
        }
        moon_rashi_num = d1p_all.get("moon",{}).get("rashi_num",0)
        if moon_rashi_num:
            moon_aspect_key = "RULE_CHANDRA_" + moon_rashi_map.get(moon_rashi_num,"") + "_ASPECT"
            if moon_aspect_key in adh18_text:
                for line in adh18_text.splitlines():
                    if line.startswith(moon_aspect_key):
                        moon_te = d1p_all.get("moon",{}).get("rashi_te","")
                        conj_rules.append(f"### చంద్రుడు {moon_te} రాశిలో — aspect effects")
                        conj_rules.append(line)
                        conj_rules.append("")
                        break

        if conj_rules:
            lines.append("## PART-Y: CONJUNCTION & ASPECT EFFECTS (Phaladeepika Adh.XVIII)")
            lines.append("\n".join(conj_rules))
            lines.append("")


    # ─── PART-Z: Dwadasha Bhava Vicharana auto-pickup ───
    # Chart లో occupied bhavas మాత్రమే pickup చేయాలి
    occupied_bhavas = set()
    for p_en, p_data in d1p_all.items():
        b = p_data.get("bhava", 0)
        if b:
            occupied_bhavas.add(b)

    bhava_rules_found = []
    for bhava_num in sorted(occupied_bhavas):
        bhava_file = os.path.join(script_dir, f"KB_Bhava{bhava_num}.txt")
        if os.path.exists(bhava_file):
            bhava_text = _load_file(bhava_file)
            # Planets in this bhava
            planets_in_bhava = [
                d1p_all[p].get("name_te", p)
                for p in d1p_all
                if d1p_all[p].get("bhava") == bhava_num
            ]
            bhava_rules_found.append(f"### {bhava_num}వ భావం ({', '.join(planets_in_bhava)})")
            bhava_rules_found.append(bhava_text)
            bhava_rules_found.append("")

    if bhava_rules_found:
        lines.append("## PART-Z: DWADASHA BHAVA VICHARANA (జాతక మార్తాండం)")
        lines.append("\n".join(bhava_rules_found))
        lines.append("")


    # ─── PART-G: Gochar Transit auto-pickup ───
    gochar_path = os.path.join(script_dir, "KB_Gochar_Transit.txt")
    if os.path.exists(gochar_path):
        gochar_text = _load_file(gochar_path)
        GOCHAR_MAP = {
            "sun":"SURYA","moon":"CHANDRA","mars":"KUJA","mercury":"BUDHA",
            "jupiter":"GURU","venus":"SHUKRA","saturn":"SHANI","rahu":"RAHU","ketu":"RAHU"
        }
        # చంద్ర రాశి నుండి ప్రతి గ్రహం ఏ bhava లో ఉన్నాడో
        moon_rashi = data.get("d1",{}).get("planets",{}).get("moon",{}).get("rashi_num",1)
        gochar_data = data.get("gochar",{}).get("planets",{})
        
        gochar_rules = []
        for p_en, suffix in GOCHAR_MAP.items():
            if p_en == "ketu": continue  # రాహు same గా వాడతాం
            p_gochar = gochar_data.get(p_en, {})
            p_rashi = p_gochar.get("rashi_num", 0)
            if not p_rashi:
                continue
            # చంద్ర రాశి నుండి bhava calculate చేయి
            transit_bhava = ((p_rashi - moon_rashi) % 12) + 1
            rule_key = f"RULE_{suffix}_TRANSIT_BHAVA{transit_bhava}"
            for line in gochar_text.splitlines():
                if line.startswith(rule_key):
                    p_te = d1p_all.get(p_en,{}).get("name_te", p_en)
                    p_rashi_te = p_gochar.get("rashi_te","")
                    gochar_rules.append(f"### {p_te} గోచారం {p_rashi_te} ({transit_bhava}వ bhava నుండి చంద్రుడు)")
                    gochar_rules.append(line)
                    gochar_rules.append("")
                    break

        # Ketu = Rahu rules
        ketu_gochar = gochar_data.get("ketu",{})
        ketu_rashi = ketu_gochar.get("rashi_num",0)
        if ketu_rashi:
            ketu_bhava = ((ketu_rashi - moon_rashi) % 12) + 1
            rule_key = f"RULE_RAHU_TRANSIT_BHAVA{ketu_bhava}"
            for line in gochar_text.splitlines():
                if line.startswith(rule_key):
                    gochar_rules.append(f"### కేతు గోచారం ({ketu_bhava}వ bhava — రాహు rules వర్తిస్తాయి)")
                    gochar_rules.append(line)
                    gochar_rules.append("")
                    break

        # General rules add చేయి
        for line in gochar_text.splitlines():
            if line.startswith("RULE_TRANSIT_DASHA_PRIORITY"):
                gochar_rules.append("### Priority Rule")
                gochar_rules.append(line)
                break

        if gochar_rules:
            lines.append("## PART-G: GOCHAR TRANSIT EFFECTS (Phaladeepika)")
            lines.append("\n".join(gochar_rules))
            lines.append("")


    # ─── PART-AV: గ్రహ అవస్థలు + స్థానాధిపత్య దోషాలు auto-attach ───
    av_files = [
        "గ్రహములకు రాషుల ఒకవిభజన.txt",
        "గ్రహములకు రాశుల ఒక విభజన.txt",
    ]
    av_text = None
    for fname in av_files:
        fpath = os.path.join(script_dir, fname)
        if os.path.exists(fpath):
            av_text = _load_file(fpath)
            av_source = fname
            break

    if av_text:
        # గ్రహ అవస్థలు extract — each graha's avastha based on strength
        av_rules = []

        # AVASTHA rules — graha strength బట్టి relevant rule
        AVASTHA_MAP = {
            "ఉచ్చం": "RULE_AVASTHA_2",
            "మూల త్రికోణం": "RULE_AVASTHA_2",
            "స్వరాశి": "RULE_AVASTHA_3",
            "మిత్ర రాశి": "RULE_AVASTHA_4",
            "నీచం": "RULE_AVASTHA_10",
            "శత్రు రాశి": "RULE_AVASTHA_8",
        }

        for p_en, p_data in d1p_all.items():
            strength = p_data.get("graha_strength", p_data.get("strength",""))
            avastha_key = AVASTHA_MAP.get(strength, "")
            combust = p_data.get("is_combust", False)
            if combust:
                avastha_key = "RULE_AVASTHA_11"  # వికలావస్థ
            if avastha_key:
                for line in av_text.splitlines():
                    if line.startswith(avastha_key):
                        p_te = p_data.get("name_te", p_en)
                        av_rules.append(f"### {p_te} — {strength} ({avastha_key})")
                        av_rules.append(line)
                        av_rules.append("")
                        break

        # స్థానాధిపత్య దోష check — MD + AD lords 6/8 లో ఉన్నారా
        md_en = data.get("dasha",{}).get("mahadasha",{}).get("planet_en","")
        ad_en = data.get("dasha",{}).get("antardasha",{}).get("planet_en","")
        if md_en and ad_en:
            md_bhava = d1p_all.get(md_en,{}).get("bhava",0)
            ad_bhava = d1p_all.get(ad_en,{}).get("bhava",0)
            if md_bhava and ad_bhava:
                diff = abs(md_bhava - ad_bhava)
                if diff in (5, 7):  # 6th or 8th from each other
                    av_rules.append("### ⚠️ స్థానాధిపత్య దోషం detected")
                    for line in av_text.splitlines():
                        if line.startswith("RULE_DOSHA_1"):
                            av_rules.append(line)
                            av_rules.append("")
                            break

        if av_rules:
            lines.append("## PART-AV: GRAHA AVASTHA & STHANADHIPATYA DOSHA (జాతక మార్తాండం)")
            lines.append("\n".join(av_rules))
            lines.append("")

    lines.append("## PART-D: DB10 CHART JSON")
    lines.append("```json")
    lines.append(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    lines.append("```")
    lines.append("")
    lines.append("═" * 72)
    lines.append(f"పై data చూసి V27.0 ప్రకారం {lagna_name} లగ్న జాతక విశ్లేషణ తెలుగులో ఇవ్వండి.")
    lines.append("STAGE 0 — STEP-0.0 FORCED ECHO నుండి మొదలు పెట్టండి.")
    lines.append("")
    lines.append("━" * 72)
    lines.append("⚠️  IMPORTANT INSTRUCTION:")
    lines.append("ఈ analysis prompt తో పాటు అటాచ్ చేసిన అన్ని files —")
    lines.append("ఏవైతే అటాచ్ చేయబడ్డాయో వాటన్నిటినీ తప్పనిసరిగా చదవాలి.")
    lines.append("ఆ files లో ఉన్న అన్ని RULE_ entries analysis లో వాడాలి.")
    lines.append("ఏ file కూడా skip చేయకూడదు.")
    lines.append("━" * 72)
    lines.append("═" * 72)

    return "\n".join(lines)


def main():
    print("═"*42)
    print("🔱 DB11-DIVYA BRAHMA ENGINE v11.0")
    print("   Brihat Jataka>BPHS>Jataka Martanda | 17 Charts | 8+9 Additions + 5 Cal Notes")
    print("═"*42)
    dob=input("జన్మ తేదీ  (DD/MM/YYYY): ").strip()
    tob_raw=input("జన్మ సమయం (6.19am/06:19): ").strip()
    pob=input("జన్మ స్థలం: ").strip()
    ayan_mode=select_ayanamsha()
    tob=parse_time(tob_raw)
    print(f"  ✅ సమయం: {tob}")
    print(f"\n  📍 '{pob}' coordinates...")
    loc_result=get_location(pob)
    if loc_result is None:
        lat,lon=17.2473,80.1514  # Default Khammam
        print(f"  ⚠️ Location not found, using default: {lat},{lon}")
    else:
        lat,lon=loc_result
    print("\n  ⏳ DB10: 17 charts + bhava sputamu + bridge layer...")
    try:
        data=generate_v21(dob,tob,lat,lon,pob,5.5,ayan_mode)
    except Exception as e:
        print(f"\n❌ Error: {e}"); import traceback; traceback.print_exc(); return
    step0_display(data)
    print("\nజాతక వివరాలు సరిగ్గా ఉన్నాయా?")
    if not get_confirmation():
        print("మళ్ళీ run చేయండి."); return
    import shutil, os
    home = os.path.expanduser("~")
    out = f"DB11_{dob.replace('/','')}"
    jf = os.path.join(home, f"{out}.json")
    sf = os.path.join(home, f"{out}_summary.txt")
    with open(jf,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False,default=str)
    with open(sf,"w",encoding="utf-8") as f:
        f.write(generate_summary(data))
    # ── Bridge Layer ──────────────────────────────────────────────────────────
    # Search for KB2.txt in multiple locations
    dl = os.path.join(home,"storage","downloads")
    # Current folder ముందు check చేయాలి — DivyaBrahma Working files లో run అవుతుంటే
    script_dir = None
    search_dirs = [
        os.path.dirname(os.path.abspath(__file__)),  # engine ఉన్న folder ముందు
        os.getcwd(),
        dl,
        home,
    ]
    for d in search_dirs:
        if os.path.exists(os.path.join(d,"KB2.txt")):
            script_dir = d
            break
    kb2_ok = script_dir is not None
    v26_ok = script_dir is not None and os.path.exists(os.path.join(script_dir,"V27MasterPrompt.txt"))
    if kb2_ok and v26_ok:
        lagna_name = data.get("lagna",{}).get("rashi_te","లగ్నం")
        print(f"\n  🔗 Bridge: {lagna_name} KB2 section + V26 combine...")
        prompt = build_analysis_prompt(data, script_dir)
        cf = os.path.join(home, f"{out}_analysis_prompt.txt")
        with open(cf,"w",encoding="utf-8") as f:
            f.write(prompt)
        print(f"  ✅ {out}_analysis_prompt.txt తయారయింది")
        print(f"     ↳ ఈ file Claude కి paste చేయండి → Telugu analysis వస్తుంది")
    else:
        missing = []
        if not kb2_ok: missing.append("KB2.txt")
        elif not v26_ok: missing.append("V27MasterPrompt.txt")
        print(f"\n⚠️  Bridge skip: {missing} కనుగొనలేదు")
        print(f"   Search చేసిన folders: {search_dirs}")
        cf = None
    # ── Save to Downloads ─────────────────────────────────────────────────────
    if os.path.isdir(dl):
        shutil.copy2(jf, os.path.join(dl, f"{out}.json"))
        shutil.copy2(sf, os.path.join(dl, f"{out}_summary.txt"))
        if cf and os.path.exists(cf):
            shutil.copy2(cf, os.path.join(dl, f"{out}_analysis_prompt.txt"))
        ds = "✅ Downloads లో save"
    else:
        ds = "⚠️  home లో save"
    print(f"\n✅ Complete!")
    print(f"📁 {out}.json")
    print(f"📋 {out}_summary.txt")
    if cf:
        print(f"🔗 {out}_analysis_prompt.txt  ← Claude కి paste చేయండి")
    print(f"📲 {ds}")
    print(f"🔱 DB11 done.")

if __name__=="__main__":
    main()
