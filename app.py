import streamlit as st
import random
import json
import os

# --- Konfiguration der Seite ---
st.set_page_config(page_title="Mamas Kochbuch", page_icon="🍳")

# --- Konstanten ---
DATEI_NAME = "gerichte.json"
PERSONEN = ["Mama", "Papa", "David", "Manuel"]

def lade_gerichte():
    if not os.path.exists(DATEI_NAME):
        return []
    with open(DATEI_NAME, "r", encoding="utf-8") as f:
        daten = json.load(f)
        
    # Sicherheits-Check: Falls noch das alte Format (Strings) vorliegt,
    # behandeln wir es temporär so, als ob es jeder mag, damit die App nicht abstürzt.
    if daten and isinstance(daten[0], str):
        return [{"name": g, "Mama": True, "Papa": True, "David": True, "Manuel": True} for g in daten]
    
    return daten

# --- Hauptbereich der App ---
st.title("🍳 Mamas Koch-Ideen")
st.write("Lass den Zufall entscheiden, was es heute gibt!")

# Gerichte laden
alle_gerichte = lade_gerichte()

if not alle_gerichte:
    st.error("Hoppla! Die Liste 'gerichte.json' wurde nicht gefunden oder ist leer.")
else:
    # --- Sidebar für Filter ---
    st.sidebar.header("Wer isst heute mit?")
    st.sidebar.write("Hake an, wer zufrieden sein muss:")
    
    # Wir erstellen ein Dictionary mit den Zuständen der Checkboxen
    filter_aktiv = {}
    for p in PERSONEN:
        # Standardmäßig sind alle angehakt (True)
        filter_aktiv[p] = st.sidebar.checkbox(p, value=True)

    # --- Filtern ---
    # Wir behalten nur Gerichte, bei denen ALLE angehakten Personen "True" haben
    moegliche_gerichte = []
    
    for gericht in alle_gerichte:
        passt = True
        for p in PERSONEN:
            # Wenn Person angehakt ist (isst mit), ABER das Gericht nicht mag -> passt nicht
            if filter_aktiv[p] and not gericht.get(p, True):
                passt = False
                break
        if passt:
            moegliche_gerichte.append(gericht)

    # Anzahl anzeigen
    st.info(f"{len(moegliche_gerichte)} von {len(alle_gerichte)} Gerichten passen zu dieser Auswahl.")

    st.divider()

    # --- Der Button ---
    if st.button("🎲 Was soll ich heute kochen?", type="primary", use_container_width=True):
        
        if not moegliche_gerichte:
            st.warning("Oje! Für diese Kombination an Essern gibt es kein Gericht in der Liste.")
        else:
            # 1. Zufälliges Gericht wählen
            gewinner = random.choice(moegliche_gerichte)
            vorschlag_name = gewinner["name"]
            
            # 2. Das Gericht groß anzeigen
            st.markdown(f"<h2 style='text-align: center; color: #2e7d32;'>{vorschlag_name}</h2>", unsafe_allow_html=True)
            
            # Zeigen, wer es mag (optional, als kleine Info darunter)
            fans = [p for p in PERSONEN if gewinner.get(p, True)]
            st.caption(f"Schmeckt: {', '.join(fans)}")
            
            st.write("") # Kleiner Abstand
            
            # 3. Der Google-Rezept Link
            such_begriff = f"Rezept {vorschlag_name}"
            google_link = f"https://www.google.com/search?q={such_begriff.replace(' ', '+')}"
            
            # Button zentriert
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.link_button(f"🔍 Rezept für '{vorschlag_name}' suchen", google_link, use_container_width=True)

    st.divider()

    # --- Liste aller Gerichte (Nur Lesen) ---
    with st.expander(f"📚 Alle Gerichte ansehen"):
        # Alphabetisch sortieren
        for gericht in sorted(alle_gerichte, key=lambda x: x['name']):
            # Icons basierend auf Likes anzeigen? 
            # Wir machen es simpel: Name + Info wenn es jemand NICHT mag
            nicht_fans = [p for p in PERSONEN if not gericht.get(p, True)]
            zusatz = ""
            if nicht_fans:
                zusatz = f" (nicht für: {', '.join(nicht_fans)})"
            
            st.write(f"• {gericht['name']}{zusatz}")