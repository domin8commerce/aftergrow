"""Aftergrow Reels: turn a carousel into a 9:16 video with a soft original soundtrack.

Each slide is re-rendered at 1080 x 1920 with its text kept out of the areas Instagram covers (the account
name at the top, the caption and buttons at the bottom). Slides stay on screen long enough to read and
cross-fade into each other. The soundtrack is generated here, so it is ours: Facebook plays it as is, and
on Instagram the post can swap in a track from Instagram's own music library instead.

Usage (from the repo root): python3 -I engine/reel.py <out_dir> [carousel IDs]
Writes <out_dir>/<ID>.mp4 and <out_dir>/<ID>_cover.jpg (the first frame, used as the thumbnail).
"""
import hashlib, pathlib, re, subprocess, sys, tempfile

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import carousel as C  # noqa: E402

FPS = 30
FADE = 0.3           # slide-to-slide transition, seconds (a left swipe, like the carousel)
SR = 44100


def durations(c):
    """Seconds per slide: about 4 words a second, at least 2.8 s and at most 6.5 s. The cover is the hook, and the
    sources slide is there for trust rather than reading, so both are short. A replay counts in our favor."""
    out = []
    for i, s in enumerate(c["slides"]):
        words = len(re.findall(r"[A-Za-z0-9']+", C.alt_for(s)))
        fixed = {"cta": 3.0, "sources": 2.6}
        d = 2.6 if i == 0 else fixed.get(s["t"], min(6.5, max(2.8, words / 4.0 + 0.8)))
        out.append(round(d, 2))
    return out


# ------------------------------------------------------------------ the soundtrack
def _hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


CHORDS = [[48, 55, 59, 64, 67],   # C major 7
          [45, 52, 55, 60, 64],   # A minor 7
          [41, 48, 52, 57, 60],   # F major 7
          [43, 50, 55, 57, 62]]   # G add 9


def soundtrack(seconds, seed):
    """A slow, warm pad with a few soft bell notes: four chords, four seconds each, looped."""
    from scipy.signal import butter, fftconvolve, sosfilt
    rng = np.random.default_rng(seed)
    n = int((seconds + 3) * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    bar = 4.0
    for k in range(int(seconds // bar) + 2):
        notes = CHORDS[k % 4]
        start, length = k * bar, bar + 2.2
        i0, i1 = int(start * SR), min(n, int((start + length) * SR))
        if i0 >= n:
            break
        tt = t[i0:i1] - start
        env = np.minimum(1, tt / 1.4) * np.clip((length - tt) / 2.2, 0, 1)
        pad = np.zeros_like(tt)
        for m in notes:
            f = _hz(m)
            for det in (-0.0023, 0.0, 0.0023):
                ph = rng.uniform(0, 2 * np.pi)
                pad += np.sin(2 * np.pi * f * (1 + det) * tt + ph) + 0.22 * np.sin(4 * np.pi * f * (1 + det) * tt + ph)
        pad *= env * 0.045 * (1 + 0.08 * np.sin(2 * np.pi * 0.21 * tt))
        bass = np.sin(2 * np.pi * _hz(notes[0] - 12) * tt) * np.minimum(1, tt / 0.4) * np.clip((length - tt) / 2.2, 0, 1) * 0.16
        out[i0:i1, 0] += pad + bass
        out[i0:i1, 1] += pad + bass
        for beat in range(4):  # sparse bells, high and soft
            if rng.random() < 0.45:
                b0 = int((start + beat + rng.uniform(0, 0.25)) * SR)
                if b0 >= n:
                    continue
                f = _hz(rng.choice(notes[1:]) + 24)
                bt = np.arange(min(int(2.5 * SR), n - b0)) / SR
                bell = (np.sin(2 * np.pi * f * bt) + 0.18 * np.sin(2 * np.pi * f * 2.76 * bt)) * np.exp(-bt / 0.8) * 0.05
                bell *= np.minimum(1, bt / 0.004)
                pan = rng.uniform(0.25, 0.75)
                out[b0:b0 + len(bt), 0] += bell * (1 - pan) * 2
                out[b0:b0 + len(bt), 1] += bell * pan * 2
    out = sosfilt(butter(2, 4200, "low", fs=SR, output="sos"), out, axis=0)
    ir_t = np.arange(int(2.8 * SR)) / SR
    wet = np.stack([fftconvolve(out[:, ch], rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.9), mode="full")[:n]
                    for ch in (0, 1)], axis=1)
    wet *= np.abs(out).max() / (np.abs(wet).max() + 1e-9)
    mix = out * 0.8 + wet * 0.45
    m = int(seconds * SR)
    mix = mix[:m]
    fade_in, fade_out = int(0.6 * SR), int(2.0 * SR)
    mix[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    mix[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    return mix / (np.abs(mix).max() + 1e-9) * 0.85


def write_wav(path, x):
    from scipy.io import wavfile
    wavfile.write(path, SR, (x * 32767).astype(np.int16))


# ------------------------------------------------------------------ frames and video
def render_frames(c, d):
    from playwright.sync_api import sync_playwright
    paths = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": C.W, "height": C.REEL_H}, device_scale_factor=1)
        for i in range(len(c["slides"])):
            pg.set_content(C.build_slide(c, i, fmt="reel"), wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(80)
            p = d / f"f{i:02d}.png"
            pg.screenshot(path=str(p), clip={"x": 0, "y": 0, "width": C.W, "height": C.REEL_H})
            paths.append(p)
        br.close()
    return paths


def make(c, out_dir):
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    durs = durations(c)
    total = round(sum(durs) - FADE * (len(durs) - 1), 2)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        frames = render_frames(c, tmp)
        seed = int(hashlib.sha1(c["id"].encode()).hexdigest()[:8], 16)
        write_wav(tmp / "music.wav", soundtrack(total, seed))
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for f, dur in zip(frames, durs):
            cmd += ["-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(f)]
        cmd += ["-i", str(tmp / "music.wav")]
        fc = [f"[{i}:v]fps={FPS},format=yuv420p,settb=AVTB[v{i}]" for i in range(len(frames))]
        last, acc = "v0", durs[0]
        for i in range(1, len(frames)):
            off = round(acc - FADE, 3)
            fc.append(f"[{last}][v{i}]xfade=transition=slideleft:duration={FADE}:offset={off}[x{i}]")
            last, acc = f"x{i}", acc + durs[i] - FADE
        fc.append(f"[{len(frames)}:a]atrim=0:{total},loudnorm=I=-16:TP=-1.5:LRA=7[a]")
        cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "[a]",
                "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium",
                "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-ar", str(SR), "-ac", "2",
                "-movflags", "+faststart", "-t", str(total), str(out_dir / f"{c['id']}.mp4")]
        subprocess.run(cmd, check=True)
        from PIL import Image
        Image.open(frames[0]).convert("RGB").save(out_dir / f"{c['id']}_cover.jpg", "JPEG", quality=90, optimize=True)
    return total


if __name__ == "__main__":
    out = sys.argv[1]
    for c in C.load(set(sys.argv[2:]) or None):
        print(c["id"], make(c, out), "seconds")
