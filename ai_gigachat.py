import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

class GigaChatAuthError(Exception):
    pass


class GigaChatRequestError(Exception):
    pass


def connect_gigachat() -> str:
    """
    Подключение к API: получаем access_token.
    Ожидаем переменные окружения:
      - GIGACHAT_CLIENT_ID

      - GIGACHAT_CLIENT_SECRET

    Возвращает строку access_token.
    """
    client_id = os.getenv("GIGACHAT_CLIENT_ID")
    client_secret = os.getenv("GIGACHAT_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise GigaChatAuthError(
            "Не заданы переменные окружения GIGACHAT_CLIENT_ID / GIGACHAT_CLIENT_SECRET"
        )

    # Базовая авторизация: base64(client_id:client_secret)
    basic = client_secret

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Authorization": f"Basic {basic}",
        "RqUID": str(uuid.uuid4()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = {"scope": "GIGACHAT_API_PERS"}

    resp = requests.post(url, headers=headers, data=data, timeout=30, verify=False)
    if resp.status_code != 200:
        raise GigaChatAuthError(f"Ошибка авторизации: {resp.status_code} {resp.text}")


    payload = resp.json()
    token = payload.get("access_token")
    if not token:
        raise GigaChatAuthError(f"Не найден access_token в ответе: {payload}")

    return token



def ask_gigachat(text: str, *, system_prompt: str = "Ты полезный ассистент.") -> str:
    """
    Отправляет текст в модель и возвращает ответ.
    """
    token = connect_gigachat()

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",

        "Accept": "application/json",
    }

    body = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0.4,
    }

    resp = requests.post(url, headers=headers, json=body, timeout=60, verify=False)
    if resp.status_code != 200:
        raise GigaChatRequestError(f"Ошибка запроса: {resp.status_code} {resp.text}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise GigaChatRequestError(f"Неожиданная структура ответа: {data}") from e



if __name__ == "__main__":
    prompt = "Сделай очень краткое саммари: LLM помогают автоматизировать интеллектуальные задачи."
    print(ask_gigachat(prompt))
