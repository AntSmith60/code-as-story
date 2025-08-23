from codices import CODEX, ENTITY
'''
THROUGHLINE:
Every token of interest from the parse (i.e. those that survived the granulator's purification stage) visits the Registrar — which may seem draconian, but such is the nature of symbolic governance.

The Registrar’s records are private. The only sanctioned access is through `record_history`, which returns the current known lineage for each notable recorded subject.

Most subjects are notable and have their lineage recorded.
Though draconian, the process remains relatively democratic.

Unnotables are the DENTS.
The Registrar must still track them, as a DEDENT may signal the end of a lineage — depending on the INDENTS that preceded it.

Lineage only extends when a true identity is married to a progenitor (`class` or `def` + name).
The resilience of this family line then waxes and wanes, governed by INDENTS and DEDENTS.

When resilience falls back to the level of the originating progenitor, the family line dies out, and the current lineage contracts.

Lineage is NOT returned for growth/decline subjects (DENTS), as they are not actual 'things' — just indicators of resilience.

Similarly, lineage is NOT returned for honourifics, since they merely address things, but are not things themselves.
'''

'''
FIGURATION:
The Registrar recognises and declares subject titles according to the evolving lineage of recorded subjects.

Some subjects (DENTS and PROGENITORS) do not receive titles, but they influence the shape and continuity of the lineage.

Other subjects (HONOURIFICS) are not recorded at all — they serve only to address true subjects, and are thus excluded from lineage.
'''
class REGISTRAR:
    def __init__(self, registrant):
        # KNOWLEDGE: tracks how the heritage line waxes and wanes
        self._resilience = 0

        # KNOWLEDGE: A new register is created for each registrant (grand forebear)
        self._register = []
        self._register.append({'id': registrant, 'wedded_resilience': self._resilience})

        # DISPOSITION: are we currently looking for the true identity of an heir apparent, or else just recording subject titles
        self._heir_apparent = False
        # KNOWLEDGE: the true identity of an heir apparent
        self._heir = ''

    '''
    BEHAVIOUR:
    Provides the current lineage relevant to a subject, IF this is a notable subject.

    But NOTE - what a topsy-turvey world we live in!
    Because we have to look forwards we find new progenitors before we find their identity!
    So instead of simply saying: 
    > Prepare for heir, seek heir, record heir...
    we have to say:
    > record (the current) heir, seek (another) heir, prepare for (next) heir
    
    Kind of backwards really, I guess it stems from 'invasion culture' wherein conquered peoples are dehumanised by being reduced to 'station' afore 'identity', m'lord!
    '''
    def record_history(self, subject):
        new_family_line = False

        # PROSE: on how the code-tree grows and withers
        # First, keep an eye on the resilience of the current family line
        if self._lineage_fluxed(subject):
            return False, None

        # Add any found heir to the lineage
        # So that GOING FORWARD the title is recognised
        self._record_heir()

        # Once we find a new heir, keep it safe for now
        # So the title is awarded on the next cycle
        # Otherwise we lose sight of this heir's own lineage
        new_family_line = self._seek_heir_apparent(subject)

        # Have a look-see if we have met a new heir-apparent
        self._prepare_for_heir(subject)

        # Finally all are remembered in the trace of lineage they leave behind 
        # BUT it is only the true that get entitled
        if LINEAGE.is_true_identity(subject) or \
            LINEAGE.is_descender(subject) or \
            LINEAGE.is_true_subject(subject):
            return new_family_line, self._entitle()

        return False, None


    '''
    SKILL:
    Detects flux in the current family line, signing-off the register if the line has died out
    '''
    def _lineage_fluxed(self, subject):
        if not (LINEAGE.growth(subject) or LINEAGE.decline(subject)):
            return False

        if LINEAGE.growth(subject):
            self._resilience += 1

        if LINEAGE.decline(subject):
            self._resilience -= 1
            if not self._register_empty():
                if self._resilience <= self._register[-1]['wedded_resilience']:
                    self._sign_off_record()

        return True

    '''
    DISPOSITION:
    Switches our disposition from seeking an identity to seeking a progenitor
    whilst setting the current found heir apparent
    '''
    def _seek_heir_apparent(self, subject):
        if self._heir_apparent:
            if LINEAGE.is_true_identity(subject):
                self._heir = LINEAGE.subject_name(subject)
                self._heir_apparent = False
                return True
        return False

    '''
    SKILL:
    Joins up all the identities in our current lineage to form a single, recordable, title
    '''
    def _entitle(self):
        lineage = '.'.join(d['id'] for d in self._register if 'id' in d)
        return lineage.strip('.')

    '''
    DISPOSITION:
    Prepares a progenitor's new lineage, in case there is then a marriage
    Switches our disposition from seeking a progenitor to seeking an identity
    '''
    def _prepare_for_heir(self, subject):
        if LINEAGE.is_progenitor(subject):
            self._register.append({'id': '', 'wedded_resilience': self._resilience})
            self._heir_apparent = True

    '''
    SKILL:
    Fills in the new lineage, and sets the baseline of this family line's resilience,
    which builds upon that of previous generations
    '''
    def _record_heir(self):
        if self._heir:
            if not self._register:
                self._register.append({'id': '', 'wedded_resilience': self._resilience})
            self._register[-1]['id'] = self._heir
        self._heir = ''

    '''
    SKILL:
    Marks the end of a family line by removing its lineage
    '''
    def _sign_off_record(self):
        self._register = self._register[:-1]

    '''
    FLAW:
    Allows us to check if the register is empty before we try to remove a family line
    '''
    def _register_empty(self):
        return not self._register


'''
AFFORDANCE:
Casts the symbolic LEXICON of the base CODEX into lineage parlance, allowing us to identify lineage related ENTITIES
'''
class LINEAGE(CODEX):
    # KNOWLEDGE: The subjects that (potentially) start a new generation in the lineage
    PROGENITORS = ENTITY('NAME', 'ENCAPSULATORS')
    
    # KNOWLEDGE: The ways in which subjects may be addressed, not actual subject identities
    HONOURIFICS = ENTITY('NAME', 'RESERVED')

    # KNOWLEDGE: The subjects that may be true identities
    IDENTITIES = ENTITY('NAME')

    # KNOWLEDGE: The subjects that give rise to descendents
    DESCENDERS = ENTITY('OP', 'ACCESSOR')

    # KNOWLEDGE: Represents a waxing in the current family-line's resilience
    GROWTH = ENTITY('INDENT')

    # KNOWLEDGE: Represents a waning in the current family-line's resilience
    DECLINE = ENTITY('DEDENT')

    # KNOWLEDGE: True subjects - the things we want to record
    TRUE_SUBJECTS = ENTITY('STRING')
    TRUE_SUBJECTS.add('COMMENT')

    '''
    SKILL:
    Matches with the subjects we want to record
    '''
    @staticmethod
    def is_true_subject(subject):
        return LINEAGE.TRUE_SUBJECTS.is_entity(subject)

    '''
    SKILL:
    Matches progenitor type subjects only
    '''
    @staticmethod
    def is_progenitor(subject):
        return LINEAGE.PROGENITORS.is_entity(subject)

    '''
    SKILL:
    Matches descender type subjects only
    '''
    @staticmethod
    def is_descender(subject):
        return LINEAGE.DESCENDERS.is_entity(subject)

    '''
    SKILL:
    Matches subjects that are true identities (not honourifics)
    '''
    @staticmethod
    def is_true_identity(subject):
        if LINEAGE.IDENTITIES.is_entity(subject):
            return not LINEAGE.HONOURIFICS.is_entity(subject)
        return False
            
    '''
    SKILL:
    Detects when the current family line grows
    '''
    @staticmethod
    def growth(subject):
        return LINEAGE.GROWTH.is_entity(subject)

    '''
    SKILL:
    Detects when a current family line has declined
    '''
    @staticmethod
    def decline(subject):
        return LINEAGE.DECLINE.is_entity(subject)

    '''
    MECHANISM:
    we DO need to know the actual name of a subject!
    '''
    @staticmethod
    def subject_name(subject):
        return CODEX.token_val(subject)