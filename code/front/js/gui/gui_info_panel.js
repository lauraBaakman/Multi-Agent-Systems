define("gui_info_panel", ["d3", "mathjax"], function(d3, MathJax) {

    function InfoPanel(container, model, app) {

        var self = this;

        var loading = null;

        this.send = function() {
            var formula = document.getElementById("formula").value;
            var state = document.getElementById("state").value;

            var model_obj = model.save_to_model_object()
            model_obj.logic = document.getElementById("logic").value;


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

                    console.log(data.model);

                    if(data.truth_value) {
                        response.className += " success"
                    } else {
                        response.className += " failure"
                    }

                    MathJax.Hub.Queue(["Typeset", MathJax.Hub, "response"]);

                    var new_model = JSON.parse(data.model);

                    model.load_from_model_object(new_model);
                    app.redraw();

                    document.getElementById("playground").removeChild(loading);
                })
                .on("error", function(error) {
                    console.log("error");
                    document.getElementById("playground").removeChild(loading);
                    d3.select('#response')
                        .classed('failure', true)
                        .html(JSON.parse(error.response).title);
                    console.log(JSON.parse(error.response).title);

                })
                .post(JSON.stringify({
                    state: state,
                    formula: formula,
                    model: model_obj
                }));

            console.log(JSON.stringify({
                state: state,
                formula: formula,
                model: model_obj
            }));
        };

        this.init = function() {
            var submit_button = document.getElementById("json_submit_button");
            submit_button.onclick = self.send;
        };
    }
    return InfoPanel;
});
