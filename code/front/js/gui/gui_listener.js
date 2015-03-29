define("gui_listener", ["d3"], function(d3) {

    function Listener(graph_canvas) {
        var self = this;

        var gui = graph_canvas;

        var last_key_down = -1;

        var mousedown_node = null;
        var mouseup_node = null;
        var mousedown_link = null;

        this.mousedown = function() {
            console.log("Mouse down");
            if (last_key_down === 65) {
                gui.get_model().add_state();
                gui.draw();
            }
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

        this.mouseup = function(d) {
            console.log("Mouse up");
            if (mousedown_node) {
                // hide drag line
                gui.get_drag_line()
                    .classed('hidden', true)
                    .style('marker-end', '');
            }
            // because :active only works in WebKit?
            // gui.get_canvas().classed('active', false);
            // clear mouse event vars
            self.reset_mouse_vars();
        };

        this.mousedown_state = function(d) {
            console.log("Mouse down on state: " + d.id);

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
            console.log("Mouse up on state: " + d.id);

            if (!mousedown_node) return;
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

            if (gui.get_model().link_exists(mousedown_node.id, mouseup_node.id) === null) {
                gui.get_model().add_link(mousedown_node.id, mouseup_node.id);
                gui.selected_node = null;
                gui.draw();
            }
        }

        this.mousedown_link = function(d) {
            console.log('Mousedown on link: ' + d.id);
            if (d3.event.altKey) return;

            // select link
            mousedown_link = d;
            if (mousedown_link === gui.selected_link) gui.selected_link = null;
            else gui.selected_link = mousedown_link;
            gui.selected_node = null;

            console.log(gui.selected_link);
            gui.draw();
        }

        this.keydown = function() {
            d3.event.preventDefault();

            if (last_key_down !== -1) return;
            last_key_down = d3.event.keyCode;

            if (d3.event.keyCode === 18) {
                gui.get_nodes().call(gui.get_layout().drag);
                // gui.get_canvas().classed('alt', true);
            }

            if (!gui.selected_node && !gui.selected_link) return;
            switch (d3.event.keyCode) {
                case 8: // backspace
                case 46: // delete
                    if (gui.selected_node) {
                        console.log("Delete selected node!" + gui.selected_node.id);
                        gui.get_model().remove_state(gui.selected_node.id);
                    } else if (gui.selected_link) {
                        console.log("Delete selected link!" + gui.selected_link.id);
                        gui.get_model().remove_link(gui.selected_link.id);
                    }
                    gui.selected_link = null;
                    gui.selected_node = null;
                    gui.draw();
                    break;
            }

        };

        this.keyup = function() {
            last_key_down = -1;

            if (d3.event.keyCode === 18) {
                gui.get_nodes()
                    .on('mousedown.drag', null)
                    .on('touchstart.drag', null);
            }
        };
    }

    return Listener;

});
