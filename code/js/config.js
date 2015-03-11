require.config({
	paths: {
		// Vendor
		'd3': 'libs/d3.min',
		'mathjax': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
		// Our own shit
		'epl_converters': 'epl/epl_converters',
		'epl_regexp': 'epl/epl_regexp',
		'epl_model': 'epl/epl_model',
		'epl_formula': 'epl/epl_formula',
	},

	shim: {
		mathjax: {
			export: "MathJax",
			init: function() {
				MathJAx.Hub.Config({
					tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
				});
				MathJAx.Hub.Startup.onload();
				return MathJax;
			}
		}
	}
});

require(['app'],function(app){
	// Start app.js
    app.setAppMode(app.MODE.EDIT);

    // ugly
    window.app = app;
});

