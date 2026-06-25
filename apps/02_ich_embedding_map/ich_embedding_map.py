"""GAImagination Mini Lab 02: ICH Embedding Map."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

FEATURES = ["motion", "music", "visual", "ritual", "craft", "narrative", "performance", "community"]
DEFAULT_CSV = "data/ich_items.csv"


def load_items(path: str):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vector = np.array([float(row[k]) for k in FEATURES], dtype=float)
            rows.append({"name": row["name"], "english": row.get("english", row["name"]), "category": row.get("category", ""), "vector": vector})
    return rows


def pca_2d(matrix: np.ndarray) -> np.ndarray:
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    return centered @ vt[:2].T


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return 0.0 if denom == 0 else float(np.dot(a, b) / denom)


def find_query_index(items, query: str | None) -> int:
    if not query:
        return 0
    q = query.lower()
    for i, item in enumerate(items):
        if q in item["name"].lower() or q in item["english"].lower():
            return i
    return 0


def write_similarity(items, query_idx: int, out_csv: Path) -> None:
    qv = items[query_idx]["vector"]
    sims = [(item["name"], item["english"], item["category"], cosine(qv, item["vector"])) for item in items]
    sims.sort(key=lambda x: x[3], reverse=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "name", "english", "category", "cosine_similarity"])
        for rank, row in enumerate(sims, 1):
            writer.writerow([rank, *row[:3], f"{row[3]:.4f}"])


def plot_map(items, coords: np.ndarray, query_idx: int, out_png: Path) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 7))
    cats = sorted(set(item["category"] for item in items))
    cat_to_num = {c: i for i, c in enumerate(cats)}
    values = [cat_to_num[item["category"]] for item in items]
    ax.scatter(coords[:, 0], coords[:, 1], s=160, c=values, alpha=0.82)
    ax.scatter(coords[query_idx, 0], coords[query_idx, 1], s=360, marker="*", edgecolors="black", linewidths=1.2)
    for item, (x, y) in zip(items, coords):
        ax.text(x + 0.015, y + 0.015, item["name"], fontsize=10)
    ax.axhline(0, linewidth=0.6, alpha=0.4)
    ax.axvline(0, linewidth=0.6, alpha=0.4)
    ax.set_title("ICH Embedding Space Map")
    ax.set_xlabel("PCA dimension 1")
    ax.set_ylabel("PCA dimension 2")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(out_png, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a 2D semantic map of ICH items.")
    parser.add_argument("--csv", default=DEFAULT_CSV, help="Input CSV with feature columns.")
    parser.add_argument("--query", default="Lion Dance", help="Highlight and rank items similar to this query.")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    items = load_items(args.csv)
    matrix = np.vstack([item["vector"] for item in items])
    coords = pca_2d(matrix)
    query_idx = find_query_index(items, args.query)
    out_dir = Path(args.out_dir)
    plot_map(items, coords, query_idx, out_dir / "ich_embedding_map.png")
    write_similarity(items, query_idx, out_dir / "ich_similarity.csv")
    (out_dir / "ich_embedding_summary.md").write_text(
        f"# ICH Embedding Map\n\nHighlighted query: **{items[query_idx]['name']}**\n\nGenerated `ich_embedding_map.png` and `ich_similarity.csv`.\n",
        encoding="utf-8",
    )
    print(f"Generated files in {out_dir}")


if __name__ == "__main__":
    main()
