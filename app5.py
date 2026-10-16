

import streamlit as st
import os
import re
import base64

# ---------- КОНФИГУРАЦИЯ ----------
CATEGORIES = [
    "Technik", "Sprünge", "Pirouetten", "Schritte", "Choreosequenz",
    "Grundelementen", "Einzellauf", "Paarlauf", "Eistanz",
    "Synchroneiskunstlauf", "Richterlexikon", "Abkürzungen", "Zubehör"
]

# ---------- ПАРСЕР ----------
def parse_entry(line):
    fields = [f.strip() for f in line.split("|")]
    if len(fields) < 3:
        return None

    word = fields
    pos_raw = fields

    # Определение перевода и грамматики
    if re.search(r'[\u0400-\u04FF]', fields):
        grammar_raw = ""
        translation = fields
        rest = fields[3:]
    else:
        if len(fields) < 4:
            return None
        grammar_raw = fields
        translation = fields
        rest = fields[4:]

    grammar_display = f"{pos_raw}, {grammar_raw}" if grammar_raw else pos_raw
    is_noun = (pos_raw.lower() == "substantiv")

    # Поиск начала падежей (der, die, das...)
    cases = None
    extra =   # ИСПРАВЛЕНО: инициализация пустым списком
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
            cases = rest[start_idx:start_idx+4]
            extra = rest[start_idx+4:]
        else:
            extra = rest
    else:
        extra = rest

    # Поиск имени картинки
    image_name = ""
    cleaned_extra =   # ИСПРАВЛЕНО: инициализация пустым списком
    for item in reversed(extra):
        item_stripped = item.strip()
        if item_stripped.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_name = item_stripped
        else:
            cleaned_extra.insert(0, item)
    extra = cleaned_extra

    # Парсинг секций (Beschreibung, Beispiel...)
    sections = {}
    current_key = None
    current_text =   # ИСПРАВЛЕНО: инициализация пустым списком
    rubric_pattern = re.compile(r'^(Beschreibung|Herkunft|Beispiel):\s*(.*)\$', re.IGNORECASE)

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
            current_text = [start_text] if start_text else 
        else:
            if current_key is not None:
                current_text.append(item)
    if current_key is not None:
        sections[current_key] = "\n\n".join(current_text).strip()

    return {
        "word": word,
        "grammar": grammar_display,
        "translation": translation,
        "cases": cases,
        "image": image_name,
        "sections": sections,
        "is_noun": is_noun,
    }

@st.cache_data
def load_dictionary(file_path="dictionary_new.txt"):
    entries =   # ИСПРАВЛЕНО: инициализация пустым списком
    if not os.path.exists(file_path):
        return entries
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("Abkürzungen", "—")):
                continue
            entry = parse_entry(line)
            if entry:
                entries.append(entry)
    return entries

@st.cache_data
def load_categories(file_path="categories.txt"):
    cats = {}
    if not os.path.exists(file_path):
        return cats
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2:
                continue
            left, cat = parts, parts
            word = left.split(" - ", 1).strip()
            cats.setdefault(word.lower(), ).append(cat)
    return cats

@st.cache_data
def load_abbreviations(file_path="categories.txt"):
    abbrevs =   # ИСПРАВЛЕНО: инициализация пустым списком
    if not os.path.exists(file_path):
        return abbrevs
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2:
                continue
            cat = parts
            if cat != "Abkürzungen":
                continue
            left = parts
            chunks = [c.strip() for c in left.split(" - ")]
            if len(chunks) >= 3:
                abbr, german, translation = chunks, " - ".join(chunks[1:-1]), chunks[-1]
            elif len(chunks) == 2:
                abbr, german, translation = chunks, chunks, ""
            else:
                abbr, german, translation = left, "", ""
            abbrevs.append({
                "word": german or abbr,
                "abbr": abbr,
                "grammar": "Abkürzung",
                "translation": translation,
                "cases": None,
                "image": "",
                "sections": {},
                "is_noun": False
            })
    return abbrevs

def find_image_by_word(word, images_dir="images"):
    if not os.path.exists(images_dir):
        return None
    word_lower = word.lower()
    for ext in ['.gif', '.jpg', '.jpeg', '.png', '.webp']:
        candidate = os.path.join(images_dir, word_lower + ext)
        if os.path.exists(candidate):
            return candidate
    return None

def show_gif(gif_path, width=150):
    with open(gif_path, "rb") as f:
        contents = f.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{width}" style="display:block; margin:0 auto;">', unsafe_allow_html=True)

# ---------- ФУНКЦИЯ КАРТОЧКИ ----------
def show_card(entry, images_dir="images", links_data=None):
    word = entry["word"]
    grammar = entry["grammar"]
    translation = entry["translation"]
    cases = entry["cases"]
    image_name = entry["image"]
    sections = entry["sections"]
    is_noun = entry["is_noun"]
    abbr = entry.get("abbr")

    # --- 1. Заголовок и Перевод (Снаружи экспандера) ---
    if abbr:
        st.subheader(f"{abbr} — {word}")
    else:
        st.subheader(word)

    st.caption(translation)

    # --- 2. Expander: Form | Grammatik ---
    with st.expander("📋 Form | Grammatik"):
        if is_noun and cases:
            article_word = cases if cases else ""

            gender_part = ""
            pos_part = grammar

            if "(" in grammar:
                parts = grammar.split("(")
                pos_part = parts.strip()
                gender_part = parts.replace(")", "").strip()
            elif "," in grammar:
                parts = grammar.split(",")
                pos_part = parts.strip()
                gender_part = parts.strip()

            gender_de = {"maskulin": "Maskulinum", "feminin": "Femininum", "neutrum": "Neutrum"}.get(gender_part.lower(), gender_part)

            if gender_part:
                st.write(f"{article_word}, {pos_part} ({gender_de})")
            else:
                st.write(f"{article_word}, {pos_part}")

            # Таблица склонения через st.dataframe
            pad_ru = ["Nom.", "Gen.", "Dat.", "Akk."]
            data =   # ИСПРАВЛЕНО: инициализация пустым списком
            if len(cases) == 8:
                for i in range(4):
                    data.append([pad_ru[i], cases[i], cases[i+4]])
            elif len(cases) == 4:
                for i in range(4):
                    data.append([pad_ru[i], cases[i], "—"])

            st.dataframe(data, use_container_width=True, hide_index=True, column_config={
                0: st.column_config.ColumnConfig(header="Kasus"),
                1: st.column_config.ColumnConfig(header="Sing."),
                2: st.column_config.ColumnConfig(header="Pl.")
            })

        elif is_noun:
            st.write("Нет данных о склонении.")
        else:
            st.write(grammar)

    # --- 3. Картинка ---
    if not abbr:
        img_path = None
        if image_name:
            candidate = os.path.join(images_dir, image_name)
            if os.path.exists(candidate):
                img_path = candidate
        if img_path is None:
            img_path = find_image_by_word(word, images_dir)

        if img_path:
            if img_path.lower().endswith('.gif'):
                st.session_state.current_gif = img_path
                st.info("GIF Animation Here")
            else:
                st.image(img_path, use_column_width=True)

    # --- 4. Доп. информация: Beschreibung, Beispiel, Herkunft ---
    if sections:
        cols = st.columns(2)
        with cols:
            st.markdown("**Beschreibung**")
            desc = sections.get("Beschreibung", "…………………")
            st.write(desc)
        with cols:
            st.markdown("**Beispiel**")
            example = sections.get("Beispiel", "…………………")
            st.write(example)

        origin = sections.get("Herkunft", "")
        if origin:
            st.caption(f"Herkunft: {origin}")
    else:
        # Если секций нет вообще — всё равно показываем заглушки
        cols = st.columns(2)
        with cols:
            st.markdown("**Beschreibung**")
            st.write("…………………")
        with cols:
            st.markdown("**Beispiel**")
            st.write("…………………")

# Обработка GIF в конце страницы
if hasattr(st.session_state, 'current_gif') and st.session_state.current_gif:
    show_gif(st.session_state.current_gif, width=300)
    del st.session_state.current_gif

# ---------- ИНТЕРФЕЙС ----------
st.set_page_config(page_title="Eiskunstlauf-Wörterbuch", layout="wide")
st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")

try:
    entries = load_dictionary("dictionary_new.txt")
    entries += load_abbreviations("categories.txt")
    st.success(f"✅ Hochgeladene Einträge: {len(entries)}")
except FileNotFoundError:
    st.error("❌ Файл dictionary_new.txt не найден!")
    entries = 
except Exception as e:
    st.error(f"Ошибка: {e}")
    entries = 

categories_map = load_categories("categories.txt")

search = st.text_input("🔍 Wortsuche (Deutsch oder Russisch)", "")
if search:
    filtered = [e for e in entries if search.lower() in e["word"].lower() or search.lower() in e["translation"].lower()]
else:
    filtered = entries

st.write(f"Einträge: {len(filtered)}")

tab_names = ["Alle"] + CATEGORIES
tabs = st.tabs(tab_names)

for tab, cat_name in zip(tabs, tab_names):
    with tab:
        if cat_name == "Alle":
            cat_entries = filtered
        else:
            cat_entries = [
                e for e in filtered
                if cat_name in categories_map.get(e.get("abbr", e["word"]).lower(), )
            ]

        if not cat_entries:
            st.info(f"В категории «{cat_name}» пока нет записей.")
        else:
            cols = st.columns(3)
            for idx, entry in enumerate(cat_entries):
                with cols[idx % 3]:
                    show_card(entry)
```




