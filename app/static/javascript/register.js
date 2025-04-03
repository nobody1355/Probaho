// app/static/javascript/register.js

// Handle image upload and preview
document.getElementById('user_image').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const preview = document.getElementById('profile-img-preview');
        preview.src = e.target.result;  // Set the preview image to the uploaded file
    };

    if (file) {
        reader.readAsDataURL(file);  // Convert the file to a data URL and preview it
    }
});
