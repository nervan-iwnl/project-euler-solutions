#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Создаёт каркас для новой задачи:
  bucket/pN/solution.py (если нет)
и запускает tools/update.py, чтобы подтянуть README и обновить корневой прогресс.

Пример:
  python tools/new.py 42
"""

from __future__ import annotations
import sys
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BUCKET_SIZE = 100

def bucket_name(n: int) -> str:
    start = ((n - 1) // BUCKET_SIZE) * BUCKET_SIZE + 1
    end = start + BUCKET_SIZE - 1
    return f"{start:03d}-{end:03d}"

TEMPLATE = """def solve():
    # write your solution here
    return None

if __name__ == "__main__":
    print(solve())
"""

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python tools/new.py <problem_number>")
        sys.exit(2)
    n = int(sys.argv[1])
    if n < 1:
        print("problem number must be >= 1")
        sys.exit(2)

    b = bucket_name(n)
    prob_dir = ROOT / b / f"p{n}"
    prob_dir.mkdir(parents=True, exist_ok=True)

    sol = prob_dir / "solution.py"
    if not sol.exists():
        sol.write_text(TEMPLATE, encoding="utf-8")
        print(f"[ok] created {sol}")
    else:
        print(f"[skip] {sol} already exists")

    subprocess.run([sys.executable, str(ROOT / "tools" / "update.py")], check=False)

if __name__ == "__main__":
    main()
