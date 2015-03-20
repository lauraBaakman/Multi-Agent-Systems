define("gui_graph_canvas", ["d3"], function(d3) {

    function GraphCanvas(container, model) {

        var self = this;

        // General visualisation variables
        var canvas,
            layout,
            width,
            height,
            colors,
            drag_line;

        // Specific/model :p visualisation variables
        var nodes = null,
            links = null,
            link_labels = null;

        var selected_link = null;
        var selected_node = null;

        function init_canvas() {
            // Get meassurement of the container of the graph canvas
            width = container.node().getBoundingClientRect().width;
            height = container.node().getBoundingClientRect().height;
            colors = d3.scale.category10();
            canvas = container
                .append('svg')
                .attr('width', width)
                .attr('height', height);
        }

        function init_layout() {
            layout = d3.layout.force()
                .nodes(model.get_states())
                .links(model.get_links())
                .size([width, height])
                .linkDistance(250)
                .charge(-50)
                .on('tick', tick);
        }

        function tick() {
            links.attr('d', function(d) {
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,

                    // Piet
                    dist = Math.sqrt(dx * dx + dy * dy),
                    norm_x = dx / dist,
                    norm_y = dy / dist,
                    
                    source_padding = 0,
                    target_padding = 26,

                    source_x = d.source.x + (source_padding * norm_x),
                    source_y = d.source.y + (source_padding * norm_y),
                    target_x = d.target.x - (target_padding * norm_x),
                    target_y = d.target.y - (target_padding * norm_y);

                var source_id = d.source.id;
                var target_id = d.target.id

                if (model.is_target_state(source_id, target_id)) {
                    return 'M' +
                        source_x + ',' +
                        source_y + 'A' +
                        dist + ',' + dist + ' 0 0,1 ' +
                        target_x + ',' + 
                        target_y;
                }
                return 'M' +
                    source_x + ',' +
                    source_y + 'L' +
                    target_x + ',' + target_y;
            });

            nodes.attr('transform', function(d) {
                return 'translate(' + d.x + ',' + d.y + ')';
            });
        };

        function init_arrow_markers() {
            canvas.append('svg:defs').append('svg:marker')
                .attr('id', 'end-arrow')
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 6)
                .attr('markerWidth', 6)
                .attr('markerHeight', 6)
                .attr('orient', 'auto')
                .append('svg:path')
                .attr('d', 'M0,-5L10,0L0,5')
                .attr('fill', '#000');
        }

        function init_drag_line() {
            drag_line = canvas.append('svg:path')
                .attr('class', 'link dragline hidden')
                .attr('d', 'M0,0L0,0');
        }

        function init_handles() {
            links = canvas.append('svg:g').selectAll('path');
            nodes = canvas.append('svg:g').selectAll('g');
            link_labels = canvas.append('svg:g').selectAll('g.link_labels');
        }

        function relation_to_string(link) {
            var agent_to_unicode = {
                0: '\u2080',
                1: '\u2081',
                2: '\u2082',
                3: '\u2083',
                4: '\u2084',
            }

            var str = 'R\u208D ';

            link.agents.forEach(function(agent) {
                str += agent_to_unicode[agent];
            });

            return str + ' \u208E'
        }

        function draw_paths() {
            // path (link) group
            links = links.data(model.get_links());

            // update existing links
            links.classed('selected', function(d) {
                    return d === selected_link;
                })
                .style('marker-end', function(d) {
                    return 'url(#end-arrow)';
                });

            // add new links
            links.enter().append('svg:path')
                .attr('class', 'link')
                .classed('selected', function(d) {
                    return d === selected_link;
                })
                .style('marker-end', function(d) {
                    return 'url(#end-arrow)';
                })
                .attr("id", function(d) {
                    return "linkId_" + d.id;
                });

            // remove old links
            links.exit().remove();

            link_labels = link_labels.data(model.get_links());

            link_labels.enter().append("g").attr("class", "link_label_holder")
                .append("text")
                .attr("class", "link_label")
                .attr("dx", 110)
                .attr("dy", -8)
                .attr("text-anchor", "middle")
                .append("textPath")
                .attr("xlink:href", function(d) {
                    return "#linkId_" + d.id;
                })
                .text(relation_to_string);
        }

        function valuation_to_string(node) {
            var vals = node.vals,
                output_props = [];
            for (var i = 0; i < model.get_prop_count(); i++) {
                // attach 'not' symbol to false values
                output_props.push((vals[i] ? '' : '\u00ac') + model.get_default_props()[i]);
            }
            return output_props.join(', ');
        }

        function draw_nodes() {
            // circle (node) group
            // NB: the function arg is crucial here! nodes are known by id, not by index!
            nodes = nodes.data(model.get_states(), function(d) {
                return d.id;
            });

            // update existing nodes (reflexive & selected visual states)
            nodes.selectAll('circle')
                .style('fill', function(d) {
                    return (d === selected_node) ? d3.rgb('#DDD').brighter().toString() : d3.rgb('#DDD');
                })
                .classed('reflexive', function(d) {
                    return d.reflexive;
                });

            // add new nodes
            var g = nodes.enter().append('svg:g');

            g.append('svg:circle')
                .attr('class', 'node')
                .attr('r', 22)
                .style('fill', function(d) {
                    return (d === selected_node) ? d3.rgb('#DDD').brighter().toString() : d3.rgb('#DDD');
                })
                .style('stroke', function(d) {
                    return d3.rgb('#DDD').darker().toString();
                })
                .classed('reflexive', function(d) {
                    return d.reflexive;
                });

            // show node IDs
            g.append('svg:text')
                .attr('x', 0)
                .attr('y', 4)
                .attr('class', 'id')
                .text(function(d) {
                    return d.id;
                });

            // text shadow
            g.append('svg:text')
                .attr('x', 24)
                .attr('y', 4)
                .attr('class', 'shadow')
                .text(valuation_to_string);

            // text foreground
            g.append('svg:text')
                .attr('x', 24)
                .attr('y', 4)
                .text(valuation_to_string);

            // remove old nodes
            nodes.exit().remove();
        }

        this.draw = function() {
            draw_paths();
            draw_nodes();
            layout.start();
        }

        this.start = function() {
            // General canvas and force layout
            init_canvas();
            init_layout();

            // Init the variable drawable object (nodes, links)
            init_handles();

            // Define helper objects
            init_arrow_markers();
            init_drag_line();

            // First draw call
            self.draw();
        }
    }
    return GraphCanvas
});
