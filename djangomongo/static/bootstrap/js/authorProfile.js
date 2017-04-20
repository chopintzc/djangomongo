


var $t = jQuery.noConflict();
$t(document).ready(function(){
	$t('#id_tps').empty()
    $t('#id_cats').change(function(){
    	cats_id = $t(this).val();
		request_url = 'get_choices/' + cats_id + '/';
        $t.ajax({
        	async: false,
        	type: 'POST',
        	url: request_url,
        	dataType: 'json',
        	data: "cats_id=" + $t('#id_cats').val(),
            success: function(data){
            	console.log( cats_id );
            	$t('#id_tps').empty()
			    $t.each(data.item_list, function(key, value){
			    	$t.each(value, function(id, name){
		    	    	console.log( id, name );
	                    $t('#id_tps').append('<option value="' + id + '">' + name +'</option>');
			    	});
                });            
			},
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });
});