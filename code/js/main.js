require.config({
	paths: {
		'd3': 'libs/d3.min',
		'Converters': 'EPL/Converters',
		'RegularExpressions': 'EPL/RegularExpressions',
		'EPLModel': 'EPL/EPLModel'
	}
});

require(['app'],function(app){
	// Start app.js
    app.setAppMode(app.MODE.EDIT);
});