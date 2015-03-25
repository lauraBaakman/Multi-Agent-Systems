define("gui_info_panel", ["d3", "json_editor"], function(d3, JSONEditor) {

    function InfoPanel(container, model) {

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

        this.send = function() {
            // Ajax call to backend to send the formula
            // d3.json(url, callback) :)

            // Maybe only preprocess and give a json/string 
            // back and let the app.js send it

            d3.json("http://localhost:8000/valuation")
                .header("Access-Control-Allow-Origin", "*")
                // .header("application/json")
                .post(json, function(error, data) {
                    console.log(data);
                });
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