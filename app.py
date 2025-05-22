import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import fiona
import random
import json
import matplotlib.pyplot as plt

# Daten laden
filename = "geodata/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
layer_name = "tlm_kantonsgebiet"
gdf = gpd.read_file(filename, layer=layer_name).to_crs(epsg=2056)

# Namen extrahieren
namen_liste = []
with fiona.open(filename, layer=layer_name) as src:
    for feature in src:
        name = feature["properties"].get("name")
        if name:
            namen_liste.append(name)
namen_liste = sorted(set(namen_liste))

# Streamlit-Konfiguration
st.set_page_config(page_title="Spiel", layout="wide")
st.title("Kantonsumrisse erkennen Schweiz")

# Session-State-Variablen
if "remaining" not in st.session_state:
    st.session_state.remaining = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = None
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "spiel_gestartet" not in st.session_state:
    st.session_state.spiel_gestartet = False

# Spiel starten
if st.button("▶️ Spiel starten"):
    st.session_state.remaining = namen_liste.copy()
    st.session_state.score = 0
    st.session_state.current = None
    st.session_state.spiel_gestartet = True
    st.session_state.feedback = ""

if not st.session_state.spiel_gestartet:
    st.info("Drücke **Spiel starten**, um zu beginnen.")
    st.stop()

# Nächster Kanton
if st.button("⏭️ Weiter"):
    if not st.session_state.remaining:
        st.session_state.feedback = "Alle Kantone waren dran. Spiel zurückgesetzt!"
        st.session_state.remaining = namen_liste.copy()
        st.session_state.current = None
    else:
        st.session_state.current = random.choice(st.session_state.remaining)
        st.session_state.remaining.remove(st.session_state.current)
        st.session_state.feedback = ""

# Nur anzeigen, wenn ein Kanton aktiv ist
if st.session_state.current:
    # Kanton anzeigen
    zufaellig = gdf[gdf["name"] == st.session_state.current].iloc[0]
    Koordinaten = zufaellig.geometry
    gdf_plot = gpd.GeoDataFrame(geometry=[Koordinaten])
    col1, col2, col3 = st.columns([1, 4, 1])  # Zentrierung: 2/3 Breite in der Mitte
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 8))
        gdf_plot.plot(ax=ax, color='lightblue', edgecolor='black')
        ax.axis('off')
        st.pyplot(fig)

    # Auswahlformular
    with st.form("antwort_form"):
        auswahl = st.selectbox("Welcher Kanton ist das?", namen_liste)
        prüfen = st.form_submit_button("✅ Bestätigen")

    if prüfen:
        if auswahl == st.session_state.current:
            st.session_state.score += 1
            st.session_state.feedback = f"✅ Richtig! Das war **{st.session_state.current}**."
        else:
            st.session_state.feedback = f"❌ Falsch! Das war **{st.session_state.current}**."
        st.session_state.current = None  # Antwort wurde abgegeben

# Rückmeldung
if st.session_state.feedback:
    st.success(st.session_state.feedback)

# Sidebar
st.sidebar.header("📊 Statistik")
st.sidebar.write(f"Punktestand: **{st.session_state.score}**")
st.sidebar.write(f"Verbleibende Kantone: **{len(st.session_state.remaining)}**")
