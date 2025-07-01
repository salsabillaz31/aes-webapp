import re
#from utils.preprocessing import text_preprocessing

def normalize_text(text):
    """
    Normalisasi teks:
    - Lowercase
    - Hilangkan tanda baca
    - Gabungkan spasi ganda jadi satu
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # hapus semua tanda baca
    text = re.sub(r'\s+', ' ', text)     # spasi ganda → satu spasi
    return text.strip()

def keyword_matching_score(answer, keywords, mode="strict"):
    if not answer or not keywords:
        return 0, []

    matched_keywords = []

    # Normalisasi jawaban
    answer_norm = normalize_text(answer)

    if mode == "strict":
        for kw in keywords:
            kw_norm = normalize_text(kw)
            if kw_norm in answer_norm:
                matched_keywords.append(kw)

    elif mode == "loose":
        answer_words = set(answer_norm.split())
        for kw in keywords:
            kw_words = set(normalize_text(kw).split())
            if kw_words & answer_words:
                matched_keywords.append(kw)

    matched_count = len(matched_keywords)
    total_keywords = len(keywords)

    if total_keywords == 0:
        return 0, []

    match_ratio = matched_count / total_keywords

    if match_ratio == 1.0:
        return 5, matched_keywords
    elif match_ratio >= 0.75:
        return 4, matched_keywords
    elif match_ratio >= 0.5:
        return 3, matched_keywords
    elif match_ratio >= 0.3:
        return 2, matched_keywords
    elif match_ratio > 0:
        return 1, matched_keywords
    else:
        return 0, matched_keywords



