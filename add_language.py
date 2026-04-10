"""
Add a new language to a CoachBoard app.
1. Read strings_en.dart
2. Translate all values
3. Write strings_XX.dart
4. Register in app_localizations.dart
"""
import re
import os
import sys

BASE = r"C:\Users\SMART"

# Word-level translation dictionaries
TRANSLATIONS = {
    "pt": {  # PT-BR
        # Common UI
        "Save": "Salvar", "Cancel": "Cancelar", "Delete": "Excluir", "Edit": "Editar",
        "Close": "Fechar", "Yes": "Sim", "No": "Não", "OK": "OK", "Done": "Concluído",
        "Add": "Adicionar", "Remove": "Remover", "Back": "Voltar", "Next": "Próximo",
        "Skip": "Pular", "Share": "Compartilhar", "Export": "Exportar", "Print": "Imprimir",
        "Search": "Buscar", "Settings": "Configurações", "Appearance": "Aparência",
        "Language": "Idioma", "Loading": "Carregando", "Error": "Erro", "Saved": "Salvo",
        "Reset": "Redefinir", "Undo": "Desfazer", "Redo": "Refazer", "Select": "Selecionar",
        "Start": "Iniciar", "End": "Finalizar", "Stop": "Parar", "Continue": "Continuar",
        # Sports
        "Player": "Jogador", "Players": "Jogadores", "Team": "Equipe", "Teams": "Equipes",
        "Match": "Partida", "Matches": "Partidas", "Game": "Jogo", "Games": "Jogos",
        "Score": "Placar", "Season": "Temporada", "Stats": "Estatísticas", "Statistics": "Estatísticas",
        "Lineup": "Escalação", "Formation": "Formação", "Bench": "Suplentes",
        "Home": "Casa", "Away": "Fora", "Win": "Vitória", "Loss": "Derrota", "Draw": "Empate",
        "Goal": "Gol", "Goals": "Gols", "Assist": "Assistência", "Assists": "Assistências",
        "Shot": "Chute", "Shots": "Chutes", "Penalty": "Pênalti",
        "Substitution": "Substituição", "Record": "Registro", "History": "Histórico",
        "Rating": "Avaliação", "Overall": "Geral", "Average": "Média", "Total": "Total",
        "Upgrade": "Atualizar", "Premium": "Premium", "Pro": "Pro", "Free": "Grátis",
        "Coach": "Treinador", "Opponent": "Adversário", "Schedule": "Agenda",
        "Calendar": "Calendário", "Training": "Treino", "Tactical": "Tático",
        "Board": "Quadro", "Uniform": "Uniforme", "Uniforms": "Uniformes",
        "Dark Mode": "Modo Escuro", "Light Mode": "Modo Claro",
        "Name": "Nome", "Number": "Número", "Position": "Posição", "Age": "Idade",
        "Height": "Altura", "Weight": "Peso", "Nationality": "Nacionalidade",
        "Summary": "Resumo", "Details": "Detalhes", "Notes": "Notas",
        "Performance": "Desempenho", "Feedback": "Feedback",
    },
    "tr": {  # Turkish
        "Save": "Kaydet", "Cancel": "İptal", "Delete": "Sil", "Edit": "Düzenle",
        "Close": "Kapat", "Yes": "Evet", "No": "Hayır", "OK": "Tamam", "Done": "Tamamlandı",
        "Add": "Ekle", "Remove": "Kaldır", "Back": "Geri", "Next": "İleri",
        "Skip": "Atla", "Share": "Paylaş", "Export": "Dışa Aktar", "Print": "Yazdır",
        "Search": "Ara", "Settings": "Ayarlar", "Appearance": "Görünüm",
        "Language": "Dil", "Loading": "Yükleniyor", "Error": "Hata", "Saved": "Kaydedildi",
        "Reset": "Sıfırla", "Undo": "Geri Al", "Redo": "Yinele", "Select": "Seç",
        "Start": "Başla", "End": "Bitir", "Stop": "Dur", "Continue": "Devam",
        "Player": "Oyuncu", "Players": "Oyuncular", "Team": "Takım", "Teams": "Takımlar",
        "Match": "Maç", "Matches": "Maçlar", "Game": "Oyun", "Games": "Oyunlar",
        "Score": "Skor", "Season": "Sezon", "Stats": "İstatistikler", "Statistics": "İstatistikler",
        "Lineup": "Kadro", "Formation": "Diziliş", "Bench": "Yedek",
        "Home": "Ev Sahibi", "Away": "Deplasman", "Win": "Galibiyet", "Loss": "Mağlubiyet", "Draw": "Beraberlik",
        "Goal": "Gol", "Goals": "Goller", "Assist": "Asist", "Assists": "Asistler",
        "Shot": "Şut", "Shots": "Şutlar", "Penalty": "Penaltı",
        "Substitution": "Oyuncu Değişikliği", "Record": "Kayıt", "History": "Geçmiş",
        "Rating": "Puan", "Overall": "Genel", "Average": "Ortalama", "Total": "Toplam",
        "Coach": "Antrenör", "Opponent": "Rakip", "Schedule": "Program",
        "Calendar": "Takvim", "Training": "Antrenman", "Tactical": "Taktik",
        "Board": "Tahta", "Uniform": "Forma", "Uniforms": "Formalar",
        "Dark Mode": "Karanlık Mod", "Light Mode": "Aydınlık Mod",
        "Name": "İsim", "Number": "Numara", "Position": "Pozisyon",
        "Summary": "Özet", "Details": "Detaylar", "Notes": "Notlar",
    },
    "pl": {  # Polish
        "Save": "Zapisz", "Cancel": "Anuluj", "Delete": "Usuń", "Edit": "Edytuj",
        "Close": "Zamknij", "Yes": "Tak", "No": "Nie", "OK": "OK", "Done": "Gotowe",
        "Add": "Dodaj", "Remove": "Usuń", "Back": "Wstecz", "Next": "Dalej",
        "Share": "Udostępnij", "Export": "Eksportuj", "Print": "Drukuj",
        "Search": "Szukaj", "Settings": "Ustawienia", "Appearance": "Wygląd",
        "Language": "Język", "Loading": "Ładowanie", "Error": "Błąd", "Saved": "Zapisano",
        "Player": "Zawodnik", "Players": "Zawodnicy", "Team": "Drużyna", "Teams": "Drużyny",
        "Match": "Mecz", "Matches": "Mecze", "Game": "Gra",
        "Score": "Wynik", "Season": "Sezon", "Stats": "Statystyki",
        "Lineup": "Skład", "Formation": "Ustawienie", "Bench": "Ławka",
        "Home": "Gospodarze", "Away": "Goście", "Win": "Wygrana", "Loss": "Przegrana", "Draw": "Remis",
        "Goal": "Gol", "Goals": "Gole", "Assist": "Asysta", "Shot": "Strzał",
        "Substitution": "Zmiana", "Record": "Zapis", "History": "Historia",
        "Coach": "Trener", "Opponent": "Przeciwnik", "Schedule": "Harmonogram",
        "Training": "Trening", "Tactical": "Taktyczny", "Board": "Tablica",
        "Summary": "Podsumowanie", "Notes": "Notatki",
    },
    "de": {  # German
        "Save": "Speichern", "Cancel": "Abbrechen", "Delete": "Löschen", "Edit": "Bearbeiten",
        "Close": "Schließen", "Yes": "Ja", "No": "Nein", "OK": "OK", "Done": "Fertig",
        "Add": "Hinzufügen", "Remove": "Entfernen", "Back": "Zurück", "Next": "Weiter",
        "Share": "Teilen", "Export": "Exportieren", "Print": "Drucken",
        "Settings": "Einstellungen", "Appearance": "Darstellung",
        "Player": "Spieler", "Players": "Spieler", "Team": "Team", "Teams": "Teams",
        "Match": "Spiel", "Matches": "Spiele", "Game": "Spiel",
        "Score": "Ergebnis", "Season": "Saison", "Stats": "Statistiken",
        "Lineup": "Aufstellung", "Formation": "Formation", "Bench": "Bank",
        "Home": "Heim", "Away": "Auswärts", "Win": "Sieg", "Loss": "Niederlage", "Draw": "Unentschieden",
        "Goal": "Tor", "Goals": "Tore", "Assist": "Vorlage", "Shot": "Schuss",
        "Substitution": "Auswechslung", "Record": "Aufzeichnung", "History": "Verlauf",
        "Coach": "Trainer", "Opponent": "Gegner", "Schedule": "Spielplan",
        "Training": "Training", "Tactical": "Taktik", "Board": "Tafel",
        "Summary": "Zusammenfassung", "Notes": "Notizen",
    },
    "ru": {  # Russian
        "Save": "Сохранить", "Cancel": "Отмена", "Delete": "Удалить", "Edit": "Редактировать",
        "Close": "Закрыть", "Yes": "Да", "No": "Нет", "OK": "ОК", "Done": "Готово",
        "Add": "Добавить", "Remove": "Удалить", "Back": "Назад", "Next": "Далее",
        "Share": "Поделиться", "Export": "Экспорт", "Print": "Печать",
        "Settings": "Настройки", "Appearance": "Оформление",
        "Player": "Игрок", "Players": "Игроки", "Team": "Команда", "Teams": "Команды",
        "Match": "Матч", "Matches": "Матчи", "Game": "Игра",
        "Score": "Счёт", "Season": "Сезон", "Stats": "Статистика",
        "Lineup": "Состав", "Formation": "Расстановка", "Bench": "Запасные",
        "Home": "Дома", "Away": "В гостях", "Win": "Победа", "Loss": "Поражение", "Draw": "Ничья",
        "Goal": "Гол", "Goals": "Голы", "Assist": "Передача", "Shot": "Бросок",
        "Substitution": "Замена", "Record": "Запись", "History": "История",
        "Coach": "Тренер", "Opponent": "Соперник", "Schedule": "Расписание",
        "Training": "Тренировка", "Tactical": "Тактика", "Board": "Доска",
        "Summary": "Итоги", "Notes": "Заметки",
    },
    "it": {  # Italian
        "Save": "Salva", "Cancel": "Annulla", "Delete": "Elimina", "Edit": "Modifica",
        "Close": "Chiudi", "Yes": "Sì", "No": "No", "OK": "OK", "Done": "Fatto",
        "Add": "Aggiungi", "Remove": "Rimuovi", "Back": "Indietro", "Next": "Avanti",
        "Share": "Condividi", "Export": "Esporta", "Print": "Stampa",
        "Settings": "Impostazioni", "Appearance": "Aspetto",
        "Player": "Giocatore", "Players": "Giocatori", "Team": "Squadra", "Teams": "Squadre",
        "Match": "Partita", "Matches": "Partite", "Game": "Gioco",
        "Score": "Punteggio", "Season": "Stagione", "Stats": "Statistiche",
        "Lineup": "Formazione", "Formation": "Schema", "Bench": "Panchina",
        "Home": "Casa", "Away": "Trasferta", "Win": "Vittoria", "Loss": "Sconfitta", "Draw": "Pareggio",
        "Goal": "Gol", "Goals": "Gol", "Assist": "Assist", "Shot": "Tiro",
        "Substitution": "Sostituzione", "Record": "Registro", "History": "Cronologia",
        "Coach": "Allenatore", "Opponent": "Avversario", "Schedule": "Calendario",
        "Training": "Allenamento", "Tactical": "Tattica", "Board": "Lavagna",
        "Summary": "Riepilogo", "Notes": "Note",
    },
    "sk": {  # Slovak
        "Save": "Uložiť", "Cancel": "Zrušiť", "Delete": "Vymazať", "Edit": "Upraviť",
        "Close": "Zavrieť", "Yes": "Áno", "No": "Nie", "OK": "OK", "Done": "Hotovo",
        "Add": "Pridať", "Remove": "Odstrániť", "Back": "Späť", "Next": "Ďalej",
        "Share": "Zdieľať", "Export": "Exportovať", "Print": "Tlačiť",
        "Settings": "Nastavenia", "Appearance": "Vzhľad",
        "Player": "Hráč", "Players": "Hráči", "Team": "Tím", "Teams": "Tímy",
        "Match": "Zápas", "Matches": "Zápasy", "Game": "Hra",
        "Score": "Skóre", "Season": "Sezóna", "Stats": "Štatistiky",
        "Lineup": "Zostava", "Formation": "Formácia", "Bench": "Lavička",
        "Home": "Domáci", "Away": "Hostia", "Win": "Výhra", "Loss": "Prehra", "Draw": "Remíza",
        "Goal": "Gól", "Goals": "Góly", "Assist": "Asistencia", "Shot": "Strela",
        "Substitution": "Striedanie", "Record": "Záznam", "History": "História",
        "Coach": "Tréner", "Opponent": "Súper",
        "Summary": "Zhrnutie", "Notes": "Poznámky",
    },
    "da": {  # Danish
        "Save": "Gem", "Cancel": "Annuller", "Delete": "Slet", "Edit": "Rediger",
        "Close": "Luk", "Yes": "Ja", "No": "Nej", "OK": "OK", "Done": "Færdig",
        "Add": "Tilføj", "Remove": "Fjern", "Back": "Tilbage", "Next": "Næste",
        "Share": "Del", "Export": "Eksporter", "Print": "Udskriv",
        "Settings": "Indstillinger", "Appearance": "Udseende",
        "Player": "Spiller", "Players": "Spillere", "Team": "Hold", "Teams": "Hold",
        "Match": "Kamp", "Matches": "Kampe", "Game": "Spil",
        "Score": "Resultat", "Season": "Sæson", "Stats": "Statistik",
        "Lineup": "Opstilling", "Formation": "Formation", "Bench": "Bænk",
        "Home": "Hjemme", "Away": "Ude", "Win": "Sejr", "Loss": "Nederlag", "Draw": "Uafgjort",
        "Goal": "Mål", "Goals": "Mål", "Assist": "Assist", "Shot": "Skud",
        "Substitution": "Udskiftning", "Record": "Optag", "History": "Historik",
        "Coach": "Træner", "Opponent": "Modstander",
        "Summary": "Oversigt", "Notes": "Noter",
    },
    "hr": {  # Croatian
        "Save": "Spremi", "Cancel": "Odustani", "Delete": "Obriši", "Edit": "Uredi",
        "Close": "Zatvori", "Yes": "Da", "No": "Ne", "OK": "OK", "Done": "Gotovo",
        "Add": "Dodaj", "Remove": "Ukloni", "Back": "Natrag", "Next": "Sljedeće",
        "Share": "Podijeli", "Export": "Izvoz", "Print": "Ispis",
        "Settings": "Postavke", "Appearance": "Izgled",
        "Player": "Igrač", "Players": "Igrači", "Team": "Tim", "Teams": "Timovi",
        "Match": "Utakmica", "Matches": "Utakmice", "Game": "Igra",
        "Score": "Rezultat", "Season": "Sezona", "Stats": "Statistika",
        "Lineup": "Postava", "Formation": "Formacija", "Bench": "Klupa",
        "Home": "Domaći", "Away": "Gosti", "Win": "Pobjeda", "Loss": "Poraz", "Draw": "Neriješeno",
        "Goal": "Gol", "Goals": "Golovi", "Assist": "Asistencija", "Shot": "Udarac",
        "Substitution": "Zamjena", "Record": "Zapis", "History": "Povijest",
        "Coach": "Trener", "Opponent": "Protivnik",
        "Summary": "Sažetak", "Notes": "Bilješke",
    },
    "si": {  # Sinhala
        "Save": "සුරකින්න", "Cancel": "අවලංගු", "Delete": "මකන්න", "Edit": "සංස්කරණය",
        "Close": "වසන්න", "Yes": "ඔව්", "No": "නැත", "OK": "හරි", "Done": "සම්පූර්ණයි",
        "Player": "ක්‍රීඩකයා", "Team": "කණ්ඩායම", "Match": "තරගය",
        "Score": "ලකුණු", "Season": "වාරය", "Stats": "සංඛ්‍යාලේඛන",
        "Lineup": "ලයිනප්", "Formation": "සැකැස්ම", "Bench": "බංකුව",
        "Home": "නිවස", "Away": "පිටස්තර", "Win": "ජය", "Loss": "පරාජය",
        "Goal": "ගෝලය", "Assist": "සහය",
        "Coach": "පුහුණුකරු", "Opponent": "ප්‍රතිවාදී",
    },
    "ta": {  # Tamil
        "Save": "சேமி", "Cancel": "ரத்து", "Delete": "நீக்கு", "Edit": "திருத்து",
        "Close": "மூடு", "Yes": "ஆம்", "No": "இல்லை", "OK": "சரி", "Done": "முடிந்தது",
        "Player": "வீரர்", "Team": "அணி", "Match": "போட்டி",
        "Score": "மதிப்பெண்", "Season": "பருவம்", "Stats": "புள்ளிவிவரங்கள்",
        "Lineup": "லைன்அப்", "Formation": "அணிவகுப்பு", "Bench": "பெஞ்ச்",
        "Home": "வீடு", "Away": "வெளி", "Win": "வெற்றி", "Loss": "தோல்வி",
        "Goal": "கோல்", "Assist": "உதவி",
        "Coach": "பயிற்சியாளர்", "Opponent": "எதிரணி",
    },
}


def parse_en_file(filepath):
    """Parse EN dart strings file, return list of (key, value) in order."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    # Match 'key': 'value', or 'key': "value",
    # Handle escaped quotes (\') inside single-quoted values
    pairs = []
    for m in re.finditer(r"'([^']+)':\s*'((?:[^'\\]|\\.)*)'", text):
        key = m.group(1)
        val = m.group(2).replace("\\'", "'")  # unescape
        pairs.append((key, val))
    for m in re.finditer(r"'([^']+)':\s*\"([^\"]*)\"", text):
        key = m.group(1)
        val = m.group(2)
        if not any(k == key for k, v in pairs):
            pairs.append((key, val))
    return pairs


def translate_value(en_value, lang):
    """Best-effort translate."""
    wmap = TRANSLATIONS.get(lang, {})
    if not wmap:
        return en_value

    # Exact match
    if en_value in wmap:
        return wmap[en_value]

    # Short/abbreviation — keep as-is
    if len(en_value) <= 3 or en_value.isupper():
        return en_value

    # Try longest-match word replacement
    result = en_value
    for en_word, translated in sorted(wmap.items(), key=lambda x: -len(x[0])):
        if en_word in result:
            result = result.replace(en_word, translated, 1)
            if result != en_value:
                return result

    return en_value


def get_var_name(lang):
    """strings_pt.dart -> stringsPt"""
    parts = lang.split("_")
    return "strings" + "".join(p.capitalize() for p in parts)


def create_language_file(app_dir, lang, sport_subtitle):
    l10n_dir = os.path.join(BASE, app_dir, "lib", "core", "l10n")
    en_file = os.path.join(l10n_dir, "strings_en.dart")
    out_file = os.path.join(l10n_dir, f"strings_{lang}.dart")

    if os.path.exists(out_file):
        print(f"  SKIP {lang}: file already exists")
        return False

    pairs = parse_en_file(en_file)
    var_name = get_var_name(lang)

    lines = [f"const Map<String, String> {var_name} = {{"]
    for key, en_val in pairs:
        # Special handling for appSubtitle
        if key == "appSubtitle" and sport_subtitle:
            translated = sport_subtitle
        else:
            translated = translate_value(en_val, lang)
        # Use double quotes if value contains apostrophe
        if "'" in translated:
            lines.append(f'  \'{key}\': "{translated}",')
        else:
            lines.append(f"  '{key}': '{translated}',")
    lines.append("};")
    lines.append("")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Created strings_{lang}.dart ({len(pairs)} keys)")
    return True


def register_in_localizations(app_dir, lang, package_name):
    l10n_file = os.path.join(BASE, app_dir, "lib", "core", "l10n", "app_localizations.dart")
    with open(l10n_file, encoding="utf-8") as f:
        content = f.read()

    var_name = get_var_name(lang)
    import_line = f"import 'package:{package_name}/core/l10n/strings_{lang}.dart';"

    if import_line in content:
        print(f"  SKIP register {lang}: already imported")
        return

    # Add import after last import
    last_import = content.rfind("import 'package:")
    end_of_line = content.index("\n", last_import)
    content = content[:end_of_line + 1] + import_line + "\n" + content[end_of_line + 1:]

    # Add to locale map — find the map and add entry
    # Pattern: 'xx': stringsXx,
    locale_code = lang.replace("_", "-") if "_" in lang else lang
    map_entry = f"    '{locale_code}': {var_name},"

    # Find the closing of the _localizedStrings map
    map_pattern = r"(final Map<String, Map<String, String>> _localizedStrings = \{[^}]*)"
    match = re.search(map_pattern, content, re.DOTALL)
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + "\n" + map_entry + content[insert_pos:]
    else:
        # Try alternate pattern: look for last locale entry and add after
        last_entry = content.rfind("': strings")
        if last_entry > 0:
            end_line = content.index("\n", last_entry)
            content = content[:end_line + 1] + map_entry + "\n" + content[end_line + 1:]

    with open(l10n_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Registered {lang} in app_localizations.dart")


TASKS = [
    # (app_dir, package_name, lang, sport_subtitle)
    ("coachboard", "coachboard", "pt", "- Futebol"),
    ("coachboard", "coachboard", "tr", "- Futbol"),
    ("coachboard", "coachboard", "pl", "- Piłka Nożna"),

    ("coachboard-basketball", "coachboard_basketball", "de", "- Basketball"),
    ("coachboard-basketball", "coachboard_basketball", "pt", "- Basquete"),
    ("coachboard-basketball", "coachboard_basketball", "tr", "- Basketbol"),

    ("coachboard-baseball", "coachboard_baseball", "pt", "- Beisebol"),

    ("coachboard-cricket", "coachboard_cricket", "si", "- ක්‍රිකට්"),
    ("coachboard-cricket", "coachboard_cricket", "ta", "- கிரிக்கெட்"),

    ("coachboard-hockey", "coachboard_hockey", "sk", "- Hokej"),

    ("coachboard-volleyball", "coachboard_volleyball", "ru", "- Волейбол"),
    ("coachboard-volleyball", "coachboard_volleyball", "de", "- Volleyball"),

    ("coachboard-handball", "coachboard_handball", "da", "- Håndbold"),
    ("coachboard-handball", "coachboard_handball", "hr", "- Rukomet"),

    ("coachboard-rugby", "coachboard_rugby", "it", "- Rugby"),
]


def main():
    for app_dir, package_name, lang, subtitle in TASKS:
        sport = app_dir.replace("coachboard-", "").replace("coachboard", "soccer")
        print(f"=== {sport} + {lang} ===")
        created = create_language_file(app_dir, lang, subtitle)
        if created:
            register_in_localizations(app_dir, lang, package_name)


if __name__ == "__main__":
    main()
