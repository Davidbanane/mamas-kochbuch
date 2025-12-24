import streamlit as st
import random
import json
import os

# --- Konfiguration der Seite ---
st.set_page_config(page_title="Mamas Kochbuch", page_icon="🍳")

# --- Daten laden ---
DATEI_NAME = "gerichte.json"

def lade_gerichte():
    if not os.path.exists(DATEI_NAME):
        return []
    with open(DATEI_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Hauptbereich der App ---
st.title("🍳 Mamas Koch-Ideen")
st.write("Lass den Zufall entscheiden, was es heute gibt!")

# Gerichte laden
gerichte = lade_gerichte()

if not gerichte:
    st.error("Hoppla! Die Liste 'gerichte.json' wurde nicht gefunden oder ist leer.")
else:
    # Der große Button
    st.divider()
    if st.button("🎲 Was soll ich heute kochen?", type="primary", use_container_width=True):
        
        # 1. Zufälliges Gericht wählen
        vorschlag = random.choice(gerichte)
        
        # 3. Das Gericht groß anzeigen
        st.markdown(f"<h2 style='text-align: center; color: #2e7d32;'>{vorschlag}</h2>", unsafe_allow_html=True)
        st.write("") # Kleiner Abstand
        
        # 4. Der Google-Rezept Link
        # Wir bauen den Link so: https://www.google.com/search?q=Rezept+Wiener+Schnitzel...
        such_begriff = f"Rezept {vorschlag}"
        google_link = f"https://www.google.com/search?q={such_begriff.replace(' ', '+')}"
        
        # Button zentriert anzeigen (mit Spalten-Trick)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.link_button(f"🔍 Rezept für '{vorschlag}' suchen", google_link, use_container_width=True)

    st.divider()

    # --- Liste aller Gerichte (Nur Lesen) ---
    with st.expander(f"📚 Alle {len(gerichte)} Gerichte ansehen"):
        # Wir sortieren die Liste alphabetisch für bessere Übersicht
        for gericht in sorted(gerichte):
            st.write(f"• {gericht}")