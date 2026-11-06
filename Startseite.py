
import streamlit as st
import base64

st.set_page_config(
    page_title="Eiskunstlauf-Wörterbuch",
    layout="wide",
    page_icon="⛸️",
)

# ---------- Выбор языка ----------
lang = st.sidebar.radio("🌐 Sprache / Язык", ["Deutsch", "Русский"])

# ---------- Заголовок (строго сверху) ----------
if lang == "Deutsch":
    st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")
else:
    st.title("📖 Немецко-русский словарь терминологии фигурного катания")

# ---------- Подзаголовок (строго под заголовком) ----------
untertitel = ("Ein Projekt mit ❤️ für den Eiskunstlauf"
              if lang == "Deutsch"
              else "Проект с ❤️ для фигурного катания")
st.subheader(untertitel)

# ---------- Картинка-баннер (чуть ниже, голова не обрежется!) ----------
# Сначала готовим base64, чтобы картинка точно загрузилась
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

b64 = img_to_b64("banner.png")

# Добавляем CSS для полупрозрачной вуали прямо на картинку
st.markdown(
    f"""
    <style>
    .banner-wrapper {{
        position: relative;
        display: block;
        margin-top: 20px;       /* отступ от подзаголовка */
        border-radius: 20px;
        overflow: hidden;       /* чтобы вуаль не вылезала за скругления */
    }}
    .banner-wrapper::after {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255, 255, 255, 0.75); /* белая вуаль, можно менять 0.75 на 0.5 или 0.85 */
        pointer-events: none;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Вставляем картинку в обёртку
st.markdown(
    f"""
    <div class="banner-wrapper">
        <img src="data:image/png;base64,{b64}" style="width: 100%; height: auto; display: block;">
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Навигация: цветная плашка (сразу под картинкой) ----------
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

# Дальше твой код (приветствие, разделы и т.д.) без изменений...

if lang == "Deutsch":
    st.markdown(
        """
        ### Willkommen! ⛸️❄️

        Ein Projekt für alle, die den Eiskunstlauf auf Deutsch und Russisch
        verstehen wollen. В этом Wörterbuch findest du **240 Einträge**
        aus 13 Kategorien — von **Sprüngen** und **Pirouetten** bis zum
        **Paarlauf** и **Richterlexikon**. Jedes Wort wird mit Übersetzung
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

# ... (остальной твой код с разделами и подвалом) ...

if lang == "Deutsch":
    st.markdown("Made with ❤️ für den Eiskunstlauf — viel Erfolg beim Lernen!")
else:
    st.markdown("Сделано с ❤️ для фигурного катания — успехов в изучении!")
