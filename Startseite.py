
import streamlit as st

st.set_page_config(
    page_title="Eiskunstlauf-Wörterbuch",
    layout="wide",
    page_icon="⛸️",
)

# ---------- Выбор языка (сначала!) ----------
lang = st.sidebar.radio("🌐 Sprache / Язык", ["Deutsch", "Русский"])

# ---------- Заголовок ----------
if lang == "Deutsch":
    st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")
else:
    st.title("📖 Немецко-русский словарь терминологии фигурного катания")

# ---------- Навигация: цветная плашка ----------
if lang == "Deutsch":
    st.info(
        "🧭 **Wählen Sie einen Abschnitt aus:**  Wörterbuch · Über das Projekt · Wörterbuchzonen",
        icon="➡️",
    )
else:
    st.info(
        "🧭 **Выберите раздел:**  Словарь · О проекте · Тематические зоны",
        icon="➡️",
    )

# ---------- Статистика ----------
N_WÖRTER = 240
KATEGORIEN = [
    "Technik", "Sprünge", "Pirouetten", "Schritte", "Choreosequenz",
    "Grundelemente", "Einzellauf", "Paarlauf", "Eistanz",
    "Synchroneiskunstlauf", "Richterlexikon", "Abkürzungen", "Zubehör",
]

if lang == "Deutsch":
    c1, c2 = st.columns(2)
    c1.metric("📚 Wörter insgesamt", N_WÖRTER)
    c2.metric("🗂️ Kategorien", len(KATEGORIEN))
else:
    c1, c2 = st.columns(2)
    c1.metric("📚 Всего слов", N_WÖRTER)
    c2.metric("🗂️ Категорий", len(KATEGORIEN))

# ---------- Приветствие ----------
if lang == "Deutsch":
    st.markdown(
        """
        ### Willkommen! 🧊

        Ein Projekt für alle, die den Eiskunstlauf auf Deutsch und Russisch
        verstehen wollen. In diesem Wörterbuch findest du **240 Einträge**
        aus 13 Kategorien — von **Sprüngen** und **Pirouetten** bis zum
        **Paarlauf** und **Richterlexikon**. Jedes Wort wird mit Übersetzung
        und Grammatik erklärt.
        """
    )
else:
    st.markdown(
        """
        ### Добро пожаловать! 🧊

        Проект для всех, кто хочет понимать фигурное катание на немецком
        и русском. В словаре **240 записей** в 13 категориях — от **прыжков**
        и **вращений** до **парного катания** и **словаря судьи**.
        Каждое слово даётся с переводом и грамматикой.
        """
    )

# ---------- Разделы: по одному блоку на каждый язык ----------
if lang == "Deutsch":
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
if lang == "Deutsch":
    st.subheader("🗂️ Wörterbuchzonen")
else:
    st.subheader("🗂️ Тематические зоны")
st.write(" ".join(f"`{k}`" for k in KATEGORIEN))

st.divider()

# ---------- Подвал ----------
if lang == "Deutsch":
    st.markdown("Made with ❄️ für den Eiskunstlauf — viel Erfolg beim Lernen!")
else:
    st.markdown("Сделано с ❄️ для фигурного катания — успехов в изучении!")
