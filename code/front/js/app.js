define("app", ["d3", "gui_graph_canvas", "gui_info_panel", "epl_model", "gui_listener", "mathjax"], function(d3, GraphCanvas, InfoPanel, EplModel, Listener, MathJax) {

    function App(graph_id, info_id) {

        var model = new EplModel();

        var container = d3.select(graph_id);
        var graph_canvas = new GraphCanvas(container, model);
        graph_canvas.set_listener(new Listener(graph_canvas, model));
        graph_canvas.start();

        this.redraw = function() {
            graph_canvas.reset();
        };

        container = d3.select(info_id);
        var info_panel = new InfoPanel(container, model, this);
        info_panel.init();

        this.get_listener = function() {
            return graph_canvas.get_listener();
        }
    }
    return App;
});
