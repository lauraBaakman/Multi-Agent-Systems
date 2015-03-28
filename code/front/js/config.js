require.config({
    paths: {
        // Vendor
        'd3': 'libs/d3.min',
        'mathjax': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
        'json_editor': 'libs/jsoneditor-4/dist/jsoneditor.min',
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
                    tex2jax: {
                        inlineMath: [
                            ['$', '$'],
                            ['\\(', '\\)']
                        ]
                    },
                    TeX: {
                        equationNumbers: {
                            autoNumber: "AMS"
                        },
                        Macros: {
                        	m: "\\text{m}",
                            K: ["\\text{K}_{#1}", 1],
                            KEC: ["\\text{KEC}_{#1}", 1],
                            KI: ["\\text{KI}_{#1}", 1],
                            T: ["\\text{T}_{#1}", 1],
                            TEC: ["\\text{TEC}_{#1}", 1],
                            TI: ["\\text{TI}_{#1}", 1],                            
                            SV: ["\\text{S4}_{#1}", 1],
                            SVEC: ["\\text{S4EC}_{#1}", 1],
                            SVI: ["\\text{S4I}_{#1}", 1],                                                        
                            SF: ["\\text{S5}_{#1}", 1],
                            SFEC: ["\\text{S5EC}_{#1}", 1],
                            SFI: ["\\text{S5I}_{#1}", 1],  
                            model: "\\mathcal{M}"                                                                                  
                        }
                    }
                });
                MathJax.Hub.Startup.onload();
                return MathJax;
            }
        }
    }
});

require(['app'], function(App) {
    var app = new App("#app-canvas", "#app-info");
});
