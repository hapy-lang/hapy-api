// Difficulty: "Moderate"
// Hapy language definition.
// Only trickiness is that we need to check strings before identifiers
// since they have letter prefixes. We also treat ':' as an @open bracket
// in order to get auto identation.
function monarchSettings () { return {
	defaultToken: 'invalid',
	tokenPostfix: '.hapy',

	keywords: [
        'in', 'if',
        'then', 'then',
        'indai', 'while',
        'ma', 'for',
        'karo', 'import',
        'iri', 'class',
        'yanada', 'has',
        'gada', 'inherits',
        'anfani', 'use',
        'wuce', 'pass',
        'daga', 'from',
        'imbahakaba', 'else',
        'cikin', 'in',
        'Babu', 'None',
        'dawo', 'return',
        'ayyana', 'def',
        'Gaskiya', 'True',
        'Karya', 'False',

		'int',
		'float',
		'long',
		'complex',
		'hex',

		'abs',
		'all',
		'any',
		'apply',
		'basestring',
		'bin',
		'bool',
		'buffer',
		'bytearray',
		'callable',
		'chr',
		'classmethod',
		'cmp',
		'coerce',
		'compile',
		'complex',
		'delattr',
		'dict',
		'dir',
		'divmod',
		'enumerate',
		'eval',
		'execfile',
		'file',
		'filter',
		'format',
		'frozenset',
		'getattr',
		'globals',
		'hasattr',
		'hash',
		'help',
		'id',
		'input',
		'intern',
		'isinstance',
		'issubclass',
		'iter',
		'len',
		'locals',
		'list',
		'map',
		'max',
		'memoryview',
		'min',
		'next',
		'object',
		'oct',
		'open',
		'ord',
		'pow',
		'print',
		'property',
		'reversed',
		'range',
		'raw_input',
		'reduce',
		'reload',
		'repr',
		'reversed',
		'round',
		'set',
		'setattr',
		'slice',
		'sorted',
		'staticmethod',
		'str',
		'sum',
		'super',
		'tuple',
		'type',
		'unichr',
		'unicode',
		'vars',
		'xrange',
		'zip',

		'True',
		'False',

		'__dict__',
		'__methods__',
		'__members__',
		'__class__',
		'__bases__',
		'__name__',
		'__mro__',
		'__subclasses__',
		'__init__',
		'__import__'
	],

	brackets: [
		{ open: '{', close: '}', token: 'delimiter.curly' },
		{ open: '[', close: ']', token: 'delimiter.bracket' },
		{ open: '(', close: ')', token: 'delimiter.parenthesis' }
	],

	tokenizer: {
		root: [
			{ include: '@whitespace' },
			{ include: '@numbers' },
			{ include: '@strings' },

			[/[,:;]/, 'delimiter'],
			[/[{}\[\]()]/, '@brackets'],

			[/@[a-zA-Z]\w*/, 'tag'],
			[/[a-zA-Z]\w*/, {
				cases: {
					'@keywords': 'keyword',
					'@default': 'identifier'
				}
			}]
		],

		// Deal with white space, including single and multi-line comments
		whitespace: [
			[/\s+/, 'white'],
			[/(^#.*$)/, 'comment'],
			[/('''.*''')|(""".*""")/, 'string'],
			[/'''.*$/, 'string', '@endDocString'],
			[/""".*$/, 'string', '@endDblDocString']
		],
		endDocString: [
			[/\\'/, 'string'],
			[/.*'''/, 'string', '@popall'],
			[/.*$/, 'string']
		],
		endDblDocString: [
			[/\\"/, 'string'],
			[/.*"""/, 'string', '@popall'],
			[/.*$/, 'string']
		],

		// Recognize hex, negatives, decimals, imaginaries, longs, and scientific notation
		numbers: [
			[/-?0x([abcdef]|[ABCDEF]|\d)+[lL]?/, 'number.hex'],
			[/-?(\d*\.)?\d+([eE][+\-]?\d+)?[jJ]?[lL]?/, 'number']
		],

		// Recognize strings, including those broken across lines with \ (but not without)
		strings: [
			[/'$/, 'string.escape', '@popall'],
			[/'/, 'string.escape', '@stringBody'],
			[/"$/, 'string.escape', '@popall'],
			[/"/, 'string.escape', '@dblStringBody']
		],
		stringBody: [
			[/[^\\']+$/, 'string', '@popall'],
			[/[^\\']+/, 'string'],
			[/\\./, 'string'],
			[/'/, 'string.escape', '@popall'],
			[/\\$/, 'string']
		],
		dblStringBody: [
			[/[^\\"]+$/, 'string', '@popall'],
			[/[^\\"]+/, 'string'],
			[/\\./, 'string'],
			[/"/, 'string.escape', '@popall'],
			[/\\$/, 'string']
		]
	}
};
}