# Web-App: Kantonsumrisse der Schweiz erkennen 

Zum [Spiel](https://kantonsumrisse-ch-erkennen.streamlit.app)

Der Spielaufbau und weitere Informationen zum Spiel sieht man auf der [GitHub Pages.](https://ckeller888.github.io/CLS.py/)


## Repository lokal klonen

Mit Git in einem Terminal das GitHub Repository in ein lokales Verzeichnis klonen.

```shell
cd /path/to/workspace
# Clone Repository
git clone https://github.com/ckeller888/CLS.py
```

oder  

Öffne ein neues Visual Studio Code Fenster und wähle unter Start *Clone Git Repository*. Alternativ öffne die Command Palette in VS Code `CTRL+Shift+P` (*View / Command Palette*) und wähle `Git: clone`.
Füge die Git web URL `https://github.com/ckeller888/CLS.py` ein und bestätige die Eingabe mit Enter. Wähle einen Ordner in welchen das Repository *geklont* werden soll.


### streamlit & requirements installieren
``` shell
# Erstelle ein neues Conda Environment und füge die Python Packges requirements.txt hinzu
conda create --name map-game python=3.11
# aktiviere die conda Umgebung map-game
conda activate map-game
# Bibliotheken importieren
pip install -r requirements.txt
```

### Web-App starten
``` shell
# Webapp starten
streamlit run app.py
```
