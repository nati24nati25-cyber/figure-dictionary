
import streamlit as st


col1, _ = st.columns([1, 5])
with col1:
    if st.button("🔙 Zur Startseite / Назад на главную", type="secondary"):
        st.switch_page("Startseite.py")
st.divider()

# ---------------------------------------------------------------
# Заголовок страницы
# ---------------------------------------------------------------
st.title("📘 Über das Projekt / О проекте")

st.markdown(
    """
    Wählen Sie die Sprache der Projektbeschreibung / Выберите язык описания проекта:
    """
)

tab_de, tab_ru = st.tabs(["🇩🇪 Deutsch", "🇷🇺 Русский"])

# ===============================================================
# НЕМЕЦКАЯ ВЕРСИЯ (первая)
# ===============================================================
with tab_de:

    st.subheader("Über das Projekt: Wörterbuch der Eiskunstlauf-Terminologie")

    st.markdown(
        """
        Diese Seite beschreibt die Konzeption des Projekts, die Methodik der Datenerhebung und -verarbeitung
        sowie die praktische Bedeutung des Wörterbuchs für das Übersetzen und die sportliche Lexikographie.
        """
    )

    # -----------------------------------------------------------
    # Блок 1: Was ist das für ein Wörterbuch?
    # -----------------------------------------------------------
    with st.expander("🗂 Was ist das für ein Wörterbuch und wie wurde es erstellt?", expanded=True):
        st.write("""
        **Typ des Wörterbuchs:** Terminologisches, zweisprachiges (**Deutsch-Russisch**), fachspezifisches Wörterbuch.
        **Fachgebiet:** Eiskunstlauf (Termini für Elemente, Wertung, Programmbeschreibungen, Kommentatorensprache).

        **Schritte der Datenerfassung und Verarbeitung:**
        1. **Datensammlung:** Transkripte von Wettkämpfen der ISU (International Skating Union),
           Materialien des Deutschen Eislaufverbands (DEU), Interviews mit Athleten auf Deutsch,
           Artikel der Sportmedien und offizielle Regelwerke.
        2. **Terminextraktion:** Häufigkeitsanalyse der Lexik + fachliche Verifizierung
           (manuelle Prüfung der Terminliste auf Übereinstimmung mit der realen Praxis).
        3. **Normalisierung und Bereinigung:** Entfernung von Duplikaten, Normierung der Schreibweise,
           Filterung irrelevanter Texte.
        4. **Strukturierung und Markierung:** Hinzufügen grammatischer Angaben (Genus, Deklination),
           stilistischer Marker, Auswahl von Äquivalenten und kontextbezogenen Beispielen.
           Die Daten sind in einem strukturierten Textformat gespeichert, um automatisches Parsing zu ermöglichen.
        """)

    # -----------------------------------------------------------
    # Блок 2: Praktische Bedeutung
    # -----------------------------------------------------------
    with st.expander("💡 Praktische Bedeutung für das Übersetzen"):
        st.write("""
        Das Wörterbuch löst konkrete Probleme der Übersetzung im Sportbereich:
        *   **Etablierte Übersetzungsvarianten:** Zeigt, welche russischen Äquivalente tatsächlich
            in Übertragungen und Artikeln verwendet werden (vermeidet Kalkierungen und wörtliche Übersetzungen).
        *   **Grammatische Zonen:** Illustriert das Deklinationsschema deutscher Substantive,
            was für die korrekte Kongruenz im russischen Text entscheidend ist.
        *   **Kontextualisierung:** Beispiele für den Gebrauch von Termini in realen Berichten helfen,
            die passende Variante für den jeweiligen Texttyp zu wählen (Nachricht, Reportage, technisches Protokoll).
        *   **Multimodalität:** Die Verfügbarkeit von Audioaussprache und Illustrationen ermöglicht es dem Übersetzer,
            die Referenz des Terminus genauer zu erfassen (z. B. einen Sprung anhand des visuellen Bildes von einem anderen zu unterscheiden).
        """)

    # -----------------------------------------------------------
    # Блок 3: Technologien
    # -----------------------------------------------------------
    with st.expander("🛠 Verwendete Module und Technologien (für den GitHub-Deploy)"):
        st.write("""
        | Modul | Zweck |
        | --- | --- |
        | `streamlit` | Web-Interface der Anwendung, Navigation zwischen den Seiten |
        | `re` (regular expressions) | Parsing der strukturierten Textdateien des Wörterbuchs |
        | `base64` | Einbindung von Audio- und Grafikdateien in die Oberfläche |
        | `html` / `markdown` | Formatierung der Wörterbuchartikel und Zonen |

        *Hinweis:* In der aktuellen Implementierung werden die Daten in Textdateien (`dictionary_new.txt`, `categories.txt`)
        gespeichert, um die Struktur maximal transparent zu halten. Für eine Erweiterung ist eine Migration zu `sqlite3` vorgesehen.
        """)
        st.info("Die vollständige Liste der Abhängigkeiten finden Sie in der Datei `requirements.txt` im GitHub-Repository.")

    # -----------------------------------------------------------
    # Блок 4: Deploy
    # -----------------------------------------------------------
    with st.expander("⚠️ Besonderheiten des Deploys (Streamlit)"):
        st.write("""
        Die Anwendung wurde mit Streamlit entwickelt. Für einen stabilen Betrieb im Hosting (inkl. Streamlit Cloud)
        ist eine korrekte Ordnerstruktur im Repository entscheidend:
        - Die Datendateien (`dictionary_new.txt` usw.) müssen im Wurzelverzeichnis liegen.
        - Der Ordner `pages` darf nur Seitendateien enthalten.
        - `st.set_page_config` muss ausschließlich in der Hauptdatei (`Startseite.py`) stehen.

        Für den lokalen Start genügt der Befehl: `streamlit run Startseite.py`.
        Für einen professionellen Deploy wird die Verpackung in einen Docker-Container (Datei `Dockerfile`) empfohlen.
        """)


# ===============================================================
# РУССКАЯ ВЕРСИЯ (вторая)
# ===============================================================
with tab_ru:

    st.subheader("О проекте: Словарь терминов фигурного катания")

    st.markdown(
        """
        Эта страница раскрывает концепцию проекта, методику сбора и разметки данных,
        а также практическую значимость словаря для сферы переводоведения и спортивной лексикографии.
        """
    )

    # -----------------------------------------------------------
    # Блок 1: Что за словарь и как он собирался
    # -----------------------------------------------------------
    with st.expander("🗂 Что за словарь и как он собирался?", expanded=True):
        st.write("""
        **Тип словаря:** Терминологический, двуязычный (**немецко-русский**), узкоспециальный.
        **Предметная область:** Фигурное катание (термины элементов, судейства, описания программ, лексика комментаторов).

        **Этапы сбора и обработки данных:**
        1. **Сбор корпуса и источников:** Транскрипты соревнований ISU (International Skating Union),
           материалы немецкого союза фигурного катания (DEU), интервью спортсменов на немецком языке,
           статьи спортивных СМИ и официальные правила.
        2. **Извлечение терминов:** Частотный анализ лексики + экспертная верификация
           (ручная проверка списка терминов на соответствие реальной практике).
        3. **Нормализация и очистка:** Удаление дублей, приведение к нормативной форме,
           фильтрация нерелевантных текстов.
        4. **Структурирование и разметка:** Добавление грамматических помет (род, склонение),
           стилистических маркеров, подбор эквивалентов и контекстных примеров.
           Данные сохранены в структурированном текстовом формате для автоматического парсинга.
        """)

    # -----------------------------------------------------------
    # Блок 2: Практическая значимость
    # -----------------------------------------------------------
    with st.expander("💡 Практическая значимость для переводоведения"):
        st.write("""
        Словарь решает конкретные проблемы переводчика в спортивной сфере:
        *   **Устоявшиеся варианты перевода:** Показывает, какие русские эквиваленты реально используются
            в трансляциях и статьях (избегает калькирования и буквализмов).
        *   **Грамматические зоны:** Демонстрирует парадигму склонения немецких существительных,
            что критично для корректного согласования в русском тексте.
        *   **Контекстуализация:** Примеры употребления терминов в реальных репортажах помогают
            выбрать вариант, подходящий под конкретный тип текста (новость, репортаж, технический протокол).
        *   **Мультимодальность:** Наличие аудиопроизношения и иллюстраций позволяет переводчику
            точнее понять референцию термина (например, отличить один прыжок от другого по визуальному образу).
        """)

    # -----------------------------------------------------------
    # Блок 3: Технологии
    # -----------------------------------------------------------
    with st.expander("🛠 Используемые модули и технологии (для деплоя на GitHub)"):
        st.write("""
        | Модуль | Назначение |
        | --- | --- |
        | `streamlit` | Веб-интерфейс приложения, навигация между страницами |
        | `re` (regular expressions) | Парсинг структурированных текстовых файлов словаря |
        | `base64` | Встраивание аудио- и графических файлов в интерфейс |
        | `html` / `markdown` | Форматирование словарных статей и зон |

        *Примечание:* В текущей реализации данные хранятся в текстовых файлах (`dictionary_new.txt`, `categories.txt`)
        для максимальной прозрачности структуры. Для масштабирования предусмотрена возможность миграции на `sqlite3`.
        """)
        st.info("Полный список зависимостей указан в файле `requirements.txt` в репозитории на GitHub.")

    # -----------------------------------------------------------
    # Блок 4: Деплой
    # -----------------------------------------------------------
    with st.expander("⚠️ Особенности деплоя (про Streamlit)"):
        st.write("""
        Приложение разработано на Streamlit. Для стабильной работы на хостинге (в т.ч. Streamlit Cloud)
        критически важно корректное размещение файлов в репозитории:
        - Файлы данных (`dictionary_new.txt` и др.) должны находиться в корне репозитория.
        - Папка `pages` должна содержать только файлы страниц.
        - `st.set_page_config` должен быть только в главном файле (`Startseite.py`).

        Для локального запуска достаточно команды: `streamlit run Startseite.py`.
        Для промышленного деплоя рекомендуется упаковка в Docker-контейнер (файл `Dockerfile` прилагается).
        """)

    
