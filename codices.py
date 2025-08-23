# CONTINUUM: Lets us know the structure of a token, specifically, type and value (.string)
import token
# CONTINUUM: Tokenizes a text stream in-line with Python  syntax 
import tokenize

'''
THROUGHLINE:
Behind all the metaphor, we are parsing Python script files - using the standard `tokenize` library to extract symbolic structure from source code.

Tokenization gives us a symbolic view of the source, simplifying parsing.
It turns complex syntax into a simple (though intermediate) lexicon.

So:
>def parse(source):

becomes:
>NAME NAME OP NAME OP OP

Tokens have limited understanding of their role, but great clarity about what they are.
For example, a token knows that 'def' is a NAME, but not that it's a Python reserved word.

Meaning emerges through layered symbolism.

So:
>NAME NAME OP NAME OP OP

might, if parsing for execution, become:
>keyword identity lbrace identity rbrace colon

But we are not parsing to execute — we are parsing to extract a limited set of precise entities:
prescriptive texts and the things they prescribe, within their Pythonic scope.

We do not care about things like braces and colons.

The base CODEX provides the layered symbolism we do care about.
For example, it tells us whether a NAME token is an ENCAPSULATOR —
a symbol that opens a new scope (like `def` or `class`).

Note: this module fully wraps the TOKEN structure, which is never directly referenced elsewhere.
'''

# KNOWLEDGE: Objects define the nature of subjects. E.g. the subject 'def' is a NAME object, in raw token parlance.
CODEX_OBJECTS = {name: code for code, name in token.tok_name.items()}


'''
AFFORDANCE:
Though literally a tree trunk (from the Latin *codex*), the term has come to signify a book of law — or more precisely, of lore.

Not 'law' in the contemporary sense, but rather 'ritual' or 'rite': the correct sequence of symbols that achieves a result.

And herein, our codices do just that — they prescribe the correct sequence of things in terms of their symbolism (ruinic nature).

In the base CODEX, very little is known beyond the symbolic meaning of what occurs in the provided sequence.

Thus, the base CODEX offers:
- a symbolic lexicon (as a dict),
- a means to generate the sequence (objectify the source),
- and a way to discern the true name (or value) of encountered symbols.
'''
class CODEX:
    # KNOWLEDGE: Symbolises specific python token subjects that direct our layered parsing
    LEXICON = {
        'DECORATOR':     ['@',],
        'ACCESSOR':      ['.',],
        'ENCAPSULATORS': ['class', 'def'],
        'RESERVED': [
            'and', 'as', 'assert', 
            'break', 
            'class', 'continue', 
            'def', 'del', 
            'elif', 'else', 'except', 
            'False', 'finally', 'for', 'from', 
            'global', 
            'if', 'import', 'in', 'is', 
            'lambda', 
            'None', 'nonlocal', 'not', 
            'or', 
            'pass', 
            'raise', 'return', 
            'True', 'try', 
            'while', 'with', 
            'yield'
        ]
    }

    '''
    MECHANISM:
    Encapsulates the tokenisation process
    '''
    @staticmethod
    def objectify(source):
        return tokenize.tokenize(source.readline)

    '''
    MECHANISM:
    We want to contain ALL token structure knowledge to the base CODEX
    so here's how we get to what a token actually IS.
    '''
    def token_val(token):
        return token.string

    '''
    MECHANISM:
    We want to contain ALL token structure knowledge to the base CODEX
    so here's how we get where the token occurred
    '''
    def token_start(token):
        return token.start


'''
AFFORDANCE:
Derived codices apply the base CODEX LEXICON through sets of ENTITIES — statements of what we care about, expressed as layered symbolism, in the derived metaphor.

For example, when building a lineage, we want to ignore Python RESERVED words.
We're interested only in NAME tokens that represent actual Pythonic objects (variables, classes, etc).

Reserved words like `def` and `yield` serve as HONOURIFICS—titles that address true identities.

So we might define:
    HONOURIFICS = ENTITY('NAME', 'RESERVED')
E.g. an HONOURIFIC as any NAME in the set of RESERVED values

Entities are compound matching structures — ritual instruments that determine whether a given 'thing' satisfies the lore of the codex.

Each codex offers a distinct lens on shared material, and begins by defining the entities of interest.
This class serves as their oracle, revealing when those entities have been fulfilled — or left wanting.

The 'things' we encounter consist of both type and value.
Entities allow us to match by type alone, or by both type and value.
'''
class ENTITY:
    def __init__(self, object_name='', candidates=''):
        self.members = {}
        if object_name:
            self.add(object_name, candidates)

    '''
    MECHANISM:
    Extends the ENTITY's potence by adding more types and values it recognises.
    '''
    def add(self, object_name, candidates=''):
        object_type = CODEX_OBJECTS[object_name]
        if candidates:
            self.members[object_type] = CODEX.LEXICON[candidates]
        else:
            self.members[object_type] = []

    '''
    SKILL:
    Determines if this ENTITY recognise a given token.
    '''
    def is_entity(self, token):
        if token.type in self.members:
            if self.members[token.type]:
                return token.string.lower() in self.members[token.type]
            else:
                return True
        return False
