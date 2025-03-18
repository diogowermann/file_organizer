document.getElementById("add-rule").addEventListener("click", function () {
    let rulesContainer = document.getElementById("rules-container");
    let ruleDiv = document.createElement("div");
    ruleDiv.classList.add("rule-group", "mb-2");
    ruleDiv.innerHTML = `
        <input type="text" class="form-control rule-key" placeholder="File extension or name (e.g., .pdf or invoice)">
        <input type="text" class="form-control rule-value mt-1" placeholder="Destination folder (e.g., PDFs)">
    `;
    rulesContainer.appendChild(ruleDiv);
});

async function selectFolder(inputId) {
    fetch("/select-folder")
        .then(response => response.json())
        .then(data => {
            if (data.folder) {
                document.getElementById(inputId).value = data.folder;
            } else {
                alert("Folder selection was canceled.");
            }
        })
        .catch(error => console.error("Error selecting folder:", error));
}

document.getElementById("organizer-form").addEventListener("submit", function (e) {
    e.preventDefault();

    let sourceFolder = document.getElementById("source_folder").value;
    let destinationFolder = document.getElementById("destination_folder").value;
    let rules = {};

    document.querySelectorAll(".rule-group").forEach(rule => {
        let key = rule.querySelector(".rule-key").value.trim();
        let value = rule.querySelector(".rule-value").value.trim();
        if (key && value) {
            rules[key] = value;
        }
    });

    fetch("/organize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_folder: sourceFolder, destination_folder: destinationFolder, rules: rules })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response-message").innerHTML = `<div class="alert alert-info">${data.message || data.error}</div>`;
    });
});

document.getElementById("schedule-button").addEventListener("click", function () {
    let sourceFolder = document.getElementById("source_folder").value;
    let destinationFolder = document.getElementById("destination_folder").value;
    let intervalMinutes = document.getElementById("interval").value;
    let rules = {};

    document.querySelectorAll(".rule-group").forEach(rule => {
        let key = rule.querySelector(".rule-key").value.trim();
        let value = rule.querySelector(".rule-value").value.trim();
        if (key && value) {
            rules[key] = value;
        }
    });

    fetch("/schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_folder: sourceFolder, destination_folder: destinationFolder, interval_minutes: intervalMinutes, rules: rules })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response-message").innerHTML = `<div class="alert alert-info">${data.message || data.error}</div>`;
    });
});

document.getElementById("cancel-schedule-button").addEventListener("click", function () {
    fetch("/cancel-schedule", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response-message").innerHTML = `<div class="alert alert-warning">${data.message || data.error}</div>`;
    });
});
