





var $b = jQuery.noConflict();
$b(document).ready(function(){
    $b("#filterButton").click(function(){
		console.log( 'ok' );
    	filter_id = $b('#id_filt').val();
    	author_id = $b('#id_author').val();
		request_url = 'get_title/' + author_id + '/';
        $b.ajax({
        	async: false,
        	type: 'POST',
        	url: request_url,
        	dataType: 'json',
        	data: "author_id=" + author_id + '&filter_id=' + filter_id,
            success: function(data){
            	$b('#id_titles').empty()
            	$b('#id_abstract').empty()
            	$b('#id_tp').empty()
			    $b.each(data.item_list, function(key, value){
			    	$b.each(value, function(id, name){
			    		$b('#id_titles').append('<option value="' + id + '">' + name +'</option>');
			    	});
                });            
			},
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });
});