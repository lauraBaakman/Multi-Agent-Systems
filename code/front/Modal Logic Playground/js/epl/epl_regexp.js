// name, deps, callback
define("epl_regexp", [], function() {
	'use strict';

    // sub-regexes
    var beginPart = '^\\(',
        unaryPart = '(?:~|\\[\\]|<>)',
        propOrBinaryPart = '(?:\\w+|\\(.*\\))',
        subwffPart = unaryPart + '*' + propOrBinaryPart,
        endPart = '\\)$';

    // binary connective regexes
    var conjRegEx = new RegExp(beginPart + '(' + subwffPart + ')&(' + subwffPart + ')' + endPart), // (p&q)
        disjRegEx = new RegExp(beginPart + '(' + subwffPart + ')\\|(' + subwffPart + ')' + endPart), // (p|q)
        implRegEx = new RegExp(beginPart + '(' + subwffPart + ')->(' + subwffPart + ')' + endPart), // (p->q)
        equiRegEx = new RegExp(beginPart + '(' + subwffPart + ')<->(' + subwffPart + ')' + endPart); // (p<->q)

    // proposition regex
    var propRegEx = /^\w+$/;


    // Global objects
    return {
    	conjunction: conjRegEx,
		disjunction: disjRegEx,
		implication: implRegEx,
		equivalence: equiRegEx,
		proposition: propRegEx 
    };

});
