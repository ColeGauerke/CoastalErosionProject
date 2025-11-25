class RiskLevels {
	static colors = ['#22c55e', '#f97316', '#ef4444', '#b91c1c', '#1e3a8a', '#999999'];

	static determineRisk(predictedDangerLevel) {
        if (predictedDangerLevel == "LOW RISK") {
            return 0;
        }
		else if (predictedDangerLevel == "MODERATE RISK") {
            return 1;
        }
        else if (predictedDangerLevel == "HIGH RISK") {
            return 2;
        }
        else if (predictedDangerLevel == "CRITICAL") {
            return 3;
        }
        else if (predictedDangerLevel == "UNDERWATER") {
            return 4;
        }
		else {
			return 5;
		}
	}

	static getColor(riskLevel) {
		return this.colors[riskLevel];
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
		this.dangerLevel = null;
		this.waterLevel = null;
	}

	updateStyle(waterLevel, dangerLevel) {
		this.dangerLevel = dangerLevel;
		const riskLevel = RiskLevels.determineRisk(dangerLevel);
		const color = RiskLevels.getColor(riskLevel);

		this.layer.setStyle({
			color: color,
			fillColor: color,
			fillOpacity: 0.25,
			weight: 2
		});

		let popupText;
		if (dangerLevel !== null) {
			popupText = this.name + ": " + waterLevel +  " feet above sea level. This is a " + dangerLevel + " risk town";
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

		const bayouCaneJson = {
			"type": "FeatureCollection",
			"features": [
			  {
				"type": "Feature",
				"properties": {},
				"geometry": {
				  "type": "Polygon",
				  "coordinates": [[
					[-90.75393937371751,29.659461210302666],
					[-90.77201013723884,29.65349661167079],
					[-90.76332499492892,29.63718250990685],
					[-90.76360518945003,29.632190317112602],
					[-90.76094358182968,29.628659091672958],
					[-90.77537265859112,29.614167283502766],
					[-90.7739718438442,29.607834026596606],
					[-90.74567330066526,29.59236935105291],
					[-90.72928443954007,29.61161316837274],
					[-90.73404712369924,29.619650472387434],
					[-90.73283426371904,29.63277999075241],
					[-90.75393937371751,29.659461210302666]
				  ]]
				}
			  }
			]
		};
		
		const bayouCaneLayer = L.geoJSON(bayouCaneJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const bayouCane = new Region('Bayou Cane', bayouCaneJson, bayouCaneLayer, [29.626, -90.752], 11);
		bayouCane.updateStyle(null);
		this.region.set('Bayou Cane', bayouCane);
		
		const chauvinJson = {
			"type": "FeatureCollection",
			"features": [
			  {
				"type": "Feature",
				"properties": {},
				"geometry": {
				  "coordinates": [
					[
					  [-90.58452927854887, 29.41657883535167],
					  [-90.57455057560401, 29.433382299931694],
					  [-90.58818813629514, 29.442941651015047],
					  [-90.5911817471788, 29.449314051652394],
					  [-90.57820943335086, 29.48232826324272],
					  [-90.58419665511755, 29.484934190560637],
					  [-90.5915143706101, 29.47422050528874],
					  [-90.60548455473317, 29.47537879613013],
					  [-90.60781291875358, 29.44583824635839],
					  [-90.61779162169786, 29.433961680163904],
					  [-90.60648242502712, 29.42729860791347],
					  [-90.61180439993117, 29.40324997346255],
					  [-90.60714767189036, 29.401221515173617],
					  [-90.60082782669176, 29.421794001127367],
					  [-90.58452927854887, 29.41657883535167]
					]
				  ],
				  "type": "Polygon"
				}
			  }
			]
		};
		
		const chauvinLayer = L.geoJSON(chauvinJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const chauvin = new Region('Chauvin', chauvinJson, chauvinLayer, [29.443, -90.594], 11);
		chauvin.updateStyle(null);
		this.region.set('Chauvin', chauvin);
		
		const cocodrieJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.6353400992966,29.273891993332043],[-90.7243170352215,29.272978884719734],[-90.74760805668424,29.233022399989125],[-90.74996332851772,29.204929362869322],[-90.67590311420348,29.19876156756355],[-90.61885319646315,29.234620958989865],[-90.6353400992966,29.273891993332043]]]}}]};
		
		const cocodrieLayer = L.geoJSON(cocodrieJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const cocodrie = new Region('Cocodrie', cocodrieJson, cocodrieLayer, [29.237, -90.684], 11);
		cocodrie.updateStyle(null);
		this.region.set('Cocodrie', cocodrie);
		
		const cutOffJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.34240294986903,29.46940644277086],[-90.3307561632373,29.49010664115248],[-90.31765352827648,29.493485863869196],[-90.31231541773711,29.478700932354926],[-90.30115391388145,29.479968296725957],[-90.31037428663153,29.50573460119992],[-90.29387467223648,29.517137266117672],[-90.2992127827763,29.52178242798375],[-90.31231541773711,29.530227630477512],[-90.31231541773711,29.547538091200295],[-90.32978559768472,29.563157182023843],[-90.3535644537247,29.542049729408774],[-90.3797697236459,29.561468748068748],[-90.38510783418569,29.550493239503183],[-90.36327010925086,29.530649872095466],[-90.34240294986903,29.46940644277086]]]}}]};
		
		const cutOffLayer = L.geoJSON(cutOffJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const cutOff = new Region('Cut Off', cutOffJson, cutOffLayer, [29.515, -90.334], 11);
		cutOff.updateStyle(null);
		this.region.set('Cut Off', cutOff);
		
		const dulacJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.70673391373018,29.288087400638474],[-90.6866958690512,29.3292336857198],[-90.67570726390458,29.33092427403298],[-90.68023198367077,29.36642015258593],[-90.67796962378767,29.434841549975573],[-90.70867307934441,29.42583395756435],[-90.71028905068981,29.43793772534123],[-90.7219240443741,29.43737479138875],[-90.73679098074919,29.3424758773144],[-90.70673391373018,29.288087400638474]]]}}]};
		
		const dulacLayer = L.geoJSON(dulacJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const dulac = new Region('Dulac', dulacJson, dulacLayer, [29.363, -90.702], 11);
		dulac.updateStyle(null);
		this.region.set('Dulac', dulac);
		
		const gallianoJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.25978590349854,29.386050655645477],[-90.2575920637014,29.399112182481446],[-90.29232786048702,29.465349686210203],[-90.29781245997923,29.47999252900962],[-90.30622217920114,29.478719322290786],[-90.30987857886282,29.48954106956259],[-90.3190195780167,29.487949708621755],[-90.31646009825357,29.4764911720483],[-90.34132361595273,29.47044308879309],[-90.30622217920114,29.40516451637299],[-90.27660534194175,29.41057945708374],[-90.25978590349854,29.386050655645477]]]}}]};
		
		const gallianoLayer = L.geoJSON(gallianoJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const galliano = new Region('Galliano', gallianoJson, gallianoLayer, [29.438, -90.300], 11);
		galliano.updateStyle(null);
		this.region.set('Galliano', galliano);
		
		const goldenMeadowJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.25277746121121,29.364620167782988],[-90.25842473512822,29.384305040325927],[-90.26971928296277,29.396332810335053],[-90.27379786968082,29.40972569840939],[-90.29105342887205,29.397426173449006],[-90.27568029432,29.37309606568479],[-90.27599403175968,29.356690463260534],[-90.25277746121121,29.364620167782988]]]}}]};
		
		const goldenMeadowLayer = L.geoJSON(goldenMeadowJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const goldenMeadow = new Region('Golden Meadow', goldenMeadowJson, goldenMeadowLayer, [29.383, -90.272], 11);
		goldenMeadow.updateStyle(null);
		this.region.set('Golden Meadow', goldenMeadow);
		
		const houmaJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.67332893519664,29.547563162624],[-90.63600753804998,29.54791227624942],[-90.66249369086364,29.582817547728013],[-90.68617070625766,29.593984686380054],[-90.72108427133087,29.599567792227333],[-90.72148557667632,29.612128650422733],[-90.73874170654018,29.612128650422733],[-90.74355737068781,29.598172044735563],[-90.73432734773733,29.593286776421778],[-90.73954431723111,29.585609448249414],[-90.75559653105789,29.59049508831025],[-90.77365527161268,29.60096352040381],[-90.78288529456316,29.582468554731946],[-90.77686571437776,29.576186474467562],[-90.76402394331674,29.57479040353995],[-90.75037956156413,29.56117770039559],[-90.72108427133087,29.568158803013375],[-90.7226894927134,29.583166539516725],[-90.71506469114544,29.568507845478365],[-90.70984772165167,29.581421568504567],[-90.67332893519664,29.547563162624]]]}}]};
		
		const houmaLayer = L.geoJSON(houmaJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const houma = new Region('Houma', houmaJson, houmaLayer, [29.580, -90.705], 11);
		houma.updateStyle(null);
		this.region.set('Houma', houma);
		
		const lafitteJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.10939333992793,29.665742283004477],[-90.12498845383055,29.666273694340774],[-90.11979008252969,29.649532888764597],[-90.1063354744568,29.652721828361763],[-90.09563294530811,29.641560097761598],[-90.09135193364807,29.644749289931383],[-90.08003783140549,29.71462037004335],[-90.09991395696758,29.7170105360546],[-90.10664126100376,29.728960512394096],[-90.1145917112288,29.746219076816985],[-90.12651738656585,29.741440079388127],[-90.11581485741715,29.731084803654767],[-90.11122805921019,29.722321812321624],[-90.12009586907664,29.71647939297044],[-90.10113710315593,29.703199902565586],[-90.09899659732618,29.68619959255122],[-90.10939333992793,29.665742283004477]]]}}]};
		
		const lafitteLayer = L.geoJSON(lafitteJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const lafitte = new Region('Lafitte', lafitteJson, lafitteLayer, [29.694, -90.103], 11);
		lafitte.updateStyle(null);
		this.region.set('Lafitte', lafitte);
		
		const laroseJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.41035250516141,29.57897175148591],[-90.42076848562006,29.56085306627297],[-90.39077046189965,29.55614167566597],[-90.37577145003944,29.557228939152537],[-90.35243965381231,29.536206438505673],[-90.32035843400018,29.551067624696273],[-90.37285497551109,29.58404440072053],[-90.37160505785599,29.58802987483773],[-90.38243767753274,29.59056600368598],[-90.39160374033625,29.574985919679335],[-90.41035250516141,29.57897175148591]]]}}]};
		
		const laroseLayer = L.geoJSON(laroseJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const larose = new Region('Larose', laroseJson, laroseLayer, [29.563, -90.365], 11);
		larose.updateStyle(null);
		this.region.set('Larose', larose);
		
		const lockportJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.5398068917353,29.63489992871733],[-90.52109309683108,29.64384578535676],[-90.5377015898088,29.65421385191],[-90.55314047060479,29.647098627082016],[-90.5398068917353,29.63489992871733]]]}}]};
		
		const lockportLayer = L.geoJSON(lockportJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const lockport = new Region('Lockport', lockportJson, lockportLayer, [29.644, -90.537], 11);
		lockport.updateStyle(null);
		this.region.set('Lockport', lockport);
		
		const mathewsJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.55873141795455,29.703059326457492],[-90.57857423354338,29.684688157769457],[-90.56343103217321,29.67629527185953],[-90.56264776313678,29.65905363306389],[-90.5386275126875,29.665179290588995],[-90.5396718714026,29.67221199294167],[-90.53027264296573,29.673119402585627],[-90.53053373264487,29.67697580222557],[-90.55873141795455,29.703059326457492]]]}}]};
		
		const mathewsLayer = L.geoJSON(mathewsJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const mathews = new Region('Mathews', mathewsJson, mathewsLayer, [29.681, -90.554], 11);
		mathews.updateStyle(null);
		this.region.set('Mathews', mathews);
		
		const montegutJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.55488849746307,29.423547220233544],[-90.56438197212368,29.4412648109263],[-90.55353228679736,29.475510051567227],[-90.53895302213957,29.472853506963347],[-90.55081081490684,29.48531964665004],[-90.55319519284795,29.489989543833104],[-90.55677175975963,29.482379230596976],[-90.57246891453708,29.480822505205097],[-90.5758196355001,29.43313125465285],[-90.56668101679773,29.431227974882262],[-90.55488849746307,29.423547220233544]]]}}]};
		
		const montegutLayer = L.geoJSON(montegutJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const montegut = new Region('Montegut', montegutJson, montegutLayer, [29.457, -90.557], 11);
		montegut.updateStyle(null);
		this.region.set('Montegut', montegut);
		
		const morganCityJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-91.17549718529409,29.683672294593606],[-91.17549724557469,29.695409393839512],[-91.17178192374864,29.70714500072269],[-91.18427926540807,29.706264969048235],[-91.18799475901022,29.71799931971738],[-91.17245771528411,29.735597824031487],[-91.1778619160761,29.73589119146139],[-91.18596819132024,29.724745869005574],[-91.20994971943949,29.7247461664913],[-91.21906960936013,29.71359940633789],[-91.21265203019563,29.688073953242466],[-91.17549718529409,29.683672294593606]]]}}]};
		
		const morganCityLayer = L.geoJSON(morganCityJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const morganCity = new Region('Morgan City', morganCityJson, morganCityLayer, [29.710, -91.197], 11);
		morganCity.updateStyle(null);
		this.region.set('Morgan City', morganCity);
		
		const racelandJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.58214418246267,29.69331666862783],[-90.55997264624646,29.712574998741246],[-90.59402179114984,29.730798230726805],[-90.55403384190323,29.75795501801582],[-90.59639731288671,29.73251723273924],[-90.69379370412027,29.750736842935325],[-90.70448355193865,29.742143099638923],[-90.7104223562826,29.721858945481202],[-90.62252805199863,29.707072995520647],[-90.60035651578244,29.70604133635399],[-90.58214418246267,29.69331666862783]]]}}]};
		
		const racelandLayer = L.geoJSON(racelandJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const raceland = new Region('Raceland', racelandJson, racelandLayer, [29.726, -90.632], 11);
		raceland.updateStyle(null);
		this.region.set('Raceland', raceland);
		
		const thibodauxJson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-90.81300108055677,29.836445440790214],[-90.83434693034336,29.79800226714201],[-90.85409625966464,29.80402431904392],[-90.87492968244904,29.767419318153586],[-90.86211686826447,29.759077368419796],[-90.8493010661654,29.787808625850204],[-90.84289365331911,29.789662184055032],[-90.84930405407943,29.775760573287357],[-90.82687786720197,29.77437232617656],[-90.81352662343345,29.771595451798504],[-90.81299261649781,29.761864884698383],[-90.80285373489562,29.74332338396742],[-90.79698331538816,29.747492514660294],[-90.8076565094192,29.759546193827646],[-90.7996517372245,29.767421709674124],[-90.8076565094192,29.77159423987402],[-90.79591627472529,29.793368075108177],[-90.80659060492061,29.798001695248146],[-90.80392533717598,29.821625055237774],[-90.81300108055677,29.836445440790214]]]}}]};
		
		const thibodauxLayer = L.geoJSON(thibodauxJson, {
			style: { 
				color: '#999999', 
				fillColor: '#999999', 
				fillOpacity: 0.25, 
				weight: 2 
			}
		}).addTo(this.map);
		const thibodaux = new Region('Thibodaux', thibodauxJson, thibodauxLayer, [29.798, -90.833], 11);
		thibodaux.updateStyle(null);
		this.region.set('Thibodaux', thibodaux);
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
			city: this.city,
			year: parseInt(this.year),
		};

		try {
			const response = await fetch('http://localhost:5073/api/Coasty/GetRisks', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(dataToSend)
			});

			const data = await response.json();

			console.log("Success:", data);

			const dangerLevel = data[0];

			const region = this.region.get(this.city);
			if (region != null) {
				region.updateStyle(dangerLevel[this.year + "_worst_case"].toFixed(3), dangerLevel[this.year + "_status"]);
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