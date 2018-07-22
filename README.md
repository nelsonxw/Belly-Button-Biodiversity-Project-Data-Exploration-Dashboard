## The Belly Button Biodiversity Project Data Exploration Dashboard  

Link to web application: https://interactive-viz-dashboard.herokuapp.com/  

<img src="/images/Capture_1.PNG" width="800">  
<img src="/images/Capture_2.PNG" width="800">

### Objectives:

To create an interacive dashboard on the web that allows uses to explore the data from [Belly Button Biodiversity Project](http://robdunnlab.com/projects/belly-button-biodiversity/). 

### Tools used:
HTML, CSS, Bootstrap, JavaScript, Plotly.js, Pandas, Flask, Heruko

### Major Steps:
+ Used HTML, CSS and Bootstrap to build the index page which includes a pie chart, bubble chart, gauge chart and user input section.
+ Used Flask to set up routes for different datasets, including sample data, OTU(operational taxonomic unit), Meta data.  Used Pandas to read data, manipulate it and output filtered data as needed. Jsonify the output and make it ready for consumptions by JavaScript codes.
+ Used Plotly.d3.json function to populate selection field and show meta data
```javascript
/*populate selection options*/
var name_url = "/names";
/*get sample names from route "names"*/
Plotly.d3.json(name_url, function(error, data) {
    if (error) return console.warn(error);
    names = Object.values(data);
    /*add list options*/
    for (var n = 0; n < names.length; n++) {
        var $option = document.createElement("option");
        var $selection = document.querySelector("#selSample")
        $option.value = names[n];
        $option.innerHTML = names[n];
        $selection.appendChild($option);
    };
})

/*show metadata*/
var default_selection = "BB_940";

show_metadata(default_selection);

function show_metadata (route) {
	/*get metadata from route "metadata/sample name"*/
	Plotly.d3.json(`/metadata/${route}`, function(error, data) {
        if (error) return console.warn(error);
        /*insert row and cells under table to display metadata*/
        var $tbody = document.querySelector("#metadata");
        $tbody.innerHTML="";
        for (k in data[0]) {
			var $tr = document.createElement("tr");
			var $td = document.createElement("td");
			$td.innerText = k + ": " + data[0][k];
        	$tr.appendChild($td);
        	$tbody.appendChild($tr);
        };
        /*define table cell styles*/
        var $tds = document.querySelectorAll("td");
        for (var i=0;i<$tds.length;i++) {
        	$tds[i].style.paddingLeft="30px";
        	$tds[i].style.paddingBottom="5px";
        }
    });
}
```
+ Used Plotly.newPlot function to plot pie chart, bubble chart and gauge chart
```javascript
/*Plot pie chart and bubble chart*/
/*get sample data from route "samples/sample name"*/
Plotly.d3.json(`/samples/${default_selection}`, function(error, data) {
    if (error) return console.warn(error);
    var sample_value = data[0].sampleValue;
    var otuID = data[0].otu_id
    var otuDescription = data[0].otu_descriptions
    /*select first top 10 values*/
    var sample_top10 = sample_value.slice(0,10);
    var otuID_top10 = otuID.slice(0,10);
    var otuDescription_top10 = otuDescription.slice(0,10);
    /*define pie chart data*/
    var piedata = [{
        labels: otuID_top10,
        values: sample_top10,
        type: "pie",
        hovertext:otuDescription_top10
    }];
    /*define pie chart layout*/
    var layout_pie = {
      title: "<b>Top 10 Samples by OTU ID</b>",
      height: 400,
      width: 500,
      margin: {
	    l: 50,
	    r: 0,
	    b: 50,
	    t: 50
	  },
    };
	Plotly.newPlot("pieChart",piedata,layout_pie);
	/*define bubble chart data*/
	var bubbledata = [{
	  x: otuID,
	  y: sample_value,
	  text: otuDescription,
	  mode: 'markers',
	  marker: {
	    size: sample_value,
	    color: otuID,
	    colorscale:"Earth",
	  }
	}];
	/*define bubble chart layout*/
	var layout_bubble = {
      title: "<b>Sample Values vs. OTU ID</b>",
      height: 600,
      width: 1500
    };
	Plotly.newPlot("bubbleChart",bubbledata,layout_bubble);
}); 

/*create gauge chart*/
draw_gaugeChart(default_selection);

function draw_gaugeChart(route) {
	/*get weekly scrub frequency data from route "wfreq/sample name"*/
	Plotly.d3.json(`/wfreq/${route}`, function(error, data) {
	if (error) return console.warn(error);
	/*define x and y position of pointer tip*/
	var degrees = (9-data[0])*20,
	     radius = .5;
	var radians = degrees * Math.PI / 180;
	var x = radius * Math.cos(radians);
	var y = radius * Math.sin(radians);

	/*create a triangle to represent a pointer*/
	var mainPath = 'M .0 -0.025 L .0 0.025 L ',
	     pathX = String(x),
	     space = ' ',
	     pathY = String(y),
	     pathEnd = ' Z';
	var path = mainPath.concat(pathX,space,pathY,pathEnd);
	/*define data for dot (scatter) and pie chart*/
	var data = [
		{ type: 'scatter',
	   	x: [0,], y:[0],
	    marker: {size: 28, color:'850000'},
	    showlegend: false,
	    name: 'scrubs',
	    text: data[0],
	    hoverinfo: 'text+name'},
	  	
	  	{ values: [50/9, 50/9, 50/9, 50/9, 50/9, 50/9,50/9,50/9,50/9, 50],
	  	rotation: 90,
	  	text: ['8-9', '7-8', '6-7','5-6', '4-5', '3-4', '2-3',
	            '1-2', '0-1', ''],
	  	textinfo: 'text',
	  	textposition:'inside',
	  	marker: {colors:['rgba(30,120,30, .5)', 'rgba(55,135,55, .5)','rgba(80,150,80, .5)',
	  					'rgba(105,165,105, .5)', 'rgba(130,180,130, .5)','rgba(155,195,155, .5)',
	  					 'rgba(180,210,180, .5)','rgba(205,225,205, .5)', 'rgba(230,240,230, .5)',
	                         'rgba(255, 255, 255, 0)']},
	  	hoverinfo: 'none',
	  	hole: .5,
	  	type: 'pie',
	  	showlegend: false}
		];
	/*define the layout, shape and path*/
	var layout = {
	  		shapes:[{
	      	type: 'path',
	      	path: path,
	      	fillcolor: '850000',
	      	line: { color: '850000' }
	    	}],
	  		title: '<b>Belly Button Washing Frequency</b><br>Scrups per Week',
		  	height: 600,
		  	width: 600,
		  	/*move the zero point to the middle of the pie chart*/
		  	xaxis: {zeroline:false, showticklabels:false,
	             showgrid: false, range: [-1, 1]},
	  		yaxis: {zeroline:false, showticklabels:false,
	             showgrid: false, range: [-1, 1]}
			};

	Plotly.newPlot('gaugeChart', data, layout);
	});
}
```
+ Created a function to use Plotly.restyle function to update charts when user selections are changed.
```javascript
/*update the plot with new data*/
function updateCharts(route) {
    Plotly.d3.json(`/samples/${route}`, function(error, newdata) {
    	if (error) return console.warn(error);
        var newsample_value = newdata[0].sampleValue;
        var newotuID = newdata[0].otu_id;
        var newotuDescription = newdata[0].otu_descriptions;
        var newsample_top10 = newsample_value.slice(0,10);
        var newotuID_top10 = newotuID.slice(0,10);
        var newotuDescription_top10 = newotuDescription.slice(0,10);
        
        /*define new data for the pie chart*/
        var update_pie = {
        	labels: [newotuID_top10],
            values: [newsample_top10],
            hovertext:[newotuDescription_top10]
        }
        /*re-plot pie chart*/
        Plotly.restyle("pieChart", update_pie);
		/*define new data for the bubble chart*/
        var update_bubble = {
		  x: [newotuID],
		  y: [newsample_value],
		  text: [newotuDescription],
		};
		/*re-plot bubble chart*/
		Plotly.restyle("bubbleChart",update_bubble);
	});


}
```
