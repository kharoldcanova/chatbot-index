document.getElementById('chatbotForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const userInput = document.getElementById('userInput').value;
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }) // Asegúrate de que esto coincida con la expectativa de tu API
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('chatbotResponse').innerText = data.reply.response;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}); 