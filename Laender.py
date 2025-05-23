import streamlit as st
import geopandas as gpd
import fiona
import random
import matplotlib.pyplot as plt
from shapely.affinity import translate
import numpy as np
import cartopy.crs as ccrs


# Streamlit-Konfiguration
st.set_page_config(page_title="Länder-Spiel", layout="wide")
st.title("Länderumrisse der ganzen Welt erkennen")

# Daten laden
filename = "geodata/geoBoundariesCGAZ_ADM0.gpkg"
layer_laender = "globalADm0"

@st.cache_data
def load_data():
    gdf = gpd.read_file(filename, layer=layer_laender).to_crs(epsg=4326)
    return gdf
gdf_land = load_data()

namen_liste = sorted({f["properties"]["shapeName"] for f in fiona.open(filename, layer=layer_laender)})

# Session-State initialisieren
for key, default in {
    "remaining": [],
    "score": 0,
    "current": None,
    "feedback": "",
    "feedback_color": "success",
    "spiel_gestartet": False,
    "antwort_gegeben": False,
    "auswahl": None,
    "richtig_gewählt": [],
    "falsch_gewählt": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sidebar – Statistik
st.sidebar.header("Statistik")
st.sidebar.write(f"Punktestand: **{st.session_state.score}**")
st.sidebar.write(f"Verbleibende Länder: **{len(st.session_state.remaining)}**")
st.sidebar.write(f"Richtig beantwortet: **{len(st.session_state.richtig_gewählt)}**")
st.sidebar.write(f"Falsch beantwortet: **{len(st.session_state.falsch_gewählt)}**")

# Spiel starten oder neu starten
start_label = "🔄 Neu starten" if st.session_state.spiel_gestartet else "▶️ Spiel starten"
if st.button(start_label):
    st.session_state.spiel_laender = random.sample(namen_liste, 30)
    st.session_state.remaining = st.session_state.spiel_laender.copy()
    st.session_state.score = 0
    st.session_state.spiel_gestartet = True
    st.session_state.feedback = ""
    st.session_state.antwort_gegeben = False
    st.session_state.current = random.choice(st.session_state.remaining)
    st.session_state.remaining.remove(st.session_state.current)
    st.session_state.auswahl = None
    st.session_state.richtig_gewählt = []
    st.session_state.falsch_gewählt = []

if not st.session_state.spiel_gestartet:
    st.info("Drücke **Spiel starten**, um zu beginnen.")
    st.stop()

# Wenn noch keine Antwort gegeben wurde: Land zeigen & Formular
if not st.session_state.antwort_gegeben and st.session_state.current:
    land_geom = gdf_land[gdf_land["shapeName"] == st.session_state.current].geometry.iloc[0]
    bounds = land_geom.bounds
    gdf_geom = gpd.GeoDataFrame(geometry=[land_geom])

    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        fig, ax = plt.subplots(figsize=(4, 4), dpi=400)
        gdf_geom.plot(ax=ax, color='lightblue', edgecolor='black')
        ax.axis('off')
        st.pyplot(fig)


    with st.form("antwort_form"):
        auswahl = st.selectbox("Welches Land ist das?", namen_liste)
        prüfen = st.form_submit_button("Bestätigen")

    if prüfen:
        st.session_state.antwort_gegeben = True
        st.session_state.auswahl = auswahl
        korrekt = auswahl == st.session_state.current

        if korrekt:
            st.session_state.score += 1
            st.session_state.feedback = f"Richtig! Das war **{st.session_state.current}**."
            st.session_state.feedback_color = "success"
            st.session_state.richtig_gewählt.append(st.session_state.current)
        else:
            st.session_state.feedback = f"Falsch! Das war **{st.session_state.current}**."
            st.session_state.feedback_color = "error"
            st.session_state.falsch_gewählt.append(st.session_state.current)

# Nach Antwort: Weltkarte mit Verlauf zeigen
if st.session_state.antwort_gegeben:
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:

#         # plt.figure(figsize=(15, 9))
#         fig2, ax2 = plt.subplots(figsize=(6, 4), dpi=100)
#         ax2 = plt.axes(projection=ccrs.PlateCarree())
#         ax2.coastlines(resolution="110m")
#         ax2.gridlines()
#         gdf_land.plot(ax=ax2, color='white', edgecolor='black')

#         # Falsche Länder rot
#         if st.session_state.falsch_gewählt:
#             gdf_land[gdf_land["shapeName"].isin(st.session_state.falsch_gewählt)].plot(ax=ax2, color='red', edgecolor='black', alpha=0.5)

#         # Richtige Länder grün
#         if st.session_state.richtig_gewählt:
#             gdf_land[gdf_land["shapeName"].isin(st.session_state.richtig_gewählt)].plot(ax=ax2, color='green', edgecolor='black', alpha=0.5)

#         ax2.axis('off')
#         st.pyplot(fig2)

    if st.session_state.feedback_color == "success":
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

    if st.button("⏭️ Weiter"):
        st.session_state.antwort_gegeben = False
        st.session_state.feedback = ""
        st.session_state.auswahl = None

        if st.session_state.remaining:
            st.session_state.current = random.choice(st.session_state.remaining)
            st.session_state.remaining.remove(st.session_state.current)
        else:
            st.session_state.current = None
            st.session_state.spiel_gestartet = False
            st.success("Alle Länder waren dran. Spiel beendet!")
        st.rerun()

        