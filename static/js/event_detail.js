function initialize() {
  var lat = document.getElementById('id_lat').value || -35.245619;
  var lng = document.getElementById('id_lng').value || -65.492249;

  console.log(lat, lng);

  var myLatlng = new google.maps.LatLng(lat, lng);
  var mapOptions = {
    zoom: 4,
    center: myLatlng
  }
  
  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: 'Aca es el evento.'
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

