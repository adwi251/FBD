from flask import Flask, request, jsonify, render_template
from pathlib import Path

app = Flask(__name__)
FBDARROWS_PATH = Path(__file__).resolve().parent.parent / "Projects" / "FBDarrows.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arrows', methods=['GET'])
def get_arrows():
    if FBDARROWS_PATH.exists():
        with open(FBDARROWS_PATH, 'r') as f:
            arrows = f.readlines()
        return jsonify({'arrows': [line.strip() for line in arrows]})
    return jsonify({'arrows': []})

@app.route('/arrows', methods=['POST'])
def update_arrows():
    data = request.json
    arrows = data.get('arrows', [])
    
    with open(FBDARROWS_PATH, 'w') as f:
        f.write(f"{len(arrows)}\n")
        for arrow in arrows:
            f.write(f"{arrow}\n")
    
    return jsonify({'message': 'FBDarrows.txt updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)