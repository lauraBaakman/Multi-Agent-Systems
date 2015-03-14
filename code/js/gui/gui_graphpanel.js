define("gui_graphpanel", ["d3"], function(d3) {

    // With real objects now
    function GuiGraphPanel() {

        var self = this;

        // Setup for d3 svg canvas
        var initSvg = function(container) {
            var _svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height);
            return _svg;
        };

        var initLayout = function() {
            var _layout = d3.layout.force()
                .nodes(nodes)
                .links(links)
                .size([self.width, self.height])
                .linkDistance(150)
                .charge(-500)
                .on('tick', tick);
        };

        var initMarkers = function() {
            self.svg.append('svg:defs').append('svg:marker')
                .attr('id', 'end-arrow')
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 6)
                .attr('markerWidth', 3)
                .attr('markerHeight', 3)
                .attr('orient', 'auto')
                .append('svg:path')
                .attr('d', 'M0,-5L10,0L0,5')
                .attr('fill', '#000');

            self.svg.append('svg:defs').append('svg:marker')
                .attr('id', 'start-arrow')
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 4)
                .attr('markerWidth', 3)
                .attr('markerHeight', 3)
                .attr('orient', 'auto')
                .append('svg:path')
                .attr('d', 'M10,-5L0,0L10,5')
                .attr('fill', '#000');
        };

        /**
         *	Initializes everything ;)
         *	width - width of the svg container
         * 	height - height of the svg container
         * 	container - css id/class identifier
         */
        this.init = function(width, height, container) {
            // Need to be given to the constructor
            self.width = width;
            self.height = height;

            // Don't care about what colors we use.
            self.colors = d3.scale.category10();

            // Setup SVG for D3
            self.svg = initSvg(container);

            // Setup d3 force layout
            self.layout = initLayout()

            initMArkers();
        };
    }

    // Export the global methods
    return {
        GuiGraphPanel: GuiGraphPanel
    }
});
