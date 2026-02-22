from __future__ import annotations

from ai_gigachat import connect_gigachat
from article import article_to_text, NotAvailable

import requests


class Summarizer:
    def __init__(self) -> None:
        self._token = connect_gigachat()

    def __article_to_text(self, link: str) -> str:
        """
        Загружает текст статьи и возвращает не более 3000 символов.
        """
        text = article_to_text(link)
        return text[:3000]

    def __send_gigachat(self, text: str) -> str:
        """
        Отправляет текст в Гигачат и возвращает ответ модели.
        """
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        prompt = (
            "Сделай краткое содержание научной статьи и переведи саммари на русский язык.\n"
            "Требования:\n"
            "1) 7–12 буллетов.\n"
            "2) Отдельно строкой: 'Ключевые идеи:' и 3–6 пунктов.\n"
            "3) Без выдуманных фактов. Если данных не хватает — так и скажи.\n"
        )

        body = {
            "model": "GigaChat",
            "messages": [
                {"role": "system", "content": "Ты аккуратный научный редактор."},
                {"role": "user", "content": f"{prompt}\n\nТекст статьи:\n{text}"},
            ],
            "temperature": 0.3,
        }

        resp = requests.post(url, headers=headers, json=body, timeout=90, verify=False)
        if resp.status_code != 200:
            raise RuntimeError(f"Ошибка запроса к модели: {resp.status_code} {resp.text}")

        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def summarize(self, link: str) -> str:
        """
        Публичный метод: получает ссылку, грузит текст и возвращает саммари.
        """
        try:
            text = self.__article_to_text(link)
        except NotAvailable as e:
            return f"Ошибка: {e}"

        return self.__send_gigachat(text)


if __name__ == "__main__":
    s = Summarizer()
    print(s.summarize("https://arxiv.org/pdf/1804.08875"))

