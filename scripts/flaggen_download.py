import os
import requests
from urllib.parse import quote
import cairosvg

# Liste der 26 Kantone (verwende möglichst offizielle Schreibweise)
kantone = [
    "Aargau",
    "Appenzell Ausserrhoden",
    "Appenzell Innerrhoden",
    "Basel-Landschaft",
    "Basel-Stadt",
    "Bern",
    "Freiburg",
    "Genf",
    "Glarus",
    "Graubünden",
    "Jura",
    "Luzern",
    "Neuenburg",
    "Nidwalden",
    "Obwalden",
    "Schaffhausen",
    "Schwyz",
    "Solothurn",
    "St. Gallen",
    "Tessin",
    "Thurgau",
    "Uri",
    "Waadt",
    "Wallis",
    "Zug",
    "Zürich",
]

# Speicherort für die Bilder
output_dir = "flags_svg"
os.makedirs(output_dir, exist_ok=True)

# Basis-URL bei Wikimedia Commons
base_url = (
    # "https://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20{}%20canton.svg"
    # "https://upload.wikimedia.org/wikipedia/commons/2/2c/Wappen_%20%20{}%20_matt.svg"
    "https://de.wikipedia.org/wiki/Liste_der_Wappen_und_Fahnen_der_Schweizer_Kantone#/media/Datei:Wappen_%20%20{}%20_matt.png"
)

for kanton in kantone:
    # Erzeuge URL mit kodiertem Kantonsnamen
    url = base_url.format(quote(kanton))
    filename = f"{output_dir}/{kanton}.svg"

    try:
        print(f"Lade {kanton} ...")
        r = requests.get(url)
        r.raise_for_status()
        with open(filename, "wb") as f:
            f.write(r.content)
        print(f"Gespeichert: {filename}")
    except Exception as e:
        print(f"Fehler bei {kanton}: {e}")


# Eingabe- und Ausgabeordner
svg_dir = "flags_svg"
png_dir = "flags_png"

# PNG-Ausgabeordner erstellen (falls nicht vorhanden)
os.makedirs(png_dir, exist_ok=True)

# Alle SVGs durchgehen und konvertieren
for filename in os.listdir(svg_dir):
    if filename.endswith(".svg"):
        svg_path = os.path.join(svg_dir, filename)
        png_path = os.path.join(png_dir, filename.replace(".svg", ".png"))
        print(f"Konvertiere {filename} ...")
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        print(f"✅ Gespeichert: {png_path}")
