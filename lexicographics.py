# CONTINUUM: allows us to create named structures for attestations, and lexemes
from dataclasses import dataclass
from dataclasses import field
from typing import List, Tuple
from enum import Enum

# CONTINUUM: allows us to format and export our linguistic set as JSON
import json
import re

from granulator import GrainType as LexicalCategory
from granulator import Grain as Entry

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
THROUGHLINE:
Earlier processing has delivered parcels consisting of a blend of IDENTITY and TEXT grains

The IDENTITY grains are atomic entities providing the name, Pythonic scope and source references of discovered Python objects in the source code. Obvs these discovered objects can occur in multiple places (since objects are declared so that they can be used), but we only care about existence to help bind semantics to lexicals. The occurences are accumulated into an overall list of attestations (an attestation being a recorded evidence of a lexical entity). This results in a list of everything that has been (or can be) refferred to.

The TEXT grains are a muddled collection of discovered strings and comments, so the LEXICOGRAPHER sifts through these looking for those that have semantic meaning, i.e. begin with expositional tags (ExpoTags). When a meaning is disccovered it is (typically) associated with the next attestation of a lexical - i.e semantic meaning becomes attached to the canonical attestation of a lexical. These entities (lexemes) are then accumulated into the all_expositions list so that the semantics of a lexical are known at any point the lexical is found (and in fact, also, where exactly its canonical form can be found).

Mostly, semantics are attached to classes and methods, or to other Pythonic objects (vars) - immediately preceeding that which they define[^1]. There are some exceptions to this semantic binding, and in fact more work needed to make the semantic binding complete, vis-à-vis:
- THROUGHLINES, are bound to the module; but currently only by convention of their placement in a module
- CONTINUUM, ought to bind to the last identity in a '[from x] import y [as z]' expression; currently it doesnt and is poorly bound
- PROSE, is bound to the most recent semantic entity; i.e. PROSE extends the current semantic with a list of detailed steps

[^1]:Special attention has been made to decorators which also must preceded that which they decorate. Semantic expositions are aware of that Python restriction, and have allowed for the intrusion of such (in the earlier processing).

Most of the expositions are wholly provisioned by the substance of their text grain - either because they were very simple (found in an in-line comment); or, they were encapsulated within a multiline string within the code.

PROSE expositions are somewhat different. By design the PROSE is woven in and amongst the code using in-line commentary; so that, when we have significant code-blocks, we can annotate it with its story. A '# PROSE:' comment causes all in-line comments to be accumulated, until such time another exposition is encountered. This is convenient, but a little blunt since any normal code comments will also get swept up into the expositionary prose. It's easy to imagine many better methods, but this will do for now!
'''

'''
FIGURATION:
Sifts through a given set of 'entries' to generate:
    - a lexicon of known lexicals(!), erm, I mean a list of things that can be known about
    - the linguistical set of those things that have meaning
'''
class LEXICOGRAPHER:
    '''
    BEHAVIOUR:
    Creates a json file containing the full linguistic set and a text file listing the canonicals
    '''
    def save_to_file(lexemes, dictout, indexout):
        serializable = {
            str(key): {
                'category': value.category.name,
                'canonical': str(value.canonical),
                'content': re.sub(r'\r\n', '\n\n', value.content),
                'reference': str(value.reference)
            }
            for key, value in lexemes.items()
        }
        with open(dictout, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2)

        if indexout:
            with open(indexout, 'w', encoding='utf-8') as f:
                for key, value in lexemes.items():
                    f.write(f"{str(key)}:{value.category.name}\n")

    '''
    BEHAVIOUR:
    returns a list of lexeme summaries from a linguistical set
    '''
    @staticmethod
    def list_expositions(expositions, filtered=None, with_print=True):
        summaries = []
        for expo in expositions.values():
            if filtered and expo.category != filtered:
                continue
            summaries.append(expo.summary)
        summaries = sorted(summaries)
        if with_print:
            for expo_summary in summaries:
                print(expo_summary)
        return summaries

    '''
    BEHAVIOUR:
    prints a linguistical set
    '''
    @staticmethod
    def print_expositions(expositions, filtered=None):
        for expo in expositions.values():
            if filtered and expo.category != filtered:
                continue
            LEXICOGRAPHER.print_expo(expo)

    '''
    BEHAVIOUR:
    formats and prints a single lexeme, indenting as per the depth of its attestation.
    '''
    @staticmethod
    def print_expo(expo):
        indent_level = max(0, len(expo.canonical.diachronic) - 1)

        if indent_level == 0:
            print(LEXICOGRAPHER._indent('-' * 20, indent_level))

        if expo.category != ExpoTags.PROSE:
            lexical = LEXICOGRAPHER._indent(str(expo.canonical), indent_level)
            print(f"{lexical}:{expo.category.name};")

        semantic = LEXICOGRAPHER._indent(expo.content, indent_level+1)
        print(semantic.rstrip())


    @staticmethod
    def print_identities(entries):
        identities = {}
        for entry in entries:
            this_entry = entry.semantics()
            if this_entry['category'] == LexicalCategory.IDENTITY.name:
                key = f"{this_entry['attestation']}.{this_entry['semantic']}"
                if key not in identities.keys() or this_entry['is_canonical']:
                    identities[key] = this_entry['reference']

        for identity, ref in identities.items():
            print(f"[{ref}]:{identity}")


    @staticmethod
    def print_attestations(entries):
        for entry in entries:
            this_entry = entry.semantics()
            if this_entry['category'] == LexicalCategory.IDENTITY.name:
                marker = '!' if this_entry['is_canonical'] else ''
                print(f"{marker}[{this_entry['reference']}]:{this_entry['attestation']}.{this_entry['semantic']}")

    '''
    MECHANISM:
    performs an identation of a semantic unit as decoration for direct printed output
    '''
    @staticmethod
    def _indent(semantic, indent_level):
        lines = semantic.splitlines(keepends=True)
        for i, line in enumerate(lines):
            indent = '   ' * indent_level
            if line:
                lines[i] = indent + lines[i]
        return ''.join(lines)

    '''
    BEHAVIOUR:
    Sifts through the entries for TEXTs to generate the semantics which are combined to lexicals to ppprovide our lexemes
    '''
    @staticmethod
    def extract(entries):
        texts = []

        if not entries:
            return {}, {}

        # PROSE: On the extraction of meaning...
        for i, entry in enumerate(entries):
            # Every entry has some kind of meaning, for meaning is a layered construct
            this_entry = entry.semantics()

            # when the meaning relates to one of our lexemes, we're gonna need to find the following lexical (probably)
            next_entry = None
            if i < len(entries) - 1:
                next_entry = entries[i + 1].semantics()

            # At this point we only care about this TEXT's semantic content and the next IDENTITY's lexical value
            if this_entry['category'] == LexicalCategory.TEXT.name:
                unpacked_text_entry = LEXICOGRAPHER._unpack_text_entry(this_entry, next_entry)
                if unpacked_text_entry is not None:
                    texts.append(unpacked_text_entry)

        # clean-up the extracted semantics...
        lexemes = LEXICOGRAPHER.package_prose(texts)

        return lexemes


    '''
    BEHAVIOUR:
    Finds the lexical to associate with a semenatic TEXT, dropping TEXTs that are deifnitely NOT semantic.
    Keeps all COMMENT type texts as they are handled later when we package up any PROSE
    '''
    @staticmethod
    def _unpack_text_entry(this_entry, next_entry=None):
        if next_entry is None or next_entry['category'] != LexicalCategory.IDENTITY.name:
            # we can't find a subsequent identity to associate this with, so we don't
            lexical = ''
        else:
            lexical = next_entry['semantic']

        lexical = LexicalOccurence(this_entry['attestation'], lexical)

        inline_expo = this_entry['semantic'].startswith('#')
        semantic = LEXICOGRAPHER._nonjudgemental_clean(this_entry['semantic'])
        if not inline_expo and semantic.startswith('#'):
            # having stripped the quotes, don't let the residual text fool us into thinking it was an inline comment!
            return None

        if LEXICOGRAPHER._is_expo(semantic) or semantic.startswith('#'):
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
            if LEXICOGRAPHER._is_expo(semantic):
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
    BEHAVIOUR:
    Up to now we have preserved semantic PROSE and non-semantic comment-type texts so we can unpick the commentary from the code in order to build prose blocks.
    This is where we collate comment texts within a prose section to form a single semantic prose block - throwing away comment type texts that are NOT inside a prose section.
    '''
    @staticmethod
    def package_prose(texts):
        # PROSE: Some prose on packaging prose...
        # At this point the TEXTs are still a little muddled, you know how strings like to tie themselves into knots right?
        # Although we removed TEXTs that are not tagged as exposition, we elected to keep all in-line comments so we can block-up interwoven prose
        # At least we now know that any TEXT that doesn't start with HASH[^2], IS a true semantic exposition, so we can focus on the HASH lines here
        # We will either keep, drop or merge the HASH lines - so we will end up with fewer TEXTs; lets start with an empty list that will hold the survivors
        # [^2]: This handling of TEXTs that start with # works because ExpoTags themselves never start with # and at this point we know that ALL off our TEXTs start with either # (because they were a COMMENT) or start with an ExpoTag (because we already filtered STRINGs that are not ExpoTags)
        survivors = {}
        latest_survivor = None

        # and an empty package into which we build-up the texts to be merged.
        package_semantic = []
        package_lexical = None
        package_reference = None

        # Now looking at each text, we initially have no impetus to merge them together...
        merging = False
        for lexical, semantic, reference in texts:
            # We will start merging if this is an in-line comment that introduces PROSE[^3]
            # [^3]: Note in the code that I test against ("PROSE" + ":") and noot simply ("PROSE:"). This is because I do not want a string in the code that LOOKS like an ExpoTag. A little awkward huh? I coulda done more work upstream to avoid this possibility becoming an issue - but its just not worth it. We'd need more proficient tooling in a large codebase I would imagine...
            merging = LEXICOGRAPHER._is_prose_transition(merging, semantic)

            # While we are merging we pour the lines into our package, without the comment marker which is now obviated, redundant, utterly useless to us.
            if merging:
                package_lexical, package_semantic, package_reference = LEXICOGRAPHER._update_semantic_package(
                    lexical,
                    semantic, 
                    reference,
                    package_lexical, 
                    package_semantic,
                    package_reference
                )

            else:
                survivors, latest_survivor, package_semantic = LEXICOGRAPHER._update_survivors(
                    survivors, 
                    latest_survivor,
                    lexical,
                    semantic, 
                    reference,
                    package_lexical, 
                    package_semantic,
                    package_reference
                )

        # AND... a final flush if prose block reaches EOF
        if package_semantic:
            LEXICOGRAPHER._extend_content(survivors, latest_survivor, package_lexical, package_semantic, package_reference)

        return survivors

    '''
    MECHANISM:
    Adds any package of semantics we have been collating to the latest survivor before adding this survivor also
    unless this survivor is just  some itinerant programmer's comment (outside of a prose block)
    '''
    @staticmethod
    def _update_survivors(
        survivors, 
        latest_survivor,
        lexical,
        semantic, 
        reference,
        package_lexical, 
        package_semantic,
        package_reference):

        if package_semantic:
            latest_survivor = LEXICOGRAPHER._extend_content(survivors, latest_survivor, package_lexical, package_semantic, package_reference)
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
    def _update_semantic_package(
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
    def _is_prose_transition(in_prose, semantic):
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
    def _extend_content(survivors, survivor_lexical, extension_lexical, extension_content, reference):
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
