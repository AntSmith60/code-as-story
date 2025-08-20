# CONTINUUM: allows us to create named structures for attestations, etymologies, and lexemes
from dataclasses import dataclass
from dataclasses import field
from typing import List, Tuple
from enum import Enum

import json
import re

from granulator import GrainType as LexicalCategory
from granulator import Grain as Entry

# KNOWLEDGE: If we want to use prose blocks, we need to ensure not to include literal hash in any strings inside the prose block!
HASH_SIGIL = chr(0x23)  # '#' character

# KNOWLEDGE: The types of semantic meaning we can use to adorn our code-base.
class ExpoTags(Enum):
    # PROSE: CONTINUUM - alien facets that we use, typically within their own metaphor
    CONTINUUM = 'CONTINUUM'
    # THROUGHLINE - the metaphoric interface, explaining the relationship between the module-metaphore and the world at large
    THROUGHLINE = 'THROUGHLINE'
    # FIGURATIONs and AFFORDANCEs - high-order CHARACTERISATIONS providing a semantic package. I'm as yet somewhat unclear on their precise differentiation...
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

The IDENTITY grains are atomic entities providing the name, Pythonic scope and source references of discovered Python objects in the source code. Obvs these discovered objects can occur in multiple places (since objects are declared so that they can be used). Each occurence is accumulated into an Etymology, and each Etymmology is accumulated into the overall list of all_attestations (an attestation being a recorded evidence of a lexical entity). This results in a list of everything that has been (or can be) refferred to.

The TEXT grains are a muddled collection of discovered strings and comments, so the LEXICOGRAPHER sifts through these looking for those that have semantic meaning, i.e. begin with expositional tags (ExpoTags). When a meaning is disccovered it is (typically) associated with the next attestation of a lexical - i.e semantic meaning becomes attached to the canonical attestation of a lexical. These entities (lexemes) are then accumulated into the all_expositions list so that the semantics of a lexical are known at any point the lexical is found (and in fact, also, where exactly its canonical form can be found).

Mostly, semantics are attached to classes and methods, or to other Pythonic objects (vars) - immediately preceeding that which they define. Special attention has been made to decorators which also must preceded that which they decorate. Semantic expositions are aware of that Python restriction, and have allowed for the intrusion of such (in the earlier processing). There are some exceptions to this semantic binding, and in fact more work needed to make the semantic binding complete, vis-à-vis:
    - THROUGHLINES, are bound to the module; but currently only by convention of their placement in a module
    - CONTINUUM, ought to bind to the last identity in a '[from x] import y [as z]' expression; currently it doesnt and is poorly bound
    - PROSE, is bound to the container (method, class or module) in which it is found, rather than the next specific object, method or class name

Most of the expositions are wholly provisioned by the substance of their text grain - either because they were very simple (found in an in-line comment); or, they were encapsulated within a multiline string within the code.

PROSE expositions are somewhat different. By design the PROSE is woven in and amongst the code using in-line commentary; so that, when we have significant code-blocks, we can annotate it with its story. A '# PROSE:' comment causes all in-line comments to be accumulated, until such time another exposition is encountered. This is convenient, but a little blunt since any normal code comments will also get swept up into the expositionary prose. It's easy to imagine many better methods, but this will do for now!

Oh! Also, any strings that contain '#' will collect garbage into the prose block also! So it really is weak at the moment!!!
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
    def save_to_file(lexemes, path):
        serializable = {
            str(key): {
                'category': value.category.name,
                'canonical': str(value.canonical),
                'content': re.sub(r'\r\n', '\n', value.content)
            }
            for key, value in lexemes.items()
        }
        with open(path+'.json', 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2)

        with open(path+'.txt', 'w', encoding='utf-8') as f:
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
    formats and prints a single lexeme, indenting as per the etymological depth.
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


    '''
    MECHANISM:
    performs an identation of a semantic unit
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
    Sifts through IDENTITY and TEXT entries to generate the required outputs
    Tracks the etymology of lexicals and extracts/combines the semantics from TEXTs
    Generates the lexemes by binding semantics to lexicals
    '''
    @staticmethod
    def extract(entries):
        attestations = {}
        texts = []

        if not entries:
            return {}, {}

        # PROSE:
        # On the extraction of meaning...
        # -------------------------------
        for i, entry in enumerate(entries):
            # Every entry has some kind of meaning, for meaning is a layered construct
            this_entry = entry.semantics()

            # when the meaning relates to one of our lexemes, we're gonna need to find the following lexical (probably)
            next_entry = None
            if i < len(entries) - 1:
                next_entry = entries[i + 1].semantics()

            # When the meaning we found is a lexical's name, create or extend the etymology with this attestation
            if this_entry['category'] == LexicalCategory.IDENTITY.name:
                attestation = LexicalOccurence(this_entry['attestation'], this_entry['semantic'])
                if attestation in attestations:
                    attestations[attestation].add_to_etymology(this_entry['reference'], this_entry['is_canonical'])
                else:
                    attestations[attestation] = Etymology(attestation, [this_entry['reference']])

            # Otherwise unpack this meaning to extract any semantics it contains relevant to our lexemes
            elif this_entry['category'] == LexicalCategory.TEXT.name:
                unpacked_text_entry = LEXICOGRAPHER._unpack_text_entry(this_entry, next_entry)
                if unpacked_text_entry is not None:
                    texts.append(unpacked_text_entry)

        # clean-up the extracted semantics...
        lexemes = LEXICOGRAPHER.package_prose(texts)

        return attestations, lexemes


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
        semantic = LEXICOGRAPHER._nonjudgemental_clean(this_entry['semantic'])

        if LEXICOGRAPHER._is_expo(semantic) or semantic.startswith('#'):
            return ([lexical, semantic])

        return None

    '''
    BEHAVIOUR:
    Essentially strips delimiting quotes from a text, but doesn't get all judgy if the text is somehow poorly delimited.
    Also removes commentary markers from in-line semantics (except PROSE which is cleaned up later)
    '''
    @staticmethod
    def _nonjudgemental_clean(text):
        unclean = text

        # PROSE:
        # On cleaning the TEXTs...
        # ------------------------
        # Firstly we deal with COMMENT type texts
        # If they are in-line semantics (except PROSE) we return them without the comment marker
        # otherwise in-line comments are returned unadulterated, so the prose block handler has themm available later.
        if text.startswith('#'):
            semantic = text.lstrip(HASH_SIGIL).lstrip()
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
        # PROSE:
        # Some prose on packaging prose...
        # ---------------------------------
        # At this point the TEXTs are still a little muddled, you know how strings like to tie themselves into knots right?
        # Although we removed TEXTs that are not tagged as exposition, we elected to keep all in-line comments so we can block-up interwoven prose...
        # ...so BEWARE we might have rogue strings that happened to start with the in-line comment marker!
        # At least we now know that any TEXT that doesn't start with HASH, IS a true semantic exposition, so we can focus on the HASH lines here
        #
        # We will either keep, drop or merge the HASH lines - so we will end up with fewer TEXTs; lets start with an empty list that will hold the survivors
        survivors = {}

        # and and empty package into which we build-up the texts to be merged.
        package_semantic = []
        package_lexical = None

        #
        # Now looking at each text, we initially have no impetus to merge them together...
        merging = False
        for lexical, semantic in texts:
            # We will start merging if this is an in-line comment that introduces PROSE
            # (and note how I avoid creating a string that LOOKS like an expositional tag, awkward I admit)
            if not merging:
                if semantic.startswith(HASH_SIGIL):
                    merging = semantic.upper().lstrip(HASH_SIGIL).lstrip().startswith("PROSE" + ':')
            else:
                # And we stop merging when we hit another exposition (that is, a line that doesn't start with HASH)
                merging = semantic.startswith(HASH_SIGIL)

            #
            # While we are merging we pour the lines into our package, without the comment marker which is now obviated, redundant, utterly useless to us.
            if merging:
                if not package_semantic:
                    package_lexical = lexical
                package_semantic.append(semantic.lstrip(HASH_SIGIL).lstrip())

            else:
                #
                # If we are not merging, we add any previous merged package to the survivor's list...
                if package_semantic:
                    survivors[package_lexical] = Lexeme.from_parts(package_lexical, "\n".join(package_semantic))
                    package_semantic = []

                # ...and we add this text to the survivors list, unless its just some itinerant programmer's comment (outside of a prose block)
                if not semantic.startswith('#'):
                    survivors[lexical] = Lexeme.from_parts(lexical, semantic)

        # AND... a final flush if prose block reaches EOF
        if package_semantic:
            survivors[package_lexical] = Lexeme.from_parts(package_lexical, "\n".join(package_semantic))

        return survivors


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

    '''
    MECHANISM:
    Creates a lexeme by extracting category from a semantic text
    '''
    @classmethod
    def from_parts(cls, lexical: LexicalOccurence, semantic: str) -> 'Lexeme':
        head, _, tail = semantic.partition(':')
        category = ExpoTags.from_string(head.strip())
        content = cls._dedent(tail.strip())
        return cls(category, lexical, content)


    '''
    SKILL:
    Summarises a lexeme to category and canonical reference
    '''
    @property
    def summary(self):
        return f"{self.category.name}: {str(self.canonical)}"

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

    def __len__(self):
        return 3

    def __getitem__(self, index):
        return list(iter(self))[index]

    def __repr__(self):
        return f"<Lexeme {self.cataegory.name}: {str(self.canonical)}; '{self.content}'>"

    def __str__(self):
        return f"{self.cataegory.name}: {str(self.canonical)}; '{self.content}'"

# KNOWLEDGE: holds a list of all occurances of a certain lexical (i.e. with an attestation), noting also where the canonical reference can be found
@dataclass
class Etymology:
    occurance: LexicalOccurence
    references: List[Tuple[int, int]]
    canonical: int = field(default=0)  # either the first occurance, or else indexes references for the canonical

    def add_to_etymology(self, reference, as_canonical):
        self.references.append(reference)
        if as_canonical:
            self.canonical = len(self.references) - 1

    def to_dict(self, frame_num):
        return {
            'occurance': self.occurance.to_dict(),
            'references': self.references,
            'canonical': self.canonical
        }

    def __iter__(self):
        yield self.occurance
        yield self.references
        yield self.canonical

    def __len__(self):
        return 3

    def __getitem__(self, index):
        return list(iter(self))[index]

    @staticmethod
    def _stringify_references(references, canonical):
        here_text = ''
        for i, here in enumerate(references):
            here_text += f"{here}"
            if i == canonical:
                here_text += '*'
            if i < len(references) - 1:
                here_text += ','
        return here_text

    @staticmethod
    def _stringify_occurance(occurance):
        attested = occurance.attestation
        if occurance.diachronic[-1] != occurance.lexical:
            attested += '.' + occurance.lexical
        return attested

    def __repr__(self):
        return f"<Etymologies of: '{self._stringify_occurance(self.occurance)}' at {self._stringify_references(self.references, self.canonical)}>"

    def __str__(self):
        return f"{self._stringify_occurance(self.occurance)}': {self._stringify_references(self.references, self.canonical)}>"
