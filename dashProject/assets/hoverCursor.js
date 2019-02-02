

function hoverCallBack(layer)
{
	return function(data){
		layer.style.cursor = 'pointer'
	}
}

function unhoverCallBack(layer)
{
	return function(data){
		layer.style.cursor = ''
	}
}

function clickCallBack(plot, layer)
{
	return function(data){
		//First, check if the selectgroup property is defined:
		if (!('selectgroup' in data.points[0].data))
		{
			//nothing to do
			return
		}

		//For all selected points
		//saving selectedPoint length as we will be pushing into this array!
		var nSelected = data.points[0].data.selectedpoints.length 
		for(var spIdx = 0; spIdx < nSelected; spIdx++){
			var selectedPoint = data.points[0].data.selectedpoints[spIdx]

			//Find which selected group this point belongs to
			var selectedGroup = data.points[0].data.selectgroup[selectedPoint]

			//Next, look through all the data sets in the plot, and if any are
			//within the same group, then we should also toggle them to selected!
			for(var dIdx = 0; dIdx < plot.data.length; ++dIdx){
				var d = plot.data[dIdx];
				// for (var d in plot.data){
				if ('selectgroup' in d){
					for(var i = 0; i < d.selectgroup.length; ++i){
						if(d.selectgroup[i] == selectedGroup){
							d.selectedpoints.push(i)
						}
					}
				}
			}
		}

		//Tell plotly to restyle based on the newly selected data
	    Plotly.restyle(plot, '', '')
	}
}


function updateCallBack(plot, layer)
{


	return function(args)
	{
        try {
        	var [data, traces] = args.data
        	var layout = args.layout
			if ('SelectFromUpdateMenu' in data){
				var points = []

				for(let j=0; j < traces.length; ++j){
					//Get the curvenumber
					var curveNumber = traces[j]
					//Selected points is an array, for each trace
					//but in the event the array is not long enough, it is assumed
					//to be circularly applied to the traces
					var selectedpointsForThisTrace = data.selectedpoints[j%data.selectedpoints.length]				
					for(let i = 0; i < selectedpointsForThisTrace.length; ++i){
						var pointNumber = selectedpointsForThisTrace[i]
						points.push({pointNumber, curveNumber})
					}
				}
				//console.log('Got some data: Emitting plotly_selected event')
				//console.log({points})
				plot.emit('plotly_selected', {points})
			}
		} catch (ignore) {
			console.error('failed to run updateCallBack')
		}
	}
}


var dragLayers = document.getElementsByClassName('nsewdrag')
for(var i = 0 ; i < dragLayers.length; ++i)
{
	//var myPlot = document.getElementById(graphIds[i])
	var dragLayer = dragLayers[i]
	
	// dragLayer.style.cursor = 'pointer'

	var myPlot = dragLayer.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode

	myPlot.on('plotly_hover', hoverCallBack(dragLayer));

	myPlot.on('plotly_unhover', unhoverCallBack(dragLayer));

	myPlot.on('plotly_click', clickCallBack(myPlot, dragLayer));

	myPlot.on('plotly_update', updateCallBack(myPlot, dragLayer))

}
