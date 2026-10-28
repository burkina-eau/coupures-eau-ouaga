import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Coupures Eau Ouaga", layout="wide")
st.title("💧 Carte Complète - Tous les Quartiers de Ouagadougou")
st.markdown("🔴 Coupure | 🟠 Faible pression | 🟢 Eau OK")
st.markdown("---")

# LISTE COMPLÈTE DES QUARTIERS DE OUAGADOUGOU
data = [
    # Centre-ville
    {"quartier": "Paspanga", "lat": 12.368, "lon": -1.515, "statut": "Coupure"},
    {"quartier": "Dapoya", "lat": 12.375, "lon": -1.530, "statut": "Coupure"},
    {"quartier": "Koulouba", "lat": 12.364, "lon": -1.519, "statut": "Eau OK"},
    {"quartier": "Kamsaoghin", "lat": 12.370, "lon": -1.510, "statut": "Faible pression"},
    {"quartier": "Samandin", "lat": 12.380, "lon": -1.540, "statut": "Coupure"},
    {"quartier": "Gounghin Nord", "lat": 12.360, "lon": -1.550, "statut": "Faible pression"},
    {"quartier": "Gounghin Sud", "lat": 12.345, "lon": -1.545, "statut": "Coupure"},
    {"quartier": "Bilbalogho", "lat": 12.355, "lon": -1.525, "statut": "Coupure"},
    {"quartier": "Ouidi", "lat": 12.365, "lon": -1.535, "statut": "Eau OK"},
    {"quartier": "Larlé", "lat": 12.385, "lon": -1.520, "statut": "Eau OK"},
    
    # Nord
    {"quartier": "Tampouy", "lat": 12.395, "lon": -1.555, "statut": "Coupure"},
    {"quartier": "Kilwin", "lat": 12.410, "lon": -1.560, "statut": "Faible pression"},
    {"quartier": "Tanghin", "lat": 12.400, "lon": -1.515, "statut": "Coupure"},
    {"quartier": "Toudoubweogo", "lat": 12.425, "lon": -1.530, "statut": "Coupure"},
    {"quartier": "Kossodo", "lat": 12.430, "lon": -1.500, "statut": "Faible pression"},
    {"quartier": "Somgandé", "lat": 12.415, "lon": -1.490, "statut": "Eau OK"},

    # Est
    {"quartier": "Dassasgho", "lat": 12.370, "lon": -1.485, "statut": "Faible pression"},
    {"quartier": "Wayalghin", "lat": 12.380, "lon": -1.475, "statut": "Coupure"},
    {"quartier": "Zogona", "lat": 12.385, "lon": -1.495, "statut": "Eau OK"},
    {"quartier": "Wemtenga", "lat": 12.360, "lon": -1.485, "statut": "Eau OK"},
    {"quartier": "Dag Noen", "lat": 12.355, "lon": -1.465, "statut": "Coupure"},

    # Sud
    {"quartier": "Zone 1", "lat": 12.340, "lon": -1.510, "statut": "Eau OK"},
    {"quartier": "Kalgodin", "lat": 12.345, "lon": -1.495, "statut": "Coupure"},
    {"quartier": "Cissin", "lat": 12.330, "lon": -1.530, "statut": "Coupure"},
    {"quartier": "Patte d'Oie", "lat": 12.315, "lon": -1.520, "statut": "Faible pression"},
    {"quartier": "Pissy", "lat": 12.320, "lon": -1.550, "statut": "Coupure"},
    {"quartier": "Ouaga 2000", "lat": 12.305, "lon": -1.495, "statut": "Eau OK"},
    {"quartier": "Balkuy", "lat": 12.290, "lon": -1.510, "statut": "Faible pression"},
    {"quartier": "Trame d'Accueil", "lat": 12.295, "lon": -1.530, "statut": "Coupure"},

    # Ouest
    {"quartier": "Cité An II", "lat": 12.350, "lon": -1.565, "statut": "Eau OK"},
    {"quartier": "Cité Azimmo", "lat": 12.335, "lon": -1.570, "statut": "Faible pression"},
    {"quartier": "Yagma", "lat": 12.415, "lon": -1.590, "statut": "Coupure"},
    {"quartier": "Bassinko", "lat": 12.450, "lon": -1.580, "statut": "Coupure"},
    {"quartier": "Kamsoaghin (Ouest)", "lat": 12.345, "lon": -1.585, "statut": "Faible pression"},
    {"quartier": "Hamdalaye", "lat": 12.365, "lon": -1.555, "statut": "Eau OK"},
    {"quartier": "Nonsin", "lat": 12.405, "lon": -1.535, "statut": "Coupure"},
]

df = pd.DataFrame(data)

m = folium.Map(location=[12.36, -1.52], zoom_start=12)

for _, row in df.iterrows():
    color = "red" if row["statut"] == "Coupure" else "orange" if row["statut"] == "Faible pression" else "green"
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=f"{row['quartier']} : {row['statut']}",
        tooltip=row['quartier'],
        icon=folium.Icon(color=color, icon="tint", prefix="fa")
    ).add_to(m)

st_folium(m, width=700, height=600, returned_objects=[])

st.markdown(f"### 📊 {len(df)} quartiers de Ouagadougou")
c1, c2, c3 = st.columns(3)
c1.metric("🔴 Coupures", len(df[df.statut=="Coupure"]))
c2.metric("🟠 Faible", len(df[df.statut=="Faible pression"]))
c3.metric("🟢 Eau OK", len(df[df.statut=="Eau OK"]))

st.dataframe(df.sort_values("quartier"), use_container_width=True)
