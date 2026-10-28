import folium
from streamlit_folium import st_folium
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Coupures d'eau - Ouaga", layout="wide")
st.title("Carte des Coupures d'eau - Ouagadougou")

st.markdown("""
### Legende
🔴 Rouge = Coupure d'eau
🟠 Orange = Faible pression
""")

data = [
    {"quartier": "Paspanga", "lat": 12.365, "lon": -1.515, "statut": "Coupure"},
    {"quartier": "Burkina", "lat": 12.35, "lon": -1.52, "statut": "Faible pression"},
    {"quartier": "Dapoya", "lat": 12.36, "lon": -1.53, "statut": "Coupure"},
]

df = pd.DataFrame(data)
m = folium.Map(location=[12.36, -1.51], zoom_start=12)

for _, row in df.iterrows():
    color = "red" if "Coupure" in row["statut"] else "orange"
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=f"{row['quartier']} - {row['statut']}",
        icon=folium.Icon(color=color, icon="tint")
    ).add_to(m)

st_folium(m, width=700, height=500)
st.write("Donnees des quartiers :")
st.dataframe(df)
