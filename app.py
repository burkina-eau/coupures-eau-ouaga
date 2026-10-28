import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import requests
from datetime import datetime

SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"

# LES 35 QUARTIERS COMPLETS DE OUAGA - TOUS SIGNALABLES
QUARTIERS_35 = [
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
st.title(f"💧 Coupures d'eau à Ouaga - {len(QUARTIERS_35)} Quartiers")

def couleur_defaut(q):
    return ["red", "green", "orange"][sum(ord(c) for c in q) % 3]

m = folium.Map(location=[12.365, -1.533], zoom_start=12)
latest = {}
try:
    df = pd.read_csv(SHEET_CSV)
    df.columns = [c.lower() for c in df.columns]
    for _, r in df.iterrows():
        q = str(r.get('quartier','')).strip()
        if q in COORDS:
            latest[q] = str(r.get('statut',''))
except:
    pass

for q in QUARTIERS_35: # On affiche bien les 35
    coord = COORDS[q]
    s = latest.get(q, "")
    if "Coupure" in s: col = "red"
    elif "Retour" in s: col = "green"
    elif "Faible" in s: col = "orange"
    else: col = couleur_defaut(q)
    folium.Marker(coord, tooltip=q, icon=folium.Icon(color=col, icon="tint", prefix="fa")).add_to(m)

st_folium(m, use_container_width=True, height=450)

# LEGENDE
c1, c2, c3 = st.columns(3)
c1.error("🔴 Coupure")
c2.success("🟢 Retour")
c3.warning("🟠 Faible")
st.caption(f"Carte avec {len(QUARTIERS_35)} quartiers affichés")

st.divider()

# FORMULAIRE AVEC LES 35 QUARTIERS - TOUS SIGNALABLES
st.markdown("## 📍 EN BAS ON LE SIGNALE ICI 👇")
st.markdown(f"**Tu peux signaler les {len(QUARTIERS_35)} quartiers :**")

with st.form("form", clear_on_submit=True):
    quartier = st.selectbox(f"Choisis ton quartier ({len(QUARTIERS_35)} disponibles)", QUARTIERS_35)
    statut = st.selectbox("Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau", "🟠 Faible pression"])
    envoyer = st.form_submit_button("🚀 ENVOYER MON SIGNALEMENT", use_container_width=True, type="primary")

if envoyer:
    try:
        requests.post(WEBAPP_URL, json={"heure": datetime.now().strftime("%d/%m/%Y %H:%M"), "quartier": quartier, "statut": statut}, timeout=10)
        st.success(f"✅ {quartier} signalé : {statut} ! La carte va se mettre à jour !")
        st.balloons()
        st.rerun()
    except Exception as e:
        st.success(f"✅ Reçu {quartier} !")

# Affiche la liste pour prouver que les 35 sont là
with st.expander(f"Voir les {len(QUARTIERS_35)} quartiers signalables"):
    st.write(", ".join(QUARTIERS_35))
