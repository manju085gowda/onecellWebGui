/*
// CUSTOM
$(document).ready(function() {
    $("div.webgui-tab-menu>div.list-group>a").click(function(e) {
        e.preventDefault();
        $(this).siblings('a.active').removeClass("active");
        $(this).addClass("active");
        var index = $(this).index();
        $("div.webgui-tab>div.webgui-tab-content").removeClass("active");
        $("div.webgui-tab>div.webgui-tab-content").eq(index).addClass("active");
    });
});


  jQuery(function(){
	jQuery('#div1').hide();
         jQuery('#showalluser').click(function(){
               jQuery('.targetDivuser').show();
        });
        jQuery('.showSingleuser').click(function(){
              jQuery('.targetDivuser').hide();
              jQuery('#div'+$(this).attr('target')).show();
        });
});


$('.moreinfo').hide();
            $('.more').click(function (ev) {
               var t = ev.target
               $('#info' + $(this).attr('target')).toggle(500, function(){
                  console.log(ev.target)
                  $(t).html($(this).is(':visible')? 'Hide the missing mandatory configurations' : 'Show the missing mandatory confgurations')
               });
               return
			});
*/
