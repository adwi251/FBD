// This file handles user interactions on the web page, such as form submissions and AJAX requests to the server to update FBDarrows.txt.

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("arrow-form");
    const arrowInput = document.getElementById("arrow-input");
    const responseDiv = document.getElementById("response");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const arrows = arrowInput.value;

        fetch("/update-arrows", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ arrows: arrows })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                responseDiv.textContent = "Arrows updated successfully!";
            } else {
                responseDiv.textContent = "Error updating arrows: " + data.error;
            }
        })
        .catch(error => {
            responseDiv.textContent = "Error: " + error;
        });
    });
});