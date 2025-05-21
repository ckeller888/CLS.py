import streamlit as st
import folium
from streamlit_folium import st_folium

# Streamlit-Konfiguration
st.set_page_config(page_title="Spiel", layout="wide")
st.title("🇨🇭 Karten-Spiel Schweiz - Klick dich zu Punkten!")

# Punktestand initialisieren
if "points" not in st.session_state:
    st.session_state.points = 0

# Startposition auf die Schweiz setzen
swiss_center = [46.8182, 8.2275]  # Geografisches Zentrum der Schweiz
m = folium.Map(location=swiss_center, zoom_start=8)

# Spielpunkte: Städte in der Schweiz
game_points = [
    {"name": "Zürich", "coords": [47.3769, 8.5417]},
    {"name": "Bern", "coords": [46.9481, 7.4474]},
    {"name": "Genf", "coords": [46.2044, 6.1432]},
    {"name": "Lugano", "coords": [46.0037, 8.9511]},
    {"name": "Basel", "coords": [47.5596, 7.5886]},
]

# Marker zu Karte hinzufügen
for point in game_points:
    folium.Marker(
        location=point["coords"],
        popup=f"<b>{point['name']}</b>",
        tooltip="Klick mich!",
        icon=folium.Icon(color="red", icon="star"),
    ).add_to(m)

# Karte anzeigen und Klick erfassen
map_data = st_folium(m, width=800, height=600)

# Klick auswerten
if map_data["last_object_clicked"]:
    clicked = map_data["last_object_clicked"]
    st.session_state.points += 1

# Punktestand anzeigen
st.header(f"Punktestand: {st.session_state.points}")
