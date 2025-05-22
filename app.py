import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import fiona
import random
import json
# import PyQt5

filename = "geodata/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
layer_name = "tlm_kantonsgebiet"

gdf = gpd.read_file(filename, layer=layer_name)

# Streamlit-Konfiguration
st.set_page_config(page_title="Spiel", layout="wide")
st.title("Kantonsumrisse erkennen Schweiz")



    # Beispieloptionen
namen_liste = []

with fiona.open(filename, layer=layer_name) as src:
    for feature in src:
        # Prüfen, ob "Namen" in den Attributen vorhanden ist
        name = feature["properties"].get("name")
        if name:
            namen_liste.append(name)

# Duplikate entfernen und sortieren
namen_liste = sorted(set(namen_liste))


if "remaining" not in st.session_state:
    st.session_state.remaining = namen_liste.copy()
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = None
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# ------------------ Play-Button ------------------
if st.button("▶️ Play"):
    if not st.session_state.remaining:
        st.session_state.feedback = "Alle Kantone waren dran – Spiel wird zurückgesetzt!"
        st.session_state.remaining = namen_liste.copy()
        st.session_state.score = 0
        st.session_state.current = None
    else:
        st.session_state.current = random.choice(st.session_state.remaining)
        st.session_state.remaining.remove(st.session_state.current)
        st.session_state.feedback = ""

if st.session_state.current is None:
    st.info("Drücke auf **Play**, um zu starten!")
    st.stop()


# Textfeld mit Filterfunktion
#eingabe = st.text_input("Kantonsname:")

# Liste der Optionen
optionen = st.session_state.remaining

# Dropdown
with st.form("kanton_form"):
    auswahl = st.selectbox("Wähle einen Kanton:", optionen)
    submitted = st.form_submit_button("Bestätigen")

if submitted:
    st.write(f"Deine Antwort: **{auswahl}**")
    antwort = auswahl

kanton = st.session_state.current
feature = gdf[gdf["name"] == kanton]
geojson_str = feature.to_json()               # das ist ein JSON-String
geojson = json.loads(geojson_str)  


kanton_name = st.session_state.current
feature = gdf[gdf["name"] == kanton_name]

# Karte ohne Hintergrund (tiles=None), zentriert auf Kanton
centroid = feature.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=9, tiles=None)
folium.GeoJson(
    feature,
    style_function=lambda _: {
        "fillColor": "#3388ff",
        "color": "#000000",
        "weight": 2,
        "fillOpacity": 0.1
    }
).add_to(m)

st.subheader("Welcher Kanton ist das?")
st_data = st_folium(m, width=700, height=500)

# ------------------ Eingabe und Auswertung ------------------
guess = st.text_input("Deine Antwort:", key="guess_input")
if st.button("✉️ Prüfen"):
    if not guess.strip():
        st.error("Bitte gib einen Kantonsnamen ein.")
    elif guess.strip().lower() == kanton_name.lower():
        st.success(f"Richtig! Es war {kanton_name}.")
        st.session_state.score += 1
    else:
        st.error(f"Leider falsch. Es war {kanton_name}.")
    # Bereits gezeigten Kanton verwerfen
    st.session_state.current = None


# ------------------ Punktestand ------------------
st.sidebar.header("📊 Statistik")
st.sidebar.write(f"Punktestand: **{st.session_state.score}**")
st.sidebar.write(f"Verbleibende Kantone: **{len(st.session_state.remaining)}**")
