
function showAlert(message, type) {
    const customAlert = document.getElementById("custom-alert");
    const alertMessage = document.getElementById("alert-message");
    const closeBtn = document.getElementById("close-btn");

    customAlert.style.backgroundColor = type === "error" ? "#f44336" : "#4CAF50";
    alertMessage.textContent = message;
    customAlert.style.display = "block";

    closeBtn.onclick = function() {
        customAlert.style.display = "none";
    }
}

