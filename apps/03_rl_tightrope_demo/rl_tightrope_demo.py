"""GAImagination Mini Lab 03: RL Tightrope Demo."""
from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

ACTIONS = [-1, 0, 1]


class TightropeEnv:
    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)
        self.angle = 0.0
        self.velocity = 0.0
        self.steps = 0

    def reset(self):
        self.angle = self.rng.uniform(-0.12, 0.12)
        self.velocity = self.rng.uniform(-0.03, 0.03)
        self.steps = 0
        return self.state()

    def state(self):
        a_bin = max(-6, min(6, int(round(self.angle * 20))))
        v_bin = max(-6, min(6, int(round(self.velocity * 30))))
        return a_bin, v_bin

    def step(self, action: int):
        push = action * 0.035
        wind = self.rng.uniform(-0.008, 0.008)
        self.velocity += 0.025 * math.sin(self.angle) - push + wind
        self.angle += self.velocity
        self.steps += 1
        done = abs(self.angle) > 0.85 or self.steps >= 220
        reward = 1.0 - abs(self.angle) * 0.7 - abs(self.velocity) * 0.25
        if done and abs(self.angle) > 0.85:
            reward = -12.0
        return self.state(), reward, done


def choose_action(q, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    values = [(q.get((state, a), 0.0), a) for a in ACTIONS]
    return max(values)[1]


def train(episodes: int, out_dir: Path, seed: int = 7):
    random.seed(seed)
    env = TightropeEnv(seed)
    q = {}
    history = []
    alpha = 0.18
    gamma = 0.94
    for ep in range(1, episodes + 1):
        state = env.reset()
        epsilon = max(0.05, 0.55 * (1 - ep / max(episodes, 1)))
        total = 0.0
        done = False
        while not done:
            action = choose_action(q, state, epsilon)
            next_state, reward, done = env.step(action)
            old = q.get((state, action), 0.0)
            future = max(q.get((next_state, a), 0.0) for a in ACTIONS)
            q[(state, action)] = old + alpha * (reward + gamma * future - old)
            total += reward
            state = next_state
        history.append((ep, env.steps, total, epsilon))
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "rl_training_history.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["episode", "survival_steps", "total_reward", "epsilon"])
        w.writerows(history)
    with (out_dir / "rl_policy.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["angle_bin", "velocity_bin", "best_action"])
        states = sorted({s for (s, _a) in q.keys()})
        for s in states:
            best = max([(q.get((s, a), 0.0), a) for a in ACTIONS])[1]
            w.writerow([s[0], s[1], best])
    return q, history


def run_gui(q):
    import tkinter as tk

    env = TightropeEnv(9)
    state = env.reset()
    root = tk.Tk()
    root.title("RL Tightrope Demo - GAImagination")
    canvas = tk.Canvas(root, width=900, height=520, bg="#06101d")
    canvas.pack()

    def tick():
        nonlocal state
        action = max([(q.get((state, a), 0.0), a) for a in ACTIONS])[1]
        state, _reward, done = env.step(action)
        canvas.delete("all")
        canvas.create_text(450, 34, text="RL Tightrope Demo / 强化学习走钢丝", fill="#00e6d2", font=("Arial", 22, "bold"))
        canvas.create_line(90, 360, 810, 360, fill="#77dfff", width=3)
        x = 450 + env.angle * 180
        y = 350
        canvas.create_oval(x - 14, y - 70, x + 14, y - 42, outline="#eaf7ff", width=2)
        canvas.create_line(x, y - 42, x, y - 5, fill="#eaf7ff", width=3)
        canvas.create_line(x, y - 28, x - 55, y - 45, fill="#00e6d2", width=3)
        canvas.create_line(x, y - 28, x + 55, y - 45, fill="#00e6d2", width=3)
        canvas.create_line(x, y - 5, x - 28, y + 32, fill="#eaf7ff", width=3)
        canvas.create_line(x, y - 5, x + 28, y + 32, fill="#eaf7ff", width=3)
        canvas.create_text(450, 440, text=f"Try → Error → Feedback → Adjust → Mastery | steps: {env.steps}", fill="#cbe7f5", font=("Arial", 16))
        if done:
            state = env.reset()
        root.after(45, tick)

    tick()
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Train a Q-learning tightrope agent.")
    parser.add_argument("--episodes", type=int, default=600)
    parser.add_argument("--out-dir", default="outputs")
    parser.add_argument("--gui", action="store_true", help="Show a Tkinter animation after training.")
    args = parser.parse_args()
    q, history = train(args.episodes, Path(args.out_dir))
    print(f"Generated: {args.out_dir}/rl_training_history.csv")
    print(f"Generated: {args.out_dir}/rl_policy.csv")
    print(f"Last 20 episodes average survival: {sum(h[1] for h in history[-20:]) / min(20, len(history)):.1f} steps")
    if args.gui:
        run_gui(q)


if __name__ == "__main__":
    main()
