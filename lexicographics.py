# CONTINUUM: allows us to create named structures for attestations, and lexemes
from dataclasses import dataclass
from dataclasses import field
from typing import List, Tuple

# CONTINUUM: allows us to create the ExpoTags (Enum) list
from enum import Enum

from granulator import GrainType as LexicalCategory

# KNOWLEDGE: The types of semantic meaning we can use to adorn our code-base.
class ExpoTags(Enum):
    # PROSE:
    # CONTINUUM - alien facets that we use, typically within their own metaphor
    CONTINUUM = 'CONTINUUM'
    # THROUGHLINE - the metaphoric interface, explaining the relationship between the module-metaphore and the world at large
    THROUGHLINE = 'THROUGHLINE'
    # FIGURATIONs and AFFORDANCEs - high-order CHARACTERISATIONS providing a semantic package. I'm as yet somewhat undecided on their precise differentiation...
    FIGURATION = 'FIGURATION'
    AFFORDANCE = 'AFFORDANCE'
    # KNOWLEDGE - Typically important datum or data classes
    KNOWLEDGE = 'KNOWLEDGE'
    # BEHAVIOUR - a small package of sequenced actions
    BEHAVIOUR = 'BEHAVIOUR'
    # MECHANISM - an action, e.g. getters/setters
    MECHANISM = 'MECHANISM'
    # SKILL - an ability, e.g. inspect entity, filter list
    SKILL = 'SKILL'
    # DISPOSITION - an indication (or detetcion), of state (or transition)
    DISPOSITION = 'DISPOSITION'
    # PROSE - story woven around code sections
    PROSE = 'PROSE'
    # FLAW - An exception or sentinel
    FLAW = 'FLAW'

    @classmethod
    def from_string(cls, tag_str):
        try:
            return cls[tag_str.strip().upper()]
        except KeyError:
            return None

'''
AFFORDANCE:
The core of a lexicographer's abilities
'''
class LEXICOGRAPHICS:
    '''
    BEHAVIOUR:
    Finds the lexical to associate with a semenatic TEXT, dropping TEXTs that are deifnitely NOT semantic.
    Keeps all COMMENT type texts as they are handled later when we package up any PROSE
    '''
    @staticmethod
    def unpack_text_entry(this_entry, next_entry=None):
        if next_entry is None or next_entry['category'] != LexicalCategory.IDENTITY.name:
            # we can't find a subsequent identity to associate this with, so we don't
            lexical = ''
        else:
            lexical = next_entry['semantic']

        lexical = LexicalOccurence(this_entry['attestation'], lexical)

        inline_expo = this_entry['semantic'].startswith('#')
        semantic = LEXICOGRAPHICS._nonjudgemental_clean(this_entry['semantic'])
        if not inline_expo and semantic.startswith('#'):
            # having stripped the quotes, don't let the residual text fool us into thinking it was an inline comment!
            return None

        if LEXICOGRAPHICS._is_expo(semantic) or semantic.startswith('#'):
            return ([lexical, semantic, this_entry['reference']])

        return None

    '''
    BEHAVIOUR:
    Essentially strips delimiting quotes from a text, but doesn't get all judgy if the text is somehow poorly delimited.
    Also removes commentary markers from in-line semantics (except PROSE which is cleaned up later)
    '''
    @staticmethod
    def _nonjudgemental_clean(text):
        unclean = text

        # PROSE: On cleaning the TEXTs...
        # Firstly we deal with COMMENT type texts
        # If they are in-line semantics (except PROSE) we return them without the comment marker
        # otherwise in-line comments are returned unadulterated, so the prose block handler has them available later.
        if text.startswith('#'):
            semantic = text.lstrip('#').lstrip()
            if LEXICOGRAPHICS._is_expo(semantic):
                if not semantic.upper().startswith('PROSE'):
                    return semantic
            return text

        # Then we remove any text delimiters around the semantic content.
        # Being careful only to consider delimiters, not any old quote-mark that might be within the semantic text
        if text[:1] not in ['"', "'"]:
            #somehow we got a string that isn't delimited, weird but okay
            return text

        if text[:3] in ['"""', "'''"]:
            if text[-3:] != text[:3]:
                # somehow the triple quoted string hasn't been terminated, so don't clip the right side
                return text[3:].lstrip()
            else:
                return text[3:-3].lstrip()
        else:
            if text[-1:] != text[:1]:
                # somehow the single quoted string hasn't been terminated, so don't clip the right side
                return text[1:].lstrip()
            else:
                return text[1:-1].lstrip()

        # Because the work is a little complex, we have a catch-all return of the unadulterated text - just in case someone decides to add a bug in the code laters...
        return unclean

    '''
    SKILL:
    Determines if a text IS semantic
    '''
    @staticmethod
    def _is_expo(text):
        # presumed we have pre-cleaned the text regards string delimiters
        return any(text.upper().startswith(marker.name+':') for marker in ExpoTags)

    '''
    MECHANISM:
    Adds any package of semantics we have been collating to the latest survivor before adding this survivor also
    unless this survivor is just  some itinerant programmer's comment (outside of a prose block)
    '''
    @staticmethod
    def update_survivors(
        survivors, 
        latest_survivor,
        lexical,
        semantic, 
        reference,
        package_lexical, 
        package_semantic,
        package_reference):

        if package_semantic:
            latest_survivor = LEXICOGRAPHICS.extend_content(survivors, latest_survivor, package_lexical, package_semantic, package_reference)
            package_semantic = []

        if not semantic.startswith('#'):
            latest_survivor = lexical
            survivors[lexical] = Lexeme.from_parts(lexical, semantic, reference)

        return survivors, latest_survivor, package_semantic

    '''
    MECHANISM:
    Adds the relevant parts of the current semantic to the packaged semantic.
    I.e. store the reference and lexical for the first packaged text, and the semantic for all packaged texts
    '''
    @staticmethod
    def update_semantic_package(
        lexical,
        semantic, 
        reference,
        package_lexical, 
        package_semantic,
        package_reference):

        content = semantic.lstrip('#').lstrip()
        if package_semantic:
            content_tail = content
        else:
            _, _, content_tail = content.partition(':')
            package_lexical = lexical
            package_reference = reference
        package_semantic.append(content_tail)

        return package_lexical, package_semantic, package_reference

    '''
    DISPOSITION:
    Detects transitions into or out of prose blocks
    '''
    @staticmethod
    def is_prose_transition(in_prose, semantic):
        if in_prose:
            # any non-comment signals end of prose block
            return semantic.startswith('#')
        else:
            # any comment starting with the PROSE tag signals start of prose block
            if semantic.startswith('#'):
                return semantic.upper().lstrip('#').lstrip().startswith("PROSE" + ':')

        # and any other semantic (i.e non-comment) signals nto in a pprose block
        return False

    '''
    SKILL:
    Extends the latest semantic with additional (prose) commentary.
    BUT if we somehow found a prose block before ANY other semantic, we will ttry to add the prose as its own semantic
    This is so we at least get to see the (mis-placed) element somewhere in the outputs, so we can fix it.

    Note, in this case it truly IS mis-placed, because (by defintion) prose annotates a previous semantic.
    Mis-placed prose in module B could even turn up annotating the last semantic of module A!
    The only defence I offer is that you at least get to see the prose SOMEWHERE...
    
    ...unless you don't. A mis-placed prose block will not be added at all IF it would overwrite an existing semantic.
    This ought to be an impossible scenario, thus the silent use of 'pass' in this code.
    FWIW: I'm sorry, sooooo sorry, if that ever trips you up ;^D
    '''
    @staticmethod
    def extend_content(survivors, survivor_lexical, extension_lexical, extension_content, reference):
        if extension_content:
            if not survivor_lexical:
                if extension_lexical not in survivors.keys():
                    survivors[extension_lexical] = Lexeme.from_parts(extension_lexical, "\n".join(extension_content), reference)
                    survivor_lexical = extension_lexical
                else:
                    pass
            else:
                survivors[survivor_lexical].content += '\n\n' + extension_content[0] + '\n\n- '
                survivors[survivor_lexical].content += '\n- '.join(extension_content[1:])
        return survivor_lexical

# KNOWLEDGE: holds an attestation contextualised lexical entity
@dataclass(frozen=True)
class LexicalOccurence:
    attestation: str
    lexical: str

    def to_dict(self):
        return {
            'attestation': self.attestation,
            'lexical': self.lexical
        }

    '''
    MECCHANISM:
    Diachronic: how language develops through time.
    If we accept that time and space are the same thing, then we can view an attestation's spatial essence (module.class.method.var...) as a series of time events! So here, the diachronic view is simply the listification of the flat string representatioon of the attestatioon :)
    '''
    @property
    def diachronic(self):
        return self.attestation.split('.')

    def __iter__(self):
        yield self.attestation
        yield self.lexical

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return list(iter(self))[index]

    def __repr__(self):
        return f"<LexicalOccurence {self.lexical} of '{self.attestation}'>"

    def __str__(self):
        return f"{self.attestation}.{self.lexical}".strip('.')


# KNOWLEDGE: holds a lexeme - the canonical occurence, category and semantic content of a lexical
@dataclass
class Lexeme:
    category: ExpoTags
    canonical: LexicalOccurence
    content: str
    reference: str

    '''
    MECHANISM:
    Creates a lexeme by extracting category from a semantic text
    '''
    @classmethod
    def from_parts(cls, lexical: LexicalOccurence, semantic: str, reference: str) -> 'Lexeme':
        head, _, tail = semantic.partition(':')
        category = ExpoTags.from_string(head.strip())
        content = cls._dedent(tail.strip())
        return cls(category, lexical, content, reference)


    '''
    SKILL:
    Summarises a lexeme to category and canonical reference
    '''
    @property
    def summary(self):
        return f"[{self.reference}]{self.category.name}: {str(self.canonical)}"

    '''
    MECHANISM:
    The discovered semantics are indented, partly due to the requirements of the originating code, and partly for semantic clarity.
    Here we remove the common margin (minimum indent) found within the semantic content.
    '''
    @staticmethod
    def _dedent(text):
        texts = text.splitlines(keepends=True)
        if len(texts) < 2:
            return text

        min_margin = 999
        for line in texts[1:]: # first line has been dedented when we extracted it
            margin = len(line) - len(line.lstrip())
            min_margin = min(min_margin, margin)

        for i, line in enumerate(texts[1:]):
            # dammit, since we enuerate from index 1 we haveta add 1 to 
            # the enumeration in order to do the indexing...
            texts[i + 1] = texts[i + 1][min_margin:]

        text = ''.join(texts)

        return text

    def __iter__(self):
        yield self.category
        yield self.canonical
        yield self.content
        yield self.reference

    def __len__(self):
        return 4

    def __getitem__(self, index):
        return list(iter(self))[index]

    def __repr__(self):
        return f"<Lexeme [{self.reference}]{self.cataegory.name}: {str(self.canonical)}; '{self.content}'>"

    def __str__(self):
        return f"[{self.reference}]{self.cataegory.name}: {str(self.canonical)}; '{self.content}'"
