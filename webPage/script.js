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