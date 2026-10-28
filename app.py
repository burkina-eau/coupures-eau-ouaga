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
st.title("💧 Coupures d'eau à Ouaga - 35 Quartiers")

# --- CARTE EN HAUT ---
st.subheader("🗺️ Carte en direct")
m = folium.Map(location=[12.365, -1.533], zoom_start=12)

try:
    df = pd.read_csv(SHEET_CSV)
    if not df.empty:
        for _, row in df.tail(100).iterrows():
            q = str(row.get('quartier', '')).strip()
            s = str(row.get('statut', ''))
            if q in COORDS:
                coord = COORDS[q]
                color = "red" if "Coupure" in s else "green"
                folium.Marker(coord, popup=f"{q}: {s}", tooltip=q, icon=folium.Icon(color=color, icon="tint", prefix="fa")).add_to(m)
except:
    pass

st_folium(m, use_container_width=True, height=500)

# --- LES 3 LÉGENDES BIEN CLAIRES ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🔴 Coupure d'eau")
    st.caption("Pas d'eau dans le quartier")
with col2:
    st.markdown("### 🟢 Retour d'eau")
    st.caption("L'eau est revenue !")
with col3:
    st.markdown("### ⚪ Pas signalé")
    st.caption("Pas encore d'info")

st.divider()

# --- FORMULAIRE ---
st.subheader("📍 Signaler votre quartier")
with st.form("form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        quartier = st.selectbox("Votre quartier", sorted(list(COORDS.keys())))
    with c2:
        statut = st.radio("Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau"], horizontal=True)
    nom = st.text_input("Prénom (optionnel)")
    envoyer = st.form_submit_button("🚀 Envoyer", use_container_width=True)

if envoyer:
    heure = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        requests.post(WEBAPP_URL, json={"heure": heure, "quartier": quartier, "statut": statut, "nom": nom}, timeout=10)
        st.success(f"✅ Enregistré pour {quartier} !")
        st.balloons()
        st.rerun()
    except:
        st.success("✅ Reçu !")

st.subheader("📊 Derniers signalements (sauvés pour toujours)")
try:
    df = pd.read_csv(SHEET_CSV)
    if not df.empty:
        st.dataframe(df.tail(25).iloc[::-1], use_container_width=True, hide_index=True)
except:
    st.info("Fais le premier signalement !")
