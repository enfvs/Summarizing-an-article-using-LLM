from __future__ import annotations

import re
import requests
from io import BytesIO
from pdfminer.high_level import extract_text


class NotAvailable(Exception):
    pass


def _normalize_arxiv_pdf_link(link: str) -> str:
    """
    Принимает разные варианты ссылок arxiv и приводит к pdf-ссылке.
    Примеры входа:
      - https://arxiv.org/abs/1804.08875
      - https://arxiv.org/pdf/1804.08875
      - https://arxiv.org/pdf/1804.08875.pdf
    """
    link = link.strip()

    # abs -> pdf
    m = re.match(r"^https?://arxiv\.org/abs/([0-9]+\.[0-9]+)", link)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}"

    # pdf с .pdf
    m = re.match(r"^https?://arxiv\.org/pdf/([0-9]+\.[0-9]+)(?:\.pdf)?$", link)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}"

    return link


def article_to_text(link: str) -> str:
    """
    article_to_text(link) -> str
    Скачивает PDF c arxiv.org и возвращает текст статьи одной строкой.
    Если ссылка недоступна — выбрасывает NotAvailable.
    """
    pdf_url = _normalize_arxiv_pdf_link(link)

    try:
        resp = requests.get(pdf_url, timeout=60)
    except requests.RequestException as e:
        raise NotAvailable(f"Ссылка недоступна: {pdf_url}") from e

    if resp.status_code != 200 or not resp.content:
        raise NotAvailable(f"Ссылка недоступна: {pdf_url} (код {resp.status_code})")

    # PDF -> текст
    try:
        text = extract_text(BytesIO(resp.content))
    except Exception as e:
        raise NotAvailable("Не удалось извлечь текст из PDF (возможно, PDF повреждён).") from e

    text = (text or "").strip()
    if not text:
        raise NotAvailable("Текст статьи пустой (возможно, в PDF нет распознаваемого текста).")

    return text


if __name__ == "__main__":
    example = "https://arxiv.org/pdf/1804.08875"
    t = article_to_text(example)
    print(t[:1000])

