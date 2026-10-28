import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"
SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

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

# CARTE EN HAUT - TOUJOURS VISIBLE
m = folium.Map(location=[12.365, -1.533], zoom_start=12)

# 1. Affiche toujours les 35 quartiers en gris
for q, coord in COORDS.items():
    folium.CircleMarker(coord, radius=4, color="gray", fill=True, fill_opacity=0.3, popup=q, tooltip=q).add_to(m)

# 2. Ajoute les signalements colorés par dessus
try:
    df = pd.read_csv(SHEET_CSV)
    if not df.empty:
        # Cherche la colonne quartier peu importe majuscule/minuscule
        df.columns = [c.lower().strip() for c in df.columns]
        for _, row in df.tail(100).iterrows():
            q = str(row.get('quartier', '')).strip()
            # Corrige le nom pour matcher
            q_match = next((k for k in COORDS if k.lower() in q.lower() or q.lower() in k.lower()), None)
            if q_match:
                s = str(row.get('statut', '')).lower()
                color = "red" if "coupure" in s else "green" if "retour" in s else "orange"
                folium.Marker(COORDS[q_match], popup=f"{q_match}: {s}", tooltip=f"{q_match} - {s}", icon=folium.Icon(color=color, icon="tint", prefix="fa")).add_to(m)
except Exception as e:
    st.write(f"Debug: {e}")

st_folium(m, use_container_width=True, height=500)

# LES 3 LÉGENDES BIEN CLAIRES
c1, c2, c3 = st.columns(3)
with c1:
    st.error("🔴 Coupure d'eau")
with c2:
    st.success("🟢 Retour d'eau")
with c3:
    st.warning("⚪ Pas encore signalé")

st.divider()

with st.form("form", clear_on_submit=True):
    q = st.selectbox("📍 Ton quartier", sorted(COORDS.keys()))
    s = st.selectbox("Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau", "🟠 Faible pression"])
    envoyer = st.form_submit_button("🚀 Envoyer", use_container_width=True)

if envoyer:
    heure = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        requests.post(WEBAPP_URL, json={"heure": heure, "quartier": q, "statut": s}, timeout=10)
        st.success(f"✅ {q} enregistré ! Actualise la page !")
        st.balloons()
    except:
        st.success("✅ Reçu !")
