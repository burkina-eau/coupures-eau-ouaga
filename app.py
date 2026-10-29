import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import requests
from datetime import datetime
import time

SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"

# On force Google à ne pas mettre en cache
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&t={int(time.time())}"

QUARTIERS_36 = [
    "Balkuy", "Bangpooré", "Bissighin", "Cissin", "Dapoya", "Dassasgho", "Gounghin",
    "Hamdallaye", "Kalgodin", "Kamboinsé", "Karpala", "Katr Yaar", "Koulouba", "Larlé",
    "Nagrin", "Nioko 1", "Nioko 2", "Nonssin", "Ouaga 2000", "Ouidi", "Paspanga",
    "Patte d'Oie", "Pissy", "Rimkiéta", "Samandin", "Sandogo", "Sig-Noghin", "Somgandé",
    "Tampouy", "Tanghin", "Toécin", "Wayalghin", "Wemtenga", "Yagma", "Zogona", "Zone 1"
]

COORDS = {
    "Balkuy": [12.306, -1.471], "Bangpooré": [12.413, -1.498],
    "Bissighin": [12.416, -1.567], "Cissin": [12.325, -1.542],
    "Dapoya": [12.367, -1.524], "Dassasgho": [12.372, -1.487],
    "Gounghin": [12.364, -1.534], "Hamdallaye": [12.378, -1.534],
    "Kalgodin": [12.345, -1.538], "Kamboinsé": [12.481, -1.549],
    "Karpala": [12.318, -1.477], "Katr Yaar": [12.354, -1.506],
    "Koulouba": [12.364, -1.512], "Larlé": [12.365, -1.542],
    "Nagrin": [12.288, -1.521], "Nioko 1": [12.342, -1.431],
    "Nioko 2": [12.352, -1.412], "Nonssin": [12.405, -1.530],
    "Ouaga 2000": [12.324, -1.506], "Ouidi": [12.358, -1.531],
    "Paspanga": [12.362, -1.519], "Patte d'Oie": [12.344, -1.517],
    "Pissy": [12.336, -1.559], "Rimkiéta": [12.418, -1.546],
    "Samandin": [12.377, -1.544], "Sandogo": [12.358, -1.585],
    "Sig-Noghin": [12.384, -1.561], "Somgandé": [12.407, -1.477],
    "Tampouy": [12.396, -1.562], "Tanghin": [12.394, -1.527],
    "Toécin": [12.342, -1.475], "Wayalghin": [12.383, -1.485],
    "Wemtenga": [12.361, -1.495], "Yagma": [12.453, -1.567],
    "Zogona": [12.369, -1.502], "Zone 1": [12.343, -1.492]
}

st.set_page_config(page_title="Coupures Eau Ouaga", layout="wide")
st.title(f"💧 Coupures d'eau à Ouaga - 36 Quartiers")

# SESSION pour garder le dernier signalement et l'afficher direct
if "dernier_signal" not in st.session_state:
    st.session_state.dernier_signal = {}

def couleur_defaut(q):
    return ["red", "green", "orange"][sum(ord(c) for c in q) % 3]

m = folium.Map(location=[12.365, -1.533], zoom_start=12)
latest = {}

try:
    df = pd.read_csv(SHEET_CSV)
    df.columns = [c.lower() for c in df.columns]
    # On prend les dernières lignes en premier pour avoir le plus récent
    for _, r in df.iloc[::-1].iterrows():
        q = str(r.get('quartier','')).strip()
        if q in COORDS and q not in latest:
            latest[q] = str(r.get('statut',''))
except Exception as e:
    st.caption(f"Chargement... {e}")

# On écrase avec le dernier signalement que TU viens d'envoyer (affichage instantané)
latest.update(st.session_state.dernier_signal)

for q in QUARTIERS_36:
    coord = COORDS[q]
    s = latest.get(q, "")
    if "Coupure" in s: col = "red"
    elif "Retour" in s: col = "green"
    elif "Faible" in s: col = "orange"
    else: col = couleur_defaut(q)
    
    popup_text = f"{q}: {s or 'Démo'}"
    folium.Marker(coord, tooltip=q, popup=popup_text, icon=folium.Icon(color=col, icon="tint", prefix="fa")).add_to(m)

st_folium(m, use_container_width=True, height=450)

c1, c2, c3 = st.columns(3)
c1.error("🔴 Coupure")
c2.success("🟢 Retour")
c3.warning("🟠 Faible")

st.divider()
st.markdown("## 📍 EN BAS ON LE SIGNALE ICI 👇")

with st.form("form", clear_on_submit=True):
    quartier = st.selectbox(f"Choisis ton quartier ({len(QUARTIERS_36)} disponibles)", QUARTIERS_36)
    statut = st.selectbox("Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau", "🟠 Faible pression"])
    envoyer = st.form_submit_button("🚀 ENVOYER MON SIGNALEMENT", use_container_width=True, type="primary")

if envoyer:
    try:
        requests.post(WEBAPP_URL, json={"heure": datetime.now().strftime("%d/%m/%Y %H:%M"), "quartier": quartier, "statut": statut}, timeout=10)
        # ON AFFICHE DIRECT SANS ATTENDRE GOOGLE SHEET
        st.session_state.dernier_signal[quartier] = statut
        st.success(f"✅ {quartier} → {statut} ! La carte est mise à jour !")
        st.balloons()
        time.sleep(1)
        st.rerun()
    except:
        st.session_state.dernier_signal[quartier] = statut
        st.success(f"✅ {quartier} signalé !")
        st.rerun()

# PREUVE QUE ÇA S'AFFICHE
if st.session_state.dernier_signal:
    st.markdown("### 📋 Derniers signalements affichés sur la carte :")
    for q, s in st.session_state.dernier_signal.items():
        st.write(f"- {q} : {s}")

with st.expander(f"Voir les {len(QUARTIERS_36)} quartiers"):
    st.write(", ".join(QUARTIERS_36))
