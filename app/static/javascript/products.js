// Product Image Preview Functionality
function previewImage(event) {
    const preview = document.getElementById('productImagePreview');  // The image element to show preview
    const file = event.target.files[0];  // The selected file

    // Handle file selection
    if (file) {
        const reader = new FileReader();  // Create a new FileReader to read the image
        reader.onload = function () {
            preview.src = reader.result;  // Set the image preview source to the result of FileReader
        };
        reader.readAsDataURL(file);  // Convert the file to a data URL
    } else {
        // If no file is selected, revert to the default image
        const defaultImageUrl = 'app\static\images\productImage\defaultImage.png';  // Define the default image path
        preview.src = defaultImageUrl;  // Set the default image if no file is selected
    }
}
