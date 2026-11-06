
import streamlit as st

st.set_page_config(
    page_title="Eiskunstlauf-Wörterbuch",
    layout="wide",
    page_icon="⛸️",
)

st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")
st.write("Wählen Sie im Menü links einen Abschnitt aus: **Wörterbuch**, **Über das Projekt** oder **Wörterbuchzonen**.")

# ---------- Приветствие ----------
st.markdown("""
Willkommen! 🧊

Dieses Wörterbuch hilft dir, die wichtigsten Begriffe des Eiskunstlaufs auf Deutsch
und Russisch zu lernen: von **Salchow** und **Lutz** bis zu **Walzsprüngen** und
**Hebefiguren**. Jedes Wort wird mit Übersetzung, Grammatik und Beispielen erklärt.
""")

# ---------- Статистика из словаря ----------
df = pd.read_csv("dictionary.csv")   # подставь свой файл/путь, как в 01_Wörterbuch.py

n_words = len(df)
n_verbs = int(df["grammar"].str.contains("Verb", na=False).sum())
n_nouns = n_words - n_verbs

c1, c2, c3 = st.columns(3)
c1.metric("📚 Wörter insgesamt", n_words)
c2.metric("🧍 Substantive", n_nouns)
c3.metric("🏃 Verben", n_verbs)

# ---------- Разделы ----------
st.header("🧭 Wo finde ich was?")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📖 Wörterbuch")
    st.write(
        "Die komplette Wortliste mit Übersetzung, Grammatik "
        "und Suchfunktion. Hier lernst du die Begriffe in Ruhe."
    )

with col2:
    st.subheader("ℹ️ Über das Projekt")
    st.write(
        "Worum es geht, wie das Wörterbuch entstanden ist und "
        "wer dahinter steckt."
    )

with col3:
    st.subheader("🗂️ Wörterbuchzonen")
    st.write(
        "Themenzonen: Sprünge, Drehungen, Schrittfolgen, "
        "Paarlaufen und mehr — alles nach Kategorien sortiert."
    )

st.divider()

# ---------- Подвал ----------
st.markdown("Made with ❄️ für den Eiskunstlauf — viel Erfolg beim Lernen!")
