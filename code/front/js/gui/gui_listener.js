define("gui_listener", ["d3"], function(d3) {

    function Listener(graph_canvas) {
    	var self = this;

        var gui = graph_canvas;

        var last_key_down = -1;

        var mousedown_node = null;
        var mouseup_node = null;

        this.mousedown = function() {
            if (d3.event.altKey || mousedown_node) return;

            gui.get_model().add_state();
            gui.draw();
        };

        this.mousemove = function() {
            if (!mousedown_node) return;
            // update drag line
            gui.get_drag_line()
            	.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);

            gui.draw();
        };

        this.reset_mouse_vars = function() {
            mousedown_node = null;
            mouseup_node = null;
        };

        this.mouseup = function() {
            if (mousedown_node) {
                // hide drag line
                gui.get_drag_line()
                    .classed('hidden', true)
                    .style('marker-end', '');
            }
            // because :active only works in WebKit?
            // svg.classed('active', false);

            // clear mouse event vars
            self.reset_mouse_vars();
        };

        this.mousedown_state = function(d) {
            if (d3.event.altKey) return;
            // select node
            mousedown_node = d;
            if (mousedown_node === gui.selected_node) gui.selected_node = null;
            else gui.selected_node = mousedown_node;
            gui.selected_link = null;

            // reposition drag line
            gui.get_drag_line()
                .style('marker-end', 'url(#end-arrow)')
                .classed('hidden', false)
                .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);

            gui.draw();
        };

        this.mouseup_state = function(d) {
        	console.log("bleh");
            if (!mousedown_node) return;

            console.log(d);

            // needed by FF
            gui.get_drag_line()
                .classed('hidden', true)
                .style('marker-end', '');

            // check for drag-to-self
            mouseup_node = d;
            if (mouseup_node === mousedown_node) {
                self.reset_mouse_vars();
                return;
            }

            gui.get_model.add_link(mousedown_node.id, mouseup_node.id);

            // selected_link = link;
            gui.selected_node = null;
            gui.draw();
        }

        this.keydown = function() {
            d3.event.preventDefault();

            if (last_key_down !== -1) return;
            last_key_down = d3.event.keyCode;

            // // ctrl
            // if (d3.event.keyCode === 18) {
            //     // circle.call(force.drag);
            //     // gui.get_canvas().classed('alt', true);
            // }

            last_key_down = -1;
        };


    }

    return Listener;

});
