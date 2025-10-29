#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Апдейтер репозитория с решениями Project Euler c «корзинами» по 100 задач.

Что делает:
  1) Рекурсивно ищет папки задач вида p{N} (где N — число) в любом месте.
  2) Считает задачу решенной, если внутри есть solution.* или main.* (конфигурируемо).
  3) Проверяет, что каждая задача лежит в правильной «корзине»:
       001-100, 101-200, 201-300, ...
     Если нет — ПЕРЕНОСИТ (git позже увидит mv).
  4) Создает pN/README.md, если его ещё нет.
     По умолчанию ТЕКСТ УСЛОВИЙ НЕ ПУБЛИКУЕТСЯ (только ссылка).
     Включить публикацию можно env-переменной PUBLISH_STATEMENTS=true.
  5) Пересобирает корневой README.md: прогресс, прогресс-бар, секции по корзинам.
  6) Определяет «сколько всего задач» через /archives на projecteuler.net (с ретраями).
     Если сайт не доступен — fallback: максимум из решённых.

Зависимости: requests, beautifulsoup4, lxml, html2text
"""

from __future__ import annotations
import os
import re
import time
import shutil
import math
from pathlib import Path
from typing import Optional, Iterable, Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
from html2text import HTML2Text

# === Конфиг ===

ROOT = Path(__file__).resolve().parents[1]
BUCKET_SIZE = 100  # размер корзины
# Какие имена файлов считаем «есть решение»
SOLUTION_FILENAMES = {
    "solution.py", "main.py", "solution.ipynb",
    "solution.cpp", "solution.cc", "solution.cxx",
    "solution.rs", "solution.java", "solution.js", "solution.ts",
    "solution.go", "solution.rb", "solution.cs",
}
# и/или любой файл, начинающийся на "solution." (например, solution.kt)
SOLUTION_PREFIX = "solution."

# Публиковать ли текст условий (по умолчанию НЕТ, чтобы не светить контент публично).
PUBLISH_STATEMENTS = os.getenv("PUBLISH_STATEMENTS", "false").lower() in {"1", "true", "yes", "on"}

# Параметры скачивания
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "25"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "4"))
BASE_SLEEP = float(os.getenv("BASE_SLEEP", "1.2"))

session = requests.Session()
session.headers.update({
    "User-Agent": "PE-Repo-Updater (+github-actions)"
})

# === Утилиты ===

def bucket_name(n: int) -> str:
    """Возвращает имя корзины для задачи n: '001-100', '101-200', ..."""
    if n < 1:
        raise ValueError("problem number must be >= 1")
    start = ((n - 1) // BUCKET_SIZE) * BUCKET_SIZE + 1
    end = start + BUCKET_SIZE - 1
    return f"{start:03d}-{end:03d}"

_PROB_DIR_RE = re.compile(r"^p(\d+)$")

def is_problem_dir(path: Path) -> Optional[int]:
    """Если каталог называется p{N}, вернуть N иначе None."""
    m = _PROB_DIR_RE.fullmatch(path.name)
    if not m:
        return None
    return int(m.group(1))

def has_solution_files(dir_path: Path) -> bool:
    """Есть ли в каталоге файлы, которые считаем решением."""
    for p in dir_path.iterdir():
        if not p.is_file():
            continue
        name = p.name
        if name in SOLUTION_FILENAMES or name.startswith(SOLUTION_PREFIX):
            return True
    return False

def http_get(url: str) -> requests.Response:
    """GET с повторами и экспоненциальной задержкой."""
    last_exc = None
    for i in range(MAX_RETRIES):
        try:
            r = session.get(url, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                return r
        except requests.RequestException as e:
            last_exc = e
        time.sleep(BASE_SLEEP ** i)
    if last_exc:
        raise last_exc
    raise RuntimeError(f"GET failed: {url}")

def html_to_md(elem) -> str:
    """Грубая конвертация HTML -> Markdown (без жёстких переносов строк)."""
    if elem is None:
        return ""
    h = HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_emphasis = False
    return h.handle(str(elem)).strip()

def fetch_problem_md(n: int) -> tuple[str, str]:
    """Возвращает (markdown, title) задачи n, вытягивая со страницы задачи."""
    url = f"https://projecteuler.net/problem={n}"
    r = http_get(url)
    soup = BeautifulSoup(r.text, "lxml")

    # Заголовок задачи
    title_node = soup.select_one("h2")
    title_text = title_node.get_text(" ", strip=True) if title_node else f"Problem {n}"

    # Контент
    content = soup.select_one("#problem_content") or soup.select_one(".problem_content")
    md_body = html_to_md(content) or "_(content not parsed)_"

    md = f"# {title_text}\n\n" \
         f"Source: {url}\n\n" \
         f"{md_body}\n"
    return md, title_text

def ensure_problem_readme(n: int, prob_dir: Path) -> str:
    """Создаёт pN/README.md если отсутствует. Возвращает title."""
    readme = prob_dir / "README.md"
    if readme.exists():
        # вытащим title из первой строки
        try:
            first = readme.read_text(encoding="utf-8", errors="ignore").splitlines()[:1]
            return first[0].lstrip("# ").strip() if first else f"Problem {n}"
        except Exception:
            return f"Problem {n}"

    if not PUBLISH_STATEMENTS:
        md = f"# Problem {n}\n\n" \
             f"Source: https://projecteuler.net/problem={n}\n\n" \
             f"> Statement is not stored in this repo (policy).\n"
        readme.write_text(md, encoding="utf-8")
        return f"Problem {n}"

    try:
        md, title = fetch_problem_md(n)
    except Exception as e:
        md = (f"# Problem {n}\n\n"
              f"Source: https://projecteuler.net/problem={n}\n\n"
              f"> Failed to fetch/parse statement: `{e}`\n")
        title = f"Problem {n}"
    readme.write_text(md, encoding="utf-8")
    return title

def fetch_total_problems() -> Optional[int]:
    """
    Пытается определить общее число задач через страницу архива.
    Стратегия: найти номер последней страницы и взять макс problem=ID.
    """
    try:
        r = http_get("https://projecteuler.net/archives")
        soup = BeautifulSoup(r.text, "lxml")
        pages = {1}
        for a in soup.select('a[href*="archives"]'):
            href = a.get("href", "")
            m = re.search(r"[?;]page=(\d+)", href)
            if m:
                pages.add(int(m.group(1)))
        last = max(pages)

        r2 = http_get(f"https://projecteuler.net/archives?page={last}")
        soup2 = BeautifulSoup(r2.text, "lxml")
        ids = []
        for a in soup2.select('a[href*="problem="]'):
            m = re.search(r"problem=(\d+)", a.get("href", ""))
            if m:
                ids.append(int(m.group(1)))
        return max(ids) if ids else None
    except Exception:
        return None

def progress_bar(solved: int, total: int, width: int = 30) -> str:
    pct = (solved / total) if total else 0.0
    filled = int(round(width * pct))
    return "█" * filled + "░" * (width - filled)

def write_root_readme(solved_map: Dict[int, Path], titles: Dict[int, str], total: Optional[int]):
    """Генерирует корневой README с секциями по корзинам."""
    solved_nums = sorted(solved_map.keys())
    if not solved_nums:
        total = total or 0
        text = (
            "# Project Euler — my solutions\n\n"
            "No solved problems yet.\n"
        )
        (ROOT / "README.md").write_text(text, encoding="utf-8")
        return

    # Группировка по корзинам
    buckets: Dict[str, List[int]] = {}
    for n in solved_nums:
        b = bucket_name(n)
        buckets.setdefault(b, []).append(n)

    total_all = total or max(solved_nums)
    solved_count = len(solved_nums)
    pct = (solved_count / total_all * 100) if total_all else 0.0
    bar = progress_bar(solved_count, total_all, width=30)
    badge = f"![progress](https://img.shields.io/badge/Project%20Euler-{solved_count}%2F{total_all}-blue)"

    lines = []
    lines.append("# Project Euler — my solutions\n")
    lines.append(f"{badge}\n\n")
    lines.append(f"**Progress:** {solved_count}/{total_all} ({pct:.2f}%)  \n")
    lines.append(f"`{bar}`\n\n")

    # Секции по корзинам
    for b in sorted(buckets.keys(), key=lambda s: int(s.split('-')[0])):
        lines.append(f"## {b}\n\n")
        lines.append("| # | title | folder |\n")
        lines.append("|---:|:------|:------|\n")
        for n in buckets[b]:
            prob_dir = solved_map[n]
            rel = prob_dir.relative_to(ROOT).as_posix()
            title = titles.get(n, f"Problem {n}")
            lines.append(f"| {n} | {title} | [{rel}]({rel}/) |\n")
        lines.append("\n")

    (ROOT / "README.md").write_text("".join(lines), encoding="utf-8")

def scan_problems() -> Dict[int, Path]:
    """
    Рекурсивно находит каталоги p{N} с решением.
    Возвращает {N: Path_to_pN}
    """
    found: Dict[int, Path] = {}
    for path in ROOT.rglob("p*"):
        if not path.is_dir():
            continue
        n = is_problem_dir(path)
        if n is None:
            continue
        if has_solution_files(path):
            found[n] = path
    return found

def ensure_in_bucket(n: int, current_dir: Path) -> Path:
    """
    Гарантирует, что p{n} лежит в правильной корзине. При необходимости — переносит.
    Возвращает актуальный путь к p{n}.
    """
    correct_bucket = bucket_name(n)
    parent = current_dir.parent
    if parent.name == correct_bucket:
        return current_dir

    # перенос
    target_parent = ROOT / correct_bucket
    target_parent.mkdir(parents=True, exist_ok=True)
    target_dir = target_parent / current_dir.name

    if target_dir.exists() and target_dir.resolve() == current_dir.resolve():
        return current_dir

    if target_dir.exists():
        # если уже есть каталог назначения — аккуратно смержим содержимое
        for item in current_dir.iterdir():
            dst = target_dir / item.name
            if dst.exists():
                # не перезаписываем — оставляем как есть
                continue
            if item.is_dir():
                shutil.copytree(item, dst)
            else:
                shutil.copy2(item, dst)
        # удаляем исходник
        shutil.rmtree(current_dir)
        return target_dir

    shutil.move(str(current_dir), str(target_dir))
    return target_dir

def main():
    # 1) найти решённые
    solved = scan_problems()  # {n: path_to_pN}

    # 2) убедиться, что все в правильных корзинах (и создать корзины)
    normalized: Dict[int, Path] = {}
    for n, p in sorted(solved.items()):
        new_path = ensure_in_bucket(n, p)
        normalized[n] = new_path

    # 3) подготовить README для задач (если нет)
    titles: Dict[int, str] = {}
    for n, p in sorted(normalized.items()):
        titles[n] = ensure_problem_readme(n, p)

    # 4) сколько всего задач?
    total = fetch_total_problems()

    # 5) пересобрать корневой README
    write_root_readme(normalized, titles, total)

if __name__ == "__main__":
    main()
