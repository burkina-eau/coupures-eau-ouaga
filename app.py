import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import requests
from datetime import datetime

SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"

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
st.title("💧 Coupures d'eau à Ouaga")

# CARTE - TA CARTE QUI MARCHE
m = folium.Map(location=[12.365, -1.533], zoom_start=12)

try:
    df = pd.read_csv(SHEET_CSV)
    df.columns = [c.lower() for c in df.columns]
    latest = {}
    for _, r in df.iterrows():
        q = str(r.get('quartier','')).strip()
        if q: latest[q] = str(r.get('statut',''))
    for q, coord in COORDS.items():
        s = latest.get(q, "")
        if "Coupure" in s: col = "red"
        elif "Retour" in s: col = "green"
        elif "Faible" in s: col = "orange"
        else: col = "blue"
        folium.Marker(coord, tooltip=q, popup=f"{q}: {s or 'Pas signalé'}", icon=folium.Icon(color=col, icon="tint", prefix="fa")).add_to(m)
except:
    for q, coord in COORDS.items():
        folium.Marker(coord, tooltip=q, icon=folium.Icon(color="blue", icon="tint", prefix="fa")).add_to(m)

st_folium(m, use_container_width=True, height=450)

# LEGENDE OFFICIELLE
st.markdown("### 📖 LÉGENDE OFFICIELLE")
c1, c2, c3, c4 = st.columns(4)
c1.error("🔴 Coupure")
c2.warning("🟠 Faible")
c3.success("🟢 Retour")
c4.info("🔵 Pas signalé")

st.divider()

# EN BAS ON LE SIGNALE - FORMULAIRE BIEN VISIBLE
st.markdown("## 📍 EN BAS ON LE SIGNALE ICI 👇")
st.markdown("Signale la situation de ton quartier pour mettre la carte à jour !")

with st.form("signalement", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        quartier = st.selectbox("Ton quartier", sorted(COORDS.keys()))
    with col2:
        statut = st.selectbox("Situation actuelle", ["🔴 Coupure d'eau", "🟢 Retour d'eau", "🟠 Faible pression"])
    
    envoyer = st.form_submit_button("🚀 ENVOYER MON SIGNALEMENT", use_container_width=True, type="primary")

if envoyer:
    try:
        requests.post(WEBAPP_URL, json={
            "heure": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "quartier": quartier,
            "statut": statut
        }, timeout=10)
        st.success(f"✅ Merci ! {quartier} est maintenant {statut} sur la carte !")
        st.balloons()
        st.rerun()
    except:
        st.success("✅ Signalement reçu ! Actualise la page !")
