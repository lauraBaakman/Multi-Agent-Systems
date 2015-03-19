require.config({
	paths: {
		// Vendor
		'd3': 'libs/d3.min',
		'mathjax': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
		// Our own shit
		'gui_graph_canvas': 'gui/gui_graph_canvas',
		'gui_info_panel': 'gui/gui_info_panel',
		'epl_model': 'epl/epl_model2'
	},

	shim: {
		mathjax: {
			export: "MathJax",
			init: function() {
				MathJax.Hub.Config({
					tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]},
					TeX: { 
						equationNumbers: { 
							autoNumber: "AMS" 
						} 
					}					
				});
				MathJax.Hub.Startup.onload();
				return MathJax;
			}
		}
	}
});

require(['app'],function(App){
    var app = new App("#app-canvas");
});

