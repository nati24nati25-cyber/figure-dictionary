
import streamlit as st
import base64

st.set_page_config(
    page_title="Eiskunstlauf-Wörterbuch",
    layout="wide",
    page_icon="⛸️",
)

# ---------- Выбор языка (сначала!) ----------
lang = st.sidebar.radio("🌐 Sprache / Язык", ["Deutsch", "Русский"])

# ---------- Баннер-фон (заголовок внутри него) ----------
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

b64 = img_to_b64("banner.png")

titel = ("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie"
         if lang == "Deutsch"
         else "📖 Немецко-русский словарь терминологии фигурного катания")
untertitel = ("Ein Projekt mit ❤️ für den Eiskunstlauf"
              if lang == "Deutsch"
              else "Проект с ❤️ для фигурного катания")

st.markdown(
    f"""
    <style>
    .hero {{
        background-image: linear-gradient(
            rgba(255, 255, 255, 0.75),
            rgba(255, 255, 255, 0.75)
        ), url(data:image/png;base64,{b64});
        background-size: cover;
        background-position: center;
        padding: 60px 40px;
        border-radius: 20px;
        margin-bottom: 20px;
    }}
    .hero h1 {{
        margin: 0;
    }}
    </style>

    <div class="hero">
        <h1>{titel}</h1>
        <h3 style="font-weight: normal;">{untertitel}</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

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

# ---------- Приветствие ----------
if lang == "Deutsch":
    st.markdown(
        """
        ### Willkommen! ⛸️❄️

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
        ### Добро пожаловать! ⛸️❄️

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

# ---------- Подвал ----------
if lang == "Deutsch":
    st.markdown("Made with ❤️ für den Eiskunstlauf — viel Erfolg beim Lernen!")
else:
    st.markdown("Сделано с ❤️ для фигурного катания — успехов в изучении!")
