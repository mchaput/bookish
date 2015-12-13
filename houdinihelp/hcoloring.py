from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import *


class VexLexer(RegexLexer):
    name = 'VEX'
    aliases = ['vex']
    filenames = ['*.vex']
    mimetypes = ['application/x-vex']

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    tokens = {
        'whitespace': [
            (r'^\s*#if\s+0', Comment.Preproc, 'if0'),
            (r'^\s*#', Comment.Preproc, 'macro'),
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text), # line continuation
            (r'//.*?\n', Comment),
            (r'/[*](.|\n)*?[*]/', Comment),
        ],
        'statements': [
            (r'"', String, 'dqstring'),
            (r'\'', String, 'sqstring'),
            (r'r"', String, 'rdqstring'),
            (r'r\'', String, 'rsqstring'),
            (r'(0x[0-9a-fA-F]|0[0-7]+|(\d+\.\d*|\.\d+)|\d+)'
             r'e[+-]\d+[lL]?', Number.Float),
            (r'0x[0-9a-fA-F]+[Ll]?', Number.Hex),
            (r'0[0-7]+[Ll]?', Number.Oct),
            (r'(\d+\.\d*|\.\d+)', Number.Float),
            (r'\d+', Number.Integer),
            (r'[~!%^&*()+=|\[\]:,.<>/?-]', Text),
            (r'(break|continue|do|else|export|forpoints|illuminance|gather|'
             r'for|foreach|if|return|while|const|_Pragma)\b', Keyword),
            (r'(int|float|vector|vector2|vector4|matrix|matrix3|string|bsdf|void)\b', Keyword.Type),
            (r'__(vex|vex_major|vex_minor)\b', Keyword.Reserved),
            (r'__(LINE|FILE|DATE|TIME)__\b', Keyword.Reserved),
            ('[a-zA-Z_][a-zA-Z0-9_]*:', Name.Label),
            ('[a-zA-Z_][a-zA-Z0-9_]*', Name),
        ],
        'root': [
            include('whitespace'),
            # functions
            (r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
             r'([a-zA-Z_][a-zA-Z0-9_]*)'             # method name
             r'(\s*\([^;]*?\))'                      # signature
             r'(' + _ws + r')({)',
             bygroups(using(this), Name.Function, using(this), Text, Keyword),
             'function'),
            # function declarations
            (r'((?:[a-zA-Z0-9_*\s])+?(?:\s|[*]))'    # return arguments
             r'([a-zA-Z_][a-zA-Z0-9_]*)'             # method name
             r'(\s*\([^;]*?\))'                      # signature
             r'(' + _ws + r')(;)',
             bygroups(using(this), Name.Function, using(this), Text, Text)),
            ('', Text, 'statement'),
        ],
        'statement' : [
            include('whitespace'),
            include('statements'),
            ('[{}]', Keyword),
            (';', Text, '#pop'),
        ],
        'function': [
            include('whitespace'),
            include('statements'),
            (';', Text),
            ('{', Keyword, '#push'),
            ('}', Keyword, '#pop'),
        ],
        'dqstring': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\"\n]+', String), # all other characters
            (r'\\\n', String), # line continuation
            (r'\\', String), # stray backslash
        ],
        'sqstring': [
            (r'[\'"]', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (r'[^\\\'\n]+', String), # all other characters
            (r'\\\n', String), # line continuation
            (r'\\', String), # stray backslash
        ],
        'rdqstring': [
            (r'"', String, '#pop'),
            (r'[^\\"\n]+', String), # all other characters
            (r'\\\n', String), # line continuation
            (r'\\', String), # stray backslash
        ],
        'rsqstring': [
            (r'[\'"]', String, '#pop'),
            (r'[^\\\'\n]+', String), # all other characters
            (r'\\\n', String), # line continuation
            (r'\\', String), # stray backslash
        ],
        'macro': [
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment),
            (r'//.*?\n', Comment, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ],
        'if0': [
            (r'^\s*#if.*?(?<!\\)\n', Comment, '#push'),
            (r'^\s*#endif.*?(?<!\\)\n', Comment, '#pop'),
            (r'.*?\n', Comment),
        ]
    }


class HScriptLexer(RegexLexer):
    name = 'HScript'
    aliases = ['hscript', 'Hscript']
    filenames = ['*.cmd']
    mimetypes = ['application/x-hscript']

    tokens = {'root': [
            (r'\b(set|if|then|else|endif|for|to|step|foreach|while|end|'
             r'break|continue)\s*\b',
             Keyword),
        
            (r'^\s*([A-Za-z][A-Za-z0-9_]+)\s*\b',
             Name.Builtin),
             
            (r'\s(-[A-Za-z][A-Za-z0-9_]*)', Operator.Word),
             
            (r'#.*\n', Comment),
            
            (r'(\b\w+\s*)(=)', bygroups(Name.Variable, Operator)),
            (r'[\[\]{}\(\)=]+', Operator),
            (r'(==|!=|<|>|<=|>=|&&|\|\|)', Operator),
            
            (r'\$\(', Keyword, 'paren'),
            (r'\${', Keyword, 'curly'),
            (r'`.+`', String.Backtick),
            (r'(\d+\.)?(\d+)(?= |\Z)', Number),
            (r'\$#?(\w+|.)', Name.Variable),
            (r'"(\\\\|\\[0-7]+|\\.|[^"])*"', String.Double),
            (r"'(\\\\|\\[0-7]+|\\.|[^'])*'", String.Single),
            (r'\s+', Text),
            (r'[^=\s\n]+', Text),
        ],
        'curly': [
            (r'}', Keyword, '#pop'),
            (r':-', Keyword),
            (r'[^}:]+', Punctuation),
            (r':', Punctuation),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            (r'[^)]*', Punctuation),
        ],
    }
    





