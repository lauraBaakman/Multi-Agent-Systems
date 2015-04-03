define("gui_listener", ["d3"], function(d3) {

    function Listener(graph_canvas, model) {
        var self = this;

        var gui = graph_canvas;

        var last_key_down = -1;

        var mousedown_node = null;
        var mouseup_node = null;
        var mousedown_link = null;

        this.mousedown = function() {
            // console.log("Mouse down");
            if (last_key_down === 65) {
                model.add_state();
                gui.draw();
            }
        };

        this.mousemove = function() {
            if (!mousedown_node) return;
            // update drag line
            gui.drag_line
                .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);

            gui.draw();
        };

        var reset_mouse_vars = function() {
            mousedown_node = null;
            mouseup_node = null;
        };

        this.mouseup = function(d) {
            // console.log("Mouse up");
            if (mousedown_node) {
                // hide drag line
                gui.drag_line
                    .classed('hidden', true)
                    .style('marker-end', '');
            }
            // because :active only works in WebKit?
            // gui.get_canvas().classed('active', false);
            // clear mouse event vars
            reset_mouse_vars();
        };

        this.mousedown_state = function(d) {
            // console.log("Mouse down on state: " + d.id);

            if (d3.event.altKey) return;
            // select node
            mousedown_node = d;

            if (mousedown_node === gui.selected_node) {
                set_selected_node(null);
            } else {
                set_selected_node(mousedown_node);
            }
            set_selected_link(null);

            // reposition drag line
            gui.drag_line
                .style('marker-end', 'url(#end-arrow)')
                .classed('hidden', false)
                .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);

            gui.draw();
        };

        this.mouseup_state = function(d) {
            // console.log("Mouse up on state: " + d.id);

            if (!mousedown_node) return;
            // needed by FF
            gui.drag_line
                .classed('hidden', true)
                .style('marker-end', '');

            // check for drag-to-self
            mouseup_node = d;
            if (mouseup_node === mousedown_node) {
                reset_mouse_vars();
                return;
            }

            if (model.link_exists(mousedown_node.id, mouseup_node.id) === null) {
                var link_id = model.add_link(mousedown_node.id, mouseup_node.id);
                model.add_agent_to_link(link_id, 0);
                set_selected_node(null);
                gui.draw();
            }
        }

        this.mousedown_link = function(d) {
            // console.log('Mousedown on link: ' + d.id);
            if (d3.event.altKey) return;

            // select link
            mousedown_link = d;
            if (mousedown_link === gui.selected_link) {
                set_selected_link(null);
            } else {
                set_selected_link(mousedown_link);
            }
            set_selected_node(null);

            // console.log(gui.selected_link);
            gui.draw();
        }

        this.keydown = function() {
            d3.event.preventDefault();

            if (last_key_down !== -1) return;
            last_key_down = d3.event.keyCode;

            if (d3.event.keyCode === 18) {
                gui.nodes.call(gui.layout.drag);
                // gui.get_canvas().classed('alt', true);
            }

            if (!gui.selected_node && !gui.selected_link) return;
            switch (d3.event.keyCode) {
                case 8: // backspace
                case 46: // delete
                    if (gui.selected_node) {
                        // console.log("Delete selected node!" + gui.selected_node.id);
                        model.remove_state(gui.selected_node.id);
                    } else if (gui.selected_link) {
                        // console.log("Delete selected link!" + gui.selected_link.id);
                        model.remove_link(gui.selected_link.id);
                    }
                    set_selected_node(null);
                    set_selected_link(null);

                    gui.draw();
                    break;
                case 82: // r
                    if (gui.selected_node) {
                        if (gui.selected_node.reflexive === false) {
                            // model.add_link(gui.selected_node.id, gui.selected_node.id);
                            model.get_state(gui.selected_node.id).reflexive = true;
                            model.get_state(gui.selected_node.id).agents.push(0);
                            // console.log(gui.selected_node);
                        } else {
                            // model.remove_link(model.link_exists(gui.selected_node.id, gui.selected_node.id));
                            model.get_state(gui.selected_node.id).reflexive = false;
                            model.get_state(gui.selected_node.id).agents = [];
                        }
                    }
                    set_selected_link(null);
                    set_selected_node(null);
                    gui.draw();
                    break;
            }

        };

        this.keyup = function() {
            last_key_down = -1;

            if (d3.event.keyCode === 18) {
                gui.nodes
                    .on('mousedown.drag', null)
                    .on('touchstart.drag', null);
            }
        };

        // Visibility of the state and link info

        var set_active = function(id, bool) {
            d3.select(id).classed("inactive", !bool);
            
        };

        var set_message = function(id, msg) {
            var msg_id = "#message"
            d3.select(id).select(msg_id).html(msg);
        };

        var set_selected_node = function(node) {
            gui.selected_node = node;
            var message = "Currently selected state: ";
            if (node) {
                message += node.id;
                set_active('#state-information', true);
            } else {
                set_active('#state-information', false);
            }
            set_message('#state-information', message);
        };

        var set_selected_link = function(link) {
            gui.selected_link = link;
            var message = "Currently selected link: ";
            if (link) {
                message += link.id;
                set_active('#link-information', true);
                activate_buttons(link);
            } else {
                set_active('#link-information', false);
            }
            set_message('#link-information', message);
        };

        // Editing of selected states and links 

        var activate_buttons = function(link) {
            d3.select('#select-agents').selectAll('button').classed('active', false);
            link.agents.forEach(function(agent){
                d3.select('#select-agents').select('#btn' + agent).classed('active', true);
            });
        };

        this.select_agent = function(agent) {
            var agents = d3.set(gui.selected_link.agents);
            if(!agents.has(agent)) {
                gui.selected_link.agents.push(agent);
            } else {
                var link = model.get_link(model.link_exists(gui.selected_link.source.id, gui.selected_link.target.id));
                link.agents = link.agents.filter(function(a) {
                    return a != agent
                });
            }
            activate_buttons(gui.selected_link);
            gui.reset();
        };
    }
    return Listener;
});
