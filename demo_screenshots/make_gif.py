"""
Assemble PNG frames into an animated GIF.
Usage: python make_gif.py <gif_name>
Frames must be in gif_frames/<gif_name>/ named 001.png, 002.png, etc.
Each frame can have an optional duration file: 001.dur containing seconds (float).
Default duration: 0.8s. Output: gif_name.gif in demo_screenshots/.
"""
import sys
import os
from pathlib import Path
from PIL import Image
import imageio.v3 as iio
import numpy as np

BASE = Path(__file__).parent

def make_gif(name: str, default_dur: float = 0.8):
    frames_dir = BASE / "gif_frames" / name
    out_path = BASE / f"{name}.gif"

    frame_files = sorted(frames_dir.glob("*.png"))
    if not frame_files:
        print(f"No frames found in {frames_dir}")
        sys.exit(1)

    frames = []
    durations = []  # milliseconds for each frame

    for f in frame_files:
        dur_file = f.with_suffix(".dur")
        dur = float(dur_file.read_text().strip()) if dur_file.exists() else default_dur
        img = Image.open(f).convert("RGB")
        frames.append(np.array(img))
        durations.append(int(dur * 1000))

    iio.imwrite(
        out_path,
        frames,
        duration=durations,
        loop=0,  # loop forever
        plugin="pillow",
    )
    total = sum(durations) / 1000
    print(f"Saved {out_path} — {len(frames)} frames, {total:.1f}s total, {out_path.stat().st_size // 1024}KB")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_gif.py <gif_name>")
        sys.exit(1)
    make_gif(sys.argv[1])
