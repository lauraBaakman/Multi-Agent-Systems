define("gui_info_panel", ["d3"], function(d3) {

	function InfoPanel(container) {

		this.send = function() {
			// Ajax call to backend to send the formula
			// d3.json(url, callback) :)

			// Maybe only preprocess and give a json/string 
			// back and let the app.js send it
		};
	}

	return InfoPanel;

});