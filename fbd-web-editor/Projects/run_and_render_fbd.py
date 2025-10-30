#!/usr/bin/env python3
"""Helper: collect arrow input, write Projects/FBDarrows.txt, and optionally run manim-pqp.

Usage examples:
  - Interactive: python3 Projects/run_and_render_fbd.py
  - Non-interactive arrows: python3 Projects/run_and_render_fbd.py --arrows "1,2; -1,0"
  - Dry run (don't call manim): python3 Projects/run_and_render_fbd.py --no-run --arrows "1,2;3,4"
"""

import argparse
import subprocess
import shutil
import os
from pathlib import Path
import sys

OUT_PATH = Path(__file__).resolve().parent / "FBDarrows.txt"


def parse_arrows_arg(s: str):
    parts = [p.strip() for p in s.split(";") if p.strip()]
    arrows = []
    for p in parts:
        p = p.replace(",", " ")
        vals = [v for v in p.split() if v]
        if len(vals) < 2:
            raise ValueError(f"Invalid arrow spec: '{p}' (need at least x and y)")
        if len(vals) == 2:
            vals.append("0")
        arrows.append([float(vals[0]), float(vals[1]), float(vals[2])])
    return arrows


def write_arrows_file(arrows, path: Path = OUT_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(str(len(arrows)) + "\n")
        for a in arrows:
            f.write(str([float(a[0]), float(a[1]), float(a[2])]) + "\n")
    print(f"Wrote {len(arrows)} arrows to {path}")


def run_manim(path: Path = OUT_PATH):
    manim_bin = shutil.which("manim-pqp") or shutil.which("manim")
    if manim_bin is None:
        print("Neither 'manim-pqp' nor 'manim' is on PATH. Install Manim or adjust your PATH.")
        sys.exit(2)

    script_dir = Path(__file__).resolve().parent
    fbd_test_path = script_dir / "FBDtest.py"
    if manim_bin.endswith("manim"):
        cmd = [manim_bin, "-pqp", str(fbd_test_path), "FBD"]
    else:
        cmd = [manim_bin, str(fbd_test_path), "FBD"]

    print("Running:", " ".join(cmd))
    env = dict(**os.environ)
    env["FBD_ARROWS"] = str(path)

    try:
        subprocess.check_call(cmd, env=env)
    except PermissionError as e:
        print(f"Permission error when trying to run {manim_bin}: {e}")
        sys.exit(3)
    except FileNotFoundError:
        print(f"Executable {manim_bin} not found. Install Manim or adjust PATH.")
        sys.exit(2)
    except subprocess.CalledProcessError as e:
        print("manim returned non-zero exit code:", e.returncode)
        sys.exit(e.returncode)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrows", type=str, help="Semicolon-separated vectors, e.g. '1,2; -1,0; 0,3'")
    parser.add_argument("--no-run", action="store_true", help="Do not invoke manim-pqp; only write the arrows file")
    args = parser.parse_args(argv)

    if args.arrows:
        try:
            arrows = parse_arrows_arg(args.arrows)
        except Exception as e:
            print(f"Error parsing --arrows: {e}")
            sys.exit(1)
    else:
        print("This script is intended to be run from the web interface. Please use the web application to modify arrows.")
        sys.exit(1)

    write_arrows_file(arrows, OUT_PATH)

    if not args.no_run:
        run_manim(OUT_PATH)


if __name__ == "__main__":
    main()