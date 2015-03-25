define("app", ["d3", "gui_graph_canvas", "gui_info_panel", "epl_model", "mathjax"], function(d3, GraphCanvas, InfoPanel, EplModel, MathJax) {

    function App(graph_id, info_id) {

        var MODE = {
            EDIT: 0,
            Eval: 1
        }

        var _app_mode = MODE.EDIT;

        // Model
        var model = new EplModel();
        // model.loadFromModelString("AS1;ApS1,2;AqS;");
        model.add_state();
        model.add_state();
        model.add_state();

        // model.edit_state(0, [true, true]);

        model.add_link(0, 1);
        model.add_link(1, 0);

        model.add_link(1, 2);
        // model.add_link(2, 1);

        model.add_link(2, 0);
        model.add_link(0, 2);
        
        model.edit_link(0, [0,1,2]);
        model.edit_link(1, [0,1,2,3]);
        model.edit_link(2, [0,1,2,3,4]);

       	// console.log(model.save_to_model_object());
        

        // model.set_prop_count(3);
        // model.set_prop_count(6);

        // model.edit_state(0, [true, false, true]);
        // model.edit_state(2, [false, true]);

        // model.remove_state(1);
        // model.add_state();

        // Info
        var container = d3.select(info_id);
        var info_panel = new InfoPanel(container, model);
        info_panel.init();

        // Graph
        container = d3.select(graph_id);
        var graph_canvas = new GraphCanvas(container, model);
        graph_canvas.start();
    }
    return App;
});
