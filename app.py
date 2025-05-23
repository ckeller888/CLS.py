import streamlit as st
import flaggen
import namen



st.set_page_config(page_title="Kantons-Spiel", layout="wide")



# Nur beim ersten Laden setzen
if "spiel" not in st.session_state:
    st.session_state.spiel = None

# Titel und Modus-Auswahl nur anzeigen, wenn kein Spiel läuft

if st.session_state.spiel is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Kantonsumrisse der Schweiz erkennen")
        st.write("Wähle einen Spielmodus:")

        if st.button("Spiel mit Kantonsnamen"):
            st.session_state.spiel = "namen"
            st.rerun()

        if st.button("Spiel mit Kantonswappen"):
            st.session_state.spiel = "flaggen"
            st.rerun()

# Spiel starten und Zurück-Button nur anzeigen, wenn ein Spiel läuft
else:
    if st.session_state.spiel == "flaggen":
        flaggen.run()
    elif st.session_state.spiel == "namen":
        namen.run()

    st.sidebar.markdown("---")
    if st.sidebar.button("Zurück zur Moduswahl"):
        st.session_state.spiel = None
        # Statistik und Spielfortschritt zurücksetzen
        for key in [
            "remaining",
            "score",
            "current",
            "feedback",
            "feedback_color",
            "spiel_gestartet",
            "antwort_gegeben",
            "auswahl",
            "richtig_gewählt",
            "falsch_gewählt",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("geodata/Schweiz.png", width=720)