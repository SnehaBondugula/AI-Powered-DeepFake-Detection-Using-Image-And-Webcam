// Access the webcam and stream video
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const resultDiv = document.getElementById('webcam-result');

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.error("Webcam error:", error);
        });
}

captureButton.addEventListener('click', function () {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');
    
    fetch('/webcam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `<h3>Result: ${data.result}</h3>`;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
