$(function() {
	var $menu_popup = $('.menu-popup');
 
	$(".menu-triger").click(function(){
		$('body').addClass('body_pointer');		
		$menu_popup.show(0);
		$menu_popup.animate(
			{right: parseInt($menu_popup.css('left'),10) == 0 ? -$menu_popup.outerWidth() : "-5%"}, 
			0
		);
		return false;
	});	
	
	$(".menu-close").click(function(){
		$('body').removeClass('body_pointer');		
		$menu_popup.animate(
			{right: parseInt($menu_popup.css('right'),10) == 0 ? -$menu_popup.outerWidth() : 0}, 
			0, 
			function(){
				$menu_popup.hide(0);
			}
		);
		return false;
	});	
	
	$(document).on('click', function(e){
		if (!$(e.target).closest('.menu-popup').length){
			$('body').removeClass('body_pointer');
			$menu_popup.animate(
				{right: parseInt($menu_popup.css('right'),10) == 0 ? -$menu_popup.outerWidth() : 0}, 
				0, 
				function(){
					$menu_popup.hide(0);
				}
			);
		}
	});
});