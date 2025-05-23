import streamlit as st
import geopandas as gpd
import fiona
import random
import matplotlib.pyplot as plt
from shapely.affinity import translate

# Streamlit-Konfiguration
st.set_page_config(page_title="Kantons-Spiel", layout="wide")
st.title("Kantonsumrisse der Schweiz erkennen")

# Daten laden
filename = "geodata/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
layer_kanton = "tlm_kantonsgebiet"
layer_land = "tlm_landesgebiet"

gdf = gpd.read_file(filename, layer=layer_kanton).to_crs(epsg=2056)
land = gpd.read_file(filename, layer=layer_land).to_crs(epsg=2056)
schweiz_geom = land[land["name"] == "Schweiz"].geometry.iloc[0]

namen_liste = sorted({f["properties"]["name"] for f in fiona.open(filename, layer=layer_kanton)})

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
st.sidebar.write(f"Verbleibende Kantone: **{len(st.session_state.remaining)}**")
st.sidebar.write(f"Richtig beantwortet: **{len(st.session_state.richtig_gewählt)}**")
st.sidebar.write(f"Falsch beantwortet: **{len(st.session_state.falsch_gewählt)}**")

# Spiel starten oder neu starten
start_label = "🔄 Neu starten" if st.session_state.spiel_gestartet else "▶️ Spiel starten"
if st.button(start_label):
    st.session_state.remaining = namen_liste.copy()
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

# Wenn noch keine Antwort gegeben wurde: Kanton zeigen & Formular
if not st.session_state.antwort_gegeben and st.session_state.current:
    kanton_geom = gdf[gdf["name"] == st.session_state.current].geometry.iloc[0]
    bounds = kanton_geom.bounds
    gdf_kanton = gpd.GeoDataFrame(geometry=[kanton_geom])

    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        fig, ax = plt.subplots(figsize=(4, 4), dpi=600)
        gdf_kanton.plot(ax=ax, color='lightblue', edgecolor='black')
        ax.axis('off')
        st.pyplot(fig)


    with st.form("antwort_form"):
        auswahl = st.selectbox("Welcher Kanton ist das?", namen_liste)
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

        st.rerun()    
    
# Nach Antwort: Schweizkarte mit Verlauf zeigen
elif st.session_state.antwort_gegeben:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 8), dpi=600)
        gpd.GeoDataFrame(geometry=[schweiz_geom]).plot(ax=ax2, color='white', edgecolor='black')

        # Falsche Kantone rot
        if st.session_state.falsch_gewählt:
            gdf[gdf["name"].isin(st.session_state.falsch_gewählt)].plot(ax=ax2, color='red', edgecolor='black', alpha=0.5)

        # Richtige Kantone grün
        if st.session_state.richtig_gewählt:
            gdf[gdf["name"].isin(st.session_state.richtig_gewählt)].plot(ax=ax2, color='green', edgecolor='black', alpha=0.5)

        ax2.axis('off')
        st.pyplot(fig2)

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
            st.success("Alle Kantone waren dran. Spiel beendet!")
        
        st.rerun()
