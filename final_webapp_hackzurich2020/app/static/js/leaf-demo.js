var map = L.map( 'map', {
  center: [47.37, 8.54],
  minZoom: 2,
  zoom: 14
})

L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  subdomains: ['a', 'b', 'c']
}).addTo( map )

var myURL = jQuery( 'script[src$="leaf-demo.js"]' ).attr( 'src' ).replace( 'leaf-demo.js', '' )
// add a marker in the given location
L.marker(center).addTo(map);

function onMapClick(e) {
  var lat  = e.latlng.lat.toFixed(5);
  var lon  = e.latlng.lng.toFixed(5);
  var gps = "";
  if (lat>0) gps+='N'; else gps+='S';
  if (10>Math.abs(lat))  gps += "0";
  gps += Math.abs(lat).toFixed(5)+" ";
  if (lon>0) gps+='E'; else gps+='W';
  if (10>Math.abs(lon))  gps += "0";
  if (100>Math.abs(lon)) gps += "0";
  gps += Math.abs(lon).toFixed(5);
  var textArea = document.createElement("textarea");
  textArea.style.position = 'fixed';
  textArea.style.top = 0;
  textArea.style.left = 0;
  textArea.style.width = '2em';
  textArea.style.height = '2em';
  textArea.style.padding = 0;
  textArea.style.border = 'none';
  textArea.style.outline = 'none';
  textArea.style.boxShadow = 'none';
  textArea.style.background = 'transparent';
  textArea.value = gps;
  document.body.appendChild(textArea);
  textArea.select();
  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'Successfully' : 'Unsuccessfully';
    console.log(msg + ' copied ' + gps + ' to clipboard ');
  } catch (err) {
    console.log('Oops, unable to copy');
  }
  document.body.removeChild(textArea);
}

map.on('click', onMapClick);


// Initialise the FeatureGroup to store editable layers
var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);

var drawPluginOptions = {
  position: 'topright',
  draw: {
    polygon: {
      allowIntersection: false, // Restricts shapes to simple polygons
      drawError: {
        color: '#e1e100', // Color the shape will turn when intersects
        message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
      },
      shapeOptions: {
        color: '#97009c'
      }
    },
    // disable toolbar item by setting it to false
    polyline: false,
    circle: false, // Turns off this drawing tool
    rectangle: false,
    marker: false,
  },
  edit: {
    featureGroup: editableLayers, //REQUIRED!!
    remove: false
  }
};

// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);

var editableLayers = new L.FeatureGroup();
map.addLayer(editableLayers);

map.on('draw:created', function(e) {
  var type = e.layerType,
    layer = e.layer;

  if (type === 'marker') {
    layer.bindPopup('A popup!');
  }

  editableLayers.addLayer(layer);
});