require.config({
	paths: {
		'd3': 'libs/d3.min'
	}
});

require(['app'],function(app){
	// Start app.js
	console.log(app);
    app.setAppMode(app.MODE.EDIT);
});