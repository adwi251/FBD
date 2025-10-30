// This file handles user interactions on the web page, such as form submissions and AJAX requests to the server to update FBDarrows.txt.

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("arrowForm");
    const arrowInput = document.getElementById("arrows");
    const responseDiv = document.getElementById("responseMessage");

    function parseArrows(input) {
        // Remove whitespace and split by semicolon
        const arrowStrings = input.split(';').map(s => s.trim()).filter(s => s);
        const arrows = [];
        
        for (const arrowStr of arrowStrings) {
            // Split by comma and convert to numbers
            const coords = arrowStr.split(',').map(n => parseFloat(n.trim()));
            
            if (coords.length !== 2 || coords.some(n => isNaN(n))) {
                throw new Error(`Invalid arrow format: ${arrowStr}. Expected "x,y"`);
            }
            
            // Add default z-coordinate of 0
            arrows.push([coords[0], coords[1], 0]);
        }
        
        return arrows;
    }

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        responseDiv.textContent = "Processing...";
        
        try {
            const arrows = parseArrows(arrowInput.value);
            
            fetch("arrows", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ arrows: arrows })
            })
            .then(response => response.json())
            .then(data => {
                responseDiv.textContent = data.message || "Arrows updated successfully!";
                if (data.error) {
                    responseDiv.classList.add("error");
                } else {
                    responseDiv.classList.remove("error");
                }
            })
            .catch(error => {
                responseDiv.textContent = "Network error: " + error.message;
                responseDiv.classList.add("error");
            });
        } catch (error) {
            responseDiv.textContent = "Input error: " + error.message;
            responseDiv.classList.add("error");
            return;
        }
    });

    // Load existing arrows when page loads
    fetch("arrows")
        .then(response => response.json())
        .then(data => {
            if (data.arrows && data.arrows.length > 1) {
                // Skip the first line (count) and parse the arrow data
                const arrowData = data.arrows.slice(1).map(line => {
                    try {
                        const arr = JSON.parse(line);
                        return `${arr[0]},${arr[1]}`;
                    } catch (e) {
                        return '';
                    }
                }).filter(s => s);
                
                arrowInput.value = arrowData.join('; ');
            }
        })
        .catch(error => {
            console.error("Error loading arrows:", error);
        });
});