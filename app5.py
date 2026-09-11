import streamlit as st
import os
import re
import base64

# ---------- ПАРСЕР (ГИБКИЙ, С РУБРИКАМИ) ----------
def parse_entry(line):
    fields = [f.strip() for f in line.split("|")]
    if len(fields) < 3:
        return None

    word = fields[0]
    pos_raw = fields[1]

    # Определяем, где перевод: если в field[2] есть кириллица — это перевод
    if re.search(r'[\u0400-\u04FF]', fields[2]):
        # Нет грамматики: слово | часть речи | перевод
        grammar_raw = ""
        translation = fields[2]
        rest = fields[3:]
    else:
        # Есть грамматика: слово | часть речи | грамматика | перевод | ...
        if len(fields) < 4:
            return None
        grammar_raw = fields[2]
        translation = fields[3]
        rest = fields[4:]

    # Формируем отображение грамматики
    if grammar_raw:
        grammar_display = f"{pos_raw}, {grammar_raw}"
    else:
        grammar_display = pos_raw
    is_noun = (pos_raw.lower() == "substantiv")

    # Поиск падежных форм
    cases = None
    extra = []
    start_idx = -1
    for i, val in enumerate(rest):
        if val and re.match(r'^(der|die|das|des|dem|den)\b', val, re.IGNORECASE):
            start_idx = i
            break

    if start_idx != -1:
        if start_idx + 8 <= len(rest):
            cases = rest[start_idx:start_idx+8]
            extra = rest[start_idx+8:]
        elif start_idx + 4 <= len(rest):
            cases = rest[start_idx:start_idx+4]  # только мн.ч.
            extra = rest[start_idx+4:]
        else:
            extra = rest
    else:
        extra = rest

    # Отделяем картинку (удаляем из extra элементы, похожие на файл)
    image_name = ""
    cleaned_extra = []
    for item in reversed(extra):
        item_stripped = item.strip()
        if item_stripped.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_name = item_stripped
        else:
            cleaned_extra.insert(0, item)
    extra = cleaned_extra

    # Парсим рубрики Beschreibung / Herkunft / Beispiel
    sections = {}
    current_key = None
    current_text = []
    rubric_pattern = re.compile(r'^(Beschreibung|Herkunft|Beispiel):\s*(.*)$', re.IGNORECASE)

    for item in extra:
        item = item.strip()
        if not item:
            continue
        match = rubric_pattern.match(item)
        if match:
            if current_key is not None:
                sections[current_key] = " ".join(current_text).strip()
            current_key = match.group(1)
            start_text = match.group(2).strip()
            current_text = [start_text] if start_text else []
        else:
            if current_key is not None:
                current_text.append(item)
    if current_key is not None:
        sections[current_key] = " ".join(current_text).strip()

    return {
        "word": word,
        "grammar": grammar_display,
        "translation": translation,
        "cases": cases,
        "image": image_name,
        "sections": sections,
        "is_noun": is_noun
    }

@st.cache_data
def load_dictionary(file_path="dictionary_new.txt"):
    entries = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("Abkürzungen", "—")):
                continue
            entry = parse_entry(line)
            if entry:
                entries.append(entry)
    return entries

# ---------- ПОИСК КАРТИНКИ / GIF ПО ИМЕНИ СЛОВА ----------
def find_image_by_word(word, images_dir="images"):
    """Ищет файл в папке images по имени слова (регистронезависимо). GIF в приоритете."""
    if not os.path.exists(images_dir):
        return None
    word_lower = word.lower()
    extensions = ['.gif', '.jpg', '.jpeg', '.png', '.webp']
    for ext in extensions:
        candidate = os.path.join(images_dir, word_lower + ext)
        if os.path.exists(candidate):
            return candidate
    return None

# ---------- ПОКАЗ GIF БЕЗ ПОТЕРИ АНИМАЦИИ ----------
def show_gif(gif_path, width=150):
    """Отображает анимированный GIF через Base64, чтобы сохранить


анимацию."""
    with open(gif_path, "rb") as f:
        contents = f.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" width="{width}">',
        unsafe_allow_html=True,
    )

# ---------- КАРТОЧКА ----------
def show_card(entry, images_dir="images"):
    word = entry["word"]
    grammar = entry["grammar"]
    translation = entry["translation"]
    cases = entry["cases"]
    image_name = entry["image"]
    sections = entry["sections"]
    is_noun = entry["is_noun"]

    with st.container(border=True):
        st.markdown(f"### **{word}** — {grammar}")
        st.markdown(f"<p style='font-size:20px;'><b>{translation}</b></p>", unsafe_allow_html=True)

        # Таблица склонения (только для существительных)
        if is_noun and cases:
            with st.expander("📊 Таблица словоизменения"):
                pad_ru = ["и.п.", "р.п.", "д.п.", "в.п."]
                if len(cases) == 8:
                    rows = [f"| {pad_ru[i]} | {cases[i]} | {cases[i+4]} |" for i in range(4)]
                    st.markdown("| падеж | ед.ч. | мн.ч. |\n|-------|-------|-------|\n" + "\n".join(rows))
                elif len(cases) == 4:
                    rows = [f"| {pad_ru[i]} | — | {cases[i]} |" for i in range(4)]
                    st.markdown("| падеж | ед.ч. | мн.ч. |\n|-------|-------|-------|\n" + "\n".join(rows))

        # Картинка или GIF
        img_path = None
        if image_name:
            candidate = os.path.join(images_dir, image_name)
            if os.path.exists(candidate):
                img_path = candidate
        if img_path is None:
            img_path = find_image_by_word(word, images_dir)

        if img_path:
            if img_path.lower().endswith('.gif'):
                show_gif(img_path, width=150)   # анимированный GIF
            else:
                st.image(img_path, width=150)   # обычная картинка

        # Дополнительная информация по рубрикам
        if sections:
            with st.expander("ℹ️ Дополнительная информация"):
                for key in ["Beschreibung", "Herkunft", "Beispiel"]:
                    if key in sections and sections[key]:
                        st.markdown(f"**{key}:** {sections[key]}")

# ---------- ИНТЕРФЕЙС ----------
st.set_page_config(page_title="Словарь фигурного катания", layout="wide")
st.title("📖 Немецко-русский словарь терминов фигурного катания")

try:
    entries = load_dictionary("dictionary_new.txt")
    st.success(f"✅ Загружено записей: {len(entries)}")
except FileNotFoundError:
    st.error("❌ Файл dictionary_new.txt не найден!")
    entries = []
except Exception as e:
    st.error(f"Ошибка: {e}")
    entries = []

search = st.text_input("🔍 Поиск по немецкому или русскому слову", "")
if search:
    filtered = [e for e in entries if search.lower() in e["word"].lower() or search.lower() in e["translation"].lower()]
else:
    filtered = entries

st.write(f"Показано записей: {len(filtered)}")

if filtered:
    cols = st.columns(3)
    for idx, entry in enumerate(filtered):
        with cols[idx % 3]:
            show_card(entry)
elif entries and not filtered:
    st.info("Ничего не найдено. Попробуйте другой запрос.")
elif not entries:
    st.info("Словарь пуст. Проверьте файл dictionary_new.txt.")
    st.info("Ничего не найдено. Попробуйте другой запрос.")
elif not entries:
    st.info("Словарь пуст. Проверьте файл dictionary_new.txt.")
