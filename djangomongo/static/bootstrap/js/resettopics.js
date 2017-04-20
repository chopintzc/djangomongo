
var $k = jQuery.noConflict();
$k(document).ready(function(){
	$k("#id_reset").click(function() {
		console.log( 'click' );
        $k.ajax({
        	async: false,
        	type: 'POST',
        	url: '/topics/request_topic/reset/',
        	dataType: 'json',
        	data: {
        		category_id: $k("#id_category").val(),
        		topic_id: $k("#id_topic").val(),
                },
            success: function(data){
            	console.log( 'success' );
			},
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
	});
});