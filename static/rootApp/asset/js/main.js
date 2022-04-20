  
var side = 'on';


$("#legendbtn").click(function() {
    if (side == 'off') {
        $(".side").show("slide", { direction: "right" }, 399);
        $(".inner1").show("slide", { direction: "right" }, 9);
        side = 'on'
    } else if (side == 'on') {
        $(".side").hide("slide", { direction: "right" }, 399);
        $(".inner1").show("slide", { direction: "right" }, 9);
    	side = 'off';
    }
});

$("#close").click(function(){
    $(".side").hide("slide", { direction: "right" }, 399);
    $(".inner1").show("slide", { direction: "right" },9);
    side = 'off';
});



$(".layer").click(function(){	
   var displaybtn = $(this).parent().find(".disp");
   if (displaybtn.hasClass("off")) {
   		$(this).addClass('on');
      	displaybtn.removeClass('fa-eye-slash');
      	displaybtn.addClass('on');
	  	displaybtn.addClass('fa-eye');
	  	displaybtn.removeClass('off');
   } else if (displaybtn.hasClass("on")) {
      	displaybtn.removeClass('fa-eye');
      	displaybtn.addClass('off');
	  	displaybtn.addClass('fa-eye-slash');
	  	displaybtn.removeClass('on');
   		$(this).removeClass('on');

   }
});


// var layerdisp ='on';

// $("#layerbar").click(function() {
//     if (layerdisp == 'off') {
//         $(".disp").removeClass('fa-eye-slash');
//         $(".disp").removeClass('fa-eye');

//         $(this)$(this).next('.disp');
//         layerdisp = 'on'
//     } else if (layerdisp == 'on') {        
//         $(".disp").removeClass('fa-eye');
//         $(".disp").addClass('fa-eye-slash');
//     	layerdisp = 'off';
//     }
// });



// $("#legendbtn").click(function() {
//     if (side == 'off') {
//         $(".side").show("slide", { direction: "right" }, 1000);
//         side = 'on'
//     } else if (side == 'on') {
//         $(".side").hide("slide", { direction: "right" }, 1000).delay(1000).queue(function(next) {
//             next();
//             side = 'off';
//         });
//     }
// });

//   $("#close").click(function(){
//     $(".side").hide("slide", { direction: "right" }, 1000).delay(1000).queue(function(next){
//          next();
//          side = 'off';
//     });
//   });


/*******************************
* ACCORDION WITH TOGGLE ICONS
*******************************/
	function toggleIcon(e) {
        $(e.target)
            .prev('.panel-heading')
            .find(".more-less")
            .toggleClass('glyphicon-plus glyphicon-minus');
    }
    $('.panel-group').on('hidden.bs.collapse', toggleIcon);
    $('.panel-group').on('shown.bs.collapse', toggleIcon);



/*******************************
* Dialog *
*******************************/




  // $( function() {
  //   var dateFormat = "yy",
  //     from = $( "#from" )
  //       .datepicker({
  //         changeYear: true,
  //       })
  //       .on( "change", function() {
  //         to.datepicker( "option", "minDate", getDate( this ) );
  //       }),
  //     to = $( "#to" ).datepicker({
  //       changeYear: true,
  //     })
  //     .on( "change", function() {
  //       from.datepicker( "option", "maxDate", getDate( this ) );
  //     });
 
  //   function getDate( element ) {
  //     var date;
  //     try {
  //       date = $.datepicker.parseDate( dateFormat, element.value );
  //     } catch( error ) {
  //       date = null;
  //     }
 
  //     return date;
  //   }
  // } );




