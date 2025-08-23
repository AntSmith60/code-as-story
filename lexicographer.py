# CONTINUUM: allows us to format and export our linguistic set as JSON
import json
import re

from granulator import GrainType as LexicalCategory

from lexicographics import LEXICOGRAPHICS, LexicalOccurence, Lexeme, ExpoTags

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
class LEXICOGRAPHER(LEXICOGRAPHICS):
    def __init__(self):
        self.lexemes = {}
        self._latest_lexeme = None

        # a package into which we build-up texts to be merged.
        self.package_semantic = []
        self.package_lexical = None
        self.package_reference = None

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
    def extract(self, entries):
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
                unpacked_text_entry = LEXICOGRAPHICS.unpack_text_entry(this_entry, next_entry)
                if unpacked_text_entry is not None:
                    texts.append(unpacked_text_entry)

        # clean-up the extracted semantics...
        lexemes = self._package_prose(texts)

        return lexemes

    '''
    BEHAVIOUR:
    Up to now we have preserved semantic PROSE and non-semantic comment-type texts so we can unpick the commentary from the code in order to build prose blocks.
    This is where we collate comment texts within a prose section to form a single semantic prose block - throwing away comment type texts that are NOT inside a prose section.
    '''
    def _package_prose(self, texts):
        # PROSE: Some prose on packaging prose...
        # At this point the TEXTs are still a little muddled, you know how strings like to tie themselves into knots right?
        # Although we removed TEXTs that are not tagged as exposition, we elected to keep all in-line comments so we can block-up interwoven prose
        # At least we now know that any TEXT that doesn't start with HASH, IS a true semantic exposition, so we can focus on the HASH lines here
        # We will either keep, drop or merge the HASH lines - so we will end up with fewer TEXTs; lets start with an empty list that will hold the survivors
        self.lexemes = {}
        self._latest_lexeme = None

        # and an empty package into which we build-up the texts to be merged.
        self.package_semantic = []
        self.package_lexical = None
        self.package_reference = None

        # Now looking at each text, we initially have no impetus to merge them together...
        merging = False
        for lexical, semantic, reference in texts:
            # We will start merging if this is an in-line comment that introduces PROSE
            merging = LEXICOGRAPHICS.is_prose_transition(merging, semantic)

            # While we are merging we pour the lines into our package, without the comment marker which is now obviated, redundant, utterly useless to us.
            if merging:
                self._update_semantic_package(lexical, semantic, reference)

            else:
                self._update_survivors(lexical, semantic, reference)

        # AND... a final flush if prose block reaches EOF
        if self.package_semantic:
            LEXICOGRAPHICS.extend_content(
                self.lexemes, 
                self._latest_lexeme, 
                self.package_lexical, 
                self.package_semantic, 
                self.package_reference
            )

        return self.lexemes


    '''
    MECHANISM:
    Adds any package of semantics we have been collating to the latest survivor before adding this survivor also
    unless this survivor is just  some itinerant programmer's comment (outside of a prose block)
    '''
    def _update_survivors(self, lexical, semantic, reference):

        if self.package_semantic:
            self._latest_lexeme = LEXICOGRAPHICS.extend_content(
                self.lexemes, 
                self._latest_lexeme, 
                self.package_lexical, 
                self.package_semantic, 
                self.package_reference
            )
            self.package_semantic = []

        if not semantic.startswith('#'):
            self._latest_lexeme = lexical
            self.lexemes[lexical] = Lexeme.from_parts(lexical, semantic, reference)

    '''
    MECHANISM:
    Adds the relevant parts of the current semantic to the packaged semantic.
    I.e. store the reference and lexical for the first packaged text, and the semantic for all packaged texts
    '''
    def _update_semantic_package(self, lexical, semantic, reference):
        content = semantic.lstrip('#').lstrip()
        if self.package_semantic:
            content_tail = content
        else:
            _, _, content_tail = content.partition(':')
            self.package_lexical = lexical
            self.package_reference = reference
        self.package_semantic.append(content_tail)

