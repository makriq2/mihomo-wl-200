#!/usr/bin/env python3
from pathlib import Path
from urllib.request import urlopen, Request
import time

SRC = 'https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt'
OUT = Path('data/wl-first-300.txt')
LIMIT = 300

last = None
for attempt in range(5):
    try:
        req = Request(SRC, headers={'User-Agent': 'wl-first-300-bot/1.0'})
        with urlopen(req, timeout=30) as r:
            raw = r.read().decode('utf-8', 'replace')
        break
    except Exception as e:
        last = e
        if attempt == 4:
            raise
        time.sleep(2 * (attempt + 1))

lines = [line for line in raw.splitlines() if line.strip()]
trimmed = lines[:LIMIT]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text('\n'.join(trimmed) + ('\n' if trimmed else ''), encoding='utf-8')
print(f'fetched={len(lines)} kept={len(trimmed)} out={OUT}')
