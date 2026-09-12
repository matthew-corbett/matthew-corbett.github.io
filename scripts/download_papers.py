"""Download open-access PDFs for matthew-corbett.com into ./papers/."""
from __future__ import annotations

import ssl
import urllib.request
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
out = repo / "papers"
out.mkdir(exist_ok=True)

PAPERS = [
    ("evaluatar-popets-2026.pdf", [
        "https://petsymposium.org/popets/2026/popets-2026-0153.pdf",
        "https://arxiv.org/pdf/2605.29177",
    ]),
    ("eyecue-ijcai-2026.pdf", [
        "https://arxiv.org/pdf/2605.07859",
    ]),
    ("eccws-ai-governance-2026.pdf", [
        "https://papers.academic-conferences.org/index.php/eccws/article/download/4710/4368",
    ]),
    ("gdrkmcc-situational-awareness-2025.pdf", [
        "https://www.ieworldconference.org/content/WP2025/Papers/GDRKMCC25_15.pdf",
    ]),
    ("dissertation-ar-security-privacy-2024.pdf", [
        "https://vtechworks.lib.vt.edu/bitstreams/2cc0c3f9-8f5b-4920-b218-7c671a185e35/download",
    ]),
    ("securing-bystander-privacy-ieee-sp-2024.pdf", [
        "https://arxiv.org/pdf/2307.12847",
    ]),
    ("gazepair-ieee-tmc-2024.pdf", [
        "https://arxiv.org/pdf/2303.07404",
    ]),
    ("bystandar-mobisys-2023.pdf", [
        "https://vtechworks.lib.vt.edu/bitstreams/991d085c-6dff-4029-a55a-fef0611f22c5/download",
    ]),
    ("shouldar-imwut-2024.pdf", [
        "https://dl.acm.org/doi/pdf/10.1145/3678573",
    ]),
]


def is_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-"


def fetch(url: str) -> bytes | None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "application/pdf,*/*",
            "Referer": "https://dl.acm.org/",
        },
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            data = resp.read()
            if is_pdf(data):
                return data
            print(f"  not pdf: {url}")
            return None
    except Exception as exc:
        print(f"  fail: {url} -> {exc}")
        return None


for name, urls in PAPERS:
    dest = out / name
    if dest.exists() and is_pdf(dest.read_bytes()):
        print(f"keep {name} ({dest.stat().st_size} bytes)")
        continue
    print(f"fetch {name}")
    for url in urls:
        data = fetch(url)
        if data:
            dest.write_bytes(data)
            print(f"  ok {url} -> {len(data)} bytes")
            break
    else:
        print(f"  MISSING {name}")
