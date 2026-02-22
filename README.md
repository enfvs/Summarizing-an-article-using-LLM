# Summarizing an article using LLM

Небольшой Python CLI, который:
1) принимает ссылку на статью с **arXiv**,
2) скачивает PDF,
3) извлекает текст через `pdfminer.six`,
4) отправляет фрагмент текста в **GigaChat API**,
5) возвращает саммари на русском языке (буллеты + ключевые идеи).

> Это учебный проект. Саммари зависит от качества извлеченного текста и ограничений модели.

## Как это работает

- `article.py` приводит ссылки `https://arxiv.org/abs/...` и `https://arxiv.org/pdf/...` к PDF ссылке и вытаскивает текст из PDF.
- `summarizer.py` берет первые **3000 символов** текста и отправляет их в `https://gigachat.devices.sberbank.ru/api/v1/chat/completions`.
- `summary.py` - точка входа (CLI).

Формат ответа, который запрашивается у модели:
- 7-12 буллетов с кратким содержанием
- отдельной строкой: `Ключевые идеи:` и 3-6 пунктов
- без выдуманных фактов (если данных не хватает, модель должна это сказать)

## Требования

- Python 3.10+
- Доступ в интернет (arXiv + GigaChat)
- Учетные данные GigaChat

Python зависимости:
- `requests`
- `python-dotenv`
- `pdfminer.six`

## Установка

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
# .venv\Scripts\activate

pip install -U pip
pip install requests python-dotenv pdfminer.six
```

## Настройка GigaChat

Проект ожидает переменные окружения:
- `GIGACHAT_CLIENT_ID`
- `GIGACHAT_CLIENT_SECRET`

В коде `ai_gigachat.py` значение `GIGACHAT_CLIENT_SECRET` используется напрямую в заголовке `Authorization: Basic ...`.
На практике это означает, что туда удобно класть **уже готовую base64 строку** вида `base64(client_id:client_secret)`.

### Вариант 1: через файл .env

Создай файл `.env` в корне проекта:

```env
GIGACHAT_CLIENT_ID=твой_client_id
GIGACHAT_CLIENT_SECRET=base64_строка_для_Basic
```

Сгенерировать base64:

Linux/macOS:
```bash
echo -n "<client_id>:<client_secret>" | base64
```

Windows PowerShell:
```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("<client_id>:<client_secret>"))
```

### Вариант 2: через переменные окружения

Linux/macOS:
```bash
export GIGACHAT_CLIENT_ID="..."
export GIGACHAT_CLIENT_SECRET="..."
```

Windows (PowerShell):
```powershell
setx GIGACHAT_CLIENT_ID "..."
setx GIGACHAT_CLIENT_SECRET "..."
```

## Запуск

Самый простой способ - через `summary.py`.

```bash
python summary.py https://arxiv.org/abs/1804.08875
# или
python summary.py https://arxiv.org/pdf/1804.08875
# или
python summary.py https://arxiv.org/pdf/1804.08875.pdf
```

Если ссылка недоступна или из PDF не удается извлечь текст, вернется сообщение об ошибке.

## Структура проекта

```
.
├─ ai_gigachat.py     # авторизация и запросы к GigaChat API
├─ article.py         # скачивание PDF с arXiv и извлечение текста
├─ summarizer.py      # бизнес-логика саммаризации
├─ summary.py         # CLI точка входа
├─ test.py            # тестовый запрос авторизации (пример)
├─ README.md
└─ LICENSE
```

## Ограничения и важные заметки

- Берется только первые **3000 символов** текста статьи. Для больших статей это может быть недостаточно.
- `pdfminer.six` извлекает текст не идеально: формулы, таблицы и колонки могут "ломаться".
- В запросах к API используется `verify=False` (отключена проверка SSL сертификатов). Для продакшена это небезопасно. Если будешь развивать проект, лучше включить проверку сертификатов и настроить доверенные CA.
