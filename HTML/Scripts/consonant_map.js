var mymap = L.map('mapid').setView([15, 10], 2);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
{
  id: 'mapbox.streets-basic',
  maxZoom: 6,
}).addTo(mymap);

function onEachFeature(feature, layer) {
  if (feature.properties && feature.properties) {
    layer.bindPopup("Langue : " + feature.properties.name + "<br> inventaire de consonnes : " + feature.properties.description1);
  }
}

function getColor(d) {
    return d == 1  ? '#f1eef6' :
           d == 2  ? '#d0d1e6' :
           d == 3  ? '#a6bddb' :
           d == 4  ? '#74a9cf' :
           d == 5  ? '#2b8cbe' :
                     '#045a8d'
}

function pointToLayer(feature, latlng) {
  return L.circleMarker(latlng, {
    radius: 6,
    fillColor: getColor(feature.properties.valueNumber1),
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 1
  });
}

L.geoJson(coordinates, { onEachFeature: onEachFeature, pointToLayer: pointToLayer
}).addTo(mymap);

var legend = L.control({position: 'bottomright'});

legend.onAdd = function(mymap)
{
  var div = L.DomUtil.create('div', 'info legend'),
  grades = [1, 2, 3, 4, 5]
  labels = ["Small", "Moderatly small", "Average", "Moderately large", "Large"];

  // loop through our density intervals and generate a label with a colored square for each interval
  div.innerHTML += "<h4>Inventaire de consonnes</h4>"
  for (var i = 0; i < grades.length; i++)
  {
    div.innerHTML += '<i style="background:' + getColor(grades[i]) + '"></i> ' +
                      labels[i] + '<br>';
  }
  return div;
};

legend.addTo(mymap);
