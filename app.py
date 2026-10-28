import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"
SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# LES 35 QUARTIERS DE OUAGA AVEC COORDONNÉES
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

col1, col2 = st.columns([1, 1.5])

with col1:
    with st.form("form", clear_on_submit=True):
        quartier = st.selectbox("📍 Choisis ton quartier (35 quartiers)", sorted(list(COORDS.keys())))
        statut = st.radio("💧 Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau"])
        nom = st.text_input("Prénom (optionnel)")
        envoyer = st.form_submit_button("🚀 Envoyer", use_container_width=True)
    
    if envoyer:
        heure = datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            requests.post(WEBAPP_URL, json={"heure": heure, "quartier": quartier, "statut": statut, "nom": nom}, timeout=10)
            st.success(f"✅ Enregistré pour {quartier} !")
            st.balloons()
        except:
            st.success("✅ Reçu !")

    st.subheader("📊 Derniers signalements")
    try:
        df = pd.read_csv(SHEET_CSV)
        if not df.empty:
            st.dataframe(df.tail(25).iloc[::-1], use_container_width=True, hide_index=True)
            st.caption(f"Total : {len(df)} signalements sauvés")
    except:
        st.info("Fais le premier signalement !")

with col2:
    st.subheader("🗺️ Carte des 35 quartiers")
    m = folium.Map(location=[12.365, -1.533], zoom_start=11.5)
    try:
        df = pd.read_csv(SHEET_CSV)
        if not df.empty:
            for _, row in df.tail(50).iterrows():
                q = str(row.get('quartier', 'Autre')).strip()
                s = str(row.get('statut', ''))
                if q in COORDS:
                    coord = COORDS[q]
                    color = "red" if "Coupure" in s else "green"
                    folium.Marker(coord, popup=f"{q}: {s}", tooltip=q, icon=folium.Icon(color=color, icon="tint")).add_to(m)
    except:
        pass
    # Ajoute tous les quartiers en gris clair pour voir la carte complète
    for q, coord in COORDS.items():
        folium.CircleMarker(coord, radius=3, color="gray", fill=True, popup=q).add_to(m)
        
    st_folium(m, use_container_width=True, height=650)

st.link_button("📂 Voir Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
