
import streamlit as st
import base64

import base64

# ---------- Фон всей страницы: banner1.jpg (лёд по бокам) ----------
def set_page_background(path):
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.warning(f"⚠️ Не найден файл фона: {path}. Проверь, что он лежит в корне репозитория.")
        return
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{b64});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center top;
        }}
        .block-container {{
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 2rem 3rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_page_background("banner1.jpg")
    
# ---------- Баннер с фигуристкой ----------
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

b64 = img_to_b64("banner.jpg")

st.markdown(
    f"""
    <style>
    .hero {{
        background-image: url(data:image/jpg;base64,{b64});
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center top;
        min-height: 280px;
        margin-top: 10px;
        margin-bottom: 20px;
        mix-blend-mode: multiply;
    }}
    </style>
    <div class="hero"></div>
    """,
    unsafe_allow_html=True,
)



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

# ---------- Баннер-фон (картинка отдельно, под заголовком) ----------
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

b64 = img_to_b64("banner.jpg")

st.markdown(
    f"""
    <style>
    .hero {{
        background-image: url(data:image/png;base64,{b64});
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center top;
        min-height: 280px;
        border-radius: 20px;
        margin-top: 10px;
        margin-bottom: 20px;
    }}
    </style>
    <div class="hero"></div>
    """,
    unsafe_allow_html=True,
)

# ---------- Приветствие (теперь сразу после баннера) ----------
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

# ---------- Навигация: переходы + описания ----------
if lang == "Deutsch":
    st.header("🧭 Wo finde ich was?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link("pages/01_Wörterbuch.py", label="📖 Wörterbuch")
        st.write("Die komplette Wortliste mit Übersetzung, Grammatik und Suchfunktion.")
    with col2:
        st.page_link("pages/02_Über_das_Projekt.py", label="ℹ️ Über das Projekt")
        st.write("Worum es geht und wie das Wörterbuch entstanden ist.")
    with col3:
        st.page_link("pages/03_Wörterbuchzonen.py", label="🗂️ Wörterbuchzonen")
        st.write("Alle Kategorien — von Sprüngen bis Zubehör — sortiert und übersichtlich.")
else:
    st.header("🧭 Что где находится?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link("pages/01_Wörterbuch.py", label="📖 Словарь")
        st.write("Полный список слов с переводом, грамматикой и поиском.")
    with col2:
        st.page_link("pages/02_Über_das_Projekt.py", label="ℹ️ О проекте")
        st.write("О чём проект и как появился словарь.")
    with col3:
        st.page_link("pages/03_Wörterbuchzonen.py", label="🗂️ Тематические зоны")
        st.write("Все категории — от прыжков до инвентаря — отсортированы и на виду.")

st.divider()

# ---------- Подвал ----------
if lang == "Deutsch":
    st.markdown("Made with ❤️ für den Eiskunstlauf — viel Erfolg beim Lernen!")
else:
    st.markdown("Сделано с ❤️ для фигурного катания — успехов в изучении!")
