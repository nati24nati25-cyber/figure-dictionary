
import streamlit as st


col1, _ = st.columns([1, 5])
with col1:
    if st.button("🔙 Zur Startseite / Назад на главную", type="secondary"):
        st.switch_page("Startseite.py")
st.divider()

# ---------------------------------------------------------------
# Заголовок
# ---------------------------------------------------------------
st.title("📚 Wörterbuchzonen und Markierungen / Словарные зоны и пометы")

st.markdown(
    """
    Diese Seite zeigt, wie ein Wörterbuchartikel aufgebaut ist, welche Zonen
    er enthält und welche Markierungen im Wörterbuch verwendet werden.
    Alle Beispiele stammen direkt aus der Datenbasis des Wörterbuchs.
    """
)

tab_de, tab_ru = st.tabs(["🇩🇪 Deutsch", "🇷🇺 Русский"])

# ===============================================================
# НЕМЕЦКАЯ ВЕРСИЯ (первая)
# ===============================================================
with tab_de:

    st.subheader("Struktur eines Wörterbuchartikels (Zonen)")

    st.markdown("""
    Jeder Wörterbuchartikel folgt einem einheitlichen Schema aus einer Abfolge
    von **Wörterbuchzonen**. Die Zusammensetzung der Zonen hängt von der Wortart ab:
    bei Substantiven wird die vollständige Deklination angegeben, bei Verben die
    drei Stammformen.
    """)

    with st.expander("🧊 Beispiel 1: Substantiv — „Axel“", expanded=True):
        st.markdown("""
        | Nr. | Zone | Inhalt im Artikel „Axel“ |
        | --- | --- | --- |
        | 1 | **Stichwort** | Axel |
        | 2 | **Grammatische Angaben** | Substantiv, maskulinum |
        | 3 | **Deklination** | der Axel / des Axels / dem Axel / den Axel; Pl.: die Axel / der Axel / den Axeln / die Axel |
        | 4 | **Übersetzung** | аксель |
        | 5 | **Definition** | von der Außenkante des linken Fußes vorwärts ausgeführter Sprung, bei dem der Läufer bzw. die Läuferin nach einer Umdrehung rückwärtslaufend mit der Außenkante des rechten Fußes wieder aufsetzt |
        | 6 | **Herkunft** | nach dem norwegischen Eiskunstläufer Axel Paulsen |
        | 7 | **Beispiel des Gebrauchs** | „Der Axel wird vorwärts von der Außenkante des linken Fußes abgesprungen. Später zeigte er noch vier weitere Dreifache, nur der zweite Axel wurde nur einfach.“ |
        | 8 | **Illustration** | axel.jpg |
        """)

    with st.expander("🏃 Beispiel 2: Verb — „abheben“"):
        st.markdown("""
        | Nr. | Zone | Inhalt im Artikel „abheben“ |
        | --- | --- | --- |
        | 1 | **Stichwort** | abheben |
        | 2 | **Grammatische Angaben** | starkes Verb (hebt ab, hob ab, hat abgehoben), vi. |
        | 3 | **Übersetzung** | отрываться от льда |
        | 4 | **Definition** | sich in die Luft erheben |
        | 5 | **Beispiel des Gebrauchs** | „Durch energische Kniestreckung heben Spitzenschritte vom Eis ab, werden zu Hüpfern oder gar kleinen Sprüngen.“ |
        """)

    with st.expander("↔️ Beispiel 3: Adverb — „auswärts“"):
        st.markdown("""
        | Nr. | Zone | Inhalt im Artikel „auswärts“ |
        | --- | --- | --- |
        | 1 | **Stichwort** | auswärts |
        | 2 | **Grammatische Angaben** | Adverb |
        | 3 | **Übersetzung** | наружу (на наружном ребре) |
        | 4 | **Definition** | Lauf auf der Außenkante |
        | 5 | **Beispiel des Gebrauchs** | „Beim Dreierschritt vorwärts auswärts erfolgt der Einlauf Lva, linker Arm und linke Körperseite vorn.“ |
        | 6 | **Bedeutungsverwandte Wörter** | Außenkante |
        """)

    with st.expander("3️⃣ Beispiel 4: Adjektiv — „dreifach“"):
        st.markdown("""
        | Nr. | Zone | Inhalt im Artikel „dreifach“ |
        | --- | --- | --- |
        | 1 | **Stichwort** | dreifach |
        | 2 | **Grammatische Angaben** | Adjektiv |
        | 3 | **Übersetzung** | тройной (в три оборота) |
        | 4 | **Definition** | mit 3 Umdrehungen |
        | 5 | **Beispiel des Gebrauchs** | „Die Weltmeisterin aus Russland stand zu Beginn des Programms zwei exzellente Vierfach-Flip, einmal in Kombination mit dem dreifachen Toeloop.“ |
        """)

    with st.expander("✅ Beispiel 5: partizipiales Adjektiv — „gestanden“"):
        st.markdown("""
        | Nr. | Zone | Inhalt im Artikel „gestanden“ |
        | --- | --- | --- |
        | 1 | **Stichwort** | gestanden |
        | 2 | **Grammatische Angaben** | partizipiales Adjektiv, pp. |
        | 3 | **Übersetzung** | выстоянный, получившийся (прыжок) |
        | 4 | **Beispiel des Gebrauchs** | „Er zeigte fünf Vierfache, drei davon waren sauber gestanden, bei den anderen beiden fiel er.“ |
        | 5 | **Bedeutungsverwandte Wörter** | Toeloop, Flip, Lutz *(vgl. analoge pp.-Markierung bei getippt, gestreckt, gespreizt)* |
        """)

    st.subheader("Verwendete Markierungen")

    st.markdown("""
    | Markierung | Bedeutung | Beispiele aus dem Wörterbuch |
    | --- | --- | --- |
    | **Substantiv + Genus** | Substantiv mit Genusangabe: maskulinum / femininum / neutrum | Axel *(maskulinum)*, Pirouette *(femininum)*, Kufentuch *(neutrum)* |
    | **starkes Verb** | Starkes Verb (mit Stammformen: 3. Pers. Sg. / Präteritum / Perfekt) | abheben (hebt ab, hob ab, hat abgehoben), auslaufen, gleiten |
    | **schwaches Verb** | Schwaches Verb | abrollen, landen, tippen |
    | **vi.** | Intransitives Verb | abspringen, bremsen, stürzen |
    | **vt.** | Transitives Verb | ausführen, einnehmen, ausstrecken |
    | **vi./vt.** | Verb in beiden Verwendungen | beugen |
    | **trennbar** | Trennbares Präfix | durchführen |
    | **Adverb** | Adverb | auswärts, einwärts, rückwärts, vorwärts |
    | **Adjektiv** | Adjektiv | dreifach, doppelt, vierfach, einfach |
    | **partizipiales Adjektiv (pp.)** | Deverbalives Adjektiv (Partizip) | gestanden, getippt, gestreckt, gespreizt, unterrotiert |
    """)

    st.info(
        "ℹ️ Die Markierungen bilden das **tatsächliche System des Wörterbuchs** ab: "
        "bei Substantiven werden Genus und vollständige Deklination erfasst, bei Verben "
        "der Konjugationstyp (stark/schwach), Transitivität und trennbare Präfixe, "
        "bei Adjektiven der Unterschied zwischen eigentlichen Adjektiven und deverbaliven "
        "Bildungen (pp.)."
    )

# ===============================================================
# РУССКАЯ ВЕРСИЯ (вторая)
# ===============================================================
with tab_ru:

    st.subheader("Структура словарной статьи (зоны)")

    st.markdown("""
    Каждая словарная статья построена по единой схеме — из последовательности
    **словарных зон**. Состав зон зависит от части речи: у существительных
    приводится полная парадигма склонения, у глаголов — три основные формы.
    """)

    with st.expander("🧊 Пример 1: Substantiv — «Axel»", expanded=True):
        st.markdown("""
        | № | Зона | Содержание в статье «Axel» |
        | --- | --- | --- |
        | 1 | **Stichwort** | Axel |
        | 2 | **Grammatische Angaben** | Substantiv, maskulinum |
        | 3 | **Deklination** | der Axel / des Axels / dem Axel / den Axel; Pl.: die Axel / der Axel / den Axeln / die Axel |
        | 4 | **Übersetzung** | аксель |
        | 5 | **Definition** | von der Außenkante des linken Fußes vorwärts ausgeführter Sprung, bei dem der Läufer bzw. die Läuferin nach einer Umdrehung rückwärtslaufend mit der Außenkante des rechten Fußes wieder aufsetzt |
        | 6 | **Herkunft** | nach dem norwegischen Eiskunstläufer Axel Paulsen |
        | 7 | **Beispiel des Gebrauchs** | „Der Axel wird vorwärts von der Außenkante des linken Fußes abgesprungen. Später zeigte er noch vier weitere Dreifache, nur der zweite Axel wurde nur einfach.“ |
        | 8 | **Illustration** | axel.jpg |
        """)

    with st.expander("🏃 Пример 2: Verb — «abheben»"):
        st.markdown("""
        | № | Зона | Содержание в статье «abheben» |
        | --- | --- | --- |
        | 1 | **Stichwort** | abheben |
        | 2 | **Grammatische Angaben** | starkes Verb (hebt ab, hob ab, hat abgehoben), vi. |
        | 3 | **Übersetzung** | отрываться от льда |
        | 4 | **Definition** | sich in die Luft erheben |
        | 5 | **Beispiel des Gebrauchs** | „Durch energische Kniestreckung heben Spitzenschritte vom Eis ab, werden zu Hüpfern oder gar kleinen Sprüngen.“ |
        """)

    with st.expander("↔️ Пример 3: Adverb — «auswärts»"):
        st.markdown("""
        | № | Зона | Содержание в статье «auswärts» |
        | --- | --- | --- |
        | 1 | **Stichwort** | auswärts |
        | 2 | **Grammatische Angaben** | Adverb |
        | 3 | **Übersetzung** | наружу (на наружном ребре) |
        | 4 | **Definition** | Lauf auf der Außenkante |
        | 5 | **Beispiel des Gebrauchs** | „Beim Dreierschritt vorwärts auswärts erfolgt der Einlauf Lva, linker Arm und linke Körperseite vorn.“ |
        | 6 | **Bedeutungsverwandte Wörter** | Außenkante |
        """)

    with st.expander("3️⃣ Пример 4: Adjektiv — «dreifach»"):
        st.markdown("""
        | № | Зона | Содержание в статье «dreifach» |
        | --- | --- | --- |
        | 1 | **Stichwort** | dreifach |
        | 2 | **Grammatische Angaben** | Adjektiv |
        | 3 | **Übersetzung** | тройной (в три оборота) |
        | 4 | **Definition** | mit 3 Umdrehungen |
        | 5 | **Beispiel des Gebrauchs** | „Die Weltmeisterin aus Russland stand zu Beginn des Programms zwei exzellente Vierfach-Flip, einmal in Kombination mit dem dreifachen Toeloop.“ |
        """)

    with st.expander("✅ Пример 5: partizipiales Adjektiv — «gestanden»"):
        st.markdown("""
        | № | Зона | Содержание в статье «gestanden» |
        | --- | --- | --- |
        | 1 | **Stichwort** | gestanden |
        | 2 | **Grammatische Angaben** | partizipiales Adjektiv, pp. |
        | 3 | **Übersetzung** | выстоянный, получившийся (прыжок) |
        | 4 | **Beispiel des Gebrauchs** | „Er zeigte fünf Vierfache, drei davon waren sauber gestanden, bei den anderen beiden fiel er.“ |
        | 5 | **Bedeutungsverwandte Wörter** | Toeloop, Flip, Lutz *(ср. аналогичную помету pp. у слов getippt, gestreckt, gespreizt)* |
        """)

    st.subheader("Используемые пометы")

    st.markdown("""
    | Помета | Значение | Примеры из словаря |
    | --- | --- | --- |
    | **Substantiv + Genus** | Существительное с указанием рода: maskulinum / femininum / neutrum | Axel *(maskulinum)*, Pirouette *(femininum)*, Kufentuch *(neutrum)* |
    | **starkes Verb** | Сильный глагол (с указанием форм: 3 л. ед. ч. / претерит / перфект) | abheben (hebt ab, hob ab, hat abgehoben), auslaufen, gleiten |
    | **schwaches Verb** | Слабый глагол | abrollen, landen, tippen |
    | **vi.** | Непереходный глагол (intransitiv) | abspringen, bremsen, stürzen |
    | **vt.** | Переходный глагол (transitiv) | ausführen, einnehmen, ausstrecken |
    | **vi./vt.** | Глагол, употребляемый в обоих значениях | beugen |
    | **trennbar** | Отделяемая приставка | durchführen |
    | **Adverb** | Наречие | auswärts, einwärts, rückwärts, vorwärts |
    | **Adjektiv** | Прилагательное | dreifach, doppelt, vierfach, einfach |
    | **partizipiales Adjektiv (pp.)** | Отглагольное прилагательное (причастие) | gestanden, getippt, gestreckt, gespreizt, unterrotiert |
    """)

    st.info(
        "ℹ️ Пометы отражают **реальную систему, использованную в словаре**: для существительных "
        "фиксируется род и полное склонение, для глаголов — тип спряжения (сильный/слабый), "
        "переходность и отделяемость приставки, для прилагательных — различие между "
        "«настоящими» прилагательными и отглагольными (pp.)."
    )
