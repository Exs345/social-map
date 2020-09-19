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