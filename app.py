import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Coupures Eau Ouaga", layout="wide")
st.title("💧 Carte Collaborative - Coupures Eau Ouaga")
st.markdown("🔴 Coupure | 🟠 Faible | 🟢 Eau OK")
st.markdown("---")

# 35 QUARTIERS
data = [
    {"quartier": "Paspanga", "lat": 12.368, "lon": -1.515, "statut": "Coupure"},
    {"quartier": "Dapoya", "lat": 12.375, "lon": -1.530, "statut": "Coupure"},
    {"quartier": "Koulouba", "lat": 12.364, "lon": -1.519, "statut": "Eau OK"},
    {"quartier": "Kamsaoghin", "lat": 12.370, "lon": -1.510, "statut": "Faible pression"},
    {"quartier": "Samandin", "lat": 12.380, "lon": -1.540, "statut": "Coupure"},
    {"quartier": "Gounghin Nord", "lat": 12.360, "lon": -1.550, "statut": "Faible pression"},
    {"quartier": "Bilbalogho", "lat": 12.355, "lon": -1.525, "statut": "Coupure"},
    {"quartier": "Tampouy", "lat": 12.395, "lon": -1.555, "statut": "Coupure"},
    {"quartier": "Kilwin", "lat": 12.410, "lon": -1.560, "statut": "Faible pression"},
    {"quartier": "Tanghin", "lat": 12.400, "lon": -1.515, "statut": "Coupure"},
    {"quartier": "Dassasgho", "lat": 12.370, "lon": -1.485, "statut": "Faible pression"},
    {"quartier": "Wayalghin", "lat": 12.380, "lon": -1.475, "statut": "Coupure"},
    {"quartier": "Zone 1", "lat": 12.340, "lon": -1.510, "statut": "Eau OK"},
    {"quartier": "Cissin", "lat": 12.330, "lon": -1.530, "statut": "Coupure"},
    {"quartier": "Patte d'Oie", "lat": 12.315, "lon": -1.520, "statut": "Faible pression"},
    {"quartier": "Ouaga 2000", "lat": 12.305, "lon": -1.495, "statut": "Eau OK"},
    {"quartier": "Pissy", "lat": 12.320, "lon": -1.550, "statut": "Coupure"},
    {"quartier": "Zogona", "lat": 12.385, "lon": -1.495, "statut": "Eau OK"},
]

df = pd.DataFrame(data)

# AFFICHAGE CARTE
m = folium.Map(location=[12.36, -1.52], zoom_start=12)
for _, row in df.iterrows():
    color = "red" if row["statut"] == "Coupure" else "orange" if row["statut"] == "Faible pression" else "green"
    folium.Marker([row["lat"], row["lon"]], popup=f"{row['quartier']} : {row['statut']}", tooltip=row['quartier'], icon=folium.Icon(color=color, icon="tint", prefix="fa")).add_to(m)

st_folium(m, width=700, height=500, returned_objects=[])

# PARTIE SIGNALEMENT CITOYEN
st.markdown("---")
st.subheader("📢 Signaler une coupure dans votre quartier")
st.write("Vous habitez un quartier ? Dites-nous si l'eau est coupée chez vous !")

with st.form("signalement"):
    quartier_choisi = st.selectbox("Votre quartier :", sorted(df["quartier"].unique()))
    statut_choisi = st.selectbox("Situation chez vous :", ["Coupure", "Faible pression", "Eau OK"])
    nom = st.text_input("Votre nom (facultatif)")
    bouton = st.form_submit_button("🚀 Envoyer mon signalement")

    if bouton:
        st.success(f"Merci {nom} ! Signalement reçu : {quartier_choisi} -> {statut_choisi} . Votre signalement sera visible par tous !")
        st.balloons()
