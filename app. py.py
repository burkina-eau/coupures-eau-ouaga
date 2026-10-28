import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Coupures d'eau - Ouaga", layout="wide")
st.title("Carte des Coupures d'Eau - Ouagadougou")

data = [
    {"quartier": "Dassasgho", "lat": 12.36, "lon": -1.50, "statut": "Coupure", "duree": "2 jours"},
    {"quartier": "Patte d'Oie", "lat": 12.32, "lon": -1.52, "statut": "Coupure", "duree": "1 jour"},
    {"quartier": "Karpala", "lat": 12.30, "lon": -1.48, "statut": "Faible pression", "duree": "3 jours"},
]

df = pd.DataFrame(data)
m = folium.Map(location=[12.364, -1.533], zoom_start=12)
for _, row in df.iterrows():
    color = "red" if row["statut"]=="Coupure" else "orange"
    folium.Marker([row["lat"], row["lon"]], popup=row["quartier"], icon=folium.Icon(color=color)).add_to(m)

st_folium(m, width=700, height=500)
st.dataframe(df)