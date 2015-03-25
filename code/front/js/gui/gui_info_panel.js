define("gui_info_panel", ["d3", "json_editor"], function(d3, JSONEditor) {

    function InfoPanel(container, model) {

        var editor;

        this.init = function() {
            // var editor_container = container.select('#json_editor');
            var editor_container = document.getElementById("json_editor");

            editor = new JSONEditor(editor_container);

            editor.setMode('text');

            var json = {
                "model": {
                    "states": [{
                        "id": "0",
                        "vals": [false, false]
                    }, {
                        "id": "1",
                        "vals": [false, false]
                    }, {
                        "id": "2",
                        "vals": [false, false]
                    }],
                    "relations": [
                        ["0", 0, "1"],
                        ["0", 1, "1"],
                        ["0", 2, "1"],
                        ["1", 0, "0"],
                        ["1", 1, "0"],
                        ["1", 2, "0"],
                        ["1", 3, "0"],
                        ["1", 0, "2"],
                        ["1", 1, "2"],
                        ["1", 2, "2"],
                        ["1", 3, "2"],
                        ["1", 4, "2"],
                        ["2", 0, "0"],
                        ["0", 0, "2"]
                    ],
                    "logic": "KM"
                },
                "formula": "p & ~p",
                "state": "0"
            };
           editor.set(json);
        }

        this.send = function() {
            // Ajax call to backend to send the formula
            // d3.json(url, callback) :)

            // Maybe only preprocess and give a json/string 
            // back and let the app.js send it
        };

    }

    return InfoPanel;

});
