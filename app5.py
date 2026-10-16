
import streamlit as st
import os
import re
import base64

# ---------- CSS СТИЛИ (Тёмная тема как на скриншоте) ----------
st.markdown("""
<style>
    /* Основной контейнер карточки */
    .vocab-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Заголовок слова */
    .vocab-word-header {
        font-size: 28px;
        color: #ffffff;
        font-weight: 700;
        margin: 0 0 10px 0;
        line-height: 1.2;
    }

    /* Перевод */
    .vocab-translation {
        font-size: 18px;
        color: #a0a0a0;
        margin: 0 0 20px 0;
        font-weight: 500;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }

    /* Стили экспандера (аккордеона) */
    .stExpander {
        background-color: #252525 !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
        box-shadow: none !important;
    }
    .stExpander .st-ec {
        color: #fff !important;
        font-weight: 600 !important;
        font-size: 16px;
    }
    .stExpander .st-ec:hover {
        color: #ffd700 !important;
    }
    .stExpander .st-expanderContent {
        padding: 15px !important;
    }

    /* Таблица склонения */
    .declension-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background: #2a2a2a;
    }
    .declension-table th, .declension-table td {
        border: 1px solid #444;
        padding: 12px;
        text-align: left;
        font-size: 14px;
    }
    .declension-table th {
        background-color: #333;
        color: #aaa;
        font-weight: 600;
    }
    .declension-table tr:nth-child(even) {
        background-color: #2d2d2d;
    }
    .declension-table tr:hover {
        background-color: #3a3a3a;
    }

    /* Блок дополнительной информации */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #333;
    }
    .info-item h4 {
        color: #ffd700;
        font-size: 13px;
        text-transform: uppercase;
        margin: 0 0 5px 0;
        letter-spacing: 0.5px;
    }
    .info-item p {
        color: #ccc;
        font-size: 14px;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Картинка */
    .img-container {
        margin-top: 20px;
        text-align: center;
    }
    .img-container img, .img-container video {
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

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
    extra = 
    start_idx = -1
    for i, val in enumerate(rest):
        if val and re.match(r'^(der|die|das|des|dem|den)\b', val, re.IGNORECASE):
            start_idx = i
            break

    if start_idx != -1:
        # Пытаемся взять 8 форм (Sing + Pl) или 4 (только Sing)
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
    cleaned_extra = 
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
    current_text = 
    rubric_pattern = re.compile(r'^(Beschreibung|Herkunft|Beispiel):\s*(.*)\$', re.IGNORECASE)

    for item in extra:
        item = item.strip()
        if not item: continue
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
    entries = 
    if not os.path.exists(file_path):
        return entries
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("Abkürzungen", "—")): continue
            entry = parse_entry(line)
            if entry: entries.append(entry)
    return entries

@st.cache_data
def load_categories(file_path="categories.txt"):
    cats = {}
    if not os.path.exists(file_path): return cats
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2: continue
            left, cat = parts, parts
            word = left.split(" - ", 1).strip()
            cats.setdefault(word.lower(), ).append(cat)
    return cats

@st.cache_data
def load_abbreviations(file_path="categories.txt"):
    abbrevs = 
    if not os.path.exists(file_path): return abbrevs
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2: continue
            cat = parts
            if cat != "Abkürzungen": continue
            left = parts
            chunks = [c.strip() for c in left.split(" - ")]
            if len(chunks) >= 3:
                abbr, german, translation = chunks, " - ".join(chunks[1:-1]), chunks[-1]
            elif len(chunks) == 2:
                abbr, german, translation = chunks, chunks, ""
            else:
                abbr, german, translation = left, "", ""
            abbrevs.append({
                "word": german or abbr, "abbr": abbr, "grammar": "Abkürzung",
                "translation": translation, "cases": None, "image": "",
                "sections": {}, "is_noun": False
            })
    return abbrevs

def find_image_by_word(word, images_dir="images"):
    if not os.path.exists(images_dir): return None
    word_lower = word.lower()
    for ext in ['.gif', '.jpg', '.jpeg', '.png', '.webp']:
        candidate = os.path.join(images_dir, word_lower + ext)
        if os.path.exists(candidate): return candidate
    return None

def show_gif(gif_path, width=150):
    with open(gif_path, "rb") as f:
        contents = f.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{width}" class="img-container">', unsafe_allow_html=True)

# ---------- ФУНКЦИЯ КАРТОЧКИ (НОВЫЙ ЛОГИКА) ----------
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
        header_content = f"<h3 class='vocab-word-header'>{abbr} — {word}</h3>"
    else:
        header_content = f"<h

    
