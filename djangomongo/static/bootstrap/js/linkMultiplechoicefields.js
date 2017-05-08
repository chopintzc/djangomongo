
/*
 * link dropdown menus of category and topic on the Select Topic page
 */

var $m = jQuery.noConflict();
$m(document).ready(function(){
	$m('#id_topics').empty()
    $m('#id_categories').change(function(){
    	categories_id = $m(this).val();
		request_url = 'get_choices/' + categories_id + '/';
        $m.ajax({
        	async: false,
        	type: 'POST',
        	url: request_url,
        	dataType: 'json',
        	data: "categories_id=" + $m('#id_categories').val(),
            success: function(data){
            	$m('#id_topics').empty()
			    $m.each(data.item_list, function(key, value){
			    	$m.each(value, function(id, name){
		    	    	console.log( id, name );
	                    $m('#id_topics').append('<option value="' + id + '">' + name +'</option>');
			    	});
                });            
			},
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });
});