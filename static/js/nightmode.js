// nightmode.js

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("night-toggle");

    // Apply stored theme preference
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        toggleBtn.innerText = "☀️ Light Mode";
    }

    toggleBtn.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");

        // Update button text and store preference
        if (document.body.classList.contains("dark-mode")) {
            toggleBtn.innerText = "☀️ Light Mode";
            localStorage.setItem("theme", "dark");
        } else {
            toggleBtn.innerText = "🌙 Night Mode";
            localStorage.setItem("theme", "light");
        }
    });
});
