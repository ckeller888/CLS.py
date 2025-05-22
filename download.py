import zipfile

with zipfile.ZipFile(
    "geodata/swissboundaries3d_2025-04_2056_5728.gpkg.zip", "r"
) as zip_ref:
    zip_ref.extractall("geodata")
