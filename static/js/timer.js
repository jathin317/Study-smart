let duration = 25 * 60;
let timeLeft = duration;
let interval = null;

function pad(num) {
    return num.toString().padStart(2, '0');
}

function displayTime() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    document.getElementById("time").innerText = pad(minutes) + ":" + pad(seconds);
}

function start() {
    if (interval)
        return;

    document.getElementById("status").innerText = "Timer running...";
    interval = setInterval(() => {
        timeLeft--;
        displayTime();

        if (timeLeft <= 0) {
            clearInterval(interval);
            interval = null;

            document.getElementById("status").innerText = "Time's up!";
            alert("Time's up!");
            logSession();
        }
    }, 1000);
}

function pause() {
    clearInterval(interval);
    interval = null;

    document.getElementById("status").innerText = "Paused";
}

function reset() {
    pause();
    timeLeft = duration;
    displayTime();

    document.getElementById("status").innerText = "Ready to begin";
}

function logSession() {
    fetch("/log_session", { method: "POST" });
}

document.getElementById("start").onclick = start;
document.getElementById("pause").onclick = pause;
document.getElementById("reset").onclick = reset;

displayTime();
