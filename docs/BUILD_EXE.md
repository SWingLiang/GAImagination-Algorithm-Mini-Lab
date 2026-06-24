# Build Windows EXE Files

This guide packages each mini app as a Windows `.exe` file for lecture sharing.

## 1. Install PyInstaller

```bash
pip install pyinstaller
```

## 2. Build Attention Visualizer

```bash
pyinstaller --onefile --name AttentionVisualizer apps/01_attention_visualizer/attention_visualizer.py
```

Output:

```text
dist/AttentionVisualizer.exe
```

## 3. Build ICH Embedding Map

```bash
pyinstaller --onefile --name ICHEmbeddingMap apps/02_ich_embedding_map/ich_embedding_map.py
```

Output:

```text
dist/ICHEmbeddingMap.exe
```

## 4. Build RL Tightrope Demo

```bash
pyinstaller --onefile --name RLTightropeDemo apps/03_rl_tightrope_demo/rl_tightrope_demo.py
```

Output:

```text
dist/RLTightropeDemo.exe
```

## 5. Suggested Release Folder

```text
release/
├── AttentionVisualizer.exe
├── ICHEmbeddingMap.exe
├── RLTightropeDemo.exe
├── sample_heritage_text.txt
├── ich_items.csv
└── README_for_audience.md
```

## Notes

- The apps do not require cloud API keys.
- The attention visualizer uses only Python standard library.
- The embedding map requires `numpy` and `matplotlib`.
- The RL demo uses standard library for CLI and Tkinter for GUI.
- Generated files are written to the local `outputs/` folder.
