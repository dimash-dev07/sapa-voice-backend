"""
Голостық роботтың жеңілдетілген логикасы.
Нақты Sapa-да бұл жерде ASR/NLU/CRM интеграциясы болады,
біз MVP-де ережеге негізделген жауап қайтарамыз.
"""
import re


INTENT_RULES: list[tuple[str, str]] = [
    (r"\b(баға|price|сколько стоит|қанша)\b", "Бағамыз туралы ақпаратты менеджер жібереді."),
    (r"\b(сағат|уақыт|time|график)\b", "Біздің жұмыс уақыты: Дс-Жм, 09:00–18:00."),
    (r"\b(мекенжай|адрес|address)\b", "Мекенжайымыз: Алматы, Абай даңғылы 10."),
]


def generate_response(text: str) -> str:
    lowered = text.lower()
    for pattern, answer in INTENT_RULES:
        if re.search(pattern, lowered):
            return answer
    return "Сұранысыңыз қабылданды, менеджер жақын арада хабарласады."