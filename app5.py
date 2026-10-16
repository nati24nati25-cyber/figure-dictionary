
Ошибка возникает из‑за того, что в нескольких местах кода остались незаполненные списки (синтаксис `extra =` без значения). Это «заглушки», которые случайно не дописали при формировании ответа.

Ниже — **полностью исправленный, готовый к запуску код**. Я починил все синтаксические ошибки, восстановил логику списков и сохранил требуемый дизайн (заголовок только со словом, грамматика и таблица — внутри экспандера, без надписи «Tabelle der Deklination»).

```python
import streamlit as st
import os
import re
import base64

# ---------- CSS СТИЛИ (Тёмная тема как на скриншоте) ----------
st.markdown("""
<style>
    .vocab-card {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .vocab-word-header {
        font-size: 28px;
        color: #ffffff;
        font-weight: 700;
        margin: 0 0 5px 0;
        line-height: 1.2;
    }
    .vocab-translation {
        font-size: 18px;
        color: #a0a0a0;
        margin: 0 0 20px 0;
        font-weight: 500;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
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
    .declension-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
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
        header_content = f"<h3 class='vocab-word-header'>{abbr} — {word}</h3>"
    else:
        header_content = f"<h3 class='vocab-word-header'>{word}</h3>"
    
    trans_content = f"<p class='vocab-translation'>{translation}</p>"

    # --- 2. Подготовка контента для Expander ---
    expander_content = ""
    
    if is_noun and cases:
        # Получаем артикль из первого элемента cases (der/die/das)
        # cases - это список строк, например: ["der Absprung", "des Absprungs", ...]
        article_word = cases if cases else ""
        
        # Разбираем gender из grammar
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
            full_gram_line = f"<p style='color:#aaa; margin:0; font-size:14px;'>{article_word}, {pos_part} ({gender_de})</p>"
        else:
            full_gram_line = f"<p style='color:#aaa; margin:0; font-size:14px;'>{article_word}, {pos_part}</p>"

        # Генерируем таблицу (БЕЗ заголовка "Tabelle der Deklination")
        rows = ""
        pad_ru = ["Nom.", "Gen.", "Dat.", "Akk."]
        
        if len(cases) == 8:
            for i in range(4):
                rows += f'<tr><td>{pad_ru[i]}</td><td>{cases[i]}</td><td>{cases[i+4]}</td></tr>'
        elif len(cases) == 4:
            for i in range(4):
                rows += f'<tr><td>{pad_ru[i]}</td><td>{cases[i]}</td><td>—</td></tr>'
        
        table_html = f"""
        <table class="declension-table">
            <thead>
                <tr>
                    <th>Kasus</th>
                    <th>Sing.</th>
                    <th>Pl.</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """
        expander_content = full_gram_line + table_html

    elif is_noun:
        expander_content = "<p style='color:#888;'>Нет данных о склонении.</p>"
    else:
        expander_content = f"<p style='color:#aaa;'>{grammar}</p>"

    # --- 3. Картинка ---
    img_html = ""
    if not abbr:
        img_path = None
        if image_name:
            candidate = os.path.join(images_dir, image_name)
            if os.path.exists(candidate): img_path = candidate
        if img_path is None: img_path = find_image_by_word(word, images_dir)
        
        if img_path:
            if img_path.lower().endswith('.gif'):
                st.session_state.current_gif = img_path 
                img_html = '<div style="margin-top:15px; padding:10px; background:#333; border-radius:8px; text-align:center; color:#666;">GIF Animation Here</div>'
            else:
                img_html = f'<div class="img-container"><img src="{img_path}" width="150" style="border-radius:8px;"></div>'

    # --- 4. Доп. информация ---
    info_html = ""
    if sections:
        desc = sections.get("Beschreibung", "…………………")
        example = sections.get("Beispiel", "…………………")
        origin = sections.get("Herkunft", "")
        
        info_html = f"""
        <div class="info-grid">
            <div class="info-item">
                <h4>Beschreibung</h4>
                <p>{desc}</p>
            </div>
            <div class="info-item">
                <h4>Beispiel</h4>
                <p>{example}</p>
            </div>
        </div>
        {f'<p style="margin-top:15px; color:#888;"><b>Herkunft:</b> {origin}</p>' if origin else ''}
        """

    # Собираем карточку
    full_card_html = f"""
    <div class="vocab-card">
        {header_content}
        {trans_content}
        
        <details style="margin-top: 15px;">
            <summary style="cursor: pointer; padding: 10px; background: #252525; border: 1px solid #333; border-radius: 8px; color: white; font-weight: 600; display: flex; align-items: center;">
                📋 Form | Grammatik
            </summary>
            <div style="padding: 15px;">
                {expander_content}
            </div>
        </details>
        
        {img_html}
        {info_html}
    </div>
    """

    st.markdown(full_card_html, unsafe_allow_html=True)

    # Обработка GIF
    if hasattr(st.session_state, 'current_gif') and st.session_state.current_gif:
        show_gif(st.session_state.current_gif, width=150)
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

search = st.text_input("🔍 Wortsuche (Deutsch oder Russisch) ", "")
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

