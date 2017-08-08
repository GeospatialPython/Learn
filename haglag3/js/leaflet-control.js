/*
 * CREATE A NEW LEAFLET CONTROL FOR THE SCALE (used by distance grids)
 */

L.Control.GridScale = L.Control.Scale.extend({
	options: {
		position: 'bottomright',
		gridType: 'none',
		showMetric: false, // true for metric, false for imperial
        metric: false,
		updateWhenIdle: true,
		maxWidth: 100,
	},
	
	onAdd: function (map) {
		this._map = map;

		var mainContainer = L.DomUtil.create('div', '');
		var className = 'leaflet-control-scale',
		    container = L.DomUtil.create('div', className, mainContainer),
		    options = this.options;

		this._addScales(options, className, container);
		this._addDistanceLabel(options, mainContainer);

		map.on(options.updateWhenIdle ? 'moveend' : 'move', this._update, this);
		map.whenReady(this._update, this);

		return mainContainer;
	},

	_addDistanceLabel: function(options, container){
		this._distLabel = L.DomUtil.create('div', 'dist-label', container);
	},

	_update: function () {
		var bounds = this._map.getBounds(),
		    centerLat = bounds.getCenter().lat,
		    halfWorldMeters = 6378137 * Math.PI * Math.cos(centerLat * Math.PI / 180),
		    dist = halfWorldMeters * (bounds.getNorthEast().lng - bounds.getSouthWest().lng) / 180,
		    options = this.options,
		    gridSize = this._gridSpacing(options),
		    size = this._map.getSize(),
		    maxMeters = 0;
		if (size.x > 0) {
			maxMeters = dist * (options.maxWidth / size.x);
		}

		this._updateDistance(gridSize);

		this._updateScales(options, maxMeters);
	},

	_updateDistance: function (gridSize) {	
		if(gridSize){
			this._distLabel.innerHTML = 'Grid : ' + gridSize;
		}else{
			this._distLabel.innerHTML = '';
		}
	},

	_gridSpacing: function (options) {
		var zoom = this._map.getZoom(); 
		var metricSpacing = [   
            "25,000 km", // 0 
            "10,000 km", // 1
            "5000 km", // 2
            "2500 km", // 3
            "1000 km", // 4
            "500 km", // 5
            "250 km", // 6
            "100 km", // 7
            "50 km", // 8
            "25 km", // 9
            "10 km", // 10
            "5 km", // 11
            "2.5 km", // 12
            "1 km", // 13
            "500 m", // 14
            "250 m", // 15
            "100 m", // 16
            "50 m", // 17
            "25 m", // 18
        ]; 
        var imperialSpacing = [
            "10000 mi", // 0
            "5000 mi", // 1
            "2500 mi", // 2
            "1000 mi", // 3
            "500 mi", // 4
            "250 mi", // 5
            "100 mi", // 6
            "50 mi", // 7
            "25 mi", // 8
            "10 mi", // 9
            "5 mi", // 10
            "2.5 mi", // 11
            "1 mi", // 12
            "2500 ft", // 13
            "1000 ft", // 14
            "500 ft", // 15
            "250 ft", // 16
            "100 ft ", // 17
            "50 ft", // 18
            "25 ft", // 19
            "12.5 ft", // 20
            "2 yds", // 21
            "1 yd", // 22
            ".5 yds", // 23
            "9 in", // 24
            "4.5 in", // 25
            "2 in" // 26            
        ]; 
        if (options.gridType == 'distance'){
        	if(options.showMetric){
        		return metricSpacing[zoom];
        	}
        	if(!options.showMetric){
        		return imperialSpacing[zoom];
        	}
        }
	},
});

L.control.gridscale = function (options) {
	return new L.Control.GridScale(options);
};
