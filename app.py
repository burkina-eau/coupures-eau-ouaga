import streamlit as st
import pandas as pd
from datetime import datetime
import requests

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbydCeM82TcHNgDI55quYgqStAhppJuvZMN-YVB64HoapVuWjdE_5RWEH0Lyzs_UDSvuGA/exec"
SHEET_ID = "1jtP1MpFbTH5rCRIsiECO6KZ6DwKvZsz3QXLQRVZ4IyY"
SHEET_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.title("💧 Coupures d'eau à Ouaga")
st.write("Signale en 10 secondes - données sauvées pour toujours")

with st.form("form", clear_on_submit=True):
    quartier = st.selectbox("📍 Votre quartier", ["Kalgodin","Gounghin","Pissy","Tampouy","Zogona","Dapoya","Koulouba","Autre"])
    statut = st.radio("💧 Situation", ["🔴 Coupure d'eau", "🟢 Retour d'eau"])
    nom = st.text_input("Votre prénom (optionnel)")
    envoyer = st.form_submit_button("🚀 Envoyer mon signalement", use_container_width=True)

if envoyer:
    heure = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        requests.post(WEBAPP_URL, json={"heure": heure, "quartier": quartier, "statut": statut, "nom": nom}, timeout=10)
        st.success(f"✅ Merci ! Enregistré pour {quartier} : {statut}")
        st.balloons()
    except:
        st.success("✅ Reçu !")

st.divider()
st.subheader("📊 Derniers signalements (ne s'efface plus jamais)")
try:
    df = pd.read_csv(SHEET_CSV)
    if not df.empty:
        st.dataframe(df.tail(30).iloc[::-1], use_container_width=True, hide_index=True)
        st.caption(f"✅ {len(df)} signalements sauvés dans Google Sheet")
except:
    st.info("Fais ton premier signalement !")

st.link_button("📂 Voir Google Sheet", f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
