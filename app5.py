
import streamlit as st
import os
import re
import base64

# ---------- СПИСОК КАТЕГОРИЙ (порядок вкладок) ----------
CATEGORIES = [
    "Technik",
    "Sprünge",
    "Pirouetten",
    "Schritte",
    "Choreosequenz",
    "Grundelementen",
    "Einzellauf",
    "Paarlauf",
    "Eistanz",
    "Synchroneiskunstlauf",
    "Richterlexikon",
    "Abkürzungen",
    "Zubehör",
]

# ---------- ПАРСЕР СЛОВАРЯ ----------
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

    # Поиск начала падежей
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

    # Парсинг секций (Beschreibung, Beispiel и т.д.)
    sections = {}
    current_key = None
    current_text = 
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
        "is_noun": is_noun
    }

@st.cache_data
def load_dictionary(file_path="dictionary_new.txt"):
    entries = 
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(("Abkürzungen", "—")):
                continue
            entry = parse_entry(line)
            if entry:
                entries.append(entry)
    return entries

# ---------- ЗАГРУЗКА КАТЕГОРИЙ ----------
@st.cache_data
def load_categories(file_path="categories.txt"):
    """Возвращает словарь: слово (в нижнем регистре) -> список категорий."""
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

# ---------- ЗАГРУЗКА АББРЕВИАТУР ----------
@st.cache_data
def load_abbreviations(file_path="categories.txt"):
    """Формат: 'сокращение - немецкое слово - русский перевод| Abkürzungen'."""
    abbrevs = 
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
                abbr = chunks
                german = " - ".join(chunks[1:-1])
                translation = chunks[-1]
            elif len(chunks) == 2:
                abbr, german = chunks
                translation = ""
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
                "is_noun": False,
            })
    return abbrevs

# ---------- ПОИСК КАРТИНКИ / GIF ----------
def find_image_by_word(word, images_dir="images"):
    if not os.path.exists(images_dir):
        return None
    word_lower = word.lower()
    extensions = ['.gif', '.jpg', '.jpeg', '.png', '.webp']
    for ext in extensions:
        candidate = os.path.join(images_dir, word_lower + ext)
        if os.path.exists(candidate):
            return candidate
    return None

def show_gif(gif_path, width=150):
    with open(gif_path, "rb") as f:
        contents = f.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" width="{width}">',
        unsafe_allow_html=True,
    )

# ---------- КАРТОЧКА (ОБНОВЛЕННАЯ ЛОГИКА) ----------
def show_card(entry, images_dir="images", links_data=None):
    word = entry["word"]
    grammar = entry["grammar"]
    translation = entry["translation"]
    cases = entry["cases"]
    image_name = entry["image"]
    sections = entry["sections"]
    is_noun = entry["is_noun"]
    abbr = entry.get("abbr")

    with st.container(border=True):
        # --- 1. Заголовок карточки ---
        if abbr:
            # Для аббревиатур: "A. — Axel"
            st.markdown(f"### **{abbr}** — {word}")
        else:
            # Для обычных слов: "Eiskunstlauf, Substantiv (Maskulinum)"
            # Разбираем грамматику для красивого вывода рода
            pos_part = ""
            gender_part = ""
            
            # Пытаемся выделить род из строки grammar (например "Substantiv (Maskulinum)" или "Substantiv, maskulin")
            if "(" in grammar:
                parts = grammar.split("(")
                pos_part = parts.strip()
                gender_part = parts.replace(")", "").strip()
            elif "," in grammar:
                parts = grammar.split(",")
                pos_part = parts.strip()
                gender_part = parts.strip()
            else:
                pos_part = grammar

            gender_de = {"maskulin": "Maskulinum", "feminin": "Femininum", "neutrum": "Neutrum"}.get(gender_part.lower(), gender_part)
            
            if gender_part:
                st.markdown(f"### **{word}, {pos_part} ({gender_de})**")
            else:
                st.markdown(f"### **{word}, {pos_part}**")

        # --- 2. Перевод ---
        st.markdown(f"<p style='font-size:20px; color: #333; margin-top: 5px; margin-bottom: 15px;'>{translation}</p>", unsafe_allow_html=True)

        # --- 3. Expander "Form | Grammatik" ---
        if is_noun and cases:
            with st.expander("📋 Form | Grammatik", expanded=False):
                st.markdown(f"**{word}, {grammar}**") # Дублируем заголовок внутри экспандера для контекста
                st.markdown("**Tabelle der Deklination**")
                
                pad_ru = ["Nom.", "Gen.", "Dat.", "Akk."]
                
                # Логика построения таблицы строго по твоему требованию и картинке
                if len(cases) == 8:
                    # Есть и Singular и Plural
                    # cases[0-3] = Sing, cases[4-7] = Pl
                    rows = [f"| {pad_ru[i]} | {cases[i]} | {cases[i+4]} |" for i in range(4)]
                    table_md = "| Kasus | SPRING | Pl. |\n|-------|--------|------|\n" + "\n".join(rows)
                    st.markdown(table_md)
                elif len(cases) == 4:
                    # Есть только Singular (или данные неполные)
                    # cases[0-3] = Sing
                    rows = [f"| {pad_ru[i]} | {cases[i]} | — |" for i in range(4)]
                    table_md = "| Kasus | SPRING | Pl. |\n|-------|--------|------|\n" + "\n".join(rows)
                    st.markdown(table_md)
                else:
                    st.info("📜 Данные о склонении неполные.")
        else:
            if is_noun:
                st.info("📜 Для этого слова нет таблицы склонения.")

        # --- 4. Картинка ---
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
                    show_gif(img_path, width=150)
                else:
                    st.image(img_path, width=150, caption="Иллюстрация элемента")

        # --- 5. Ссылки ---
        if links_data:
            word_links = links_data.get(word.lower(), )
            if word_links:
                st.markdown("**🔗 Ссылки:**")
                for label, url in word_links:
                    st.markdown(f"- [{label}]({url})")

        # --- 6. Zusätzliche Informationen ---
        if sections:
            with st.expander("ℹ️ Zusätzliche Informationen", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    if "Beschreibung" in sections and sections["Beschreibung"]:
                        st.markdown(f"**Beschreibung:** {sections['Beschreibung']}")
                    else:
                        st.markdown("**Beschreibung:** ……………………")
                with col2:
                    if "Beispiel" in sections and sections["Beispiel"]:
                        st.markdown(f"**Beispiel:** {sections['Beispiel']}")
                    else:
                        st.markdown("**Beispiel:** ……………………")
                
                if "Herkunft" in sections and sections["Herkunft"]:
                    st.markdown(f"**Herkunft:** {sections['Herkunft']}")

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

# Поиск
search = st.text_input("🔍 Wortsuche (Deutsch oder Russisch) ", "")
if search:
    filtered = [e for e in entries if search.lower() in e["word"].lower() or search.lower() in e["translation"].lower()]
else:
    filtered = entries

st.write(f"Einträge: {len(filtered)}")

# ---------- ВКЛАДКИ ПО КАТЕГОРИЯМ ----------
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
            st.write(f"Gefunden in der Kategorie «{cat_name}»: {len(cat_entries)}")
            cols = st.columns(3)
            for idx, entry in enumerate(cat_entries):
                with cols[idx % 3]:
                    show_card(entry)

          
