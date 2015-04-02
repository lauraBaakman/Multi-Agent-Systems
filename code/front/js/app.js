define("app", ["d3", "gui_graph_canvas", "gui_info_panel", "epl_model", "mathjax"], function(d3, GraphCanvas, InfoPanel, EplModel, MathJax) {

    function App(graph_id, info_id) {

        var model = new EplModel();

        this.get_model = function() {
            return model;
        };

        var container = d3.select(graph_id);
        var graph_canvas = new GraphCanvas(container, this);
        graph_canvas.start();

        this.redraw = function() {
            graph_canvas.reset();
        };

        container = d3.select(info_id);
        var info_panel = new InfoPanel(container, this);
        info_panel.init();
    }
    return App;
});
