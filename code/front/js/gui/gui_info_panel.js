define("gui_info_panel", ["d3", "json_editor", "mathjax"], function(d3, JSONEditor, MathJax) {

    function InfoPanel(container, app) {

        var self = this;

        var editor;

        var json = {
            "state": "2",
            "formula": "K_1 M_2 p <-> q",
            "model": {
                "states": [{
                    "id": "0",
                    "vals": [true, true, false]
                }, {
                    "id": "1",
                    "vals": [true, false, true]
                }, {
                    "id": "2",
                    "vals": [false, false, true]
                }, {
                    "id": "3",
                    "vals": [false, true, false]
                }],
                "propositions": ["p", "q", "r"],
                "relations": [
                    ["2", "1", "0"],
                    ["0", "1", "0"],
                    ["0", "2", "1"],
                    ["1", "2", "0"],
                    ["1", "2", "2"],
                    ["2", "2", "1"],
                    ["2", "2", "2"],
                    ["1", "3", "1"],
                    ["1", "3", "0"],
                    ["0", "3", "1"]
                ],
                "logic": "KM"
            }
        };

        var loading = null;

        this.send = function() {
            d3.json("http://localhost:8000/valuate")
                .on("beforesend", function() {
                    loading = document.createElement('div')
                    loading.className = 'loading';
                    document.getElementById("playground").appendChild(loading);
                })
                .on("load", function(data) {
                    var new_child = document.createElement('div');
                    new_child.innerHTML = data.motivation;

                    var response = document.getElementById("response");
                    while (response.firstChild) {
                        response.removeChild(response.firstChild);
                    }
                    response.appendChild(new_child);

                    MathJax.Hub.Queue(["Typeset", MathJax.Hub, "response"]);

                    var new_model = JSON.parse(data.model);
                    console.log(new_model);

                    app.get_model().load_from_model_object(new_model);
                    app.redraw();

                    document.getElementById("playground").removeChild(loading);
                })
                .on("error", function(error) {
                    console.log("error");
                    document.getElementById("playground").removeChild(loading);
                    console.log(error.title);

                })
                .post(JSON.stringify(editor.get()));
        };



        this.init = function() {
            // var editor_container = container.select('#json_editor');
            var editor_container = document.getElementById("json_editor");

            editor = new JSONEditor(editor_container);

            editor.setMode('text');

            editor.set(json);

            var submit_button = document.getElementById("json_submit_button");
            submit_button.onclick = self.send;
        }
    }
    return InfoPanel;
});
