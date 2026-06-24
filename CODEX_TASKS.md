# Codex Task Plan — GAImagination Algorithm Mini Lab V1.0

This file is written for Codex or future coding agents. The goal is to keep the first public version lightweight, runnable, and suitable for QR-code sharing during Lecture 4.

## Product Goal

Create a small, audience-facing Python mini lab that demonstrates three algorithmic ideas behind AI-era digital heritage:

1. Transformer-style attention
2. Cultural embedding space
3. Reinforcement learning feedback loop

The repository should remain simple enough for non-CS audiences to run, but organized enough for later research/workshop expansion.

---

## Task 01 — Attention Visualizer

**Path:** `apps/01_attention_visualizer/attention_visualizer.py`

### Current status

Implemented as a dependency-free HTML generator using interpretable pseudo-attention.

### Next improvements

- Add a simple desktop GUI with `tkinter.Text` input and a “Generate Heatmap” button.
- Add export to PNG, possibly through browser screenshot or optional Pillow support.
- Add lecture presets: 粤剧、水袖、醒狮、英歌舞、广彩.
- Add an “explain mode” that shows why each token receives attention.

### Acceptance criteria

- Runs with `python apps/01_attention_visualizer/attention_visualizer.py`.
- Produces `outputs/attention_visualizer.html`.
- Uses no cloud API and no model download.
- Explains clearly that this is a teaching approximation, not a trained Transformer.

---

## Task 02 — ICH Embedding Map

**Path:** `apps/02_ich_embedding_map/ich_embedding_map.py`

### Current status

Implemented with built-in heritage feature vectors and a CSV loader. Uses numpy PCA and matplotlib.

### Next improvements

- Add more Guangdong ICH items.
- Add a Streamlit or tkinter viewer for interactive search.
- Add category filtering: 戏曲 / 舞蹈 / 工艺 / 民俗 / 武术.
- Add hover labels in an optional HTML version.
- Add a second map comparing “human-labeled features” vs “AI-generated features.”

### Acceptance criteria

- Runs with `python apps/02_ich_embedding_map/ich_embedding_map.py`.
- Produces `outputs/ich_embedding_map.png` and `outputs/ich_similarity.csv`.
- Supports `--query 粤剧` and `--csv assets/ich_items.csv`.
- Keeps dependency list minimal.

---

## Task 03 — RL Tightrope Demo

**Path:** `apps/03_rl_tightrope_demo/rl_tightrope_demo.py`

### Current status

Implemented as a compact Q-learning demo with CLI training and optional Tkinter animation.

### Next improvements

- Add an on-screen training curve.
- Add a “before training / after training” comparison.
- Add preset metaphors: 走钢丝、舞狮平衡、英歌舞步法.
- Add a reset button and episode slider.
- Improve visual style to match the dark cyan GAImagination slide style.

### Acceptance criteria

- Runs with `python apps/03_rl_tightrope_demo/rl_tightrope_demo.py --episodes 600`.
- Runs with `python apps/03_rl_tightrope_demo/rl_tightrope_demo.py --gui` on desktop Python.
- Produces `outputs/rl_training_history.csv` and `outputs/rl_policy.csv`.
- Makes the loop “Try → Error → Feedback → Adjust → Mastery” visible.

---

## Task 04 — EXE Packaging

**Path:** `docs/BUILD_EXE.md`

### Current status

PyInstaller instructions are provided.

### Next improvements

- Add GitHub Actions workflow for building Windows executables.
- Add icons for each app.
- Add a `release/` folder structure with zipped Windows builds.

### Acceptance criteria

- A Windows user can run the documented PyInstaller commands.
- Build outputs are ignored by git.
- Release package includes README and sample assets.

---

## Task 05 — Slide Integration

### Next improvements

- Add `slides/mini_lab_qr_slide.md` with slide text.
- Add a QR code image pointing to the GitHub repo.
- Add one preview screenshot per mini app.

### Suggested slide title

**FROM CONCEPT TO MINI LAB**  
**从概念，到可运行的算法小实验**

### Suggested closing sentence

AI 不是抽象概念。它可以被看见、运行、修改，并参与文化的数字化未来。
