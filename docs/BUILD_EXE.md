# Build Windows EXE Files

Use PyInstaller on Windows.

```bash
pip install pyinstaller
```

Build each mini app:

```bash
pyinstaller --onefile --name AttentionVisualizer apps/01_attention_visualizer/attention_visualizer.py
pyinstaller --onefile --name ICHEmbeddingMap apps/02_ich_embedding_map/ich_embedding_map.py
pyinstaller --onefile --name RLTightropeDemo apps/03_rl_tightrope_demo/rl_tightrope_demo.py
pyinstaller --onefile --name MotionFeatureExtractor apps/04_motion_feature_extractor/motion_feature_extractor.py
pyinstaller --onefile --name RhythmMotionMatcher apps/05_rhythm_motion_matcher/rhythm_motion_matcher.py
```

Suggested release folder:

```text
release/
├── AttentionVisualizer.exe
├── ICHEmbeddingMap.exe
├── RLTightropeDemo.exe
├── MotionFeatureExtractor.exe
├── RhythmMotionMatcher.exe
├── data/
└── README_for_audience.md
```

Notes:

- Do not commit `build/`, `dist/`, or `.spec` files.
- App 04 reads keypoint CSV. Future versions can add MediaPipe/OpenPose extraction.
- App 05 reads signal CSV. Future versions can add Librosa beat detection.
