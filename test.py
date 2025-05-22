import fiona
import zipfile

with zipfile.ZipFile(
    "geodata/packages/swissboundaries3d_2025-04_2056_5728.gpkg.zip", "r"
) as zip_ref:
    zip_ref.extractall("geodata")

filename = "geodata/packages/swissboundaries3d_2025-04_2056_5728.gpkg"
c = fiona.open(filename, "r", layer="ne_10m_populated_places")
