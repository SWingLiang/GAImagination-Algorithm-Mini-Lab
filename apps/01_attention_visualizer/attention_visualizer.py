"""GAImagination Mini Lab 01: Attention Visualizer.

A dependency-free teaching demo that converts cultural heritage text into an
HTML heatmap. It is not a trained Transformer. It uses transparent keyword and
context heuristics to make the attention idea visible for lecture audiences.
"""
from __future__ import annotations

import argparse
import html
import math
import re
from pathlib import Path

DEFAULT_TEXT = (
    "Cantonese opera sleeve movement shows rhythm, gesture, visual style, and "
    "cultural meaning. AI can connect text, image, motion, and music to support "
    "digital heritage interpretation and creative learning."
)

KEYWORDS = {
    "ai": 1.00,
    "algorithm": 0.92,
    "attention": 1.00,
    "culture": 0.90,
    "cultural": 0.90,
    "heritage": 0.95,
    "opera": 0.80,
    "yueju": 0.90,
    "cantonese": 0.75,
    "sleeve": 0.90,
    "movement": 0.85,
    "motion": 0.95,
    "gesture": 0.88,
    "rhythm": 0.86,
    "music": 0.80,
    "image": 0.76,
    "text": 0.70,
    "visual": 0.78,
    "digital": 0.80,
    "agent": 0.82,
    "avatar": 0.80,
}

STOPWORDS = {"the", "a", "an", "and", "or", "of", "to", "in", "with", "for", "is", "can"}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\s]", text)


def score_token(token: str, index: int, total: int) -> float:
    clean = re.sub(r"[^A-Za-z0-9]", "", token).lower()
    if not clean:
        return 0.08
    base = KEYWORDS.get(clean, 0.18)
    if clean in STOPWORDS:
        base = 0.08
    length_bonus = min(len(clean) / 18.0, 0.25)
    center = (index + 1) / max(total, 1)
    position_bonus = 0.08 * math.sin(math.pi * center)
    return max(0.05, min(1.0, base + length_bonus + position_bonus))


def build_html(text: str, scores: list[tuple[str, float]]) -> str:
    spans = []
    for token, score in scores:
        alpha = 0.10 + 0.75 * score
        color = f"rgba(0, 230, 210, {alpha:.2f})"
        escaped = html.escape(token)
        if re.match(r"[A-Za-z0-9]", token):
            escaped += " "
        spans.append(
            f'<span class="tok" style="background:{color}" title="attention={score:.2f}">{escaped}</span>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>GAImagination Attention Visualizer</title>
<style>
body {{ margin: 0; background: #050b14; color: #eaf7ff; font-family: Arial, sans-serif; }}
.wrap {{ max-width: 1100px; margin: 48px auto; padding: 32px; }}
.kicker {{ color: #00e6d2; letter-spacing: 0.28em; font-size: 14px; font-weight: 700; }}
h1 {{ font-size: 44px; margin: 18px 0 6px; }}
.sub {{ color: #9db5c8; font-size: 18px; margin-bottom: 34px; }}
.panel {{ border: 1px solid rgba(0,230,210,.35); border-radius: 18px; padding: 28px; background: rgba(7,20,34,.8); box-shadow: 0 0 40px rgba(0,230,210,.08); }}
.text {{ font-size: 30px; line-height: 1.85; }}
.tok {{ border-radius: 8px; padding: 5px 8px; margin: 2px; display: inline-block; color: #f8ffff; }}
.note {{ margin-top: 24px; color: #bdd4e5; font-size: 16px; line-height: 1.6; }}
.legend {{ margin-top: 22px; height: 16px; border-radius: 8px; background: linear-gradient(90deg, rgba(0,230,210,.12), rgba(0,230,210,.85)); }}
.labels {{ display: flex; justify-content: space-between; color: #88a6b8; margin-top: 8px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="kicker">ATTENTION VISUALIZER · 注意力机制</div>
  <h1>Which cultural features does AI focus on?</h1>
  <div class="sub">A transparent teaching demo for Transformer-style attention.</div>
  <div class="panel">
    <div class="text">{''.join(spans)}</div>
    <div class="legend"></div>
    <div class="labels"><span>low attention</span><span>high attention</span></div>
    <div class="note">This demo uses interpretable rules to approximate attention for teaching. It helps audiences see that AI can focus on key cultural tokens such as motion, rhythm, sleeve, heritage, and AI.</div>
  </div>
</div>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an attention heatmap HTML file.")
    parser.add_argument("--text", type=str, default=None, help="Text to visualize.")
    parser.add_argument("--input", type=str, default=None, help="Optional text file.")
    parser.add_argument("--out", type=str, default="outputs/attention_visualizer.html")
    args = parser.parse_args()

    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
    else:
        text = args.text or DEFAULT_TEXT

    tokens = tokenize(text)
    scores = [(tok, score_token(tok, i, len(tokens))) for i, tok in enumerate(tokens)]
    html_doc = build_html(text, scores)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    print(f"Generated: {out}")


if __name__ == "__main__":
    main()
