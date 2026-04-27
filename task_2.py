"""Завдання 2. Перевірка рядка на паліндром через двосторонню чергу (deque).

Алгоритм:
  1. Нормалізуємо рядок: до нижнього регістру, без пробільних символів.
  2. Складаємо всі символи у deque.
  3. Поки в deque більше одного символу — порівнюємо крайні (popleft vs pop).
     Перший збіг false → одразу повертаємо False.
  4. Якщо цикл завершився без розбіжностей → True.

Складність: O(n) за часом, O(n) за пам'яттю. Для парної та непарної довжини
працює однаково: непарна — у середині лишається 1 символ (його не порівнюємо).
"""

from __future__ import annotations

from collections import deque


def is_palindrome(text: str) -> bool:
    """Повертає True, якщо `text` є паліндромом.

    Нечутливий до регістру та пробілів (включно з табуляціями та переносами).
    Порожній рядок та рядок із самих пробілів вважаємо НЕ паліндромом
    (немає що порівнювати).
    """
    # Нормалізація: lower + видалення всіх whitespace-символів.
    # `"".join(text.split())` прибирає будь-який whitespace без regex.
    normalized = "".join(text.lower().split())

    if not normalized:
        return False

    dq: deque[str] = deque(normalized)

    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False

    return True


# ---- Демонстрація та інтерактив ---------------------------------------------

def _demo() -> None:
    cases: list[tuple[str, bool]] = [
        ("А роза упала на лапу Азора", True),   # класичний укр. паліндром
        ("Madam", True),                         # непарна довжина
        ("abba", True),                          # парна довжина
        ("Was it a car or a cat I saw", True),   # фраза, регістр + пробіли
        ("racecar", True),
        ("Hello", False),
        ("Ні", False),
        ("А", True),                             # один символ
        ("  ", False),                           # тільки пробіли
        ("", False),                             # порожній
        ("Ніколи не пізно", False),
        ("кок", True),
    ]

    print(f"{'Рядок':<35} {'Очікувано':<12} {'Отримано':<12} {'OK?'}")
    print("-" * 70)
    for text, expected in cases:
        actual = is_palindrome(text)
        status = "✓" if actual == expected else "✗ FAIL"
        display = repr(text) if len(text) < 33 else repr(text[:30]) + "..."
        print(f"{display:<35} {str(expected):<12} {str(actual):<12} {status}")


def _interactive() -> None:
    print("\n=== Інтерактивний режим (введіть 'exit' для виходу) ===")
    while True:
        try:
            text = input("Рядок: ")
        except EOFError:
            print()
            break
        if text.strip().lower() == "exit":
            break
        verdict = "Паліндром ✓" if is_palindrome(text) else "Не паліндром ✗"
        print(f"  → {verdict}")


if __name__ == "__main__":
    print("=== Перевірка паліндромів через collections.deque ===\n")
    _demo()
    _interactive()
