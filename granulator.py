# CONTINUUM: allows conversion of an underlying filepath to a batch identity
from os import path

# CONTINUUM: allows us to create a named structure for the final substance list we produce
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import List, Tuple


from codices import CODEX, ENTITY
from registrar import REGISTRAR as BX_RECORD

'''
THROUGHLINE:
We pour a batch of Python source code (.py file) into the Granulator.

Through a series of processing steps, we generate an inventory of 'grains'—each providing:
- lineage: where, in the original bulk material, this grain was found
- type: whether it is a TEXT description or an object IDENTITY
- substance: the found TEXT or IDENTITY itself
- location: in the original source material
- progenitor: is it the first of a new line?

Metaphorically, the Python source code is the bulk_material we work on.
It is tokenized into a powder of token particles, which are then purified and mixed into a precursor for refinement into grains.

Particles are tracked through a batch record, capturing the Pythonic scope in which each particle is found.

Particles are distilled into grains such that a sequence like:
>NAME.string='self' OP.string='.' NAME.string='powder'

becomes an IDENTITY grain with substance='self.powder'.

NOTE: I discovered that tokens flow around such that DEDENTS arise not after the last line of indentation but immediately before the first dedented line...
Subtle, upshot is in-line comments don't always turn up in the token stream as one might expect. 
To counter this I have added the 'suspension/bubble-up' concept during the fine-mix so that in-line semantics more reliably associate with the correct lineage.
'''

'''
FIGURATION:
Takes an unruly, heterogeneous input bulk material and turns it into an intermediate purified precursor which is then refined into grains.

Uses the SAMPLE test bed to inspect each particle and applies track&trace (via the registrar) to give just the particles of interest along with their full lineage.

Then refines particles into grains
'''
class GRANULATOR:
    def __init__(self, bulk_material, source):
        # KNOWLEDGE: identity of the overall package of materials
        bx_id = path.splitext(source)[0]
        bx_id = bx_id.replace('\\','.').strip('.')
        self._track_and_trace = BX_RECORD(bx_id)

        self._bulk_material = bulk_material

        # KNOWLEDGE: Full catalogue of the original material, as particles
        self.powder = None

        # KNOWLEDGE: list of purified particles
        self.purified = None

        # KNOWLEDGE: list of intermediates as Precursor class
        self.intermediate = None

        # KNOWLEDGE: resulting list of refined grains as Grain class
        self.refined = None

    '''
    MECHANISM:
    Shows the powderised bulk raw material
    '''
    def dump_powder(self):
        self._dump_particles(self.powder)

    '''
    MECHANISM:
    Shows the purified bulk raw material powder
    '''
    def dump_purified(self):
        self._dump_particles(self.purified)

    def _dump_particles(self, particle_list):
        for particle in particle_list:
            print(particle)
    '''
    MECHANISM:
    Shows the tracked intermediate precursors
    '''
    def dump_bx_record(self):
        self._dump_materials(self.intermediate)

    '''
    MECHANISM:
    Shows the final set of grains
    '''
    def dump_inventory(self):
        self._dump_materials(self.refined)

    def _dump_materials(self, material_list):
        widest = 0
        for material in material_list:
            widest = max(widest, len(material[0]))

        for material in material_list:
            for i, part in enumerate(material):
                if i == 0:
                    print(f"{material[i]:<{widest}}", end = '|')
                elif i < len(material) - 1:
                    print(f"{material[i]}", end = '|')
                else:
                    print(f"{material[i]}")

    '''
    BEHAVIOUR:
    Assay's the material and performs the granulation. 
    This is a distinct step from initiating the Granulator in case there are any startup issues
    (Pythonic mantra: __init__ must succeed)
    '''
    def granulate(self):
        try:
            self.powder = SAMPLE.assay(self._bulk_material)
            if not self.powder:
                return []
        except:
            # Note: we raise errors in the native (Python) metaphor, since they cross the boundary of our module metaphor
            raise TypeError("Input must be a binary file-like object with a .readline() method returning bytes.")

        self.purified = self.purify(self.powder)
        self.intermediate = self.fine_mix(self.purified, self._track_and_trace)
        self.refined = self.refine(self.intermediate)

        return self.refined

    '''
    BEHAVIOUR:
    Purifies the powder by sieving for particles of interest
    ALSO passes the sieved powder through a fine-scale filter
    AND detects/discards any clumpy sludge found in the powder
    
    Each purified particle is classified from the on-going batch records
    '''
    @staticmethod
    def purify(hopper):
        purified_powder = []
        sludge = False

        for particle in hopper:
            # PROSE: Interlude in a poet's voice...
            # CANTO I: In which The Sludge is Sloughed
            # if is sludge and has not desludged
            if sludge:
                sludge = not SAMPLE.has_desludged(particle)
            if sludge:
                continue

            # CANTO II: In which The Sludge is Sought
            # if not is sludge and now has sludged
            if not sludge:
                sludge = SAMPLE.has_sludged(particle)
            if sludge:
                continue

            # CANTO III: In which The Pure is Preserved
            # if you can sieve and be filtrate then 
            # - you'll be Purified, my son!
            if SAMPLE.sieved(particle):
                if SAMPLE.is_filtrate(particle):
                    purified_powder.append(particle)

        return purified_powder

    '''
    BEHAVIOUR:
    Sometimes particles form a suspension (COMMENTS + DENTS) that needs breaking up so that the particles will bond correctly when we refine them into grains.
    Mixing allows the DENTs to bubble up so they evapourate as we inspect and classify the remainder
    '''
    @staticmethod
    def fine_mix(hopper, bx_record):
        # PROSE: On the fine mix process...
        # Break up suspensions so the DENTs don't come between TEXTs and NAMEs
        powder_mix = GRANULATOR._mix(hopper)

        # Evapourate the DENTs so the remainder can be classified
        intermediate = GRANULATOR._evapourate(powder_mix, hopper, bx_record)

        # No longer just a powder, the intermediate is ready to be refined into grains
        return intermediate

    '''
    MECHANISM:
    Mixes the purified powder, breaking up suspensions that effect how particles adhere into grains during refinement
    '''
    @staticmethod
    def _mix(hopper):
        powder_mix = list(range(len(hopper)))
        for i in range(len(powder_mix) - 1):
            particle = hopper[powder_mix[i]]
            next_particle = hopper[powder_mix[i+1]]
            if SAMPLE._is_suspension(particle, next_particle):
                powder_mix[i], powder_mix[i+1] = powder_mix[i+1], powder_mix[i]

        return powder_mix

    '''
    MECHANISM:
    Applies track&trace while condensing the intermediate to just the components that will make up the refined IDENTITY and TEXT grains.
    '''
    @staticmethod
    def _evapourate(powder_mix, hopper, bx_record):
        classifications = {}
        intermediate = []
        for index in powder_mix:
            particle = hopper[index]
            as_new_line, classification = bx_record.record_history(particle)
            if classification is not None:
                if not as_new_line:
                    if classification not in classifications.keys():
                        classifications[classification] = True
                        as_new_line = True
                intermediate.append(Precursor(classification, as_new_line, particle))

        return intermediate

    '''
    BEHAVIOUR:
    From purification we now have muddled comments and strings which will become the TEXTS
    and split Identities with sequences of NAME(.NAME...)s

    Refines NAMEs through distillation
    '''
    @staticmethod
    def refine(hopper):
        refined_grains = []

        distil = False
        refined = Grain('', None, '', (0,0), False)
        for classification, new_product_line, particle in hopper:
            # PROSE: On the distillation process
            # If we are not already distilling, see if we should
            if not distil:
                distil = REFINE.is_distillant(particle)

            # If we are distilling, condense into previous grain
            if distil:
                refined_grains[-1].substance += SAMPLE.particle_name(particle)
                distil = REFINE.is_distillant(particle)
                continue

            # Otherwise create a new grain
            else:
                refined_type = REFINE.get_grain_type(particle)
                if not refined_type:
                    continue

                refined.lineage = classification
                refined.type = refined_type
                refined.substance = SAMPLE.particle_name(particle)
                refined.location = SAMPLE.particle_location(particle)
                refined.progenitor = new_product_line
                refined_grains.append(refined)
                refined = Grain('', None, '', (0,0), False)

        return refined_grains


'''
AFFORDANCE:
A test bench, or lab, that inspects samples of powder

Casts the symbolic LEXICON of the base CODEX into particle parlance, allowing us to identify how we purify the particles
'''
class SAMPLE(CODEX):
    # KNOWLEDGE: Allows impurities to be sieved from the powder - all particles of these objective types are collected by the sieve
    SIEVE = ENTITY('NAME')
    SIEVE.add('OP')
    SIEVE.add('COMMENT')
    SIEVE.add('STRING')
    SIEVE.add('INDENT')
    SIEVE.add('DEDENT')

    # KNOWLEDGE: when to start de-sludging the powder
    SLUDGE = ENTITY('OP', 'DECORATOR')

    # KNOWLEDGE: when we know the powder has been de-sludged
    DESLUDGE = ENTITY('NAME', 'ENCAPSULATORS')

    # KNOWLEDGE: The particle types that have finescale filters
    FILTERED = ENTITY('OP')

    # KNOWLEDGE: And The finescale filters they have
    FILTER = ENTITY('OP', 'ACCESSOR')

    # KNOWLEDGE: Particles in suspension flow outside of the norm, we need to bubble some others up when we meet a suspension
    SUSPENSIONS = ENTITY('COMMENT') 
    BUBBLE_UP = ENTITY('DEDENT')
    BUBBLE_UP.add('INDENT')

    '''
    MECHANISM:
    creates the powder from the bulk material
    '''
    @staticmethod
    def assay(bulk_material):
        return list(CODEX.objectify(bulk_material))

    '''
    SKILL:
    Blocks powder particles that don't fall through the sieve for collection
    '''
    @staticmethod
    def sieved(particle):
        return SAMPLE.SIEVE.is_entity(particle)

    '''
    DISPOSITION:
    Detects the emergence of a clump of sludge
    '''
    @staticmethod
    def has_sludged(particle):
        return SAMPLE.SLUDGE.is_entity(particle)

    '''
    DISPOSITION:
    Detects the sludge has been cleared
    '''
    @staticmethod
    def has_desludged(particle):
        return SAMPLE.DESLUDGE.is_entity(particle)

    '''
    SKILL:
    Applies a finescale filter to otherwise clean sieved powder
    '''
    @staticmethod
    def is_filtrate(particle):
        if SAMPLE.FILTER.is_entity(particle):
            # we have a finescale filter for particles of this type, and it has passed
            return True

        # otherwise it only passes if there wasn't a filter for it
        return not SAMPLE.FILTERED.is_entity(particle)

    '''
    MECHANISM:
    we DO need to know the actual name of a particle!
    '''
    @staticmethod
    def particle_name(subject):
        return CODEX.token_val(subject)

    '''
    MECHANISM:
    A precise reference that ties this particle concept back to the originating source code
    '''
    @staticmethod
    def particle_location(subject):
        return CODEX.token_start(subject)


    '''
    MECHANISM:
    Tests to see if this particle sits in suspension, and if we ought to bubble the next particle up
    '''
    def _is_suspension(this_particle, next_particle):
        if next_particle is not None:
            if SAMPLE.SUSPENSIONS.is_entity(this_particle):
                return SAMPLE.BUBBLE_UP.is_entity(next_particle)
        return False
        # return next_particle and SAMPLE.SUSPENSIONS.is_entity(this_particle) and SAMPLE.BUBBLE_UP.is_entity(next_particle)


# KNOWLEDGE: Classified particles ready to be refined (particles + classification)
@dataclass
class Precursor:
    classification: str
    as_new_line: bool
    particle: object

    def __iter__(self):
        yield self.classification
        yield self.as_new_line
        yield self.particle

    def __len__(self):
        return 3

    def __getitem__(self, index):
        return list(iter(self))[index]

    def __repr__(self):
        class_text = ''
        if self.as_new_line:
            class_text = '*'
        class_text = f"{class_text}{self.classification}"
        return f"<Precursor {self.class_text}: {self.particle}>"

    def __str__(self):
        return self.particle


# KNOWLEDGE: The kinds of grains we make, i.e. the basis for discerning lexical identity and semantic meaning
class GrainType(Enum):
    TEXT = "TEXT"
    IDENTITY = "IDENTITY"


# KNOWLEDGE: just what a grain looks like - i.e. lineage, type, content, canonicalism and original bulk material reference
@dataclass
class Grain:
    lineage: str
    type: GrainType
    substance: str
    location: Tuple[int, int]
    progenitor: bool = field(default=False)

    '''
    MECHANISM:
    Allows a grain to be viewed as a semantic entity
    '''
    def semantics(self):
        return {
            'attestation': self.lineage,
            'category': self.type.name,
            'semantic': self.substance,
            'reference': self.location,
            'is_canonical': self.progenitor
        }

    def __iter__(self):
        yield self.lineage
        yield self.type.name
        yield self.substance
        yield self.location
        yield self.progenitor

    def __len__(self):
        return 5

    def __getitem__(self, index):
        return list(iter(self))[index]

    def __repr__(self):
        loc_text = ''
        if self.progenitor:
            loc_text = '*'
        loc_text = f"{loc_text}{self.location}"
        return f"<Grain {self.type.name}@{loc_text}: '{self.substance}' from {self.lineage}>"

    def __str__(self):
        return self.substance


'''
AFFORDANCE:
Casts the symbolic LEXICON of the base CODEX into grain parlance, allowing us to identify how we refine the particles
'''
class REFINE(CODEX):
    # KNOWLEDGE: What kind of particles causes distillation
    DISTILLANT = ENTITY('OP', 'ACCESSOR')

    # KNOWLEDGE: What kind of particles create IDENTITY grains
    IDENTITY_GRAINS = ENTITY('NAME')

    # KNOWLEDGE: What kind of particles create TEXT grains
    TEXT_GRAINS = ENTITY('COMMENT')
    TEXT_GRAINS.add('STRING')

    '''
    DISPOSITION:
    Detects when we should distil
    '''
    @staticmethod
    def is_distillant(particle):
        return REFINE.DISTILLANT.is_entity(particle)

    '''
    SKILL:
    Categorizes particles
    '''
    @staticmethod
    def get_grain_type(particle):
        if REFINE.TEXT_GRAINS.is_entity(particle):
            return GrainType.TEXT
        if REFINE.IDENTITY_GRAINS.is_entity(particle):
            return GrainType.IDENTITY
        return None
