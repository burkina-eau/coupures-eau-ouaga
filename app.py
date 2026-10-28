import streamlit as st
import folium
from streamlit_folium import st_folium

COORDS = {
    "Kalgodin": [12.345, -1.538], "Ouaga 2000": [12.324, -1.506],
    "Tampouy": [12.396, -1.562], "Pissy": [12.336, -1.559],
    "Gounghin": [12.364, -1.534], "Patte d'Oie": [12.344, -1.517],
    "Zogona": [12.369, -1.502], "Karpala": [12.318, -1.477],
    "Wemtenga": [12.361, -1.495], "Dapoya": [12.367, -1.524]
}

st.set_page_config(layout="wide")
st.title("💧 Coupures d'eau à Ouaga")

# CARTE SIMPLE QUI MARCHE TOUJOURS
m = folium.Map(location=[12.365, -1.533], zoom_start=12)

# On met 3 couleurs direct pour ton modèle
folium.Marker([12.345, -1.538], popup="Kalgodin: Coupure", icon=folium.Icon(color="red")).add_to(m)
folium.Marker([12.324, -1.506], popup="Ouaga 2000: Retour", icon=folium.Icon(color="green")).add_to(m)
folium.Marker([12.396, -1.562], popup="Tampouy: Coupure", icon=folium.Icon(color="red")).add_to(m)
folium.Marker([12.336, -1.559], popup="Pissy: Faible", icon=folium.Icon(color="orange")).add_to(m)
folium.Marker([12.364, -1.534], popup="Gounghin: Retour", icon=folium.Icon(color="green")).add_to(m)

st_folium(m, width=700, height=500)

# LES 3 LÉGENDES
c1, c2, c3 = st.columns(3)
c1.error("🔴 Coupure d'eau")
c2.success("🟢 Retour d'eau")
c3.warning("🟠 Faible pression")

st.divider()
st.write("Si tu vois la carte avec 5 points colorés, c'est gagné ! Ensuite on remet les 35 quartiers.")
