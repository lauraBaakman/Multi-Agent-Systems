define("gui_graph_canvas", ["d3"], function(d3) {

    function GraphCanvas(container, model) {

        var self = this;

        // General visualisation variables
        this.canvas = null;
        this.layout = null;
        this.width = 800;
        this.height = 600;
        this.colors = null;
        this.drag_line = null;

        // Specific/model :p visualisation variables
        this.nodes = null;
        this.links = null;
        this.link_labels = null;

        this.selected_link = null;
        // this.selected_link_id = -1;

        this.selected_node = null;

        var listener = null

        this.set_listener = function(app_listener) {
            listener = app_listener;
        }

        this.get_listener = function() {
            return listener;
        }

        function init_canvas() {
            // Get meassurement of the container of the graph canvas
            var padding = 5;
            self.width = container.node().getBoundingClientRect().width;
            self.height = container.node().getBoundingClientRect().height - padding;
            self.colors = d3.scale.category10();
            self.canvas = container
                .append('svg')
                .attr('width', self.width)
                .attr('height', self.height);

            self.canvas.on('mousedown', listener.mousedown);
            self.canvas.on('mousemove', listener.mousemove);
            self.canvas.on('mouseup', listener.mouseup);
        }

        function init_layout() {
            self.layout = d3.layout.force()
                .nodes(model.get_states())
                .links(model.get_links())
                .size([self.width, self.height])
                .linkDistance(280)
                .charge(-2500)
                .gravity(0.15)
                .on('tick', tick);
        }

        function tick() {
            self.links.attr('d', function(d) {
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y;

                // Piet
                var dist = Math.sqrt(dx * dx + dy * dy);
                if (!dist) return;

                var norm_x = dx / dist,
                    norm_y = dy / dist,

                    source_padding = 0,
                    target_padding = 26,

                    source_x = d.source.x + (source_padding * norm_x),
                    source_y = d.source.y + (source_padding * norm_y),
                    target_x = d.target.x - (target_padding * norm_x),
                    target_y = d.target.y - (target_padding * norm_y);

                var source_id = d.source.id;
                var target_id = d.target.id

                // Curvy lines
                if (model.is_target_state(source_id, target_id)) {
                    return 'M' +
                        source_x + ',' +
                        source_y + 'A' +
                        dist + ',' + dist + ' 0 0,1 ' +
                        target_x + ',' +
                        target_y;
                } // Straight lines
                return 'M' +
                    source_x + ',' +
                    source_y + 'L' +
                    target_x + ',' + target_y;
            });

            self.nodes.attr('transform', function(d) {
                return 'translate(' + d.x + ',' + d.y + ')';
            });
        };

        function init_arrow_markers() {
            self.canvas.append('svg:defs').append('svg:marker')
                .attr('id', 'end-arrow')
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 5)
                .attr('markerWidth', 5)
                .attr('markerHeight', 5)
                .attr('orient', 'auto')
                .append('svg:path')
                .attr('d', 'M0,-5L10,0L0,5')
                .attr('fill', '#aaa');
        }

        function init_drag_line() {
            self.drag_line = self.canvas.append('svg:path')
                .attr('class', 'link dragline hidden')
                .attr('d', 'M0,0L0,0');
        }

        function init_handles() {
            self.links = self.canvas.append('svg:g').selectAll('path');
            self.nodes = self.canvas.append('svg:g').selectAll('g');
            self.link_labels = self.canvas.append('svg:g').selectAll('g.link_labels').append("g").attr("class", "link_label_holder");
        }

        function relation_to_string(link) {
            var agent_to_unicode = {
                    1: '\u2081',
                    2: '\u2082',
                    3: '\u2083',
                    4: '\u2084',
                    5: '\u2085'
                }
                // ( \u208D ) '\u208E'
            var str = 'R';
            console.log(link.agents);
            link.agents.forEach(function(agent) {
                console.log(agent);
                str += agent_to_unicode[agent];
            });
            return str;
        }

        function draw_paths() {
            // path (link) group
            self.links = self.links.data(model.get_links());

            // update existing links
            self.links.classed('selected', function(d) {
                    return d === self.selected_link;
                })
                .style('marker-end', function(d) {
                    return 'url(#end-arrow)';
                });

            // add new links
            self.links.enter().append('svg:path')
                .attr('class', 'link')
                .classed('selected', function(d) {
                    return d === self.selected_link;
                })
                .style('marker-end', function(d) {
                    return 'url(#end-arrow)';
                })
                .attr("id", function(d) {
                    return "linkId_" + d.id;
                })
                .on('mousedown', listener.mousedown_link);

            // remove old links
            self.links.exit().remove();

            self.link_labels = self.link_labels.data(model.get_links());

            self.link_labels.enter()
                .append("text")
                .attr("class", "link_label")
                .attr("dx", 110)
                .attr("dy", -8)
                .attr("text-anchor", "middle")
                .append("textPath")
                .attr("xlink:href", function(d) {
                    return "#linkId_" + d.id;
                })
                .text(relation_to_string)
                .attr('font-size', '16px')
                .style('fill', 'rgb(37, 91, 141)')
                .attr('stroke', 'black')
                .attr('stroke-width', '.3px');
            self.link_labels.exit().remove();
        }

        function valuation_to_string(node) {
            var vals = node.vals,
                output_props = [];
            for (var i = 0; i < model.get_prop_count(); i++) {
                // attach 'not' symbol to false values
                output_props.push((vals[i] ? '' : '\u00ac') + model.get_props()[i]);
            }
            return output_props.join(', ');
        }

        function draw_nodes() {
            // NB: the function arg is crucial here! nodes are known by id, not by index!
            self.nodes = self.nodes.data(model.get_states(), function(d) {
                return d.id;
            });

            // update existing nodes (reflexive & selected visual states)
            self.nodes.selectAll('circle')
                .style('fill', function(d) {
                    return (d === self.selected_node) ? d3.rgb('#DDD').brighter().toString() : d3.rgb('#DDD');
                })
                .classed('reflexive', function(d) {
                    return d.reflexive;
                });

            // add new nodes
            var g = self.nodes.enter().append('svg:g');

            g.append('svg:circle')
                .attr('class', 'node')
                .attr('r', 20)
                .style('fill', function(d) {
                    return (d === self.selected_node) ? d3.rgb('#DDD').brighter().toString() : d3.rgb('#DDD');
                })
                .style('stroke', function(d) {
                    return d3.rgb('#DDD').darker().toString();
                })
                .classed('reflexive', function(d) {
                    return d.reflexive;
                })
                .on('mousedown', listener.mousedown_state)
                .on('mouseup', listener.mouseup_state);

            // show node IDs
            g.append('svg:text')
                .attr('x', 0)
                .attr('y', 4)
                .attr('class', 'id')
                .text(function(d) {
                    return d.id;
                })
                .attr('font-size', '16px');

            // rgb(37, 91, 141) rgb(48, 101, 46) 193, 13, 60
            // text foreground
            g.append('svg:text')
                .attr('x', 24)
                .attr('y', 4)
                .attr('font-size', '16px')
                .attr('stroke', 'black')
                .attr('stroke-width', '.3px')
                .attr('fill', 'rgb(193, 13, 60) ')
                .text(valuation_to_string);

            // remove old nodes
            self.nodes.exit().remove();
        }

        this.draw = function() {
            // model = app.get_model();
            draw_paths();
            draw_nodes();
            self.layout.start();
        }

        this.reset = function() {
            // console.log('reset');
            self.layout.stop();

            self.canvas.remove();
            // self.canvas.selectAll('*').remove();
            self.start();
        }

        this.start = function() {
            d3.select('#num-props').select('#btn' + model.get_prop_count()).classed('active', true);
            d3.select('#select-props-state').selectAll('button').classed('disabled', true);
            for (var idx = 0; idx < model.get_prop_count(); idx++) {
                d3.select('#select-props-state').select('#btn' + idx).classed('disabled', false);
            }

            d3.select(window)
                .on('keydown', listener.keydown)
                .on('keyup', listener.keyup);

            init_canvas();
            init_layout();

            init_handles();

            init_arrow_markers();
            init_drag_line();

            self.draw();
        }
    }
    return GraphCanvas
});
