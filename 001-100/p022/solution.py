from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
names_path = BASE_DIR / "names.txt"

with names_path.open("r", encoding="utf-8") as f:
    data = f.read()

names = sorted(n.strip('"') for n in data.split(","))

ans = 0
for i, el in enumerate(names):
    ans += (sum([ord(_) - ord('A') + 1 for _ in el])) * (i + 1)

print(ans)