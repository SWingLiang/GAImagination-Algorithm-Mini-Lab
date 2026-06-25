# Codex Task Plan — GAImagination Algorithm Mini Lab V2.0

Goal: build five runnable mini apps for Lecture 4 QR-code sharing.

## V2.0 Scope

1. Attention Visualizer
2. ICH Embedding Map
3. RL Tightrope Demo
4. Motion Feature Extractor
5. Rhythm-Motion Matcher

## App 04 — Motion Feature Extractor

Path: `apps/04_motion_feature_extractor/motion_feature_extractor.py`

Deliverables:

- Read `frame,time,x,y` keypoint trajectory CSV.
- Auto-generate sample motion if no input exists.
- Extract duration, path length, displacement, speed, acceleration, turning energy, bbox size, rhythm peak count.
- Export `outputs/motion_features.csv`.
- Export `outputs/motion_timeseries.csv`.
- Export `outputs/motion_trajectory.png`.

Future upgrades:

- Add multi-keypoint support.
- Add MediaPipe/OpenPose video-to-keypoints pipeline.
- Add Lion-11 / Lion-16 schema mapping.
- Add feature comparison across multiple performances.

## App 05 — Rhythm-Motion Matcher

Path: `apps/05_rhythm_motion_matcher/rhythm_motion_matcher.py`

Deliverables:

- Read motion time series from App 04.
- Read rhythm energy CSV or auto-generate sample rhythm.
- Normalize and align motion intensity with rhythm energy.
- Detect peaks and compute matching score.
- Export `outputs/rhythm_motion_score.csv`.
- Export `outputs/rhythm_motion_alignment.png`.
- Export `outputs/rhythm_motion_summary.md`.

Future upgrades:

- Add WAV input and Librosa beat detection.
- Add tolerance slider and interactive GUI.
- Add separate matching modes for lion dance, Yingge dance, Cantonese opera, and dragon boat.

## Acceptance Criteria

- The five apps run independently.
- No cloud API key is required.
- All generated files go to `outputs/`.
- The repository can be shared by QR code at the end of Lecture 4.
