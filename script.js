// Initialize and add the map
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 4,
        center: { lat: -25.344, lng: 131.036 },
    });

    // Fetch live updates from the API
    fetch('https://api.example.com/disasters', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY'
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(disaster => {
            new google.maps.Marker({
                position: { lat: disaster.latitude, lng: disaster.longitude },
                map,
                title: disaster.name,
            });
        });
    })
    .catch(error => console.error('Error fetching data:', error));
}

window.onload = initMap;
