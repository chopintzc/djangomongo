


var $p = jQuery.noConflict();
$p(document).ready(function(){
	$p('#id_abstract').empty()
	$p('#id_tp').empty()
    $p('#id_titles').change(function(){
    	titles_id = $p(this).val();
		request_url = 'get_abstract/' + titles_id + '/';	        		        
        $p.ajax({
        	async: false,
        	type: 'POST',
        	url: request_url,
        	dataType: 'json',
        	data: "titles_id=" + $p('#id_titles').val(),
            success: function(data){
            	$p('#id_abstract').empty()
            	$p('#id_tp').empty()
			    $p.each(data.item_list, function(key, value){
			    	$p.each(value, function(id, name){
	                    $p('#id_abstract').append(id);
	                    $p.each(name, function(index, tag) {
	                    	console.log( typeof(tag) );
	                    	$p('#id_tp').append('<option value="' + tag + '">' + tag +'</option>');
	                    });
			    	});
                });            
			},
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    });
});