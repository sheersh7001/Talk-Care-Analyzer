document.getElementById('click_to_record').addEventListener('click', function() {
    var speech = true;
    window.SpeechRecognition = window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();
    recognition.interimResults = true;

    recognition.addEventListener('result', e => {
        const transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');

        document.getElementById("convert_text").value = transcript;
        console.log(transcript);
    });

    if (speech == true) {
        recognition.start();
    }
});

document.getElementById('text_form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const text = document.getElementById('convert_text').value;
    const data = { sentence: text };
    
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prediction').innerText = 'Possible Disease : ' + data.prediction;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error occurred. Please try again.');
    });
});