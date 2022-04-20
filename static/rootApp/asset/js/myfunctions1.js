// $( document ).ready(function() {






function geojsonload(url, syncvalue,  geodata, style, onEachFeature, popupname, check){
    $.ajax({
    url: url,
    async: syncvalue,
    }).done(function(res){
      geodata = L.geoJSON(res, {style: style, onEachFeature: onEachFeature});
      if (popupname) {
        geodata.on('mouseover', function(e){
          e.layer.bindTooltip(e.layer.feature.properties[popupname]).openTooltip();
        })
      }
      if (check) {mymap.addLayer(geodata)}
      
      // $(check).on('change', function(e){
      //   layerTogglefunction(map, geodata, $(this));
      // });
      
    })

    return geodata
}




function geojsonloadpoint(url, geodata, style, onEachFeature, check) {
    $.ajax({
        url: url,
        async: false,
    }).done(function(res) {
        geodata = L.geoJSON(res, {
            pointToLayer: function(feature, latlng) {
                return L.circleMarker(latlng, style);
            },
            onEachFeature: onEachFeature
        });
        if (check) { mymap.addLayer(geodata) }
    })

    return geodata

}





function layerTogglefunction(map, layername, checkbox) {
   if (layername) {
       mymap.removeLayer(layername);
       if (checkbox == true) {
          mymap.removeLayer(layername);
          mymap.addLayer(layername);
          
       } else {
        
           mymap.removeLayer(layername);
       }
   } else {
       alert('Layer not is ready for visualisation.');
       checkbox.prop('checked', false)
   }
 }



function layerseldefine(mapm, layername, layername1) {
  if (layername1){
    mapm.removeLayer(layername1);
    alert(layername1)
  }
   mapm.addLayer(layername);
   layername1 = layername
   return layername1
}


function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7,
        fillColor: 'transparent',
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}
function zoomToFeature(e) {
    mymap.fitBounds(e.target.getBounds());
}



function loadVectorlayerfunction(url, layername, storename) {
   let loaddata;
   loaddata = L.tileLayer.wms(url, {
       layers: storename + ':' + layername,
       format: 'image/png',
       transparent: true,
   });
   return loaddata;
}

var orig
function loadgogletilayer(ltile, url, brin){
  
  $.ajax({
    url: url,
    async: false,
  }).done(function(res){
    if ( res['mapid'] != 'error' ){
      ltile =  L.tileLayer(res['mapid']
      );
       layerseldefine(mymap, ltile, orig)
      if (brin){ltile.bringToBack()};
    }else{
      ltile = undefined;
    }
  })

  return ltile
}
function loadgogletilayercom(ltile, url, brin){
  
  $.ajax({
    url: url,
    async: false,
  }).done(function(res){
    if ( res['mapid'] != 'error' ){
      ltile =  L.tileLayer(res['mapid']
      );
       layerseldefine(mymap2, ltile, orig)
      if (brin){ltile.bringToBack()};
    }else{
      ltile = undefined;
    }
  })

  return ltile
}



// })

