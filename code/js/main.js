require.config({
	paths: {
		'd3': 'libs/d3.min',
		'Converters': 'EPL/Converters',
		'RegularExpressions': 'EPL/RegularExpressions'
	}
});

require(['app'],function(app){
	// Start app.js
	console.log(app);
    app.setAppMode(app.MODE.EDIT);
});