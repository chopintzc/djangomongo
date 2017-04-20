



var $c = jQuery.noConflict();
$c(document).ready(function(){
	$c('#loadButton').click(function() {
		author_id = $c('#id_author').val();
		console.log( author_id );
		filter_id = $c('#id_filt').val();
		request_url = 'get_image/' + author_id + '/' + filter_id + '/';
		
		
		
		d3.selectAll("g").remove();
		
		var svg = d3.select("svg"),
		width = +svg.attr("width"),
	    height = +svg.attr("height");

		var color = d3.scaleOrdinal(d3.schemeCategory20);
		
		var simulation = d3.forceSimulation()
	    	.force("link", d3.forceLink().id(function(d) { return d.id; }))
	    	.force("charge", d3.forceManyBody())
	    	.force("center", d3.forceCenter(width / 2, height / 2));
		
		d3.json(request_url, function(error, graph) {
			if (error) throw error;

			var link = svg.append("g")
		      	.attr("class", "links")
		      	.selectAll("line")
		      	.data(graph.links)
		      	.enter().append("line")
		      	.attr("stroke-width", function(d) { return Math.sqrt(d.value); });

			var node = svg.append("g")
		    	.attr("class", "nodes")
		    	.selectAll("circle")
		    	.data(graph.nodes)
		    	.enter().append("circle")
		    	.attr("r", 5)
		    	.attr("fill", function(d) { return color(d.group); })
				.call(d3.drag()
					.on("start", dragstarted)
			        .on("drag", dragged)
			        .on("end", dragended));
			
			node.append("title")
		        .text(function(d) { return d.id; });
			
			node.on("click", togglenode);
			
			simulation
		        .nodes(graph.nodes)
		        .on("tick", ticked);

			simulation.force("link")
		        .links(graph.links);

			function ticked() {
			    link
			        .attr("x1", function(d) { return d.source.x; })
			        .attr("y1", function(d) { return d.source.y; })
			        .attr("x2", function(d) { return d.target.x; })
			        .attr("y2", function(d) { return d.target.y; });
	
			    node
			        .attr("cx", function(d) { return d.x; })
			        .attr("cy", function(d) { return d.y; });
			}
		});
		

		function dragstarted(d) {
		  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
		  d.fx = d.x;
		  d.fy = d.y;
		}

		function dragged(d) {
		  d.fx = d3.event.x;
		  d.fy = d3.event.y;
		}

		function dragended(d) {
		  if (!d3.event.active) simulation.alphaTarget(0);
		  d.fx = null;
		  d.fy = null;
		}
		
		function togglenode(d) {
			console.log('clicked node : '+d.id);
			
			if (d3.event.defaultPrevented) return;
			
			request_url = 'get_abstract/' + d.id + '/';	        		        
	        $c.ajax({
	        	async: false,
	        	type: 'POST',
	        	url: request_url,
	        	dataType: 'json',
	        	data: "titles_id=" + d.id,
	            success: function(data){
	            	$c('#id_abstract').empty()
	            	$c('#id_tp').empty()
				    $c.each(data.item_list, function(key, value){
				    	$c.each(value, function(id, name){
		                    $c('#id_abstract').append(id);
		                    $c.each(name, function(index, tag) {
		                    	console.log( typeof(tag) );
		                    	$c('#id_tp').append('<option value="' + tag + '">' + tag +'</option>');
		                    });
				    	});
	                });            
				},
	            error: function(jqXHR, textStatus, errorThrown) {
	                alert(errorThrown);
	            }
	        });
		}		
	});
});