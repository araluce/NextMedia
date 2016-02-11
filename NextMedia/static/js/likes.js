$(document).ready(function() {
	$('#likes').click(function(){
		alert('holaa')
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/like_video/', {video: catid}, function(data){
			$('#like_count').html(data);
			$('#likes').hide();
		});
	});
});