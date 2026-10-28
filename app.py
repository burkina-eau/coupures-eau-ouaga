import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"
SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# Coordonnées approximatives Ouaga
COORDS = {
    "Kalgodin": [12.345, -1.538], "Gounghin": [12.364, -1.534],
    "Pissy": [12.336, -1.559], "Tampouy": [12.396, -1.562],
    "Zogona": [12.369, -1.502], "Dapoya": [12.367, -1.524],
    "Koulouba": [12.364, -1.512], "Autre": [12.365, -1.533]
}

st.set_page_config(page_title="Coupures Eau Ouaga", layout="wide")
st.title("💧 Coupures d'eau à Ouaga")

col1, col2 = st.columns([1, 1])

with col1:
    with st.form("form", clear_on_submit=True):
        quartier = st.selectbox("📍 Votre quartier", list(COORDS.keys()))
        statut = st.radio("💧 Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau"])
        nom = st.text_input("Votre prénom (optionnel)")
        envoyer = st.form_submit_button("🚀 Envoyer", use_container_width=True)
    
    if envoyer:
        heure = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            requests.post(WEBAPP_URL, json={"heure": heure, "quartier": quartier, "statut": statut, "nom": nom}, timeout=10)
            st.success(f"✅ Enregistré pour {quartier} !")
            st.balloons()
        except:
            st.success("✅ Reçu !")

    st.divider()
    st.subheader("📊 Derniers signalements (ne s'efface plus)")
    try:
        df = pd.read_csv(SHEET_CSV)
        if not df.empty:
            st.dataframe(df.tail(20).iloc[::-1], use_container_width=True, hide_index=True)
    except:
        st.info("Fais le premier signalement !")

with col2:
    st.subheader("🗺️ Carte de Ouaga")
    m = folium.Map(location=[12.365, -1.533], zoom_start=12)
    try:
        df = pd.read_csv(SHEET_CSV)
        if not df.empty:
            for _, row in df.tail(20).iterrows():
                q = row.get('quartier', 'Autre')
                s = row.get('statut', '')
                coord = COORDS.get(q, COORDS["Autre"])
                color = "red" if "Coupure" in str(s) else "green"
                folium.Marker(coord, popup=f"{q}: {s}", icon=folium.Icon(color=color)).add_to(m)
    except:
        pass
    st_folium(m, use_container_width=True, height=500)

st.link_button("📂 Voir Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
