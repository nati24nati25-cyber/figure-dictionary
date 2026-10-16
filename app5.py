
import streamlit as st
import os
import re
import base64

CATEGORIES = [
    "Technik", "Sprünge", "Pirouetten", "Schritte", "Choreosequenz",
    "Grundelementen", "Einzellauf", "Paarlauf", "Eistanz",
    "Synchroneiskunstlauf", "Richterlexikon", "Abkürzungen", "Zubehör"
]

def parse_entry(line):
    fields = [f.strip() for f in line.split("|")]
    # Нужно минимум 4 поля: слово, часть речи, грамматика, перевод
    if len(fields) < 4:
        return None

    word = fields[0]
    pos_raw = fields[1]
    grammar_raw = fields[2]  # это как раз maskulin/feminin/neutrum
    translation = fields[3]   # вот тут будет «прыжок аксель», а не maskulin

    # Всё, что после 4-го поля — это падежи и прочее
    rest = fields[4:]

    # Собираем падежи из rest (они там идут подряд через пробелы)
    # Если в rest несколько элементов, значит, кто-то поставил | между падежами — склеим обратно
    cases_raw = " ".join(rest).split()
    
    # Ищем, где начинаются падежи (der/die/das…)
    start_idx = -1
    for i, val in enumerate(cases_raw):
        if re.match(r'^(der|die|das|des|dem|den)\b', val, re.IGNORECASE):
            start_idx = i
            break

    cases = None
    extra = []
    if start_idx != -1:
        # Берём 8 форм если есть (ед. + мн.), иначе 4 (только ед.)
        if start_idx + 8 <= len(cases_raw):
            cases = cases_raw[start_idx:start_idx+8]
            extra = cases_raw[start_idx+8:]
        elif start_idx + 4 <= len(cases_raw):
            cases = cases_raw[start_idx:start_idx+4]
            extra = cases_raw[start_idx+4:]
        else:
            extra = cases_raw
    else:
        extra = cases_raw

    # Вытаскиваем имя картинки из extra (в конце)
    image_name = ""
    cleaned_extra = []
    for item in reversed(extra):
        item_stripped = item.strip()
        if item_stripped.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_name = item_stripped
        else:
            cleaned_extra.insert(0, item)
    extra = cleaned_extra

    # Секции (Beschreibung, Herkunft, Beispiel)
    sections = {}
    current_key = None
    current_text = []
    rubric_pattern = re.compile(r'^(Beschreibung|Herkunft|Beispiel):\s*(.*)', re.IGNORECASE)

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
        sections[current_key] = "\n\n".join(current_text).strip()

    grammar_display = f"{pos_raw}, {grammar_raw}" if grammar_raw else pos_raw
    is_noun = (pos_raw.lower() == "substantiv")

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
    if not os.path.exists(file_path):
        st.warning(f"Файл {file_path} не найден!")
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
            left = parts[0]
            cat = parts[1]
            word = left.split(" - ", 1)[0].strip()
            cats.setdefault(word.lower(), []).append(cat)
    return cats

@st.cache_data
def load_abbreviations(file_path="categories.txt"):
    abbrevs = []
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
            cat = parts[1]
            if cat != "Abkürzungen":
                continue
            left = parts[0]
            chunks = [c.strip() for c in left.split(" - ")]
            if len(chunks) >= 3:
                abbr = chunks[0]
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
        # Заголовок
        if abbr:
            st.markdown(f"### **{abbr}** — {word}")
        else:
            if cases and len(cases) > 0:
                nom_form = cases[0]
                parts = nom_form.split(" ", 1)
                if len(parts) == 2:
                    article, clean_word = parts
                    st.markdown(f"### **{clean_word}, {article}**")
                else:
                    st.markdown(f"### **{nom_form}**")
            else:
                st.markdown(f"### **{word}**")

        # Перевод
        if translation:
            st.markdown(f"<p style='font-size:20px;'><b>{translation}</b></p>", unsafe_allow_html=True)
        else:
            st.caption("⚠️ Перевод не найден — проверьте строку в словаре.")

        # Грамматика
        if is_noun and cases:
            with st.expander("📊 Grammatik / Form"):
                nom_form = cases[0] if len(cases) >= 1 else word
                g_lower = grammar.lower()
                gender_text = ""
                if "maskulin" in g_lower:
                    gender_text = "(Maskulin)"
                elif "feminin" in g_lower:
                    gender_text = "(Feminin)"
                elif "neutrum" in g_lower:
                    gender_text = "(Neutrum)"

                pos_text = grammar.split(",")[0].strip()
                st.write(f"{nom_form}, {pos_text} {gender_text}")

                pad_ru = ["Nom.", "Gen.", "Dat.", "Akk."]
                rows = []
                has_plural = len(cases) >= 8
                for i in range(4):
                    sing_form = cases[i] if i < len(cases) else "—"
                    pl_form = cases[i+4] if (has_plural and (i+4) < len(cases)) else "—"
                    rows.append(f"| {pad_ru[i]} | {sing_form} | {pl_form} |")

                md_table = "| Kasus | Sing. | Pl. |\n|-------|-------|-------|\n" + "\n".join(rows)
                st.markdown(md_table)

        # Картинка
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

        # Ссылки
        if links_data:
            word_links = links_data.get(word.lower(), [])
            if word_links:
                st.markdown("**🔗 Ссылки:**")
                for label, url in word_links:
                    st.markdown(f"- [{label}]({url})")

        # Доп. информация
        if sections:
            with st.expander("ℹ️ Zusätzliche Informationen"):
                for key in ["Beschreibung", "Herkunft", "Beispiel"]:
                    if key in sections and sections[key]:
                        st.markdown(f"**{key}:** {sections[key]}")

# ---------- ИНТЕРФЕЙС ----------
st.set_page_config(page_title="Eiskunstlauf-Wörterbuch", layout="wide")
st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")

try:
    entries_dict = load_dictionary("dictionary_new.txt")
    entries_abbr = load_abbreviations("categories.txt")
    entries = entries_dict + entries_abbr
    st.success(f"✅ Hochgeladene Einträge: {len(entries)}")
except Exception as e:
    st.error(f"Ошибка загрузки данных: {e}")
    entries = []

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
                if cat_name in categories_map.get(e.get("abbr", e["word"]).lower(), [])
            ]

        if not cat_entries:
            st.info(f"В категории «{cat_name}» пока нет записей.")
        else:
            st.write(f"Gefunden in der Kategorie «{cat_name}»: {len(cat_entries)}")
            cols = st.columns(3)
            for idx, entry in enumerate(cat_entries):
                with cols[idx % 3]:
                    show_card(entry)

 
