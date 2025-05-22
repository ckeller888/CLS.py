import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import fiona
import random
import json


filename = "geodata/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
layer_name = "tlm_kantonsgebiet"

gdf = gpd.read_file(filename, layer=layer_name).to_crs(epsg=2056)

# Streamlit-Konfiguration
st.set_page_config(page_title="Spiel", layout="wide")
st.title("Kantonsumrisse erkennen Schweiz")

namen_liste = []

with fiona.open(filename, layer=layer_name) as src:
    for feature in src:
        # Prüfen, ob "Namen" in den Attributen vorhanden ist
        name = feature["properties"].get("name")
        if name:
            namen_liste.append(name)
# Duplikate entfernen und sortieren
namen_liste = sorted(set(namen_liste))




# Definition der State-Variablen
if "remaining" not in st.session_state:
    st.session_state.remaining = namen_liste.copy()
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = None
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Play-Button
# Wenn alle Kantone gespielt wurden, zurücksetzen
if st.button("▶️ Play"):
    if not st.session_state.remaining:
        st.session_state.feedback = "Alle Kantone waren dran, Spiel wird zurückgesetzt!"
        st.session_state.remaining = namen_liste.copy()
        st.session_state.score = 0
        st.session_state.current = None
    else:
        st.session_state.current = random.choice(st.session_state.remaining)
        st.session_state.remaining.remove(st.session_state.current)
        st.session_state.feedback = ""
# Spiel starten
if st.session_state.current is None:
    st.info("Drücke auf **Play**, um zu starten!")
    st.stop()


# Liste der Optionen
optionen = st.session_state.remaining

# Dropdown
with st.form("kanton_form"):
    auswahl = st.selectbox("Wähle einen Kanton:", optionen)
    submitted = st.form_submit_button("Bestätigen")

if submitted:
    st.write(f"Deine Antwort: **{auswahl}**")
    antwort = auswahl
 

# Random Kanton auswählen
# zufaellig = gdf.sample(n=1).iloc[0]

# Kantonsumriss darstellen
Koordinaten =  st.session_state.current["geometry"]
gdf = gpd.GeoDataFrame(geometry=[Koordinaten])
gdf.plot(color='lightblue', edgecolor='black')




st.sidebar.header("📊 Statistik")
st.sidebar.write(f"Punktestand: **{st.session_state.score}**")
st.sidebar.write(f"Verbleibende Kantone: **{len(st.session_state.remaining)}**")
