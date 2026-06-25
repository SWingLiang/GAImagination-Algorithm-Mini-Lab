"""GAImagination Mini Lab 05: Rhythm-Motion Matcher.

Aligns motion intensity with rhythm energy. It can read CSV signals or generate
sample data. This is a lightweight lecture demo for multimodal cultural AI.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_rhythm(path: Path, seconds: float = 8.0, fps: int = 30) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = int(seconds * fps)
    rows = []
    beat_times = np.arange(0.83, seconds, 0.9)
    for i in range(n):
        t = i / fps
        energy = 0.12 + 0.05 * math.sin(2 * math.pi * 0.45 * t)
        for bt in beat_times:
            energy += math.exp(-((t - bt) ** 2) / (2 * 0.035 ** 2))
        rows.append((f"{t:.4f}", f"{min(1.0, energy):.6f}"))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time", "energy"])
        w.writerows(rows)


def read_signal(path: Path, value_column: str):
    times, values = [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["time"]))
            values.append(float(row[value_column]))
    return np.array(times), np.array(values)


def normalize(x):
    x = np.asarray(x, dtype=float)
    if len(x) == 0:
        return x
    mn, mx = float(np.min(x)), float(np.max(x))
    if abs(mx - mn) < 1e-9:
        return np.zeros_like(x)
    return (x - mn) / (mx - mn)


def resample(src_t, src_v, target_t):
    return np.interp(target_t, src_t, src_v)


def detect_peaks(values, threshold=0.65):
    if len(values) < 3:
        return np.array([], dtype=int)
    idx = []
    for i in range(1, len(values) - 1):
        if values[i] > values[i - 1] and values[i] > values[i + 1] and values[i] >= threshold:
            idx.append(i)
    return np.array(idx, dtype=int)


def matching_score(motion_t, motion_v, rhythm_t, rhythm_v, tolerance=0.16):
    common_t = motion_t
    rv = normalize(resample(rhythm_t, rhythm_v, common_t))
    mv = normalize(motion_v)
    motion_peaks = detect_peaks(mv)
    rhythm_peaks = detect_peaks(rv)
    if len(motion_peaks) == 0 or len(rhythm_peaks) == 0:
        peak_score = 0.0
    else:
        matched = 0
        rhythm_times = common_t[rhythm_peaks]
        for p in motion_peaks:
            if np.min(np.abs(rhythm_times - common_t[p])) <= tolerance:
                matched += 1
        peak_score = matched / max(len(motion_peaks), len(rhythm_peaks))
    corr = float(np.corrcoef(mv, rv)[0, 1]) if len(mv) > 2 and np.std(mv) > 1e-9 and np.std(rv) > 1e-9 else 0.0
    corr_score = (corr + 1) / 2
    score = 0.65 * peak_score + 0.35 * corr_score
    return score, peak_score, corr, common_t, mv, rv, motion_peaks, rhythm_peaks


def plot_alignment(t, motion, rhythm, motion_peaks, rhythm_peaks, score, out_png: Path) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.plot(t, rhythm, label="Rhythm energy")
    ax.plot(t, motion, label="Motion intensity")
    if len(rhythm_peaks):
        ax.scatter(t[rhythm_peaks], rhythm[rhythm_peaks], s=70, marker="o", label="rhythm peaks")
    if len(motion_peaks):
        ax.scatter(t[motion_peaks], motion[motion_peaks], s=80, marker="x", label="motion peaks")
    ax.set_title(f"Rhythm-Motion Alignment  score={score:.2f}")
    ax.set_xlabel("time (sec)")
    ax.set_ylabel("normalized intensity")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Match motion intensity with rhythm energy.")
    parser.add_argument("--motion", default="outputs/motion_timeseries.csv", help="Motion CSV with time and speed columns.")
    parser.add_argument("--rhythm", default="data/sample_rhythm_energy.csv", help="Rhythm CSV with time and energy columns. Auto-created if missing.")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    motion_path = Path(args.motion)
    rhythm_path = Path(args.rhythm)
    if not rhythm_path.exists():
        generate_rhythm(rhythm_path)
    if not motion_path.exists():
        from importlib.machinery import SourceFileLoader
        extractor_path = Path(__file__).parents[1] / "04_motion_feature_extractor" / "motion_feature_extractor.py"
        extractor = SourceFileLoader("motion_feature_extractor", str(extractor_path)).load_module()
        extractor.main()

    mt, mv = read_signal(motion_path, "speed")
    rt, rv = read_signal(rhythm_path, "energy")
    score, peak_score, corr, t, motion, rhythm, motion_peaks, rhythm_peaks = matching_score(mt, mv, rt, rv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_alignment(t, motion, rhythm, motion_peaks, rhythm_peaks, score, out_dir / "rhythm_motion_alignment.png")
    with (out_dir / "rhythm_motion_score.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["overall_score", f"{score:.4f}"])
        w.writerow(["peak_alignment_score", f"{peak_score:.4f}"])
        w.writerow(["correlation", f"{corr:.4f}"])
        w.writerow(["motion_peak_count", len(motion_peaks)])
        w.writerow(["rhythm_peak_count", len(rhythm_peaks)])
    (out_dir / "rhythm_motion_summary.md").write_text(
        f"# Rhythm-Motion Matcher\n\nOverall score: **{score:.2f}**\n\nThis score combines peak alignment and signal correlation.\n",
        encoding="utf-8",
    )
    print(f"Generated: {out_dir}/rhythm_motion_alignment.png")
    print(f"Generated: {out_dir}/rhythm_motion_score.csv")
    print(f"Overall score: {score:.2f}")


if __name__ == "__main__":
    main()
