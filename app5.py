
import streamlit as st
import os
import re
import base64
import uuid

st.markdown("""
<style>
    .audio-btn {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 24px;
        padding: 0;
        line-height: 1;
        color: #333;
    }
    .audio-btn:hover {
        opacity: 0.8;
        transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

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

def parse_entry(line):
    fields = [f.strip() for f in line.split("|")]
    if len(fields) < 3:
        return None

    word = fields[0]
    pos_raw = fields[1]

    if re.search(r'[\u0400-\u04FF]', fields[2]):
        grammar_raw = ""
        translation = fields[2]
        rest = fields[3:]
    else:
        if len(fields) < 4:
            return None
        grammar_raw = fields[2]
        translation = fields[3]
        rest = fields[4:]

    grammar_display = f"{pos_raw}, {grammar_raw}" if grammar_raw else pos_raw
    is_noun = (pos_raw.lower() == "substantiv")

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
            cases = rest[start_idx:start_idx+4]
            extra = rest[start_idx+4:]
        else:
            extra = rest
    else:
        extra = rest

    image_name = ""
    cleaned_extra = []
    for item in reversed(extra):
        item_stripped = item.strip()
        if item_stripped.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            image_name = item_stripped
        else:
            cleaned_extra.insert(0, item)
    extra = cleaned_extra

    sections = {}
    current_key = None
    current_text = []
    rubric_pattern = re.compile(r'^(Definition|Herkunft|Beispiel des Gebrauchs):\s*(.*)$', re.IGNORECASE)

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
            left, cat = parts[0], parts[1]
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

def find_audio_by_word(word, audio_dir="audio"):
    """Ищет аудиофайл в папке audio по имени слова (регистронезависимо)."""
    if not os.path.exists(audio_dir):
        return None
    word_lower = word.lower()
    extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
    for ext in extensions:
        candidate = os.path.join(audio_dir, word_lower + ext)
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

def show_audio_icon(audio_path):
    player_id = f"p_{uuid.uuid4().hex[:8]}"

    html = f"""
    <audio id="{player_id}" src="{audio_path}"></audio>
    <button class="audio-btn" 
            onclick="const p = document.getElementById('{player_id}'); 
                     if (!p.paused) {{ p.pause(); p.currentTime = 0; }} 
                     else {{ p.muted = false; p.play(); }}" 
            title="Прослушать">🔊</button>
    """
    st.markdown(html, unsafe_allow_html=True)


def show_card(entry, images_dir="images", audio_dir="audio", links_data=None):
    word = entry["word"]
    grammar = entry["grammar"]
    translation = entry["translation"]
    cases = entry["cases"]
    image_name = entry["image"]
    sections = entry["sections"]
    is_noun = entry["is_noun"]
    abbr = entry.get("abbr")

    with st.container(border=True):
        if abbr:
            st.markdown(f"### **{abbr}** — {word}")
        else:
            if is_noun and cases:
                article = cases[0].split()[0]  # берём "der"/"die"/"das" из Nom. Sing.
                st.markdown(f"### **{word}, {article}**")
            else:
                # Для глаголов, наречий и т.п. — просто слово
                st.markdown(f"### **{word}**")

        st.markdown(f"<p style='font-size:20px;'><b>{translation}</b></p>", unsafe_allow_html=True)

        if not abbr:
            audio_path = find_audio_by_word(word, audio_dir)
            if audio_path:
                st.markdown("**Aussprache:**")
                show_audio_icon(audio_path)

                # --- АККОРДЕОН (ОТКРЫВАЕТСЯ ВСЕГДА) ---
        with st.expander("📊 Grammatik / Form"):
            if is_noun and cases:
                # ЛОГИКА ДЛЯ СУЩЕСТВИТЕЛЬНЫХ (таблица)
                article_inner = cases[0].split()[0]
                gender_inner = grammar.split(",")[1].strip()
                st.markdown(f"**{article_inner} {word}, Substantiv ({gender_inner.capitalize()})**")

                pad_ru = ["Nom.", "Gen.", "Dat.", "Akk."]
                if len(cases) == 8:
                    rows = [f"| {pad_ru[i]} | {cases[i]} | {cases[i+4]} |" for i in range(4)]
                    st.markdown("| Kasus | Sing. | Pl. |\n|-------|-------|-------|\n" + "\n".join(rows))
                elif len(cases) == 4:
                    rows = [f"| {pad_ru[i]} | — | {cases[i]} |" for i in range(4)]
                    st.markdown("| Kasus | Sing. | Pl. |\n|-------|-------|-------|\n" + "\n".join(rows))


            else:
                # ЛОГИКА ДЛЯ ГЛАГОЛОВ — с добавлением vi./vt. в одну строку
                conjugation_text = ""
                base_type_raw = grammar

                # Вытаскиваем часть до скобок и сами формы
                if "(" in grammar and ")" in grammar:
                    parts = grammar.split("(")
                    base_type_raw = parts[0].strip()
                    conjugation_text = parts[1].split(")")[0]

                # Формируем основную строку: слово - тип (формы)
                if conjugation_text:
                    line_core = f"{word} - {base_type_raw} ({conjugation_text})"
                else:
                    # Если скобок нет, показываем как есть
                    line_core = f"{word} - {grammar}"

                # Ищем пометку vi. или vt. в исходном grammar
                marker = ""
                if "vi." in grammar:
                    marker = "vi."
                elif "vt." in grammar:
                    marker = "vt."

                # Если нашли маркер — добавляем его через запятую
                if marker:
                    final_line = f"**{line_core}, *{marker}***"
                else:
                    final_line = f"**{line_core}**"
                st.markdown(final_line)

                
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
        
        
        if links_data:
            word_links = links_data.get(word.lower(), [])
            if word_links:
                st.markdown("**🔗 Ссылки:**")
                for label, url in word_links:
                    st.markdown(f"- [{label}]({url})")

        if sections:
            with st.expander("ℹ️ Zusätzliche Informationen (Beispiele etc.)"):
                for key in ["Definition", "Herkunft", "Beispiel des Gebrauchs"]:
                    if key in sections and sections[key]:
                        st.markdown(f"**{key}:** {sections[key]}")

st.set_page_config(page_title="Eiskunstlauf-Wörterbuch", layout="wide")
st.title("📖 Deutsch-russisches Wörterbuch der Eiskunstlauf-Terminologie")

try:
    entries = load_dictionary("dictionary_new.txt")
    entries += load_abbreviations("categories.txt")
    st.success(f"✅ Hochgeladene Einträge: {len(entries)}")
except FileNotFoundError:
    st.error("❌ Файл dictionary_new.txt не найден!")
    entries = []
except Exception as e:
    st.error(f"Ошибка: {e}")
    entries = []

categories_map = load_categories("categories.txt")

search = st.text_input("🔍 Wortsuche (Deutsch oder Russisch) ", "")
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
                    show_card(entry, images_dir="images", audio_dir="audio")
