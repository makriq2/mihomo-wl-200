#!/usr/bin/env python3
from pathlib import Path
from urllib.request import urlopen, Request
import time
import random

SOURCES = [
    'https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt',
    'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt',
    'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt',
]
OUT = Path('data/mobile-whitelist-mixed-200.txt')
HEAD_COUNT = 40
RANDOM_COUNT = 160
SEED = 20260401


def fetch(url: str) -> str:
    last = None
    for attempt in range(5):
        try:
            req = Request(url, headers={'User-Agent': 'mobile-whitelist-mixed-200-bot/1.0'})
            with urlopen(req, timeout=30) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            last = e
            if attempt == 4:
                raise last
            time.sleep(2 * (attempt + 1))


primary_lines = [line for line in fetch(SOURCES[0]).splitlines() if line.strip()]
other_lines = []
for url in SOURCES[1:]:
    other_lines.extend(line for line in fetch(url).splitlines() if line.strip())

head = primary_lines[:HEAD_COUNT]
pool = primary_lines[HEAD_COUNT:] + other_lines
rng = random.Random(SEED)
sample_n = min(RANDOM_COUNT, len(pool))
random_part = rng.sample(pool, sample_n) if sample_n else []
trimmed = head + random_part

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text('\n'.join(trimmed) + ('\n' if trimmed else ''), encoding='utf-8')
print(
    f'primary={len(primary_lines)} other={len(other_lines)} kept={len(trimmed)} '
    f'head={len(head)} random={len(random_part)} seed={SEED} out={OUT}'
)
