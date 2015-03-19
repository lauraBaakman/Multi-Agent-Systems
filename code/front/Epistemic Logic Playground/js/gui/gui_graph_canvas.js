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
            links = null;

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
            // console.log("states in init_layout: ");
            // console.log(model.get_states());

            // console.log("links in init_layout: ");
            // console.log(model.get_links());

            layout = d3.layout.force()
                .nodes(model.get_states())
                .links(model.get_links())
                .size([width, height])
                .linkDistance(150)
                .charge(-500)
                .on('tick', tick);
        }

        function tick() {
            links.attr('d', function(d) {
                var deltaX = d.target.x - d.source.x,
                    deltaY = d.target.y - d.source.y,
                    dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
                    normX = deltaX / dist,
                    normY = deltaY / dist,
                    sourcePadding = d.left ? 17 : 12,
                    targetPadding = d.right ? 17 : 12,
                    sourceX = d.source.x + (sourcePadding * normX),
                    sourceY = d.source.y + (sourcePadding * normY),
                    targetX = d.target.x - (targetPadding * normX),
                    targetY = d.target.y - (targetPadding * normY);
                return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;

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
                .attr('markerWidth', 3)
                .attr('markerHeight', 3)
                .attr('orient', 'auto')
                .append('svg:path')
                .attr('d', 'M0,-5L10,0L0,5')
                .attr('fill', '#000');

            canvas.append('svg:defs').append('svg:marker')
                .attr('id', 'start-arrow')
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 4)
                .attr('markerWidth', 3)
                .attr('markerHeight', 3)
                .attr('orient', 'auto')
                .append('svg:path')
                .attr('d', 'M10,-5L0,0L10,5')
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
        }

        function draw_paths() {
            // path (link) group
            links = links.data(model.get_links());

            // update existing links
            links.classed('selected', function(d) {
                    return d === selected_link;
                })
                .style('marker-start', function(d) {
                    return d.left ? 'url(#start-arrow)' : '';
                })
                .style('marker-end', function(d) {
                    return d.right ? 'url(#end-arrow)' : '';
                });

            // add new links
            links.enter().append('svg:path')
                .attr('class', 'link')
                .classed('selected', function(d) {
                    return d === selected_link;
                })
                .style('marker-start', function(d) {
                    return d.left ? 'url(#start-arrow)' : '';
                })
                .style('marker-end', function(d) {
                    return d.right ? 'url(#end-arrow)' : '';
                });

            // remove old links
            links.exit().remove();
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
                    return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id);
                })
                .classed('reflexive', function(d) {
                    return d.reflexive;
                });

            // add new nodes
            var g = nodes.enter().append('svg:g');

            g.append('svg:circle')
                .attr('class', 'node')
                .attr('r', 12)
                .style('fill', function(d) {
                    return (d === selected_node) ? d3.rgb(colors(d.id)).brighter().toString() : colors(d.id);
                })
                .style('stroke', function(d) {
                    return d3.rgb(colors(d.id)).darker().toString();
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
                .attr('x', 16)
                .attr('y', 4)
                .attr('class', 'shadow')
                .text(valuation_to_string);

            // text foreground
            g.append('svg:text')
                .attr('x', 16)
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
