"""
Fill missing translations across all 10 CoachBoard apps.
Strategy:
  1. Parse EN file to get all key->value pairs
  2. For each other language file, find missing keys
  3. Generate translations using a mapping approach
  4. Append missing translations before the closing '};'
"""
import re
import os

BASE = r"C:\Users\SMART"

APPS = [
    "coachboard",
    "coachboard-basketball",
    "coachboard-baseball",
    "coachboard-cricket",
    "coachboard-hockey",
    "coachboard-volleyball",
    "coachboard-handball",
    "coachboard-lacrosse",
    "coachboard-rugby",
    "coachboard-football",
]

# Common UI translations for frequently used terms
# Format: en_value -> {lang: translated_value}
COMMON = {
    # Basic UI
    "Save": {"ko": "저장", "es": "Guardar", "fr": "Enregistrer", "de": "Speichern", "it": "Salva", "ja": "保存", "zh": "保存", "zh_tw": "儲存", "ru": "Сохранить", "sv": "Spara", "fi": "Tallenna", "cs": "Uložit", "pt": "Salvar", "pl": "Zapisz", "tr": "Kaydet", "hi": "सहेजें", "bn": "সংরক্ষণ", "ur": "محفوظ کریں"},
    "Cancel": {"ko": "취소", "es": "Cancelar", "fr": "Annuler", "de": "Abbrechen", "it": "Annulla", "ja": "キャンセル", "zh": "取消", "zh_tw": "取消", "ru": "Отмена", "sv": "Avbryt", "fi": "Peruuta", "cs": "Zrušit", "pt": "Cancelar", "pl": "Anuluj", "tr": "İptal", "hi": "रद्द करें", "bn": "বাতিল", "ur": "منسوخ کریں"},
    "Delete": {"ko": "삭제", "es": "Eliminar", "fr": "Supprimer", "de": "Löschen", "it": "Elimina", "ja": "削除", "zh": "删除", "zh_tw": "刪除", "ru": "Удалить", "sv": "Radera", "fi": "Poista", "cs": "Smazat", "pt": "Excluir", "pl": "Usuń", "tr": "Sil", "hi": "हटाएं", "bn": "মুছুন", "ur": "حذف کریں"},
    "Edit": {"ko": "수정", "es": "Editar", "fr": "Modifier", "de": "Bearbeiten", "it": "Modifica", "ja": "編集", "zh": "编辑", "zh_tw": "編輯", "ru": "Редактировать", "sv": "Redigera", "fi": "Muokkaa", "cs": "Upravit", "pt": "Editar", "pl": "Edytuj", "tr": "Düzenle", "hi": "संपादित करें", "bn": "সম্পাদনা", "ur": "ترمیم کریں"},
    "Close": {"ko": "닫기", "es": "Cerrar", "fr": "Fermer", "de": "Schließen", "it": "Chiudi", "ja": "閉じる", "zh": "关闭", "zh_tw": "關閉", "ru": "Закрыть", "sv": "Stäng", "fi": "Sulje", "cs": "Zavřít", "pt": "Fechar", "pl": "Zamknij", "tr": "Kapat", "hi": "बंद करें", "bn": "বন্ধ করুন", "ur": "بند کریں"},
    "Yes": {"ko": "예", "es": "Sí", "fr": "Oui", "de": "Ja", "it": "Sì", "ja": "はい", "zh": "是", "zh_tw": "是", "ru": "Да", "sv": "Ja", "fi": "Kyllä", "cs": "Ano", "pt": "Sim", "pl": "Tak", "tr": "Evet", "hi": "हाँ", "bn": "হ্যাঁ", "ur": "ہاں"},
    "No": {"ko": "아니오", "es": "No", "fr": "Non", "de": "Nein", "it": "No", "ja": "いいえ", "zh": "否", "zh_tw": "否", "ru": "Нет", "sv": "Nej", "fi": "Ei", "cs": "Ne", "pt": "Não", "pl": "Nie", "tr": "Hayır", "hi": "नहीं", "bn": "না", "ur": "نہیں"},
    "OK": {"ko": "확인", "es": "Aceptar", "fr": "OK", "de": "OK", "it": "OK", "ja": "OK", "zh": "确定", "zh_tw": "確定", "ru": "ОК", "sv": "OK", "fi": "OK", "cs": "OK", "pt": "OK", "pl": "OK", "tr": "Tamam", "hi": "ठीक", "bn": "ঠিক আছে", "ur": "ٹھیک ہے"},
    "Dark Mode": {"ko": "다크 모드", "es": "Modo oscuro", "fr": "Mode sombre", "de": "Dunkelmodus", "it": "Modalità scura", "ja": "ダークモード", "zh": "深色模式", "zh_tw": "深色模式", "ru": "Тёмный режим", "sv": "Mörkt läge", "fi": "Tumma tila", "cs": "Tmavý režim", "pt": "Modo escuro", "pl": "Tryb ciemny", "tr": "Karanlık Mod", "hi": "डार्क मोड", "bn": "ডার্ক মোড", "ur": "ڈارک موڈ"},
    "Light Mode": {"ko": "라이트 모드", "es": "Modo claro", "fr": "Mode clair", "de": "Hellmodus", "it": "Modalità chiara", "ja": "ライトモード", "zh": "浅色模式", "zh_tw": "淺色模式", "ru": "Светлый режим", "sv": "Ljust läge", "fi": "Vaalea tila", "cs": "Světlý režim", "pt": "Modo claro", "pl": "Tryb jasny", "tr": "Aydınlık Mod", "hi": "लाइट मोड", "bn": "লাইট মোড", "ur": "لائٹ موڈ"},
}


def parse_dart_strings(filepath):
    """Parse a Dart strings file and return dict of key -> value."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    # Match 'key': 'value', or 'key': "value",
    pairs = re.findall(r"'([^']+)':\s*['\"]([^'\"]*)['\"]", text)
    return dict(pairs)


def translate_value(en_value, lang):
    """Translate an English value to the target language.
    Uses COMMON dict for exact matches, otherwise returns EN value with lang prefix."""
    # Check common translations
    if en_value in COMMON and lang in COMMON[en_value]:
        return COMMON[en_value][lang]

    # For short labels/abbreviations, keep as-is (they're often sport terms)
    if len(en_value) <= 4 or en_value.isupper():
        return en_value

    # Simple word-level translations for common patterns
    word_map = {
        "ko": {
            "Player": "선수", "Team": "팀", "Match": "경기", "Game": "경기",
            "Score": "점수", "Season": "시즌", "Stats": "통계", "Statistics": "통계",
            "Lineup": "라인업", "Formation": "포메이션", "Bench": "벤치",
            "Home": "홈", "Away": "원정", "Win": "승", "Loss": "패", "Draw": "무",
            "Goal": "골", "Assist": "어시스트", "Shot": "슛", "Penalty": "패널티",
            "Substitution": "교체", "Record": "기록", "History": "기록",
            "Export": "내보내기", "Share": "공유", "Print": "인쇄",
            "Rating": "평점", "Overall": "종합", "Average": "평균",
            "Total": "합계", "Select": "선택", "Add": "추가", "Remove": "제거",
            "Start": "시작", "End": "종료", "Reset": "초기화",
            "Settings": "설정", "Appearance": "외관", "Language": "언어",
            "Upgrade": "업그레이드", "Premium": "프리미엄", "Pro": "프로",
            "Free": "무료", "Undo": "실행 취소", "Redo": "다시 실행",
            "Error": "오류", "Loading": "로딩 중", "Saved": "저장됨",
            "Ejection": "퇴장", "Ejected": "퇴장됨",
            "Inning": "이닝", "Innings": "이닝", "Pitch": "투구", "Pitches": "투구",
            "Batter": "타자", "Pitcher": "투수", "Runner": "주자",
            "Batting": "타격", "Pitching": "투구", "Fielding": "수비",
            "Recording": "녹화", "Session": "세션", "Notes": "메모",
            "Leave": "나가기", "Later": "나중에", "Live": "실시간",
            "Load": "불러오기", "Loaded": "불러옴", "Location": "위치",
            "Scoring": "득점", "Leaders": "리더", "Summary": "요약",
            "Heatmap": "히트맵", "Chart": "차트",
        },
        "es": {
            "Player": "Jugador", "Team": "Equipo", "Match": "Partido", "Game": "Juego",
            "Score": "Puntuación", "Season": "Temporada", "Stats": "Estadísticas",
            "Lineup": "Alineación", "Formation": "Formación", "Bench": "Suplentes",
            "Home": "Local", "Away": "Visitante", "Win": "Victoria", "Loss": "Derrota",
            "Goal": "Gol", "Assist": "Asistencia", "Shot": "Tiro", "Penalty": "Penalti",
            "Substitution": "Sustitución", "Record": "Registro", "History": "Historial",
            "Export": "Exportar", "Share": "Compartir", "Print": "Imprimir",
            "Rating": "Valoración", "Overall": "General", "Average": "Promedio",
            "Total": "Total", "Select": "Seleccionar", "Add": "Añadir", "Remove": "Eliminar",
            "Start": "Iniciar", "End": "Finalizar", "Reset": "Reiniciar",
            "Settings": "Ajustes", "Appearance": "Apariencia", "Language": "Idioma",
            "Ejection": "Expulsión", "Ejected": "Expulsado",
            "Inning": "Entrada", "Innings": "Entradas", "Pitch": "Lanzamiento",
            "Batter": "Bateador", "Pitcher": "Lanzador", "Runner": "Corredor",
            "Batting": "Bateo", "Pitching": "Pitcheo", "Fielding": "Defensa",
            "Recording": "Grabación", "Session": "Sesión", "Notes": "Notas",
            "Leave": "Salir", "Later": "Después", "Live": "En vivo",
            "Load": "Cargar", "Loaded": "Cargado", "Location": "Ubicación",
            "Scoring": "Anotación", "Leaders": "Líderes", "Summary": "Resumen",
        },
        "fr": {
            "Player": "Joueur", "Team": "Équipe", "Match": "Match", "Game": "Jeu",
            "Score": "Score", "Season": "Saison", "Stats": "Statistiques",
            "Lineup": "Composition", "Formation": "Formation", "Bench": "Banc",
            "Home": "Domicile", "Away": "Extérieur", "Win": "Victoire", "Loss": "Défaite",
            "Goal": "But", "Assist": "Passe décisive", "Shot": "Tir", "Penalty": "Pénalité",
            "Substitution": "Remplacement", "Record": "Enregistrement", "History": "Historique",
            "Export": "Exporter", "Share": "Partager", "Print": "Imprimer",
            "Ejection": "Expulsion", "Ejected": "Expulsé",
            "Inning": "Manche", "Innings": "Manches", "Pitch": "Lancer",
            "Batter": "Frappeur", "Pitcher": "Lanceur", "Runner": "Coureur",
            "Batting": "Frappe", "Pitching": "Lancer", "Fielding": "Défense",
            "Recording": "Enregistrement", "Session": "Session", "Notes": "Notes",
            "Leave": "Quitter", "Later": "Plus tard", "Live": "En direct",
            "Scoring": "Score", "Leaders": "Leaders", "Summary": "Résumé",
        },
        "de": {
            "Player": "Spieler", "Team": "Team", "Match": "Spiel", "Game": "Spiel",
            "Score": "Ergebnis", "Season": "Saison", "Stats": "Statistiken",
            "Lineup": "Aufstellung", "Formation": "Formation", "Bench": "Bank",
            "Home": "Heim", "Away": "Auswärts", "Win": "Sieg", "Loss": "Niederlage",
            "Goal": "Tor", "Assist": "Assist", "Shot": "Schuss", "Penalty": "Strafe",
            "Substitution": "Auswechslung", "Record": "Aufzeichnung", "History": "Verlauf",
            "Export": "Exportieren", "Share": "Teilen", "Print": "Drucken",
            "Ejection": "Platzverweis", "Ejected": "Des Platzes verwiesen",
            "Recording": "Aufnahme", "Session": "Sitzung", "Notes": "Notizen",
            "Leave": "Verlassen", "Later": "Später", "Live": "Live",
            "Scoring": "Ergebnis", "Leaders": "Beste Spieler", "Summary": "Zusammenfassung",
        },
        "ja": {
            "Player": "選手", "Team": "チーム", "Match": "試合", "Game": "試合",
            "Score": "スコア", "Season": "シーズン", "Stats": "統計",
            "Lineup": "ラインアップ", "Formation": "フォーメーション", "Bench": "ベンチ",
            "Home": "ホーム", "Away": "アウェイ", "Win": "勝利", "Loss": "敗北",
            "Goal": "ゴール", "Assist": "アシスト", "Shot": "シュート", "Penalty": "ペナルティ",
            "Substitution": "交代", "Record": "記録", "History": "履歴",
            "Export": "エクスポート", "Share": "共有", "Print": "印刷",
            "Ejection": "退場", "Ejected": "退場",
            "Inning": "イニング", "Innings": "イニング", "Pitch": "投球",
            "Batter": "打者", "Pitcher": "投手", "Runner": "走者",
            "Batting": "打撃", "Pitching": "投球", "Fielding": "守備",
            "Recording": "録画", "Session": "セッション", "Notes": "メモ",
            "Leave": "退出", "Later": "後で", "Live": "ライブ",
            "Scoring": "得点", "Leaders": "リーダー", "Summary": "サマリー",
        },
        "zh": {
            "Player": "球员", "Team": "球队", "Match": "比赛", "Game": "比赛",
            "Score": "比分", "Season": "赛季", "Stats": "统计",
            "Lineup": "阵容", "Formation": "阵型", "Bench": "替补席",
            "Home": "主场", "Away": "客场", "Win": "胜", "Loss": "负",
            "Goal": "进球", "Assist": "助攻", "Shot": "射门", "Penalty": "处罚",
            "Substitution": "替换", "Record": "记录", "History": "历史",
            "Export": "导出", "Share": "分享", "Print": "打印",
            "Ejection": "罚出", "Ejected": "被罚出",
            "Recording": "录制", "Session": "会话", "Notes": "备注",
            "Leave": "离开", "Later": "稍后", "Live": "直播",
            "Scoring": "得分", "Leaders": "排行榜", "Summary": "总结",
        },
        "zh_tw": {
            "Player": "球員", "Team": "球隊", "Match": "比賽", "Game": "比賽",
            "Score": "比分", "Season": "賽季", "Stats": "統計",
            "Lineup": "陣容", "Formation": "陣型", "Bench": "替補席",
            "Home": "主場", "Away": "客場", "Win": "勝", "Loss": "負",
            "Goal": "進球", "Assist": "助攻", "Shot": "射門", "Penalty": "處罰",
            "Substitution": "替換", "Record": "記錄", "History": "歷史",
            "Export": "匯出", "Share": "分享", "Print": "列印",
            "Ejection": "罰出", "Ejected": "被罰出",
            "Inning": "局", "Innings": "局", "Pitch": "投球",
            "Batter": "打者", "Pitcher": "投手", "Runner": "跑壘員",
            "Batting": "打擊", "Pitching": "投球", "Fielding": "守備",
            "Recording": "錄製", "Session": "回合", "Notes": "備註",
            "Leave": "離開", "Later": "稍後", "Live": "即時",
            "Scoring": "得分", "Leaders": "排行榜", "Summary": "總結",
        },
        "it": {
            "Player": "Giocatore", "Team": "Squadra", "Match": "Partita", "Game": "Partita",
            "Score": "Punteggio", "Season": "Stagione", "Stats": "Statistiche",
            "Lineup": "Formazione", "Formation": "Formazione", "Bench": "Panchina",
            "Home": "Casa", "Away": "Trasferta", "Win": "Vittoria", "Loss": "Sconfitta",
            "Goal": "Gol", "Assist": "Assist", "Shot": "Tiro", "Penalty": "Penalità",
            "Substitution": "Sostituzione", "Record": "Registro", "History": "Cronologia",
            "Export": "Esporta", "Share": "Condividi", "Print": "Stampa",
            "Ejection": "Espulsione", "Ejected": "Espulso",
            "Recording": "Registrazione", "Session": "Sessione", "Notes": "Note",
            "Leave": "Lascia", "Later": "Dopo", "Live": "In diretta",
            "Scoring": "Punteggio", "Leaders": "Migliori", "Summary": "Riepilogo",
        },
        "ru": {
            "Player": "Игрок", "Team": "Команда", "Match": "Матч", "Game": "Игра",
            "Score": "Счёт", "Season": "Сезон", "Stats": "Статистика",
            "Lineup": "Состав", "Formation": "Расстановка", "Bench": "Запас",
            "Home": "Дома", "Away": "Гости", "Win": "Победа", "Loss": "Поражение",
            "Goal": "Гол", "Assist": "Передача", "Shot": "Бросок", "Penalty": "Штраф",
            "Substitution": "Замена", "Record": "Запись", "History": "История",
            "Export": "Экспорт", "Share": "Поделиться", "Print": "Печать",
            "Ejection": "Удаление", "Ejected": "Удалён",
            "Recording": "Запись", "Session": "Сессия", "Notes": "Заметки",
            "Leave": "Покинуть", "Later": "Позже", "Live": "Вживую",
            "Scoring": "Счёт", "Leaders": "Лидеры", "Summary": "Итоги",
        },
        "sv": {
            "Player": "Spelare", "Team": "Lag", "Match": "Match", "Game": "Spel",
            "Score": "Resultat", "Season": "Säsong", "Stats": "Statistik",
            "Lineup": "Uppställning", "Formation": "Formation", "Bench": "Bänk",
            "Home": "Hemma", "Away": "Borta", "Win": "Vinst", "Loss": "Förlust",
            "Goal": "Mål", "Assist": "Assist", "Shot": "Skott", "Penalty": "Utvisning",
            "Substitution": "Byte", "Record": "Registrering", "History": "Historik",
            "Export": "Exportera", "Share": "Dela", "Print": "Skriv ut",
            "Ejection": "Utvisning", "Ejected": "Utvisad",
            "Recording": "Inspelning", "Session": "Session", "Notes": "Anteckningar",
            "Leave": "Lämna", "Later": "Senare", "Live": "Live",
        },
        "fi": {
            "Player": "Pelaaja", "Team": "Joukkue", "Match": "Ottelu", "Game": "Peli",
            "Score": "Tulos", "Season": "Kausi", "Stats": "Tilastot",
            "Lineup": "Kokoonpano", "Formation": "Muodostelma", "Bench": "Vaihto",
            "Home": "Koti", "Away": "Vieras", "Win": "Voitto", "Loss": "Tappio",
            "Goal": "Maali", "Assist": "Syöttö", "Shot": "Laukaus", "Penalty": "Jäähy",
            "Substitution": "Vaihto", "Record": "Tallenne", "History": "Historia",
            "Export": "Vie", "Share": "Jaa", "Print": "Tulosta",
            "Ejection": "Ulosajo", "Ejected": "Ajettu ulos",
        },
        "cs": {
            "Player": "Hráč", "Team": "Tým", "Match": "Zápas", "Game": "Hra",
            "Score": "Skóre", "Season": "Sezóna", "Stats": "Statistiky",
            "Lineup": "Sestava", "Formation": "Formace", "Bench": "Lavička",
            "Home": "Domácí", "Away": "Hosté", "Win": "Výhra", "Loss": "Prohra",
            "Goal": "Gól", "Assist": "Asistence", "Shot": "Střela", "Penalty": "Trest",
            "Substitution": "Střídání", "Record": "Záznam", "History": "Historie",
            "Export": "Exportovat", "Share": "Sdílet", "Print": "Tisk",
            "Ejection": "Vyloučení", "Ejected": "Vyloučen",
        },
        "pt": {
            "Player": "Jogador", "Team": "Equipa", "Match": "Jogo", "Game": "Jogo",
            "Score": "Resultado", "Season": "Temporada", "Stats": "Estatísticas",
            "Lineup": "Escalação", "Formation": "Formação", "Bench": "Suplentes",
            "Home": "Casa", "Away": "Fora", "Win": "Vitória", "Loss": "Derrota",
            "Goal": "Golo", "Assist": "Assistência", "Shot": "Remate", "Penalty": "Penálti",
            "Substitution": "Substituição", "Record": "Registo", "History": "Histórico",
            "Export": "Exportar", "Share": "Partilhar", "Print": "Imprimir",
            "Ejection": "Expulsão", "Ejected": "Expulso",
        },
        "pl": {
            "Player": "Gracz", "Team": "Drużyna", "Match": "Mecz", "Game": "Gra",
            "Score": "Wynik", "Season": "Sezon", "Stats": "Statystyki",
            "Lineup": "Skład", "Formation": "Ustawienie", "Bench": "Ławka",
            "Home": "Dom", "Away": "Wyjazd", "Win": "Wygrana", "Loss": "Przegrana",
            "Goal": "Gol", "Assist": "Asysta", "Shot": "Strzał", "Penalty": "Kara",
            "Substitution": "Zmiana", "Record": "Zapis", "History": "Historia",
            "Export": "Eksportuj", "Share": "Udostępnij", "Print": "Drukuj",
            "Ejection": "Wykluczenie", "Ejected": "Wykluczony",
        },
        "tr": {
            "Player": "Oyuncu", "Team": "Takım", "Match": "Maç", "Game": "Oyun",
            "Score": "Skor", "Season": "Sezon", "Stats": "İstatistikler",
            "Lineup": "Kadro", "Formation": "Diziliş", "Bench": "Yedek",
            "Home": "Ev sahibi", "Away": "Deplasman", "Win": "Galibiyet", "Loss": "Mağlubiyet",
            "Goal": "Gol", "Assist": "Asist", "Shot": "Şut", "Penalty": "Ceza",
            "Substitution": "Oyuncu değişikliği", "Record": "Kayıt", "History": "Geçmiş",
            "Export": "Dışa aktar", "Share": "Paylaş", "Print": "Yazdır",
            "Ejection": "İhraç", "Ejected": "İhraç edildi",
        },
        "hi": {
            "Player": "खिलाड़ी", "Team": "टीम", "Match": "मैच", "Game": "खेल",
            "Score": "स्कोर", "Season": "सीज़न", "Stats": "आंकड़े",
            "Lineup": "लाइनअप", "Formation": "फॉर्मेशन", "Bench": "बेंच",
            "Home": "होम", "Away": "अवे", "Win": "जीत", "Loss": "हार",
            "Goal": "गोल", "Assist": "असिस्ट", "Shot": "शॉट", "Penalty": "पेनल्टी",
            "Substitution": "बदलाव", "Record": "रिकॉर्ड", "History": "इतिहास",
            "Export": "निर्यात", "Share": "साझा करें", "Print": "प्रिंट",
            "Ejection": "निकालना", "Ejected": "निकाला गया",
        },
        "bn": {
            "Player": "খেলোয়াড়", "Team": "দল", "Match": "ম্যাচ", "Game": "খেলা",
            "Score": "স্কোর", "Season": "সিজন", "Stats": "পরিসংখ্যান",
            "Lineup": "লাইনআপ", "Formation": "ফর্মেশন", "Bench": "বেঞ্চ",
            "Home": "হোম", "Away": "অ্যাওয়ে", "Win": "জয়", "Loss": "হার",
            "Goal": "গোল", "Assist": "অ্যাসিস্ট", "Shot": "শট", "Penalty": "পেনাল্টি",
            "Substitution": "পরিবর্তন", "Record": "রেকর্ড", "History": "ইতিহাস",
            "Export": "রপ্তানি", "Share": "শেয়ার", "Print": "প্রিন্ট",
        },
        "ur": {
            "Player": "کھلاڑی", "Team": "ٹیم", "Match": "میچ", "Game": "کھیل",
            "Score": "سکور", "Season": "سیزن", "Stats": "اعداد و شمار",
            "Lineup": "لائن اپ", "Formation": "فارمیشن", "Bench": "بینچ",
            "Home": "ہوم", "Away": "اوے", "Win": "جیت", "Loss": "ہار",
            "Goal": "گول", "Assist": "اسسٹ", "Shot": "شاٹ", "Penalty": "پینلٹی",
            "Substitution": "تبدیلی", "Record": "ریکارڈ", "History": "تاریخ",
            "Export": "برآمد", "Share": "شیئر", "Print": "پرنٹ",
        },
    }

    # Try to translate using word-level matching
    wmap = word_map.get(lang, {})
    if not wmap:
        return en_value  # No word map for this language, keep EN

    # Try exact phrase match first
    for en_word, translated in sorted(wmap.items(), key=lambda x: -len(x[0])):
        if en_value.lower() == en_word.lower():
            return translated

    # Try if the EN value contains a known word
    result = en_value
    for en_word, translated in sorted(wmap.items(), key=lambda x: -len(x[0])):
        if en_word.lower() in en_value.lower():
            result = en_value.replace(en_word, translated)
            if result != en_value:
                return result

    # Fallback: return EN value as-is
    return en_value


def fill_missing_translations(app_dir):
    l10n_dir = os.path.join(BASE, app_dir, "lib", "core", "l10n")
    en_file = os.path.join(l10n_dir, "strings_en.dart")
    if not os.path.exists(en_file):
        return 0

    en_dict = parse_dart_strings(en_file)
    total_added = 0

    for fname in sorted(os.listdir(l10n_dir)):
        if not fname.startswith("strings_") or fname == "strings_en.dart":
            continue
        lang = fname.replace("strings_", "").replace(".dart", "")
        fpath = os.path.join(l10n_dir, fname)

        lang_dict = parse_dart_strings(fpath)
        missing_keys = set(en_dict.keys()) - set(lang_dict.keys())

        if not missing_keys:
            continue

        # Generate missing translations
        additions = []
        for key in sorted(missing_keys):
            en_val = en_dict[key]
            translated = translate_value(en_val, lang)
            # Escape single quotes in value
            translated = translated.replace("'", "\\'")
            additions.append(f"  '{key}': '{translated}',")

        # Insert before the closing '};'
        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        # Find the last '};\n' or '};'
        insert_point = content.rfind("};")
        if insert_point < 0:
            print(f"  WARN: Could not find '}}; ' in {fname}")
            continue

        new_section = f"\n  // --- Auto-filled translations ({len(additions)} keys) ---\n"
        new_section += "\n".join(additions) + "\n"

        new_content = content[:insert_point] + new_section + content[insert_point:]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

        total_added += len(additions)
        print(f"  {lang}: +{len(additions)} keys")

    return total_added


def main():
    grand_total = 0
    for app_dir in APPS:
        sport = app_dir.replace("coachboard-", "").replace("coachboard", "soccer")
        print(f"=== {sport} ===")
        added = fill_missing_translations(app_dir)
        grand_total += added
        if added == 0:
            print("  All up to date!")
    print(f"\nTotal translations added: {grand_total}")


if __name__ == "__main__":
    main()
