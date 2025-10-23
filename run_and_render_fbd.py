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
    # expect semicolon-separated vectors, e.g. "1,2; -1,0; 0,3"
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


def interactive_collect():
    while True:
        try:
            n = int(input("Number of arrows: ").strip())
            if n < 0:
                print("Please enter a non-negative integer")
                continue
            break
        except ValueError:
            print("Please enter an integer for number of arrows")
    arrows = []
    for i in range(n):
        while True:
            s = input(f"Arrow {i} (enter as 'x y' or 'x,y' or 'x y z', z optional): ").strip()
            if not s:
                print("Input cannot be empty")
                continue
            try:
                parsed = parse_arrows_arg(s.replace(";", ";"))
            except Exception as e:
                print(f"Parse error: {e}")
                continue
            if len(parsed) != 1:
                print("Please enter a single vector for this prompt")
                continue
            arrows.append(parsed[0])
            break
    return arrows


def write_arrows_file(arrows, path: Path = OUT_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(str(len(arrows)) + "\n")
        for a in arrows:
            # write as Python literal list, matching expectations in FBDtest.py
            f.write(str([float(a[0]), float(a[1]), float(a[2])]) + "\n")
    print(f"Wrote {len(arrows)} arrows to {path}")


def run_manim(path: Path = OUT_PATH):
    # detect available manim executable
    manim_bin = shutil.which("manim-pqp") or shutil.which("manim")
    if manim_bin is None:
        print("Neither 'manim-pqp' nor 'manim' is on PATH. Install Manim or adjust your PATH.")
        sys.exit(2)

    # build command as list so subprocess executes properly
    if manim_bin.endswith("manim"):
        # system 'manim' accepts flags separately; we won't pass the file path as a script arg
        cmd = [manim_bin, "-pqp", "./Projects/FBDtest.py", "FBD"]
    else:
        # manim-pqp is a wrapper executable; call scene without extra script args
        cmd = [manim_bin, "./Projects/FBDtest.py", "FBD"]

    print("Running:", " ".join(cmd))
    # pass the path via environment variable so Manim doesn't treat it as part of the script
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
        arrows = interactive_collect()

    write_arrows_file(arrows, OUT_PATH)

    if not args.no_run:
        run_manim(OUT_PATH)


if __name__ == "__main__":
    main()
