// $( document ).ready(function() {

const geojsonurl = "http://boundapi.cersgis.org/";
const geoserverUrl = "http://socrates.cersgis.org:8080/geoserver/cite/wms?";

$("#asd").mousedown(function() {
    mymap.dragging.disable();
});

$(".side").mousedown(function() {
    mymap.dragging.disable();
});

$("#toolbox").click(function() {
    mymap.dragging.disable();
});

$("html").mouseup(function() {
    mymap.dragging.enable();
});

var ghanabounds;

ghanabounds = L.latLngBounds([3.7388, -4.262], [12.1748, 2.2]);

function mapdisbled(map) {
    mymap.touchZoom.disable();
    mymap.doubleClickZoom.disable();
    mymap.scrollWheelZoom.disable();
    //map.dragging.disable();
    mymap.keyboard.disable();
    if (map.tap) map.tap.disable();
}
//enabled map
function mapenabled(map) {
    mymap.touchZoom.enable();
    mymap.doubleClickZoom.enable();
    mymap.scrollWheelZoom.enable();
    //map.dragging.enable();
    mymap.keyboard.enable();
    if (mymap.tap) mymap.tap.enable();
} //

// ################################  map tools  ####################################

$("#reload").on("click", function() {
    location.reload();
});

$("#zin").on("click", function() {
    mapdisbled(mymap);
    mymap.zoomIn(1);
});

$("#zout").on("click", function() {
    mapdisbled(mymap);
    mymap.zoomOut(1);
});

$("#Zoomextent").on("click", function() {
    mymap.setView([6.155785, -1.936499], 9);
    mymap.panTo(new L.LatLng(6.155785, -1.936499));
});

// ################################  Load region boundary  ####################################

function regionstlye() {
    return {
        fillColor: "transparent",
        weight: 2,
        opacity: 1,
        color: "black",
        dashArray: "3",
        fillOpacity: 0.7,
    };
}

function regionresetHighlight(e) {
    regionboundary.resetStyle(e.target);
}

function regiononEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: regionresetHighlight,
        click: zoomToFeature,
    });
}

// var regionboundary = geojsonload(
//      "/map/region/",
//     false,
//     regionboundary,
//     regionstlye,
//     regiononEachFeature,
//     "region"
// );
var regionboundary 

 $.get("/map/district/",function(res) {

      regionboundary = L.geoJSON(res, {style: regionstlye, onEachFeature: regiononEachFeature});
      
        regionboundary.on('mouseover', function(e){
          e.layer.bindTooltip(e.layer.feature.properties["region"]).openTooltip();
        })
      
      // if (check) {mymap.addLayer(regionboundary)}
      $("#loadregion").addClass("hidden")
    }
    );

$("body").on("click", "#regionCheck", function() {
    if (regionboundary) {
        layerTogglefunction(mymap, regionboundary, $(this).hasClass("on"));
    }
});

// ################################  Load district boundary  ####################################

function districtstye() {
    return {
        fillColor: "transparent",
        weight: 2,
        opacity: 1,
        color: "#b7a",
        dashArray: "3",
        fillOpacity: 0.7,
    };
}

function districtresetHighlight(e) {
    districtboundary.resetStyle(e.target);
}

function districtonEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: districtresetHighlight,
        click: districtzoomToFeature,
    });
}

function districtzoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
    $("#mapchart").show();
    $("#maploader").show();
    $.get(
        geojsonurl +
        "calculatearea/?districtcode=" +
        e.target.feature.properties.district,
        function(data) {
            $("#containerdiv").html(data);
            $("#maploader").hide();
        }
    );
}

// var districtboundary = geojsonload(
//     "/map/district/",
//     false,
//     districtboundary,
//     districtstye,
//     districtonEachFeature,
//     "district_n"
// );

var districtboundary 

 $.get("/map/district/",function(res) {

      districtboundary = L.geoJSON(res, {style: districtstye, onEachFeature: districtonEachFeature});
     
        districtboundary.on('mouseover', function(e){
          e.layer.bindTooltip(e.layer.feature.properties["district_n"]).openTooltip();
        })
      $("#loaddistrict").addClass("hidden")

    }
    );







$("#districtCheck").on("click", function(e) {
    if (districtboundary) {
        layerTogglefunction(mymap, districtboundary, $(this).hasClass("on"));
    }
});

// ################################  Load protected Areas  ####################################
function protectedareastye() {
    return {
        fillColor: "transparent",
        weight: 2,
        opacity: 1,
        color: "green",
        dashArray: "3",
        fillOpacity: 1,
    };
}

function proectedarearesetHighlight(e) {
    proectedarea.resetStyle(e.target);
}

function proectedareaEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: proectedarearesetHighlight,
        click: zoomToFeature,
    });
}
// var proectedarea = geojsonload(
//     "/map/protectarea/",
//     false,
//     proectedarea,
//     protectedareastye,
//     proectedareaEachFeature,
//     "reserve_na"
// );

var proectedarea
 $.get("/map/protectarea/",function(res) {

      proectedarea = L.geoJSON(res, {style: protectedareastye, onEachFeature: proectedareaEachFeature});
     
        proectedarea.on('mouseover', function(e){
          e.layer.bindTooltip(e.layer.feature.properties["reserve_na"]).openTooltip();
        })
     
     $("#loadprotected").addClass("hidden")

    }
    );








$("#proectedCheck").on("click", function(e) {
    if (proectedarea) {
        // alert()
        layerTogglefunction(mymap, proectedarea, $(this).hasClass("on"));
    }
});

// ################################  Load settlement boundary  ####################################
var communityboundary = loadVectorlayerfunction(
    geoserverUrl,
    "COMMUNITY",
    "cite"
);
$("#settlementCheck").on("click", function(e) {
    layerTogglefunction(mymap, communityboundary, $(this).hasClass("on"));
});

// ################################   Load ecowas boundary   ######################################
var ecowasboundary = loadVectorlayerfunction(
    geoserverUrl,
    "ECOWAS_boundary",
    "cite"
);
mymap.addLayer(ecowasboundary);
$("#ecowasCheck").on("click", function(e) {
    alert();
    layerTogglefunction(mymap, ecowasboundary, $(this).hasClass("on"));
});

function checkDate(dateText) {
    var arrDate = dateText.split("-");
    var today = new Date();
    useDate = new Date(arrDate[2], arrDate[1] - 1, arrDate[0]);
    return false;
}

function loadtilelayer(url, layer) {
    $("#overlay").css("display", "block");
    if (layer) {
        mymap.removeLayer(layer);
    }

    $.get(url, function(res) {
        layer = L.tileLayer(res["mapid"]);
        mymap.addLayer(layer);
        $("#overlay").css("display", "none");
    });
    return layer;
}

var layerssm, compare, query1, query2, inactivechangedet, activechangedet;

$("body").on("click", "#query1", function() {
    $("#overlay").css("display", "block");

    // loadtilelayer('/getdata/?from='+$("#from").val()+'&to='+$("#to").val()+'&color=gold' , query1 )

    if (query1) {
        mymap.removeLayer(query1);
    }

    $.get(
        "/map/getdata/?from=" +
        $("#from").val() +
        "&to=" +
        $("#to").val() +
        "&color=gold",
        function(res) {
            if (res["mapid"] == "error") {
                $("#alert").removeClass("hidden");
                $("#overlay").css("display", "none");
            } else if (res["mapid"] == "no_image") {
                $("#noimage").removeClass("hidden");
                $("#overlay").css("display", "none");
            } else {
                query1 = L.tileLayer(res["mapid"]);
                mymap.addLayer(query1);
                $("#overlay").css("display", "none");
            }

            if (
                $("#from1").val() &&
                $("#to1").val() &&
                $("#to").val() &&
                $("#to").val()
            ) {
                $.get(
                    "/map/getchangedetectionactive/?from=" +
                    $("#from").val() +
                    "&to=" +
                    $("#to").val() +
                    "&from1=" +
                    $("#from1").val() +
                    "&to1=" +
                    $("#to1").val() +
                    "&status=inactive",
                    function(res) {
                        inactivechangedet = L.tileLayer(res["mapid"]);

                        $.get(
                            "/map/getchangedetectionactive/?from=" +
                            $("#from").val() +
                            "&to=" +
                            $("#to").val() +
                            "&from1=" +
                            $("#from1").val() +
                            "&to1=" +
                            $("#to1").val() +
                            "&status=active",
                            function(res) {
                                activechangedet = L.tileLayer(res["mapid"]);
                            }
                        );
                    }
                );
            }
        }
    );

    // mymap.addLayer(layerssm);
    $("#filterlayer").addClass("disp on");
    $("#filtereye").removeClass("disp off");
    $("#filtereye").removeClass("fa-eye-slash");
    $("#filtereye").addClass("fa fa-eye");

    $("#filtereye").addClass("disp on");

    $("#query1range").removeClass("hidden");
});

$("#query2").on("click", function() {
    $("#overlay").css("display", "block");

    // if (query2){
    //     mymap.removeLayer(query2)
    // }
    // query2=loadgogletilayer(query2, '/getdata/?from='+$("#from1").val()+'&to='+$("#to1").val()+'&color=red', '','on' ,"loadquery2");

    if (query2) {
        mymap.removeLayer(query2);
    }

    $.get(
        "/map/getdata/?from=" +
        $("#from1").val() +
        "&to=" +
        $("#to1").val() +
        "&color=red",
        function(res) {
            if (res["mapid"] == "error") {
                $("#alert").removeClass("hidden");
                $("#overlay").css("display", "none");
            } else if (res["mapid"] == "no_image") {
                $("#noimage").removeClass("hidden");
                $("#overlay").css("display", "none");
            } else {
                query2 = L.tileLayer(res["mapid"]);
                mymap.addLayer(query2);
                $("#overlay").css("display", "none");
            }

            if (
                $("#from1").val() &&
                $("#to1").val() &&
                $("#to").val() &&
                $("#to").val()
            ) {
                $.get(
                    "/map/getchangedetectionactive/?from=" +
                    $("#from").val() +
                    "&to=" +
                    $("#to").val() +
                    "&from1=" +
                    $("#from1").val() +
                    "&to1=" +
                    $("#to1").val() +
                    "&status=inactive",
                    function(res) {
                        inactivechangedet = L.tileLayer(res["mapid"]);

                        $.get(
                            "/map/getchangedetectionactive/?from=" +
                            $("#from").val() +
                            "&to=" +
                            $("#to").val() +
                            "&from1=" +
                            $("#from1").val() +
                            "&to1=" +
                            $("#to1").val() +
                            "&status=active",
                            function(res) {
                                activechangedet = L.tileLayer(res["mapid"]);
                            }
                        );
                    }
                );
            }
        }
    );

    // mymap.addLayer(layerssm);
    $("#filterlayer2").addClass("disp on");
    $("#filtereye2").removeClass("disp off");
    $("#filtereye2").removeClass("fa-eye-slash");
    $("#filtereye2").addClass("fa fa-eye");

    $("#filtereye2").addClass("disp on");

    $("#query2range").removeClass("hidden");
});

$("#compareupdate1").on("click", function() {
    if (compare) {
        mymap2.removeLayer(compare);
    }
    query2 = loadgogletilayercom(
        compare,
        "/getdata/?from=" +
        $("#from2").val() +
        "&to=" +
        $("#to2").val() +
        "&color=greenyellow",
        "",
        "on"
    );

    // mymap.addLayer(layerssm);
    $("#filterlayer2").addClass("disp on");
    $("#filtereye2").removeClass("disp off");
    $("#filtereye2").removeClass("fa-eye-slash");
    $("#filtereye2").addClass("fa fa-eye");

    $("#filtereye2").addClass("disp on");
});

var landsat, aoi;
// landsat = loadgogletilayer(landsat, '/loadLandsat/', '','');

$.get('/map/loadaoi/', function(res) {

    aoi = L.tileLayer(res['mapid'])

})

$("#landsatCheck").on("click", function(e) {
    // layerseldefine(mymap, layerssm, orig)
    layerTogglefunction(mymap, landsat, $(this).hasClass("on"));
});

// aoi = loadgogletilayer(aoi, '/loadaoi/', '', '');

$("#aoicheck").on("click", function(e) {
    // console.log(aoi);
    // layerseldefine(mymap, layerssm, orig)
    layerTogglefunction(mymap, aoi, $(this).hasClass("on"));
});

// $('#update1').on('click', function() {

//     if (compare){
//         mymap2.removeLayer(compare)
//     }
//     compare = loadgogletilayercom(compare, '/getdata/?from='+$("#from1").val()+'&to='+$("#to1").val() +'&color=red' , '');

//     alert("hoopy")
//     // mymap.addLayer(layerssm);
//      $('#filterlayer').addClass("disp on")
//      $('#filtereye').removeClass("disp off")
//      $('#filtereye').removeClass("fa-eye-slash")
//      $('#filtereye').addClass("fa fa-eye")

//       $('#filtereye').addClass("disp on")

// })

var landsat;
$("body").on("change", "#landsatcompo", function() {
    // $('#landsatcompo').on('change', function(e){

    $("#overlay").css("display", "block");

    $.get("/map/loadLandsat/?year=" + $(this).val(), function(res) {
        if (landsat) {
            mymap.removeLayer(landsat);
        }

        landsat = L.tileLayer(res["mapid"]);
        mymap.addLayer(landsat);
        // landsat.bringToBack();

        $("#overlay").css("display", "none");
    });
});

$("#filterlayer").on("click", function(e) {
    // layerseldefine(mymap, layerssm, orig)
    layerTogglefunction(mymap, query1, $(this).hasClass("on"));
});

$("#query1range").on("change", function(e) {
    sliderfunct($(this).val(), query1);
});

$("#filterlayer2").on("click", function(e) {
    // layerseldefine(mymap, layerssm, orig)
    layerTogglefunction(mymap, query2, $(this).hasClass("on"));
});

$("#query2range").on("change", function(e) {
    sliderfunct($(this).val(), query2);
});

$("#filterlayer3").on("click", function(e) {
    // layerseldefine(mymap, layerssm, orig)
    layerTogglefunction(mymap, inactivechangedet, $(this).hasClass("on"));
});

$("#query3range").on("change", function(e) {
    sliderfunct($(this).val(), inactivechangedet);
});

$("#filterlayer4").on("click", function(e) {
    // layerseldefine(mymap, layerssm, orig)
    layerTogglefunction(mymap, activechangedet, $(this).hasClass("on"));
});

$("#query4range").on("change", function(e) {
    sliderfunct($(this).val(), activechangedet);
});

let coords;
var drawnItems = new L.geoJson().addTo(mymap);
drawnItems.bringToFront();
var layer;

mymap.on(L.Draw.Event.CREATED, function(event) {
    drawnItems.removeLayer(layer);
    layer = event.layer;

    // $("#dialog").dialog("open");
    drawnItems.addLayer(layer);

    let type = event.layerType;

    // if (type === 'rectangle' | ) {
    layer.on("mouseover", function() {
        coords = layer.getLatLngs();
    });
    // }
});

L.EditToolbar.Delete.include({
    removeAllLayers: false,
});

new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
    },
    draw: {
        polygon: true,
        rectangle: true,
        circlemarker: false,
        marker: false,
        polyline: false,
        circle: false,
    },
}).addTo(mymap);

var polyselect;
$("#queryselected").on("click", function() {
    if (polyselect) {
        mymap.removeLayer(polyselect);
    }
    compare = loadgogletilayer(
        polyselect,
        "/getdata/?from=" +
        $("#from_selected").val() +
        "&to=" +
        $("#to_selected").val() +
        "&color=black" +
        "&coords=" +
        coords,
        "",
        "on"
    );

    // mymap.addLayer(layerssm);
    $("#filterlayer").addClass("disp on");
    $("#filtereye").removeClass("disp off");
    $("#filtereye").removeClass("fa-eye-slash");
    $("#filtereye").addClass("fa fa-eye");

    $("#filtereye").addClass("disp on");
});

var downpolyselect;
$("#getdownload").on("click", function() {
    if (polyselect) {
        mymap.removeLayer(polyselect);
    }
    // compare = loadgogletilayer(polyselect, '/getdata/?from='+$("#from_selected").val()+'&to='+$("#to_selected").val() +'&color=black'+'&coords='+coords+'&download=yes' , '');

    $.get(
        "/getdata/?from=" +
        $("#from_selected").val() +
        "&to=" +
        $("#to_selected").val() +
        "&color=black" +
        "&coords=" +
        coords +
        "&download=yes",
        function(data) {
            $("#downloadlink").val(data);
        }
    );
    // mymap.addLayer(layerssm);
    $("#filterlayer").addClass("disp on");
    $("#filtereye").removeClass("disp off");
    $("#filtereye").removeClass("fa-eye-slash");
    $("#filtereye").addClass("fa fa-eye");

    $("#filtereye").addClass("disp on");
});

$("#sel1").on("change", function() {
    if ($("#sel1").val()) {
        $("#sel2").removeAttr("disabled");
    } else {
        $("#sel2").prop("disabled", true);
    }
});

$("body").on("click", "#subyearchart", function() {
    // $('#tto').on('change', function() {
    if (coords) {
        $(".overlay2").removeClass("hidden");
        if ($("#tto").val()) {
            $.get(
                "/map/timeseries/?tfrom=" +
                $("#tfrom").val() +
                "&tto=" +
                $("#tto").val() +
                "&coords=" +
                coords,
                function(data) {
                    $("#tsresults").html(data);
                    $(".overlay2").addClass("hidden");
                }
            );
        } else {
            $("#tto").addAttr("disabled");
        }
    } else {
        swal(
            "Sorry !!!!",
            "Please select your area of interest using the rectangle or polygon tool",
            "info"
        );
    }
});

$("body").on("click", "#subdailychart", function() {
    // $('#tto').on('change', function() {
    if (coords) {
        $(".overlay3").removeClass("hidden");
        if ($("#dateto").val()) {
            $.get(
                "/map/datetimeseries/?tfrom=" +
                $("#datefrom").val() +
                "&tto=" +
                $("#dateto").val() +
                "&coords=" +
                coords,
                function(data) {
                    $("#dateresults").html(data);
                    $(".overlay3").addClass("hidden");
                }
            );
        } else {
            $("#dateto").addAttr("disabled");
        }
    } else {
        swal(
            "Sorry !!!!",
            "Please select your area of interest using the rectangle or polygon tool",
            "info"
        );
    }
});

// $('.lgndthumb').css('border-color', '#f00')
$(".lgndthumb").click(function(e) {
    mymap.removeLayer(initialbasemap);
    $(".lgndthumb > img").css("border-color", "#3e5766");
    var toolname = $(this).attr("id");

    if (toolname == "no_basemap") {
        initialbasemap = L.tileLayer("").addTo(mymap);
    } else if (toolname == "basemap1") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>',
            }
        ).addTo(mymap);
    } else if (toolname == "basemap2") {
        initialbasemap = L.tileLayer(
            "http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", {
                maxZoom: 20,
                subdomains: ["mt0", "mt1", "mt2", "mt3"],
            }
        ).addTo(mymap);
    } else if (toolname == "basemap3") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>',
            }
        ).addTo(mymap);
    } else if (toolname == "basemap4") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
                maxZoom: 17,
                attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
            }
        ).addTo(mymap);
    } else if (toolname == "basemap5") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
                maxZoom: 17,
                attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
            }
        ).addTo(mymap);
    } else if (toolname == "basemap6") {
        initialbasemap = L.tileLayer(
            "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", {
                attribution: "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012",
            }
        ).addTo(mymap);
    } else if (toolname == "basemap7") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.openstreetmap.se/hydda/roads_and_labels/{z}/{x}/{y}.png", {
                maxZoom: 18,
                attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            }
        ).addTo(mymap);
    } else if (toolname == "basemap8") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            }
        ).addTo(mymap);
    } else if (toolname == "basemap9") {
        initialbasemap = L.tileLayer(
            "http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}", {
                attribution: "Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri",
            }
        ).addTo(mymap);
    } else if (toolname == "basemap10") {
        initialbasemap = L.tileLayer(
            "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.{ext}", {
                attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                subdomains: "abcd",
                minZoom: 0,
                maxZoom: 20,
                ext: "png",
            }
        ).addTo(mymap);
    }
    initialbasemap.bringToBack();
});

$("#buttonchange").on("click", function() {
    if (coords) {
        $(".overlay1").removeClass("hidden");

        $("#changedetection").dialog("open");

        $.get(
            "/map/areacomputation/?from=" +
            $("#from").val() +
            "&to=" +
            $("#to").val() +
            "&from1=" +
            $("#from1").val() +
            "&to1=" +
            $("#to1").val() +
            "&coords=" +
            coords,
            function(data) {
                $("#analysis_cont").html(data);
                $(".overlay1").addClass("hidden");
            }
        );
    } else {
        swal(
            "Sorry !!!!! ",
            "Please select your area of interest using the rectangle or polygon tool",
            "info"
        );
    }
});



$("body").on("click", "#download", function() {

     swal(
            "Requesting for download !!!!! ",
            "Tif will be ready shortly  ",
            "info"
        );

if (
        $("#from").val() &&
        // $("#to1").val() &&
        coords &&
        $("#to").val()
    ) {

$.get(
    "/map/getdownload/?from=" +
     $("#from").val() +
        "&to=" +
        $("#to").val() +
        "&from1=" +
        $("#from1").val() +
        "&to1=" +
        $("#to1").val() +
        "&coords="+coords,
        function(res) {
            swal.close();
            swal(
            "Please wait ...",
            " Tif will be downloaded shortly",
            "info"
        );

           window.location.href = res;
  
        }
    );
}else {

   
 swal(
            "Sorry !!!!! ",
            "Please select your area of interest using the rectangle tool and input your date in Query 1  ",
            "info"
        );



}

});






















// })