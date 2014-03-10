function initialize() {
  var lat = document.getElementById('id_lat').value || -35.245619;
  var lng = document.getElementById('id_lng').value || -65.492249;

  var myLatlng = new google.maps.LatLng(lat, lng);
  var mapOptions = {
    zoom: 4,
    center: myLatlng
  }
  
  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: 'Marcale a los demas donde es el evento.'
  });

  google.maps.event.addListener(map, 'click', function(event) {
    var lat = event.latLng.lat();
    var lng = event.latLng.lng();
                  
    var latLng = new google.maps.LatLng(lat, lng);
    marker.setPosition(latLng);
                                        
    document.getElementById("id_lat").value = lat;
    document.getElementById("id_lng").value = lng
                                                            
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

