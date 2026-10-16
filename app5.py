
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

    # Определяем, где перевод: если в поле 2 есть кириллица — перевод там, иначе дальше
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

    image_name = ""
    cleaned_extra = 
    for item in reversed(extra):
        item_stripped = item.strip()
        if item_stripped.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_name = item_stripped
        else:
            cleaned_extra.insert(0, item)
    extra = cleaned_extra

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
            if not line or line.startswith(("Abkürzungen", "—")):
                continue
            entry = parse_entry(line)
            if entry:
                entries.append(entry)
    return entries

# ---------- ЗАГРУЗКА КАТЕГОРИЙ ----------
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

# ---------- ЗАГРУЗКА АББРЕВИАТУР ----------
@st.cache_data
def load_abbreviations(file_path="categories.txt"):
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

# ---------- КАРТОЧКА (ИСПРАВЛЕННАЯ ПОД СКРИНШОТ) ----------
def show_card(entry, images_dir="images", links_data=None):
    word = entry["word"]
    grammar_full = entry["grammar"]
    translation = entry["translation"]
    cases = entry["cases"]
    image_name = entry["image"]
    sections = entry["sections"]
    is_noun = entry["is_noun"]
    abbr = entry.get("abbr")

    with st.container(border=True):
        # --- 1. ЗАГОЛОВОК: Слово, артикль ---
        if abbr:
            st.markdown(f"### **{abbr}** — {word}")
        else:
            article = ""
            if cases and len(cases) > 0:
                article = cases
            
            if article:
                st.markdown(f"### **{word}, {article}**")
            else:
                st.markdown(f"### **{word}**")

        # --- 2. ПЕРЕВОД ---
        st.markdown(f"<p style='font-size:20px; color:#D4AF37;'><b>{translation}</b></p>", unsafe_allow_html=True)

        # --- 3. АККОРДЕОН "Form & Grammatik" ---
        with st.expander("📊 Form & Grammatik"):
            article_text = cases if (cases and len(cases) > 0) else ""
            
            if article_text:
                st.write(f"{article_text} {word}, {grammar_full}")
            else:
                st.write(f"{word}, {grammar_full}")

            # --- 4. ТАБЛИЦА ПАДЕЖЕЙ (СКЛЕЙКА АРТИКЛЯ И СЛОВА) ---
            if is_noun and cases:
                pad_ru = ["Nom.", "Gen.", "Dat.", "Akk."]
                rows = 
                has_plural = len(cases) >= 8
                
                for i in range(4):
                    sing_article = cases[i] if i < len(cases) else "—"
                    pl_article = cases[i+4] if (has_plural and (i+4) < len(cases)) else "—"
                    
                    # Формируем полные формы для таблицы, склеивая артикль и слово
                    sing_full = f"{sing_article} {word}" if sing_article != "—" else "—"
                    pl_full = f"{pl_article} {word}" if pl_article != "—" else "—"
                    
                    rows.append(f"| {pad_ru[i]} | {sing_full} | {pl_full} |")

                st.markdown("| Kasus | Sing. | Pl. |\n|-------|-------|-------|\n" + "\n".join(rows))

        # --- 5. КАРТИНКА ---
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
                    st.image(img_path, width=150)

        # --- 6. ССЫЛКИ И ДОП. ИНФО ---
        if links_data:
            word_links = links_data.get(word.lower(), )
            if word_links:
                st.markdown("**🔗 Ссылки:**")
                for label, url in word_links:
                    st.markdown(f"- [{label}]({url})")

        if sections:
            with st.expander("ℹ️ Zusätzliche Informationen"):
                for key in ["Beschreibung", "Herkunft", "Beispiel"]:
                    if key in sections and sections[key]:
                        st.markdown(f"**{key}:** {sections[key]}")

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
search = st.text_input("🔍 Wortsuche (Deutsch oder Russisch)", "")
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


 
