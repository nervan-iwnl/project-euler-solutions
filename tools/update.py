#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update.py — «апдейтер» репозитория с решениями Project Euler
с иерархией «корзин» (buckets) и нормализацией имён задач.

Зачем нужен:
  - Привести структуру каталога к стабильному виду, который красиво отображается на GitHub:
      001-100/p001/, 001-100/p002/, ..., 101-200/p123/ и т.д.
    (GitHub сортирует ЛЕКСИКОГРАФИЧЕСКИ, поэтому p1, p10, p2 выглядят криво —
     лечится нулевым паддингом p001, p010, p002…).
  - Поддерживать README-файлы:
      * pNNN/README.md — заголовок + (опционально) текст условия или только ссылка.
      * README.md в корне — прогресс, прогресс-бар, списки задач по корзинам.
      * (опционально) README.md внутри каждой корзины с мини-индексом.
  - Аккуратно переносить/переименовывать каталоги задач в правильные «корзины»
    и канонические имена без потери содержимого (git увидит mv/rename).
  - Узнавать «сколько всего задач» на projecteuler.net/archives (с ретраями).

Основные принципы:
  - Имена задач — «канонические»: p{n:0{PROBLEM_PAD}d} (по умолчанию p001).
  - Корзины фиксированного размера (по умолчанию 100): 001-100, 101-200, ...
  - «Решённой» считаем задачу, если внутри pNNN/ найден хоть один файл из набора
    SOLUTION_FILENAMES или любой файл, начинающийся на "solution." (например, solution.kt).
  - Текст условий по умолчанию не публикуется (чтобы не светить контент). Можно включить
    через переменную окружения PUBLISH_STATEMENTS=true (см. workflow).
  - Сети бывают нестабильны → http_get() с ретраями и backoff.

Зависимости (устанавливаются через requirements.txt):
    requests, beautifulsoup4, lxml, html2text

Автору будущего:
  - Менять размер «корзины» — BUCKET_SIZE.
  - Менять паддинг имён задач — PROBLEM_PAD.
  - Добавлять новые расширения решений — SOLUTION_FILENAMES/SOLUTION_PREFIX.
  - Включить/выключить публикацию условий — PUBLISH_STATEMENTS (env).
  - Генерацию README внутри корзин можно отключить флагом GENERATE_BUCKET_README (env).
"""

from __future__ import annotations

import os
import re
import time
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
from html2text import HTML2Text

# === Конфиг ===

# Корень репозитория (скрипт лежит в tools/, значит ROOT = на уровень выше)
ROOT: Path = Path(__file__).resolve().parents[1]

# Размер «корзины» (001-100, 101-200, ...)
BUCKET_SIZE: int = int(os.getenv("BUCKET_SIZE", "100"))

# Паддинг для имён каталогов задач: p001, p042, p840 (можно поставить 4 → p0001 и т.д.)
PROBLEM_PAD: int = int(os.getenv("PROBLEM_PAD", "3"))

# Какие имена файлов считаем «присутствует решение»
SOLUTION_FILENAMES = {
    "solution.py", "main.py", "solution.ipynb",
    "solution.cpp", "solution.cc", "solution.cxx",
    "solution.rs", "solution.java", "solution.js", "solution.ts",
    "solution.go", "solution.rb", "solution.cs",
}
# И/или любой файл, начинающийся на "solution." (например, solution.kt, solution.hs...)
SOLUTION_PREFIX = "solution."

# Публиковать ли текст условий (по умолчанию НЕТ, чтобы не светить контент публично).
PUBLISH_STATEMENTS: bool = os.getenv("PUBLISH_STATEMENTS", "true").lower() in {"1", "true", "yes", "on"}

# Создавать ли README.md внутри каждой корзины с мини-индексом
GENERATE_BUCKET_README: bool = os.getenv("GENERATE_BUCKET_README", "false").lower() in {"1", "true", "yes", "on"}

# Сетевые параметры (для вытягивания заголовков/условий и определения общего числа задач)
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "25"))
MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "4"))
BASE_SLEEP: float = float(os.getenv("BASE_SLEEP", "1.2"))

# HTTP-сессия с вменяемым UA
session = requests.Session()
session.headers.update({"User-Agent": "PE-Repo-Updater (+github-actions)"})


# === Утилиты для имён и путей ===

def bucket_name(n: int) -> str:
    """
    Имя «корзины» для задачи n: '001-100', '101-200', ...
    """
    if n < 1:
        raise ValueError("problem number must be >= 1")
    start = ((n - 1) // BUCKET_SIZE) * BUCKET_SIZE + 1
    end = start + BUCKET_SIZE - 1
    return f"{start:03d}-{end:03d}"


def prob_dir_name(n: int) -> str:
    """
    Каноническое имя каталога задачи с нулевым паддингом: p001, p042, ...
    Паддинг задаётся PROBLEM_PAD.
    """
    return f"p{n:0{PROBLEM_PAD}d}"


# Разрешаем старые имена p1, p01, p001 — вытаскиваем число (и нормализуем дальше)
_PROB_DIR_RE = re.compile(r"^p0*(\d+)$")


def is_problem_dir(path: Path) -> Optional[int]:
    """
    Если каталог называется p{N} (включая p01, p001), возвращает N, иначе None.
    """
    m = _PROB_DIR_RE.fullmatch(path.name)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def has_solution_files(dir_path: Path) -> bool:
    """
    Считаем задачу «решённой», если в каталоге есть хотя бы один файл из SOLUTION_FILENAMES
    или файл, начинающийся на SOLUTION_PREFIX (например, solution.kt).
    """
    try:
        for p in dir_path.iterdir():
            if not p.is_file():
                continue
            name = p.name
            if name in SOLUTION_FILENAMES or name.startswith(SOLUTION_PREFIX):
                return True
        return False
    except FileNotFoundError:
        # Каталог могли переместить во время работы (маловероятно локально)
        return False


# === HTTP и парсинг страниц Project Euler ===

def http_get(url: str) -> requests.Response:
    """
    GET с повторами и экспоненциальной «лестницей» времени ожидания.
    Возвращает Response со статусом 200 или поднимает исключение.
    """
    last_exc = None
    for i in range(MAX_RETRIES):
        try:
            r = session.get(url, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                return r
        except requests.RequestException as e:
            last_exc = e
        # backoff: 1.2^i, 1.44, 1.728, ...
        time.sleep(BASE_SLEEP ** i)
    if last_exc:
        raise last_exc
    raise RuntimeError(f"GET failed: {url}")


def html_to_md(elem) -> str:
    """
    Грубая конвертация HTML → Markdown без жёстких переносов.
    """
    if elem is None:
        return ""
    h = HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_emphasis = False
    return h.handle(str(elem)).strip()


def fetch_problem_md(n: int) -> Tuple[str, str]:
    """
    Вытягивает страницу задачи n, возвращает (markdown, title).
    Если парсинг не удался — бросает исключение, которое обрабатывается выше.
    """
    url = f"https://projecteuler.net/problem={n}"
    r = http_get(url)
    soup = BeautifulSoup(r.text, "lxml")

    title_node = soup.select_one("h2")
    title_text = title_node.get_text(" ", strip=True) if title_node else f"Problem {n}"

    content = soup.select_one("#problem_content") or soup.select_one(".problem_content")
    md_body = html_to_md(content) or "_(content not parsed)_"

    md = f"# {title_text}\n\n" \
         f"Source: {url}\n\n" \
         f"{md_body}\n"
    return md, title_text


def ensure_problem_readme(n: int, prob_dir: Path) -> str:
    """
    Гарантирует наличие pNNN/README.md.
    - Если уже существует — пытается вытащить title из первой строки '###'.
    - Если публикация условий выключена — кладёт заглушку со ссылкой.
    - Если публикация включена — тянет страницу и сохраняет.
    Возвращает заголовок (title) для таблиц в корневом README.
    """
    readme = prob_dir / "README.md"
    if readme.exists():
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
    Пытается надёжно определить общее число задач на Project Euler.
    Алгоритм:
      1) /archives — собираем номера страниц из href и текстов ссылок.
      2) Открываем максимальную страницу (пробуем '?page=' и ';page='), берём максимум problem=ID.
      3) Если не вышло — шагаем назад по страницам, пока не найдём хотя бы один ID.
      4) Фоллбек: None → в корневом README используем максимум из решённых.
    """
    try:
        r = http_get("https://projecteuler.net/archives")
        soup = BeautifulSoup(r.text, "lxml")

        # собрать возможные номера страниц
        pages = {1}
        for a in soup.find_all("a"):
            href = a.get("href", "")
            m = re.search(r"(?:[?;&]|^)page=(\d+)", href)
            if m:
                pages.add(int(m.group(1)))
            t = (a.text or "").strip()
            if t.isdigit():
                pages.add(int(t))

        if not pages:
            pages = {1}
        last = max(pages)

        def max_id_on(page: int) -> int:
            ids: List[int] = []
            for sep in ("?", ";"):
                try:
                    r2 = http_get(f"https://projecteuler.net/archives{sep}page={page}")
                except Exception:
                    continue
                s2 = BeautifulSoup(r2.text, "lxml")
                for a2 in s2.find_all("a"):
                    href2 = a2.get("href", "")
                    m2 = re.search(r"problem=(\d+)", href2)
                    if m2:
                        ids.append(int(m2.group(1)))
            return max(ids) if ids else -1

        mx = max_id_on(last)
        if mx != -1:
            return mx

        for k in range(last - 1, 0, -1):
            mx = max_id_on(k)
            if mx != -1:
                return mx

        return None
    except Exception:
        return None


# === Рендер README'ов ===

def progress_bar(solved: int, total: int, width: int = 30) -> str:
    """
    Рисует «бар» из █/░ по прогрессу.
    """
    pct = (solved / total) if total else 0.0
    filled = int(round(width * pct))
    return "█" * filled + "░" * (width - filled)


def write_root_readme(solved_map: Dict[int, Path], titles: Dict[int, str], total: Optional[int]) -> None:
    """
    Генерирует корневой README.md с компактными HTML-таблицами 10×10
    для каждой «сотни» задач. Решённые: жирный номер-ссылка (001), нерешённые: серый номер.
    Без чеков и служебных заголовков — максимально узко, без горизонтального скролла.
    """
    solved_nums = sorted(solved_map.keys())
    total_all = (total or (max(solved_nums) if solved_nums else BUCKET_SIZE))
    solved_count = len(solved_nums)
    pct = (solved_count / total_all * 100) if total_all else 0.0

    badge = f"![progress](https://img.shields.io/badge/Project%20Euler-{solved_count}%2F{total_all}-blue)"
    bar = progress_bar(solved_count, total_all, width=30)

    solved_set = set(solved_nums)

    def cell_html(n: int) -> str:
        label = f"{n:03d}"
        if n in solved_set:
            rel = solved_map[n].relative_to(ROOT).as_posix() + "/"
            return f'<td align="center"><a href="{rel}"><strong>{label}</strong></a></td>'
        return f'<td align="center"><span>{label}</span></td>'

    parts = []
    parts.append("# Project Euler — my solutions\n\n")
    parts.append(f"{badge}\n\n")
    parts.append(f"**Progress:** {solved_count}/{total_all} ({pct:.2f}%)  \n")
    parts.append(f"`{bar}`\n\n")
    parts.append("<sub>Bold link = solved • Plain = not yet</sub>\n\n")

    # По всем корзинам: 1..total_all, шаг BUCKET_SIZE
    start = 1
    while start <= total_all:
        end = min(start + BUCKET_SIZE - 1, total_all)
        solved_in_bucket = sum(1 for n in range(start, end + 1) if n in solved_set)
        parts.append(f"## {start:03d}-{end:03d}  \n")
        parts.append(f"<sub>{solved_in_bucket}/{end - start + 1} solved</sub>\n\n")

        # Таблица 10×10 без заголовков
        parts.append("<table><tbody>\n")
        cur = start
        for _ in range(10):
            parts.append("<tr>")
            for _ in range(10):
                if cur <= end:
                    parts.append(cell_html(cur))
                else:
                    parts.append('<td align="center">&nbsp;</td>')
                cur += 1
            parts.append("</tr>\n")
        parts.append("</tbody></table>\n\n")
        start = end + 1

    (ROOT / "README.md").write_text("".join(parts), encoding="utf-8")
    
def write_bucket_index(bucket: str, nums: List[int]) -> None:
    """
    Создаёт/обновляет README.md внутри корзины с мини-индексом задач.
    Показывает табличку «№ → ссылка на pNNN/».
    """
    folder = ROOT / bucket
    nums = sorted(nums)
    lines = [f"# {bucket}\n\n", "| # | link |\n", "|---:|:-----|\n"]
    for n in nums:
        rel = f"{prob_dir_name(n)}/"
        lines.append(f"| {n} | [{prob_dir_name(n)}]({rel}) |\n")
    (folder / "README.md").write_text("".join(lines), encoding="utf-8")


# === Сканирование/нормализация каталога ===

def scan_problems() -> Dict[int, Path]:
    """
    Рекурсивно находит каталоги p{N} с решением.
    Возвращает {N: Path_to_pN}.
    Допускает старые имена (p1, p01, p001) — число N извлекается через is_problem_dir().
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


def merge_dir_contents(src: Path, dst: Path) -> None:
    """
    Аккуратно «смержить» содержимое src в dst (без перезаписи существующих файлов).
    Нужен на случай, когда каталог назначения уже существует.
    """
    for item in src.iterdir():
        target = dst / item.name
        if target.exists():
            continue
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def ensure_in_bucket(n: int, current_dir: Path) -> Path:
    """
    Гарантирует, что каталог p{n} лежит:
      1) в правильной корзине (001-100, 101-200, ...);
      2) имеет каноническое имя p{n:0{PROBLEM_PAD}d}.
    При необходимости переносит/переименовывает.
    Возвращает актуальный путь к каталогу pNNN.
    """
    target_parent = ROOT / bucket_name(n)
    target_parent.mkdir(parents=True, exist_ok=True)

    canonical_name = prob_dir_name(n)
    target_dir = target_parent / canonical_name

    # Уже на месте и имя каноническое
    if current_dir.parent == target_parent and current_dir.name == canonical_name:
        return current_dir

    # Если каталог назначения существует — аккуратно смержим содержимое и удалим исходник
    if target_dir.exists():
        merge_dir_contents(current_dir, target_dir)
        shutil.rmtree(current_dir)
        return target_dir

    # Обычный перенос (может включать переименование)
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(current_dir), str(target_dir))
    return target_dir


def cleanup_bucket_readmes() -> None:
    """
    Удаляет README.md (и подобные) внутри корзин вида 001-100, 101-200, ...
    Корневой README содержит всю навигацию — локальные README в корзинах не нужны.
    """
    try:
        patterns = {"README.md", "readme.md", "Readme.md", "index.md"}
        for d in ROOT.iterdir():
            if d.is_dir() and re.fullmatch(r"\d{3}-\d{3}", d.name):
                for name in patterns:
                    fp = d / name
                    if fp.exists():
                        try:
                            fp.unlink()
                        except Exception:
                            pass
    except Exception:
        # Никогда не валимся из-за косметики
        pass


# === Точка входа ===

def main() -> None:
    # 1) Найти решённые задачи (по файлам solution.* / main.*)
    solved = scan_problems()  # {n: path_to_pN}

    # 2) Привести структуру к канону (корзины + паддинг имён)
    normalized: Dict[int, Path] = {}
    for n, p in sorted(solved.items()):
        new_path = ensure_in_bucket(n, p)
        normalized[n] = new_path

    # 3) Сгенерировать pNNN/README.md (заглушки либо с текстом условия)
    titles: Dict[int, str] = {}
    for n, p in sorted(normalized.items()):
        titles[n] = ensure_problem_readme(n, p)

    # 4) Узнать «сколько всего задач» (или взять максимум из решённых как фоллбек)
    total = fetch_total_problems()
    if total is None and normalized:
        total = max(normalized.keys())

    # 5) Пересобрать корневой README
    write_root_readme(normalized, titles, total)

    # 6) (Опционально) README внутри корзин
    if GENERATE_BUCKET_README and normalized:
        buckets: Dict[str, List[int]] = {}
        for n in sorted(normalized.keys()):
            b = bucket_name(n)
            buckets.setdefault(b, []).append(n)
        for b, lst in buckets.items():
            write_bucket_index(b, lst)

    # На всякий случай чистим README в корзинах
    cleanup_bucket_readmes()


if __name__ == "__main__":
    main()
