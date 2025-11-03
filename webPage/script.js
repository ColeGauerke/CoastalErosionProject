var map = L.map('map').setView([29.2366, -89.9873], 11);

L.tileLayer('https://api.maptiler.com/maps/basic-v2/{z}/{x}/{y}.png?key=TU8rhOOYPA13t1QOPLwD', {
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    opacity: .55
}).addTo(map);

key = 'TU8rhOOYPA13t1QOPLwD';

L.maptiler.maptilerLayer({
    apiKey: key,
    style: 'https://api.maptiler.com/maps/019a0e17-9b7e-7cb8-9bd2-51da8bf36ad8/style.json?key=' + key,
}).addTo(map);

const dataToSend = {
    startDate: "1/1/15",
    endDate: "12/31/15",
    city: "Grand Isle", 
    state: "LA",
    period: "month" 
};

  fetch('https://localhost:7108/api/Coasty/GetVerifiedWaterLevels', {
    method: 'POST', // Specify the HTTP method as POST
    headers: {
      'Content-Type': 'application/json' // Indicate the type of data being sent
    },
    body: JSON.stringify(dataToSend) // Convert the JavaScript object to a JSON string
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('HTTP error! status: ${response.status}');
    }
    return response.json(); // Parse the JSON response from the server
  })
  .then(data => {
    console.log('Success:', data); // Handle the successful response data
  })
  .catch(error => {
    console.error('Error:', error); // Handle any errors during the request
  });