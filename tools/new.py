#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
new.py — создать каркас задач Project Euler под структуру с «корзинами».

Что умеет:
  - Создаёт корзину 001-100, 101-200, ...
  - Создаёт каталог задачи pNNN с нулевым паддингом (настраивается PROBLEM_PAD).
  - Кладёт шаблон solution.<ext> под выбранный язык (--lang).
  - Принимает диапазоны и списки номеров: '42' | '1,2,3' | '10-15' | '1-3,7,10-12'.
  - По умолчанию запускает tools/update.py, можно отключить --no-update.
  - Можно перезаписать файл решения флагом --force.

Примеры:
  python tools/new.py 42
  python tools/new.py 1-10,13,27
  python tools/new.py 137 --lang=cpp
  python tools/new.py 200 --no-update
  python tools/new.py 7 --lang=py --force
"""

from __future__ import annotations
import argparse
import os
import re
import subprocess
from pathlib import Path

# === Конфиг (держим в унисон с update.py) ===
ROOT = Path(__file__).resolve().parents[1]
BUCKET_SIZE = int(os.getenv("BUCKET_SIZE", "100"))
PROBLEM_PAD = int(os.getenv("PROBLEM_PAD", "3"))  # поставь 4 → p0001

# Шаблоны файлов решения под разные языки
TEMPLATES = {
    "py": (
        "solution.py",
        """def solve():
    # TODO: write solution
    return None

if __name__ == "__main__":
    print(solve())
"""
    ),
    "cpp": (
        "solution.cpp",
        r"""#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // TODO: write solution
    return 0;
}
"""
    ),
    "rs": (
        "solution.rs",
        """fn main() {
    // TODO: write solution
}
"""
    ),
    "js": (
        "solution.js",
        """function solve() {
  // TODO: write solution
  return null;
}
console.log(solve());
"""
    ),
    "ts": (
        "solution.ts",
        """function solve(): unknown {
  // TODO: write solution
  return null;
}
console.log(solve());
"""
    ),
    "go": (
        "solution.go",
        """package main
import "fmt"
func main() {
    // TODO: write solution
    fmt.Println()
}
"""
    ),
    "java": (
        "Solution.java",
        """public class Solution {
    public static void main(String[] args) {
        // TODO: write solution
    }
}
"""
    ),
}

# === Утилиты именования ===

def bucket_name(n: int) -> str:
    start = ((n - 1) // BUCKET_SIZE) * BUCKET_SIZE + 1
    end = start + BUCKET_SIZE - 1
    return f"{start:03d}-{end:03d}"

def prob_dir_name(n: int) -> str:
    return f"p{n:0{PROBLEM_PAD}d}"

# === Парсинг спецификации номеров ===

_NUM_TOKEN = re.compile(r"^\d+$")
_RANGE_TOKEN = re.compile(r"^(\d+)\s*[-–]\s*(\d+)$")

def parse_numbers(spec: str) -> list[int]:
    """
    Поддерживает:
      '42' | '1,2,3' | '10-15' | '1-3,7,10-12'
    Возвращает уникальные отсортированные номера.
    """
    nums: list[int] = []
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if _NUM_TOKEN.fullmatch(token):
            nums.append(int(token))
            continue
        m = _RANGE_TOKEN.fullmatch(token)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a > b:
                a, b = b, a
            nums.extend(range(a, b + 1))
            continue
        raise SystemExit(f"[error] не могу распарсить '{token}' (ожидал число или диапазон)")
    # валидируем и чистим
    uniq = sorted(set(n for n in nums if n >= 1))
    if not uniq:
        raise SystemExit("[error] пустой набор номеров или все < 1")
    return uniq

# === Основная логика ===

def make_problem(n: int, lang: str, force: bool) -> Path:
    if lang not in TEMPLATES:
        raise SystemExit(f"[error] неизвестный --lang '{lang}'. Доступно: {', '.join(TEMPLATES)}")

    bname = bucket_name(n)
    pname = prob_dir_name(n)
    pdir = ROOT / bname / pname
    pdir.mkdir(parents=True, exist_ok=True)

    fname, content = TEMPLATES[lang]
    fpath = pdir / fname

    if fpath.exists() and not force:
        print(f"[skip] {fpath.relative_to(ROOT)} уже существует (используй --force для перезаписи)")
    else:
        # если перезаписываем — просто пишем заново
        fpath.write_text(content, encoding="utf-8")
        print(f"[ok]  {fpath.relative_to(ROOT)}")

    return pdir

def run_update():
    """Запуск tools/update.py без падения, если его нет/сломался."""
    upd = ROOT / "tools" / "update.py"
    if not upd.exists():
        print("[warn] tools/update.py не найден — пропускаю обновление README")
        return
    try:
        subprocess.run(["python", str(upd)], check=False)
    except Exception as e:
        print(f"[warn] не удалось запустить update.py: {e}")

def main():
    ap = argparse.ArgumentParser(description="Создать каркас задач Project Euler")
    ap.add_argument("numbers", help="номера задач: '42' | '1,2,3' | '10-15' | '1-3,7,10-12'")
    ap.add_argument("--lang", default="py", help=f"язык шаблона ({', '.join(TEMPLATES.keys())}), по умолчанию py")
    ap.add_argument("--no-update", action="store_true", help="не запускать tools/update.py после генерации")
    ap.add_argument("--force", action="store_true", help="перезаписать файл решения, если он уже есть")
    args = ap.parse_args()

    nums = parse_numbers(args.numbers)
    for n in nums:
        make_problem(n, lang=args.lang, force=args.force)

    if not args.no_update:
        run_update()

if __name__ == "__main__":
    main()
