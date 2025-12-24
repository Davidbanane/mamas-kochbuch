import streamlit as st
import random
import json
import os

# --- 1. Funktionen zum Laden und Speichern der Daten ---
DATEI_NAME = "gerichte.json"

def lade_gerichte():
    if not os.path.exists(DATEI_NAME):
        return [] # Leere Liste zurückgeben, falls Datei nicht existiert
    with open(DATEI_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def speichere_gerichte(gerichte_liste):
    with open(DATEI_NAME, "w", encoding="utf-8") as f:
        json.dump(gerichte_liste, f, ensure_ascii=False, indent=4)

# --- 2. App Layout und Logik ---

st.title("🍳 Mamas Koch-Ideen")

# Daten laden
gerichte = lade_gerichte()

# Wir nutzen Tabs für eine saubere Übersicht
tab1, tab2, tab3 = st.tabs(["🎲 Was kochen?", "➕ Neu", "🗑️ Entfernen"])

# TAB 1: ZUFALLSGERICHT
with tab1:
    st.header("Mir fällt nichts ein...")
    if st.button("Schlag mir was vor!", type="primary"):
        if gerichte:
            vorschlag = random.choice(gerichte)
            st.success(f"Wie wäre es heute mit: **{vorschlag}**? 😋")
            st.balloons() # <-- NEU: Lässt Luftballons steigen (visueller Effekt)
            
            # NEU: Ein Link zum Rezept
            # Wir bauen eine Google-Such-URL zusammen
            such_url = f"https://www.google.com/search?q=Rezept+{vorschlag.replace(' ', '+')}"
            st.link_button("Rezept im Internet suchen 🔍", such_url)
            
        else:
            st.warning("Die Liste ist noch leer!")

# TAB 2: GERICHT HINZUFÜGEN
with tab2:
    st.header("Neues Lieblingsgericht hinzufügen")
    neues_gericht = st.text_input("Name des Gerichts:")
    
    if st.button("Speichern"):
        # Korrektur: Hier stand vorher fälschlicherweise "new_gericht"
        if neues_gericht and neues_gericht not in gerichte:
            gerichte.append(neues_gericht)
            speichere_gerichte(gerichte)
            st.success(f"'{neues_gericht}' wurde hinzugefügt!")
            st.rerun() # Seite neu laden, um Liste zu aktualisieren
        elif neues_gericht in gerichte:
            st.error("Das Gericht steht schon auf der Liste.")
        else:
            st.error("Bitte gib einen Namen ein.")

# TAB 3: GERICHTE LÖSCHEN
with tab3:
    st.header("Gericht von der Liste streichen")
    if gerichte:
        # Ein Dropdown Menü zum Auswählen
        zu_loeschen = st.selectbox("Welches Gericht soll weg?", gerichte)
        
        if st.button("Löschen"):
            gerichte.remove(zu_loeschen)
            speichere_gerichte(gerichte)
            st.success(f"'{zu_loeschen}' wurde gelöscht.")
            st.rerun()
    else:
        st.info("Keine Gerichte zum Löschen vorhanden.")

# Unten auf der Seite die komplette Liste anzeigen (optional)
st.divider()
st.caption(f"Aktuell sind {len(gerichte)} Gerichte in der Datenbank.")
with st.expander("Alle Gerichte ansehen"):
    for gericht in sorted(gerichte):
        st.write(f"- {gericht}")