
import streamlit as st
import streamlit.components.v1 as components
import os
import re
import base64
import uuid

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
    """Показывает кнопку произношения без стандартной панели плеера."""
    with open(audio_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("ascii")

    mime_types = {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".flac": "audio/flac",
    }
    mime_type = mime_types.get(os.path.splitext(audio_path)[1].lower(), "audio/mpeg")
    player_id = f"p_{uuid.uuid4().hex}"

    components.html(
        f"""
        <!doctype html>
        <html lang="de">
        <head>
        <meta charset="utf-8">
        <style>
            html, body {{ margin: 0; padding: 0; background: transparent; }}
            .audio-row {{
                display: flex; align-items: center; gap: 10px; min-height: 48px;
                font: 600 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                color: #31333f;
            }}
            .audio-btn {{
                display: inline-flex; align-items: center; justify-content: center;
                width: 44px; height: 44px; padding: 0; flex-shrink: 0;
                border: 1px solid #dce0e5; border-radius: 50%;
                color: #31333f; background: #f4f5f7; cursor: pointer;
                transition: background 0.15s, border-color 0.15s;
            }}
            .audio-btn:hover {{ background: #e8ebef; }}
            .audio-btn:focus-visible {{ outline: 2px solid #2563eb; outline-offset: 2px; }}
            .audio-btn[aria-pressed="true"] {{
                color: #1d4ed8; background: #e8efff; border-color: #93b4ff;
            }}
            .audio-error {{ font-size: 12px; font-weight: 400; color: #b42318; }}
        </style>
        </head>
        <body>
        <div class="audio-row">
            <span>Aussprache:</span>
            <button class="audio-btn" type="button" id="{player_id}_button"
                    title="Aussprache anhören" aria-label="Aussprache anhören"
                    aria-pressed="false">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
                     stroke-linejoin="round" aria-hidden="true">
                    <path d="M11 5 6 9H3v6h3l5 4V5Z"></path>
                    <path d="M15 8a6 6 0 0 1 0 8M18 5a10 10 0 0 1 0 14"></path>
                </svg>
            </button>
            <span id="{player_id}_error" class="audio-error" role="status"></span>
        </div>
        <audio id="{player_id}" preload="none" hidden
               src="data:{mime_type};base64,{audio_data}"></audio>
        <script>
            const audio = document.getElementById("{player_id}");
            const button = document.getElementById("{player_id}_button");
            const error = document.getElementById("{player_id}_error");
            function updateButton(playing) {{
                button.setAttribute("aria-pressed", String(playing));
                const label = playing ? "Wiedergabe stoppen" : "Aussprache anhören";
                button.setAttribute("aria-label", label);
                button.title = label;
            }}
            button.addEventListener("click", async () => {{
                error.textContent = "";
                if (!audio.paused && !audio.ended) {{
                    audio.pause();
                    audio.currentTime = 0;
                    return;
                }}
                try {{
                    audio.currentTime = 0;
                    await audio.play();
                }} catch (err) {{
                    updateButton(false);
                    error.textContent = "Audio nicht verfügbar.";
                }}
            }});
            audio.addEventListener("play", () => updateButton(true));
            audio.addEventListener("pause", () => updateButton(false));
            audio.addEventListener("ended", () => updateButton(false));
            audio.addEventListener("error", () => {{
                updateButton(false);
                error.textContent = "Audio nicht verfügbar.";
            }});
        </script>
        </body>
        </html>
        """,
        height=52,
        scrolling=False,
    )


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
                show_audio_icon(audio_path)

                # --- АККОРДЕОН (ОТКРЫВАЕТСЯ ВСЕГДА) ---
        with st.expander("📊 Grammatik / Form"):
            if is_noun and cases:
                # ЛОГИКА ДЛЯ СУЩЕСТВИТЕЛЬНЫХ (таблица)
                article_inner = cases[0].split()[0]
                gender_inner = grammar.split(",")[1].strip()
                st.markdown(f"**{article_inner} {word}**: Substantiv ({gender_inner.capitalize()})")

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
                    marker = "vi"
                elif "vt." in grammar:
                    marker = "vt"

                clean_type = grammar
                if marker == "vi":
                    clean_type = clean_type.replace("vi.", "").strip().strip(",")
                elif marker == "vt":
                    clean_type = clean_type.replace("vt.", "").strip().strip(",")
                

                # Если нашли маркер — добавляем его через запятую
                if marker:
                    rest_of_line = f"{marker} / {clean_type}"
                else:
                    rest_of_line = clean_type

                # ГЛАВНОЕ: нет ### (шрифт обычный), жирным только слово (word)
                st.markdown(f"**{word}**: {rest_of_line}")

                
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
