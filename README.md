# GAImagination Algorithm Mini Lab V2

**从算法到文化智能：可运行的小实验**  
**From Algorithms to Cultural Intelligence: runnable mini demos for lectures and workshops**

This repository supports **Lecture 4: AI 时代的数字非遗未来 / The Future of Digital Heritage in the AI Era**.

V2 contains five small Python demos. They are designed for lecture sharing through a GitHub QR code: visual, lightweight, and understandable for non-CS audiences.

## Mini Apps

| App | Chinese Title | Lecture Concept | Output |
|---|---|---|---|
| 01 | 文化文本注意力可视化器 | Transformer Attention | HTML heatmap |
| 02 | 非遗语义空间地图 | Embedding Space | PNG map + similarity CSV |
| 03 | 强化学习走钢丝演示 | Reinforcement Learning | training CSV + optional GUI |
| 04 | 非遗动作特征提取器 | Motion Features / Embodied AI | feature CSV + trajectory plot |
| 05 | 非遗节奏与动作匹配器 | Multimodal Alignment | matching score + aligned plot |

## Quick Start

```bash
git clone https://github.com/SWingLiang/GAImagination-Algorithm-Mini-Lab.git
cd GAImagination-Algorithm-Mini-Lab
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run All Demos

```bash
python apps/01_attention_visualizer/attention_visualizer.py
python apps/02_ich_embedding_map/ich_embedding_map.py --query "Lion Dance"
python apps/03_rl_tightrope_demo/rl_tightrope_demo.py --episodes 600
python apps/04_motion_feature_extractor/motion_feature_extractor.py
python apps/05_rhythm_motion_matcher/rhythm_motion_matcher.py
```

All generated files are placed in `outputs/`.

## Slide Text Before Thank You

**FROM CONCEPT TO MINI LAB**  
**从概念，到可运行的算法小实验**

Scan the QR code · Run the code · See the algorithm  
扫码下载 · 运行代码 · 看见算法

1. Attention Visualizer — 看见注意力机制  
2. ICH Embedding Map — 看见文化语义空间  
3. RL Tightrope Demo — 看见强化学习循环  
4. Motion Feature Extractor — 看见动作如何变成数据  
5. Rhythm-Motion Matcher — 看见节奏与动作如何对齐

> AI 不是抽象概念。它可以被看见、运行、修改，并参与文化的数字化未来。

## Notes

- No cloud API key is required.
- Apps 01, 03, 04, 05 can run with Python standard library plus optional plotting.
- Apps 02, 04, 05 use `numpy` and `matplotlib` for plots.
- App 04 is CSV-first: it reads keypoint trajectories exported from pose tools. Future versions can add MediaPipe/OpenPose video extraction.
- App 05 is signal-first: it aligns motion intensity with rhythm energy. Future versions can add Librosa audio beat detection.
