define("gui_info_panel", ["d3", "mathjax"], function(d3, JSONEditor, MathJax) {

    function InfoPanel(container, model) {

        var self = this;

        var loading = null;

        this.send = function() {
            // d3.json("http://localhost:8000/valuate")
            //     .on("beforesend", function() {
            //         loading = document.createElement('div')
            //         loading.className = 'loading';
            //         document.getElementById("playground").appendChild(loading);
            //     })
            //     .on("load", function(data) {
            //         var new_child = document.createElement('div');
            //         new_child.innerHTML = data.motivation;

            //         var response = document.getElementById("response");
            //         while (response.firstChild) {
            //             response.removeChild(response.firstChild);
            //         }
            //         response.appendChild(new_child);

            //         MathJax.Hub.Queue(["Typeset", MathJax.Hub, "response"]);

            //         var new_model = JSON.parse(data.model);
            //         console.log(new_model);

            //         app.get_model().load_from_model_object(new_model);
            //         app.redraw();

            //         document.getElementById("playground").removeChild(loading);
            //     })
            //     .on("error", function(error) {
            //         console.log("error");
            //         document.getElementById("playground").removeChild(loading);
            //         console.log(error.title);

            //     })
            //     .post(JSON.stringify({
            //         state: "0",
            //         formula: "K_1 M_2 p <-> q",
            //         model: model.save_to_model_object()
            //     }));

                console.log(JSON.stringify({
                    state: "0",
                    formula: "K_1 M_2 p <-> q",
                    model: model.save_to_model_object()
                }));

            // console.log(model.save_to_model_object());

            // editor.set(app.get_model().save_to_model_object());
        };

        this.init = function() {
            // var editor_container = container.select('#json_editor');
            // var editor_container = document.getElementById("json_editor");

            // editor = new JSONEditor(editor_container);

            // editor.setMode('text');

            // editor.set(json);

            var submit_button = document.getElementById("json_submit_button");
            submit_button.onclick = self.send;
        };
    }
    return InfoPanel;
});
