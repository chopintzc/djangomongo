/*
 * link choice box with the svg image on the Author Profile page
 * Add all the events to the svg image (draw, redraw, click node, zoom, pan)
 */

var $a = jQuery.noConflict();

// draw the svg image when the page is loaded
$a(document).ready(function(){
	author_id = $a('#id_author').val();
	request_url = 'get_image/' + author_id + '/' + 'none' + '/';
	
	d3.selectAll("g").remove();
	
	var height = $("#chart").height();
	var width = $("#chart").width();	
	
	// zoom property
	var zoom = d3.zoom().scaleExtent([0.1, 10]).on("zoom", zoomed);
	
	function zoomed() {
		console.log("zoom", d3.event.tranform);
	    vis.attr("transform", d3.event.transform);
	}
	
	// append the svg
	var vis = d3.select("#chart").append("svg:svg")
		.attr("width", width)
		.attr("height", height)
		.attr("pointer-events", "all")
		.append('svg:g')
			.call(zoom)
		.append('svg:g');
		
	// append the rectangle to catch the mouse zoom action
	vis.append("svg:rect")
	  .attr("width", width)
	  .attr("height", height)
	  .style("fill", "none");

	var color = d3.scaleOrdinal(d3.schemeCategory20);
	
	var simulation = d3.forceSimulation()
    	.force("link", d3.forceLink().id(function(d) { return d.id; }))
    	.force("charge", d3.forceManyBody())
    	.force("center", d3.forceCenter(width / 2, height / 2));
	
	// request data from the server
	d3.json(request_url, function(error, graph) {
		if (error) throw error;
		
		// add link
		var link = vis.append("g")
	      	.attr("class", "links")
	      	.selectAll("line")
	      	.data(graph.links, function (d) {
	            return d.target.id;
	        })
	      	.enter().append("line")
	      	.attr("x1", function(d) { return d.source.x; })
	        .attr("y1", function(d) { return d.source.y; })
	        .attr("x2", function(d) { return d.target.x; })
	        .attr("y2", function(d) { return d.target.y; })
	      	.attr("stroke-width", function(d) { return Math.sqrt(d.value); });
		
		// add node
		var node = vis.append("g")
	    	.attr("class", "nodes")
	    	.selectAll("circle")
	    	.data(graph.nodes, function (d) {
	            return d.id;
	        })
	    	.enter().append("circle")
	    	.attr("cx", function(d) { return d.x; })
	    	.attr("cy", function(d) { return d.y; })
	    	.attr("r", 5)
	    	.attr("fill", function(d) { return color(d.group); })
			.call(d3.drag()
				.on("start", dragstarted)
		        .on("drag", dragged)
		        .on("end", dragended));
		
		node.append("title")
	        .text(function(d) { return d.id; });
		
		// add click event
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
	
	// redraw the image when check box is upadeted
	$a("#mytags").change(function() {
		author_id = $a('#id_author').val();
		urls = '';
		
		// loop through all the check boxes to see which of them are checked
		tops = document.getElementById("mytags").getElementsByTagName('ul')[0].getElementsByTagName('li');
		for (var i=tops.length-1, len=tops.length; i>=0; i--) {
			t = tops[i].getElementsByTagName('label')[0]
			elem = document.getElementById(t.htmlFor)
	        if ( elem.checked ){
	        	urls = urls + 'urls=' + elem.value + '&';
	        }
	    }
		if (urls.length > 0){
			urls = urls.substring(0, urls.length - 1);
		}
		
		console.log( urls );
		request_url = 'get_image/' + author_id + '/' + urls + '/';
		
		
		d3.selectAll("g").remove(); 
		
		var height = $("#chart").height();
		var width = $("#chart").width();
		
		// add zoom property
		var zoom = d3.zoom().scaleExtent([0.1, 10]).on("zoom", zoomed);
		
		function zoomed() {
			console.log("zoom", d3.event.tranform);
		    vis.attr("transform", d3.event.transform);
		}
		
		// add the svg
		var vis = d3.select("#chart").append("svg:svg")
			.attr("width", width)
			.attr("height", height)
			.attr("pointer-events", "all")
			.append('svg:g')
				.call(zoom)
			.append('svg:g');
			
		// add the rectangle
		vis.append("svg:rect")
		  .attr("width", width)
		  .attr("height", height)
		  .style("fill", "none");

		

		var color = d3.scaleOrdinal(d3.schemeCategory20);
		
		var simulation = d3.forceSimulation()
	    	.force("link", d3.forceLink().id(function(d) { return d.id; }))
	    	.force("charge", d3.forceManyBody())
	    	.force("center", d3.forceCenter(width / 2, height / 2));
		
		// request data from the server
		d3.json(request_url, function(error, graph) {
			if (error) throw error;

			var link = vis.append("g")
		      	.attr("class", "links")
		      	.selectAll("line")
		      	.data(graph.links)
		      	.enter().append("line")
		      	.attr("stroke-width", function(d) { return Math.sqrt(d.value); });

			var node = vis.append("g")
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
			
			// add click event
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
		
		// request abstract and topics information from server when the node is clicked
		function togglenode(d) {
			console.log('clicked node : '+d.id);
			
			if (d3.event.defaultPrevented) return;
			
			request_url = 'get_abstract/' + d.id + '/';	        		        
	        $a.ajax({
	        	async: false,
	        	type: 'POST',
	        	url: request_url,
	        	dataType: 'json',
	        	data: "titles_id=" + d.id,
	            success: function(data){
	            	$a('#id_abstract').empty()
	            	$a('#id_tp').empty()
				    $a.each(data.item_list, function(key, value){
				    	$a.each(value, function(id, name){
		                    $a('#id_abstract').append(id);
		                    $a.each(name, function(index, tag) {
		                    	console.log( typeof(tag) );
		                    	$a('#id_tp').append('<option value="' + tag + '">' + tag +'</option>');
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

	// request abstract and topics information from server when the node is clicked
	function togglenode(d) {
		console.log('clicked node : '+d.id);
		
		if (d3.event.defaultPrevented) return;
		
		request_url = 'get_abstract/' + d.id + '/';	        		        
        $a.ajax({
        	async: false,
        	type: 'POST',
        	url: request_url,
        	dataType: 'json',
        	data: "titles_id=" + d.id,
            success: function(data){
            	$a('#id_abstract').empty()
            	$a('#id_tp').empty()
			    $a.each(data.item_list, function(key, value){
			    	$a.each(value, function(id, name){
	                    $a('#id_abstract').append(id);
	                    $a.each(name, function(index, tag) {
	                    	console.log( typeof(tag) );
	                    	$a('#id_tp').append('<option value="' + tag + '">' + tag +'</option>');
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