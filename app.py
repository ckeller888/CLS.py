import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import fiona
# import PyQt5

filename = "geodata/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
layer_name = "tlm_kantonsgebiet"

gdf = gpd.read_file(filename, layer=layer_name)

# Streamlit-Konfiguration
st.set_page_config(page_title="Spiel", layout="wide")
st.title("Kantonsumrisse erkennen Schweiz")

# Play Button
if st.button("Play"):
    st.write("geklickt!")

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

# Textfeld mit Filterfunktion
#eingabe = st.text_input("Kantonsname:")

# Liste der Optionen
optionen = namen_liste

# Dropdown
auswahl = st.selectbox("Wähle einen Kanton:", optionen)

# Button zum Bestätigen
if st.button("Bestätigen"):
    st.write(f"Du hast bestätigt: **{auswahl}**")


# Punktestand initialisieren
if "points" not in st.session_state:
    st.session_state.points = 0

# Startposition auf die Schweiz setzen
swiss_center = [46.8182, 8.2275]
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
