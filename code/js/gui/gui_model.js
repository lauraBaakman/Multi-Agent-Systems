define("gui_model", [], function() {

    function GuiModel() {

        var self = this;

        var initNodes = function(model) {
            var states = model.getStates();
            var nodes = [];
            states.forEach(function(state) {
                if (!state) {
                    self.lastNodeId++;
                    return;
                }
                var defaultVals = propvars.map(function() {
                        return false;
                    }),
                    node = {
                        id: ++self.lastNodeId,
                        vasl: defaultVals,
                        reflexive: false
                    };
                for (var propvar in state) {
                    var index = propvars.indexOf(propvar);
                    if (index !== -1) node.vals[index] = true;
                }
                nodes.push(node);
            });
            return nodes;
        };

        var initLinks = function() {
        	var links = [];
        	var sourceId = source.id,
                successors = model.getSuccessorsOf(sourceId);

        }

        this.init = function(model) {
            self.lastNodeId = -1;
            self.propvars = ['p', 'q', 'r', 's', 't'];
            self.nodes = initNodes(model);
            self.links = initLinks();
        };
    }

    return {
        GuiModel: GuiModel
    };
});
