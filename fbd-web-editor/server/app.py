from flask import Flask, request, jsonify, render_template, send_file
from pathlib import Path
import json
import subprocess
import sys
import mimetypes


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
MEDIA_DIR = Path(__file__).resolve().parents[3] / "media"

app = Flask(__name__, template_folder=str(TEMPLATES_DIR), static_folder=str(STATIC_DIR))
FBDARROWS_PATH = Path(__file__).resolve().parent.parent / "Projects" / "FBDarrows.txt"
RENDER_SCRIPT = Path(__file__).resolve().parent.parent / "Projects" / "run_and_render_fbd.py"

def validate_arrow(arrow):
    """Validate a single arrow data structure."""
    if not isinstance(arrow, list) or len(arrow) != 3:
        return False
    return all(isinstance(x, (int, float)) for x in arrow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image/<path:filename>')
def serve_image(filename):
    """Serve images from the media directory."""
    try:
        file_path = MEDIA_DIR / filename
        # Security: ensure the requested path is within MEDIA_DIR
        if not file_path.resolve().is_relative_to(MEDIA_DIR.resolve()):
            return jsonify({'error': 'Invalid path'}), 403
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, mimetype='image/png')
    except Exception as e:
        app.logger.error(f"Error serving image: {e}")
        return jsonify({'error': 'Error serving image'}), 500

@app.route('/arrows', methods=['GET'])
def get_arrows():
    if FBDARROWS_PATH.exists():
        with open(FBDARROWS_PATH, 'r') as f:
            arrows = f.readlines()
        return jsonify({'arrows': [line.strip() for line in arrows]})
    return jsonify({'arrows': []})

@app.route('/arrows', methods=['POST'])
def update_arrows():
    try:
        data = request.json
        if not data or 'arrows' not in data:
            return jsonify({'error': 'No arrow data provided'}), 400

        arrows = data['arrows']
        if not isinstance(arrows, list):
            return jsonify({'error': 'Arrows must be provided as a list'}), 400

        # Validate each arrow
        if not all(validate_arrow(arrow) for arrow in arrows):
            return jsonify({'error': 'Invalid arrow format. Each arrow must be [x, y, angle]'}), 400

        # Save arrows to file
        with open(FBDARROWS_PATH, 'w') as f:
            f.write(f"{len(arrows)}\n")
            for arrow in arrows:
                f.write(json.dumps(arrow) + '\n')

        # Attempt to render the scene synchronously by calling the helper script.
        # Build an arrows string in the same format the script expects: "x,y; x,y; ..."
        try:
            arrow_strs = []
            for a in arrows:
                # include angle if present (third value)
                if len(a) >= 3:
                    arrow_strs.append(f"{a[0]},{a[1]},{a[2]}")
                else:
                    arrow_strs.append(f"{a[0]},{a[1]}")
            arrows_arg = ";".join(arrow_strs)

            proc = subprocess.run(
                [sys.executable, str(RENDER_SCRIPT), "--arrows", arrows_arg],
                capture_output=True,
                text=True,
                timeout=120,
            )

            # Locate the most recent rendered image for the scene.
            repo_root = Path(__file__).resolve().parents[3]
            scene_module = (RENDER_SCRIPT.parent / "FBDtest.py").stem
            images_dir = repo_root / "media" / "images" / scene_module
            rendered_file = None
            if images_dir.exists() and images_dir.is_dir():
                files = [p for p in images_dir.iterdir() if p.is_file()]
                if files:
                    rendered_file = max(files, key=lambda p: p.stat().st_mtime)

            resp = {
                'message': 'Arrows updated successfully',
                'count': len(arrows),
                'render_returncode': proc.returncode,
                'stdout': proc.stdout,
                'stderr': proc.stderr,
            }
            if rendered_file:
                # Convert absolute path to relative path from MEDIA_DIR for serving
                try:
                    rel_path = rendered_file.relative_to(MEDIA_DIR)
                    resp['rendered_image'] = str(rel_path)
                except ValueError:
                    resp['rendered_image'] = str(rendered_file)

            # If the renderer failed, return 500 so client knows there was an error during render.
            status = 200 if proc.returncode == 0 else 500
            return jsonify(resp), status

        except subprocess.TimeoutExpired as e:
            app.logger.error(f"Render timed out: {e}")
            return jsonify({'error': 'Rendering timed out'}), 504
        except Exception as e:
            app.logger.error(f"Unexpected error while rendering: {e}")
            return jsonify({'error': 'Server error while rendering arrows'}), 500

    except Exception as e:
        app.logger.error(f"Error updating arrows: {str(e)}")
        return jsonify({'error': 'Server error while processing arrows'}), 500

if __name__ == '__main__':
    app.run(debug=True)