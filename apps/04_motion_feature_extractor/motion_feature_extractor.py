"""GAImagination Mini Lab 04: Motion Feature Extractor.

CSV-first MVP for embodied cultural motion. It reads a keypoint trajectory
(frame,time,x,y) and extracts interpretable motion features.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_sample(path: Path, fps: int = 30, seconds: float = 8.0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    n = int(fps * seconds)
    for frame in range(n):
        t = frame / fps
        # A stylized lion-dance / sleeve arc: periodic side motion plus vertical pulses.
        x = 0.5 + 0.32 * math.sin(2 * math.pi * 0.55 * t) + 0.04 * math.sin(2 * math.pi * 1.8 * t)
        y = 0.5 + 0.22 * math.sin(2 * math.pi * 1.10 * t + 0.7) + 0.03 * math.cos(2 * math.pi * 2.2 * t)
        rows.append((frame, f"{t:.4f}", f"{x:.5f}", f"{y:.5f}"))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frame", "time", "x", "y"])
        w.writerows(rows)


def load_points(path: Path):
    if not path.exists():
        generate_sample(path)
    frames, times, xs, ys = [], [], [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(float(row["frame"])))
            times.append(float(row["time"]))
            xs.append(float(row["x"]))
            ys.append(float(row["y"]))
    return np.array(frames), np.array(times), np.array(xs), np.array(ys)


def compute_features(times, xs, ys):
    dt = np.diff(times)
    dt[dt == 0] = np.nan
    dx = np.diff(xs)
    dy = np.diff(ys)
    dist = np.sqrt(dx * dx + dy * dy)
    speed = dist / dt
    speed = np.nan_to_num(speed)
    accel = np.diff(speed) / dt[1:]
    accel = np.nan_to_num(accel)
    angles = np.arctan2(dy, dx)
    turns = np.abs(np.diff(np.unwrap(angles)))
    duration = float(times[-1] - times[0]) if len(times) > 1 else 0.0
    path_length = float(dist.sum())
    displacement = float(math.sqrt((xs[-1] - xs[0]) ** 2 + (ys[-1] - ys[0]) ** 2))
    rhythm_peaks = int(np.sum((speed[1:-1] > speed[:-2]) & (speed[1:-1] > speed[2:]) & (speed[1:-1] > np.percentile(speed, 70)))) if len(speed) > 3 else 0
    return {
        "duration_sec": duration,
        "path_length": path_length,
        "net_displacement": displacement,
        "movement_density": path_length / duration if duration > 0 else 0.0,
        "mean_speed": float(np.mean(speed)) if len(speed) else 0.0,
        "max_speed": float(np.max(speed)) if len(speed) else 0.0,
        "mean_acceleration": float(np.mean(np.abs(accel))) if len(accel) else 0.0,
        "turning_energy": float(np.mean(turns)) if len(turns) else 0.0,
        "bbox_width": float(xs.max() - xs.min()),
        "bbox_height": float(ys.max() - ys.min()),
        "rhythm_peak_count": rhythm_peaks,
    }, speed


def save_outputs(times, xs, ys, speed, features, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "motion_features.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["feature", "value"])
        for k, v in features.items():
            w.writerow([k, f"{v:.6f}" if isinstance(v, float) else v])
    with (out_dir / "motion_timeseries.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time", "x", "y", "speed"])
        for i, t in enumerate(times):
            s = speed[i - 1] if i > 0 and len(speed) else 0.0
            w.writerow([f"{t:.4f}", f"{xs[i]:.5f}", f"{ys[i]:.5f}", f"{s:.6f}"])
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot(xs, ys, linewidth=2)
    ax.scatter([xs[0]], [ys[0]], s=120, marker="o", label="start")
    ax.scatter([xs[-1]], [ys[-1]], s=120, marker="*", label="end")
    ax.set_title("Motion Trajectory")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.invert_yaxis()
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "motion_trajectory.png", dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Extract motion features from a keypoint trajectory CSV.")
    parser.add_argument("--input", default="data/sample_motion_points.csv", help="CSV with frame,time,x,y columns. Auto-created if missing.")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()
    path = Path(args.input)
    frames, times, xs, ys = load_points(path)
    features, speed = compute_features(times, xs, ys)
    save_outputs(times, xs, ys, speed, features, Path(args.out_dir))
    print(f"Input: {path}")
    print(f"Generated: {args.out_dir}/motion_features.csv")
    print(f"Generated: {args.out_dir}/motion_timeseries.csv")
    print(f"Generated: {args.out_dir}/motion_trajectory.png")


if __name__ == "__main__":
    main()
