
import streamlit as st

st.set_page_config(
    page_title="Eiskunstlauf-Wörterbuch",
    layout="wide",
    page_icon="⛸️",
)

st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")
st.write("Wählen Sie im Menü links einen Abschnitt aus: **Wörterbuch**, **Über das Projekt** oder **Wörterbuchzonen**.")

# ---------- Выбор языка ----------
lang = st.sidebar.radio("🌐 Sprache / Язык", ["Deutsch", "Русский"])

st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")

# ---------- Статистика ----------
KATEGORIEN = [
    "Technik", "Sprünge", "Pirouetten", "Schritte", "Choreosequenz",
    "Grundelementen", "Einzellauf", "Paarlauf", "Eistanz",
    "Synchroneiskunstlauf", "Richterlexikon", "Abkürzungen", "Zubehör",
]
N_WÖRTER = 240
N_KATEGORIEN = len(KATEGORIEN)

c1, c2 = st.columns(2)
c1.metric("📚 Wörter / Слов" if lang == "Deutsch" else "📚 Всего слов",
          N_WÖRTER)
c2.metric("🗂️ Kategorien / Категорий" if lang == "Deutsch" else "🗂️ Категорий",
          N_KATEGORIEN)

# ---------- Приветствие ----------
if lang == "Deutsch":
    st.caption("Ein Projekt für alle, die den Eiskunstlauf auf Deutsch und Russisch verstehen wollen.")
    st.markdown("""
    Willkommen! 🧊

    In diesem Wörterbuch findest du **240 Einträge** aus 13 Kategorien —
    von **Sprüngen** und **Pirouetten** bis zum **Paarlauf** und
    **Richterlexikon**. Jedes Wort wird mit Übersetzung und Grammatik erklärt.
    """)
    st.header("🧭 Wo finde ich was?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📖 Wörterbuch")
        st.write("Die komplette Wortliste mit Übersetzung, Grammatik und Suchfunktion.")
    with col2:
        st.subheader("ℹ️ Über das Projekt")
        st.write("Worum es geht und wie das Wörterbuch entstanden ist.")
    with col3:
        st.subheader("🗂️ Wörterbuchzonen")
        st.write("Alle Kategorien — von Sprüngen bis Zubehör — sortiert und übersichtlich.")
else:
    st.caption("Проект для всех, кто хочет понимать фигурное катание на немецком и русском.")
    st.markdown("""
    Добро пожаловать! 🧊

    В словаре **240 записей** в 13 категориях — от **прыжков** и **вращений**
    до **парного катания** и **словаря судьи**. Каждое слово даётся
    с переводом и грамматикой.
    """)
    st.header("🧭 Что где находится?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📖 Словарь")
        st.write("Полный список слов с переводом, грамматикой и поиском.")
    with col2:
        st.subheader("ℹ️ О проекте")
        st.write("О чём проект и как появился словарь.")
    with col3:
        st.subheader("🗂️ Тематические зоны")
        st.write("Все категории — от прыжков до инвентаря — отсортированы и на виду.")

st.divider()

# ---------- Категории «плашками» ----------
st.subheader("🗂️ Wörterbuchzonen / Тематические зоны" if lang == "Deutsch"
             else "🗂️ Тематические зоны")
st.write(" ".join(f"`{k}`" for k in KATEGORIEN))

st.divider()
st.markdown("Made with ❄️ für den Eiskunstlauf — viel Erfolg beim Lernen! / Успехов в изучении!")
