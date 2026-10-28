import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Coupures d'eau - Ouaga", layout="wide")
st.title("Carte des Coupures d'Eau - Ouagadougou 💧")

# --- LÉGENDE CLAIRE ---
st.markdown("""
### 📖 Légende
🔴 **Rouge = Coupure d'eau**
🟠 **Orange = Faible pression**
""")

data = [
    {"quartier": "Paspanga", "lat": 12.36, "lon": -1.50, "statut": "Coupure", "duree": "2 j"},
    {"quartier": "Burkina", "lat": 12.39, "lon": -1.53, "statut": "Coupure", "duree": "1 j"},
    {"quartier": "Dapoya", "lat": 12.36, "lon": -1.48, "statut": "Faible pression", "duree": "3 j"},
]

df = pd.DataFrame(data)

m = folium.Map(location=[12.36, -1.51], zoom_start=12)

for _, row in df.iterrows():
    color = "red" if "Coupure" in row["statut"] else "orange"
    folium.Marker(
        [row["lat"], row["lon"]], 
        popup=f"{row['quartier']} - {row['statut']} ({row['duree']})",
        icon=folium.Icon(color=color, icon="tint")
    ).add_to(m)

st_folium(m, width=700, height=500)
st.write("Données des quartiers :")
st.dataframe(df)
