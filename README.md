# GAImagination Algorithm Mini Lab

**从算法到文化智能：可运行的小实验**  
**From Algorithms to Cultural Intelligence: runnable mini demos for lectures and workshops**

This repository supports the GAImagination distinguished lecture series, especially **Lecture 4: AI 时代的数字非遗未来 / The Future of Digital Heritage in the AI Era**. It provides three lightweight Python mini applications that audiences can run after scanning a GitHub QR code.

The first version is designed for lecture demonstration: clear, visual, and easy to explain. It does not require cloud API keys.

---

## V1.0 Mini Apps

| App | Chinese Title | Lecture Concept | Main Output |
|---|---|---|---|
| 01 | 文化文本注意力可视化器 | Transformer Attention / 注意力机制 | HTML heatmap |
| 02 | 非遗语义空间地图 | Embedding Space / 向量语义空间 | PNG map + similarity CSV |
| 03 | 强化学习走钢丝演示 | Reinforcement Learning / 强化学习 | GUI demo + training CSV |

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/SWingLiang/GAImagination-Algorithm-Mini-Lab.git
cd GAImagination-Algorithm-Mini-Lab

# 2. Create an environment, optional but recommended
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Run the Three Apps

### 01 Attention Visualizer

```bash
python apps/01_attention_visualizer/attention_visualizer.py
python apps/01_attention_visualizer/attention_visualizer.py --input assets/sample_heritage_text.txt
```

Output:

```text
outputs/attention_visualizer.html
```

Use this app to explain: **AI does not treat every word equally; attention highlights meaningful cultural tokens and relationships.**

---

### 02 ICH Embedding Map

```bash
python apps/02_ich_embedding_map/ich_embedding_map.py
python apps/02_ich_embedding_map/ich_embedding_map.py --query 醒狮
python apps/02_ich_embedding_map/ich_embedding_map.py --csv assets/ich_items.csv
```

Outputs:

```text
outputs/ich_embedding_map.png
outputs/ich_similarity.csv
outputs/ich_embedding_summary.md
```

Use this app to explain: **text, image, motion, music, craft, ritual, and performance can be translated into comparable coordinates in a semantic space.**

---

### 03 RL Tightrope Demo

```bash
python apps/03_rl_tightrope_demo/rl_tightrope_demo.py --episodes 600
python apps/03_rl_tightrope_demo/rl_tightrope_demo.py --gui
```

Outputs:

```text
outputs/rl_training_history.csv
outputs/rl_policy.csv
```

Use this app to explain: **AI learns through trial, error, reward, penalty, feedback, and adjustment.**

---

## Suggested Lecture Slide Before “Thank You”

**FROM CONCEPT TO MINI LAB**  
**从概念，到可运行的算法小实验**

Scan the QR code · Run the code · See the algorithm  
扫码下载 · 运行代码 · 看见算法

1. Attention Visualizer — 看见注意力机制  
2. ICH Embedding Map — 看见文化语义空间  
3. RL Tightrope Demo — 看见强化学习循环

> AI 不是抽象概念。它可以被看见、运行、修改，并参与文化的数字化未来。

---

## Build Windows EXE Files

See [docs/BUILD_EXE.md](docs/BUILD_EXE.md).

---

## Repository Structure

```text
GAImagination-Algorithm-Mini-Lab/
├── README.md
├── CODEX_TASKS.md
├── requirements.txt
├── assets/
│   ├── sample_heritage_text.txt
│   └── ich_items.csv
├── apps/
│   ├── 01_attention_visualizer/
│   ├── 02_ich_embedding_map/
│   └── 03_rl_tightrope_demo/
├── docs/
│   └── BUILD_EXE.md
└── outputs/              # generated locally, ignored by git
```

---

## Academic Positioning

This mini lab supports the GAImagination framework by connecting cultural heritage education with computational concepts:

- **Gather / Abstract**: turn cultural materials into structured features.
- **Interpret**: visualize attention and semantic similarity.
- **Imagine / Actualize**: produce runnable demos and audience-facing artifacts.
- **Transform**: move from cultural archives toward cultural intelligence.

---

## License

For lecture, teaching, and research demonstration. A formal license can be added later.
