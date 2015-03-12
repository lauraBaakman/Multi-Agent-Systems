define("epl_formula", ["epl_converters"], function(epl_converters) {
/**
     * Constructor for EPL wff. Takes either ASCII or JSON representation as input.
     * @constructor
     */
    function Formula(asciiOrJSON) {
        // Strings for the four representations: ASCII, JSON, LaTeX, and Unicode.
        var _ascii = '',
            _json = '',
            _latex = '',
            _unicode = '';

        this.ascii = function() {
            return _ascii;
        };

        this.json = function() {
            return _json;
        };

        this.latex = function() {
            return _latex;
        };

        this.unicode = function() {
            return _unicode;
        };

        if (typeof asciiOrJSON === 'string') {
            // ASCII input: remove whitespace before conversion, re-insert it after
            var ascii = asciiOrJSON.match(/\S+/g).join('');
            _json = epl_converters.asciiToJSON(ascii);
            _ascii = ascii.replace(/&/g, ' & ')
                .replace(/\|/g, ' | ')
                .replace(/<->/g, '***')
                .replace(/->/g, ' -> ')
                .replace(/\*\*\*/g, ' <-> ');
        } else if (typeof asciiOrJSON === 'object') {
            // JSON input
            var json = asciiOrJSON;
            _ascii = epl_converters.jsonToASCII(json);
            _json = json;
        } else return;

        _latex = epl_converters.asciiToLaTeX(_ascii);
        _unicode = epl_converters.asciiToUnicode(_ascii);
    }

    return {
        Formula: Formula
    };
});