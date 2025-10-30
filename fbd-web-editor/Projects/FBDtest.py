import os

'''python3 -m venv .venv
source .venv/bin/activate
python3 ./fbd-web-editor/server/app.py'''

def load_arrows_from_file(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    arrows = []
    for line in lines[1:]:  # Skip the first line which contains the count
        arrow = eval(line.strip())  # Convert string representation of list to actual list
        arrows.append(arrow)

    return arrows

def render_arrows(arrows):
    # This function would contain the logic to render arrows using a graphics library
    # For now, we'll just print them to the console
    for arrow in arrows:
        print(f"Rendering arrow: {arrow}")

def main():
    arrows_file_path = os.path.join(os.path.dirname(__file__), 'FBDarrows.txt')
    arrows = load_arrows_from_file(arrows_file_path)
    render_arrows(arrows)

if __name__ == "__main__":
    main()
