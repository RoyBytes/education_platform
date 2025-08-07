async function ask() {
    const prompt = document.getElementById("prompt").value;
    const responseBox = document.getElementById("response");
    responseBox.innerHTML = "Thinking...";

    const response = await fetch('/ask', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt: prompt})
    });

    const data = await response.json();
    responseBox.innerHTML = `<p><strong>Answer:</strong></p><div> ${data.answer}</div>`;
}
