
/*
 * link dropdown menus of category and topic on the Create page
 */

var $j = jQuery.noConflict();
$j(document).ready(function(){
	$j('#id_mytopics').empty()
    $j('#id_dropdown').change(function(){
    	dropdown_id = $j(this).val();
		if (window.location.href.indexOf("?/edit/") > -1) {
			request_url = '/edit/get_topics/' + dropdown_id + '/';
		}
		else {
			request_url = 'get_topics/' + dropdown_id + '/';
		} 	        		        
        $j.ajax({
        	async: false,
        	type: 'POST',
        	url: request_url,
        	dataType: 'json',
        	data: "dropdown_id=" + $j('#id_dropdown').val(),
            success: function(data){
            	$j('#id_mytopics').empty()
			    $j.each(data.item_list, function(key, value){
			    	$j.each(value, function(id, name){
		    	    	console.log( id, name );
	                    $j('#id_mytopics').append('<option value="' + id + '">' + name +'</option>');
			    	});
                });            
			},
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });
});