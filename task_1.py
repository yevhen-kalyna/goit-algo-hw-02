"""Завдання 1. Імітація системи обробки заявок у сервісному центрі.

Використовується клас Queue з модуля queue (FIFO).
Структура коду відповідає псевдокоду з умови ДЗ.
"""

from __future__ import annotations

import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
from queue import Queue

# ---- Модель заявки -----------------------------------------------------------

_id_counter = count(1)
_CUSTOMERS = (
    "Олена", "Іван", "Марія", "Петро", "Анна",
    "Дмитро", "Софія", "Юрій", "Катерина", "Андрій",
)


@dataclass
class Request:
    """Заявка з унікальним ідентифікатором та метаданими."""

    id: int
    customer: str
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return (
            f"Заявка #{self.id:04d} | клієнт: {self.customer:<10} "
            f"| створена: {self.created_at:%H:%M:%S}"
        )


# ---- Основні функції (за псевдокодом) ----------------------------------------

def generate_request(q: Queue[Request]) -> Request:
    """Створює нову заявку та додає її до черги."""
    req = Request(id=next(_id_counter), customer=random.choice(_CUSTOMERS))
    q.put(req)
    print(f"  [+] Додано до черги:  {req}")
    return req


def process_request(q: Queue[Request]) -> Request | None:
    """Видаляє заявку з черги та "обробляє" її. Повертає None, якщо черга порожня."""
    if q.empty():
        print("  [!] Черга порожня — немає заявок для обробки")
        return None
    req = q.get()
    print(f"  [✓] Оброблено заявку: {req}")
    return req


# ---- Режими роботи -----------------------------------------------------------

def run_interactive(q: Queue[Request]) -> None:
    """Інтерактивне меню — користувач сам вирішує, коли генерувати чи обробляти."""
    actions = {
        "1": "Створити нову заявку",
        "2": "Обробити заявку з черги",
        "3": "Показати розмір черги",
        "0": "Вийти",
    }
    while True:
        print("\n=== Сервісний центр ===")
        for key, label in actions.items():
            print(f"  {key}. {label}")
        choice = input("Оберіть дію: ").strip()

        if choice == "0":
            print("Завершення роботи. До побачення!")
            break
        elif choice == "1":
            generate_request(q)
        elif choice == "2":
            process_request(q)
        elif choice == "3":
            print(f"  [i] У черзі зараз: {q.qsize()} заявок")
        else:
            print("  [!] Невідома команда")


def run_auto(q: Queue[Request], iterations: int = 15, delay: float = 0.4) -> None:
    """Автоматичний режим — імітує безперервний потік заявок та їх обробку.

    Імовірність генерації навмисне вища за обробку (60% / 40%), щоб черга
    природно росла та було видно, що FIFO працює коректно.
    """
    print(f"=== Авто-режим: {iterations} ітерацій, затримка {delay}s ===\n")
    for i in range(1, iterations + 1):
        print(f"-- Ітерація {i}/{iterations} --")
        if random.random() < 0.6 or q.empty():
            generate_request(q)
        else:
            process_request(q)
        time.sleep(delay)

    print(f"\n[i] Залишилось у черзі: {q.qsize()}. Дообробляю всі заявки...")
    while not q.empty():
        process_request(q)
        time.sleep(delay / 2)


# ---- Точка входу -------------------------------------------------------------

def main() -> None:
    q: Queue[Request] = Queue()

    # Підтримуємо обидва режими: запуск з прапорцем `--auto` або без нього.
    if len(sys.argv) > 1 and sys.argv[1] in ("--auto", "-a"):
        run_auto(q)
    else:
        run_interactive(q)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПерервано користувачем.")
        sys.exit(0)
