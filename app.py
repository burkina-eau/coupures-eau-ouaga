import streamlit as st
import folium
from streamlit_folium import st_folium

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

st.set_page_config(layout="wide")
st.title("💧 Coupures d'eau à Ouaga")

m = folium.Map(location=[12.365, -1.533], zoom_start=12)

# On affiche les 35 quartiers avec les 3 couleurs comme ton modèle préféré
# 12 en ROUGE, 12 en VERT, 11 en ORANGE
quartiers = list(COORDS.keys())
for i, q in enumerate(quartiers):
    coord = COORDS[q]
    if i < 12:
        color = "red"
    elif i < 24:
        color = "green"
    else:
        color = "orange"
    
    folium.Marker(
        coord,
        tooltip=q,
        popup=q,
        icon=folium.Icon(color=color, icon="tint", prefix="fa")
    ).add_to(m)

st_folium(m, use_container_width=True, height=550)

st.markdown("### 📖 LÉGENDE OFFICIELLE")
c1, c2, c3 = st.columns(3)
with c1:
    st.error("🔴 ROUGE = Coupure d'eau")
with c2:
    st.success("🟢 VERT = Eau de retour")
with c3:
    st.warning("🟠 ORANGE = Faible pression")

st.info("✅ Modèle avec 35 quartiers - Carte colorée fixe")
