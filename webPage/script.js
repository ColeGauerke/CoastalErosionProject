class RiskLevels {
	static colors = ['#64b5f6', '#ff9999', '#c41e3a', '#999999'];
	static risk = ['moderate', 'high', 'extreme', 'unknown'];

	static determineRisk(predictedWaterLevel) {
        if (predictedWaterLevel == null) {
            return 3;
        }
        if (predictedWaterLevel >= .05) {
            return 0;
        }
        else if (predictedWaterLevel <= -.05) {
            return 2;
        }
        else {
            return 1;
        }
	}

	static getColor(riskLevel) {
		return this.colors[riskLevel];
	}

	static getRiskName(riskLevel) {
		return this.risk[riskLevel];
	}
}

class Region {
    name = null;
    geoJson = null;
    layer = null;
    center = null;
    zoom = null;
    waterLevel = null;

	constructor(name, geoJson, layer, center, zoom) {
		this.name = name;
		this.geoJson = geoJson;
		this.layer = layer;
		this.center = center;
		this.zoom = zoom;
		this.waterLevel = null;
	}

	updateStyle(waterLevel) {
		this.waterLevel = waterLevel;
		const riskLevel = RiskLevels.determineRisk(waterLevel);
		const color = RiskLevels.getColor(riskLevel);
		const riskName = RiskLevels.getRiskName(riskLevel);

		this.layer.setStyle({
			color: color,
			fillColor: color,
			fillOpacity: 0.25,
			weight: 2
		});

		let popupText;
		if (waterLevel !== null) {
			popupText = this.name + ": " + waterLevel.toFixed(2) +  " feet above sea level. This is a " + riskName + " risk town";
		} else {
			popupText = this.name;
		}

		this.layer.bindPopup(popupText);
	}

	focusOnMap(map) {
		map.setView(this.center, this.zoom);
	}
}

class CoastMap {
    apiKey = null;
    region = null;
    year = null;
    city = null;
    state = null;

	constructor(mapElementId, apiKey) {
		this.apiKey = apiKey;
		this.region = new Map();
		
		this.year = document.getElementById('year').value;
		this.city = document.getElementById('city').value;
		this.state = document.getElementById('state').value;

		this.initializeMap(mapElementId);
		this.initializeRegion();
		this.setupEventListeners();
	}

	initializeMap(elementId) {
		this.map = L.map(elementId, { minZoom: 10 }).setView([29.2366, -89.9873], 11);

		L.tileLayer('https://api.maptiler.com/maps/basic-v2/{z}/{x}/{y}.png?key=' + this.apiKey, {
			attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
			opacity: 0.55
		}).addTo(this.map);

		L.maptiler.maptilerLayer({
			apiKey: this.apiKey,
			style: 'https://api.maptiler.com/maps/019a0e17-9b7e-7cb8-9bd2-51da8bf36ad8/style.json?key=' + this.apiKey,
		}).addTo(this.map);
	}

	initializeRegion() {
		const grandIsleGeoJson = {
			"type": "FeatureCollection",
			"features": [{
				"type": "Feature",
				"properties": {},
				"geometry": {
					"coordinates": [[
						[-89.95539314390433, 29.269923566778616],
						[-89.9682275827845, 29.257159540630454],
						[-90.00596083309154, 29.237450547513177],
						[-90.05319156816985, 29.210568531312703],
						[-90.08348084392675, 29.189730116863487],
						[-90.08887130825626, 29.180990166522633],
						[-90.08656110925772, 29.16799091463652],
						[-90.04959792528349, 29.188609652024738],
						[-89.99184295032363, 29.231402709080243],
						[-89.95821672045831, 29.250217033002073],
						[-89.94948930201991, 29.26141439304608],
						[-89.9507727459077, 29.266564767009328],
						[-89.95539314390433, 29.269923566778616]
					]],
					"type": "Polygon"
				}
			}]
		};
		const grandIsleLayer = L.geoJSON(grandIsleGeoJson, {
			style: { 
                color: '#999999', 
                fillColor: '#999999', 
                fillOpacity: 0.25, 
                weight: 2 
            }
		}).addTo(this.map);
		const grandIsle = new Region('Grand Isle', grandIsleGeoJson, grandIsleLayer, [29.2366, -89.9873], 11);
		grandIsle.updateStyle(null);
		this.region.set('Grand Isle', grandIsle);

		const portFGeoJson = {
			"type": "FeatureCollection",
			"features": [{
				"type": "Feature",
				"properties": {},
				"geometry": {
					"coordinates": [[
						[-90.08763578628167, 29.16693562585887],
						[-90.08726771501644, 29.17850541354298],
						[-90.08505928742363, 29.20710290045821],
						[-90.101254423103, 29.24982360129549],
						[-90.28234548569856, 29.220274339986517],
						[-90.26026120977265, 29.095881421221023],
						[-90.22400746974094, 29.085252014458547],
						[-90.18284499401163, 29.10475293990808],
						[-90.08763578628167, 29.16693562585887]
					]],
					"type": "Polygon"
				}
			}]
		};
		const portFLayer = L.geoJSON(portFGeoJson, {
			style: { 
                color: '#999999', 
                fillColor: '#999999', 
                fillOpacity: 0.25, 
                weight: 2 
            }
		}).addTo(this.map);
		const portF = new Region('Port Fourchon', portFGeoJson, portFLayer, [29.1056, -90.1944], 11);
		portF.updateStyle(null);
		this.region.set('Port Fourchon', portF);

		const newOrleansGeoJson = {
			"type": "FeatureCollection",
			"features": [{
				"type": "Feature",
				"properties": {},
				"geometry": {
					"coordinates": [[
						[-89.81309249125796, 30.04645690312799],
						[-89.76079130832214, 30.043279804136432],
						[-89.73693462838673, 30.022626177309476],
						[-89.71399551306374, 30.0265983628792],
						[-89.7295941114832, 30.059958436935005],
						[-89.68371588083807, 30.075046207743213],
						[-89.68096318699914, 30.10680241543821],
						[-89.65435381322482, 30.120295714672096],
						[-89.62957956867614, 30.15124396474323],
						[-89.68830370390226, 30.17266399019418],
						[-89.7415224514509, 30.173457235094503],
						[-89.88649766029069, 30.14886367468202],
						[-90.12414689503358, 30.02024278957782],
						[-90.14158062267872, 29.94473922817336],
						[-90.13699279961452, 29.913726416734292],
						[-90.1057956027756, 29.906568241894817],
						[-90.06542275980748, 29.920088806897326],
						[-90.05532954906545, 29.946329368225975],
						[-90.03330799835571, 29.89861411096952],
						[-89.9149421632907, 29.871565316785038],
						[-89.9149421632907, 29.909749716447166],
						[-90.0048634953557, 29.939173537788122],
						[-89.99018246154908, 29.982100796445877],
						[-89.81309249125796, 30.04645690312799]
					]],
					"type": "Polygon"
				}
			}]
		};
		const newOrleansLayer = L.geoJSON(newOrleansGeoJson, {
			style: { 
                color: '#999999', 
                fillColor: '#999999', 
                fillOpacity: 0.25, 
                weight: 2 
            }
		}).addTo(this.map);
		const newOrleans = new Region('New Orleans', newOrleansGeoJson, newOrleansLayer, [29.9509, -90.0758], 11);
		newOrleans.updateStyle(null);
		this.region.set('New Orleans', newOrleans);
	}

	setupEventListeners() {
		document.getElementById('year').addEventListener('change', (e) => {
			this.year = e.target.value;
			console.log('Year changed to:', this.year);
		});

		document.getElementById('city').addEventListener('change', (e) => {
			this.city = e.target.value;
			console.log('City changed to:', this.city);
		});

		document.getElementById('state').addEventListener('change', (e) => {
			this.state = e.target.value;
			console.log('State changed to:', this.state);
		});

		document.getElementById('predictBtn').addEventListener('click', () => {
			this.getPrediction();
		});
	}

	async getPrediction() {
		console.log("User wants a prediction");

		const dataToSend = {
			startDate: "1/1/" + this.year.slice(-2),
			endDate: "1/31/" + this.year.slice(-2),
			city: this.city,
			state: this.state,
			period: "year"
		};

		try {
			const response = await fetch('http://localhost:5073/api/Coasty/GetVerifiedWaterLevels', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(dataToSend)
			});

			const data = await response.json();
			const avgWaterLevel = data[0].avg_verified_ft;

			console.log('Water level:', avgWaterLevel);
			console.log("Success:", data);

			const region = this.region.get(this.city);
			if (region != null) {
				region.updateStyle(avgWaterLevel);
				region.focusOnMap(this.map);
			}

			document.body.insertAdjacentHTML("beforeend", "<p style='color:green'>API Connected Successfully</p>");
		} catch (error) {
			console.error("Error:", error);
			document.body.insertAdjacentHTML("beforeend", "<p style='color:red'>API Connection Failed</p>");
		}
	}
}

const MapPredictor = new CoastMap('map', 'TU8rhOOYPA13t1QOPLwD');