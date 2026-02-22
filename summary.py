import sys
from summarizer import Summarizer


def main() -> int:
    if len(sys.argv) < 2:
        print("Ошибка: передай ссылку на статью.")
        print("Пример: python summary.py https://arxiv.org/pdf/1804.08875")

        return 1

    link = sys.argv[1]

    try:
        s = Summarizer()
        result = s.summarize(link)
        print(result)
        return 0

    except Exception as e:
        print(f"Ошибка: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
