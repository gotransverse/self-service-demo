(function($){

	$('.tech-link').click(function(e){
		e.preventDefault();
		$('.tech-link').parents().removeClass('active');
		$(this).parents().addClass('active');
		var scroll = $(this).attr('data-scroll');
		$('html, body').animate({
			scrollTop: $(scroll).offset().top
		}, 500);
	});

})(jQuery);