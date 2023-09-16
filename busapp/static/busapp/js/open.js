document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const photo = document.getElementById('photo');
    const captureButton = document.getElementById('capture');

    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err) {
            console.error('Error accessing the camera: ', err);
        });

    captureButton.addEventListener('click', function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageDataURL = canvas.toDataURL('image/png');
        photo.src = imageDataURL;

        // Send the captured image data to the server (e.g., using AJAX).
        // You can use Django views to process and save the image.
    });
});
