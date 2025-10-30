# fbd-web-editor

This project is a web-based editor for managing arrow data used in the FBD (Free Body Diagram) rendering process. The application allows users to input arrow vectors through a web interface, which are then saved to a text file (`FBDarrows.txt`). This file is subsequently used by a Python script to generate visual representations of the arrows.

## Project Structure

- **server/**: Contains the main server application.
  - `app.py`: The main server application using Flask, handling HTTP requests and serving the HTML page.
  - `requirements.txt`: Lists the dependencies required for the server application.

- **templates/**: Contains HTML templates for the web interface.
  - `index.html`: The main HTML page where users can input arrow data.

- **static/**: Contains static files such as CSS and JavaScript.
  - **css/**: Contains styles for the web interface.
    - `styles.css`: CSS styles defining the layout and appearance of the web page.
  - **js/**: Contains JavaScript code for client-side interactions.
    - `editor.js`: JavaScript code that handles form submissions and AJAX requests to update `FBDarrows.txt`.

- **Projects/**: Contains the scripts for processing and rendering the arrow data.
  - `run_and_render_fbd.py`: The script that processes the `FBDarrows.txt` file.
  - `FBDtest.py`: The script that uses the data from `FBDarrows.txt` for rendering.
  - `FBDarrows.txt`: The text file that stores the arrow data input by users.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fbd-web-editor
   ```

2. **Install dependencies**:
   Navigate to the `server` directory and install the required Python packages:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. **Run the server**:
   Start the Flask server:
   ```bash
   python app.py
   ```

4. **Access the web interface**:
   Open a web browser and go to `http://localhost:5000` to access the arrow input interface.

## Usage

- Use the web interface to input arrow vectors in the specified format.
- Submit the data to save it to `FBDarrows.txt`.
- Run the `run_and_render_fbd.py` script to process the updated arrow data and generate visualizations.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.