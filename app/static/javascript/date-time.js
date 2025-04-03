// Function to update Date and Time
function updateDateTime() {
    const dateTimeElement = document.getElementById('date-time');

    // Get the current date and time
    const now = new Date();

    // Extract date and time components
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(now.getDate()).padStart(2, '0');
    const year = now.getFullYear();

    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const isPM = hours >= 12;

    // Convert to 12-hour format
    hours = (hours % 12) || 12; // Convert 0 to 12 for midnight
    const ampm = isPM ? 'PM' : 'AM';

    // Format the date and time string
    const formattedDateTime = `${month}/${day}/${year}, ${hours}:${minutes}:${seconds} ${ampm}`;

    // Set the content of the date-time element
    dateTimeElement.textContent = formattedDateTime;
}

// Update the time every second (1000 milliseconds)
setInterval(updateDateTime, 1000);

// Initial call to set the date-time immediately when the page loads
updateDateTime();
