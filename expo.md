# *** INTRODUCTION ***

The purpose here is just to exercise the concept of marrying narrative (story) to source code.



The underlying concept is that narrative is a foundational aspect of human cognition - it is through story that we get to experience the abstract; for understanding arises not just from knowing, but from experiencing (feeling) that which is known.



We believe coding is a creative process, but to be so the code must ignite cognition.



This is the fundamental tenet of the Narratival-Exposition Paradigm, which we explore with this code base.



So, this code base reads this code base to produce this code base's documentation...



## Pre-requisites

These scripts require a code base that has been written in the (evolving) Narratival-Exposition's grammar - e.g. this code base!



## World View

Generating the narrative happens in 3 phases (well, 3 phases after actually writing the code):

- Extracting points of story; textual commentary attached to Pythonic objects.

- Editorialisation of their order (i.e. so that the narrative is orthogonal to the code architecture)

- Narration: pouring the story points into the editorialsation to generate the narrative arc



Herein, we see the narration of the phase 1 code base: the extraction process. This produces the files needed for the (manual) editorialisation phase, which then allows the narration script to produce the doccumentation.



During extraction the core concepts we will meet are:

- CODICES: books or lore that offer symbolic overlays to the source code

- GRANULATION: the powderisation, purification, mixing and refinement of the codified symbolism

- REGISTRAR: of births, deaths and marriages; providing the lineage (Pythonic scope) of granular entities

- LEXICOGRAPHICS: the mechanisms that sift and convert the lineage-tracked symbolic grains to generate lexemes: the discovered lexical tokens in the source code along with their canonical reference and semantic meaning.



# *** CHAPTER - CODICES ***

First we talk about codices... how they provide a symbolic view of Python source code through a variety of lenses

## THROUGHLINE

_(6, 0)throughline_:codices

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

## PROVISIONS

**The basic CODEX provides:**

_(1, 0)continuum_:codices.token: Lets us know the structure of a token, specifically, type and value (.string)

_(3, 0)continuum_:codices.tokenize: Tokenizes a text stream in-line with Python  syntax

_(42, 0)knowledge_:codices.CODEX_OBJECTS: Objects define the nature of subjects. E.g. the subject 'def' is a NAME object, in raw token parlance.

_(46, 0)affordance_:codices.CODEX

Though literally a tree trunk (from the Latin *codex*), the term has come to signify a book of law — or more precisely, of lore.



Not 'law' in the contemporary sense, but rather 'ritual' or 'rite': the correct sequence of symbols that achieves a result.



And herein, our codices do just that — they prescribe the correct sequence of things in terms of their symbolism (ruinic nature).



In the base CODEX, very little is known beyond the symbolic meaning of what occurs in the provided sequence.



Thus, the base CODEX offers:

- a symbolic lexicon (as a dict),

- a means to generate the sequence (objectify the source),

- and a way to discern the true name (or value) of encountered symbols.

_(62, 4)knowledge_:codices.CODEX.LEXICON: Symbolises specific python token subjects that direct our layered parsing

_(87, 4)mechanism_:codices.CODEX.objectify: Encapsulates the tokenisation process

_(95, 4)mechanism_:codices.CODEX.token_val: We want to contain ALL token structure knowledge to the base CODEX

so here's how we get to what a token actually IS.

_(103, 4)mechanism_:codices.CODEX.token_start: We want to contain ALL token structure knowledge to the base CODEX

so here's how we get where the token occurred

## ENTITIES and VIEWS

**And then to support the different views:**

_(112, 0)affordance_:codices.ENTITY

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

_(139, 4)mechanism_:codices.ENTITY.add: Extends the ENTITY's potence by adding more types and values it recognises.

_(150, 4)skill_:codices.ENTITY.is_entity: Determines if this ENTITY recognise a given token.

---

**Which gifts us these varying views:**

_(267, 0)affordance_:granulator.SAMPLE

A test bench, or lab, that inspects samples of powder



Casts the symbolic LEXICON of the base CODEX into particle parlance, allowing us to identify how we purify the particles

_(454, 0)affordance_:granulator.REFINE

Casts the symbolic LEXICON of the base CODEX into grain parlance, allowing us to identify how we refine the particles

_(166, 0)affordance_:registrar.LINEAGE

Casts the symbolic LEXICON of the base CODEX into lineage parlance, allowing us to identify lineage related ENTITIES

---

---

# *** CHAPTER - GRANULATION ***

## THROUGHLINE

_(14, 0)throughline_:granulator

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

## DESCRIPTION, contexts and knowledge:

_(40, 0)figuration_:granulator.GRANULATOR

Takes an unruly, heterogeneous input bulk material and turns it into an intermediate purified precursor which is then refined into grains.



Uses the SAMPLE test bed to inspect each particle and applies track&trace (via the registrar) to give just the particles of interest along with their full lineage.



Then refines particles into grains

_(1, 0)continuum_:granulator.os: allows conversion of an underlying filepath to a batch identity

_(4, 0)continuum_:granulator.dataclasses: allows us to create a named structure for the final substance list we produce

_(50, 8)knowledge_:granulator.GRANULATOR.__init__.bx_id: identity of the overall package of materials

_(57, 8)knowledge_:granulator.GRANULATOR.__init__.self.powder: Full catalogue of the original material, as particles

_(60, 8)knowledge_:granulator.GRANULATOR.__init__.self.purified: list of purified particles

_(63, 8)knowledge_:granulator.GRANULATOR.__init__.self.intermediate: list of intermediates as Precursor class

_(66, 8)knowledge_:granulator.GRANULATOR.__init__.self.refined: resulting list of refined grains as Grain class

## Key BEHAVIOURS and supporting mechanisms

_(114, 4)behaviour_:granulator.GRANULATOR.granulate: Assay's the material and performs the granulation. 

This is a distinct step from initiating the Granulator in case there are any startup issues

(Pythonic mantra: __init__ must succeed)

_(69, 4)mechanism_:granulator.GRANULATOR.dump_powder: Shows the powderised bulk raw material

_(76, 4)mechanism_:granulator.GRANULATOR.dump_purified: Shows the purified bulk raw material powder

_(86, 4)mechanism_:granulator.GRANULATOR.dump_bx_record: Shows the tracked intermediate precursors

_(93, 4)mechanism_:granulator.GRANULATOR.dump_inventory: Shows the final set of grains

---

---

## *** GRANULATION: PURIFY AND MIX ***

Transforms the powderised particles into:

_(373, 0)knowledge_:granulator.Precursor: Classified particles ready to be refined (particles + classification)

### SAMPLE CODEX

**This stage of Granulation uses the SAMPLE derived codex, which provides:**

_(299, 4)mechanism_:granulator.SAMPLE.assay: creates the powder from the bulk material

_(344, 4)mechanism_:granulator.SAMPLE.particle_name: we DO need to know the actual name of a particle!

_(352, 4)mechanism_:granulator.SAMPLE.particle_location: A precise reference that ties this particle concept back to the originating source code

**Along with these pairings of knowledge and skills:**

_(274, 4)knowledge_:granulator.SAMPLE.SIEVE: Allows impurities to be sieved from the powder - all particles of these objective types are collected by the sieve

_(307, 4)skill_:granulator.SAMPLE.sieved: Blocks powder particles that don't fall through the sieve for collection

_(282, 4)knowledge_:granulator.SAMPLE.SLUDGE: when to start de-sludging the powder

_(315, 4)disposition_:granulator.SAMPLE.has_sludged: Detects the emergence of a clump of sludge

_(285, 4)knowledge_:granulator.SAMPLE.DESLUDGE: when we know the powder has been de-sludged

_(323, 4)disposition_:granulator.SAMPLE.has_desludged: Detects the sludge has been cleared

_(288, 4)knowledge_:granulator.SAMPLE.FILTERED: The particle types that have finescale filters

_(291, 4)knowledge_:granulator.SAMPLE.FILTER: And The finescale filters they have

_(331, 4)skill_:granulator.SAMPLE.is_filtrate: Applies a finescale filter to otherwise clean sieved powder

_(294, 4)knowledge_:granulator.SAMPLE.SUSPENSIONS: Particles in suspension flow outside of the norm, we need to bubble some others up when we meet a suspension

_(361, 4)mechanism_:granulator.SAMPLE._is_suspension: Tests to see if this particle sits in suspension, and if we ought to bubble the next particle up

### Key behaviours

_(135, 4)behaviour_:granulator.GRANULATOR.purify: Purifies the powder by sieving for particles of interest

ALSO passes the sieved powder through a fine-scale filter

AND detects/discards any clumpy sludge found in the powder



Each purified particle is classified from the on-going batch records

 Interlude in a poet's voice...

- CANTO I: In which The Sludge is Sloughed
- if is sludge and has not desludged
- CANTO II: In which The Sludge is Sought
- if not is sludge and now has sludged
- CANTO III: In which The Pure is Preserved
- if you can sieve and be filtrate then 
- - you'll be Purified, my son!

_(173, 4)behaviour_:granulator.GRANULATOR.fine_mix: Sometimes particles form a suspension (COMMENTS + DENTS) that needs breaking up so that the particles will bond correctly when we refine them into grains.

Mixing allows the DENTs to bubble up so they evapourate as we inspect and classify the remainder

 On the fine mix process...

- Break up suspensions so the DENTs don't come between TEXTs and NAMEs
- Evapourate the DENTs so the remainder can be classified
- No longer just a powder, the intermediate is ready to be refined into grains

granulator.GRANULATOR._mix

granulator.GRANULATOR._evapourate

---

---

## *** GRANULATION: REFINE ***

**Transforms the precursor into:**

_(408, 0)knowledge_:granulator.Grain: just what a grain looks like - i.e. lineage, type, content, canonicalism and original bulk material reference

**Additional material details:**

_(402, 0)knowledge_:granulator.GrainType: The kinds of grains we make, i.e. the basis for discerning lexical identity and semantic meaning

_(417, 4)mechanism_:granulator.Grain.semantics: Allows a grain to be viewed as a semantic entity

### REFINE CODEX

**This stage of Granulation uses the REFINE derived codex, which provides these pairings of knowledge and skills**

_(459, 4)knowledge_:granulator.REFINE.DISTILLANT: What kind of particles causes distillation

_(469, 4)disposition_:granulator.REFINE.is_distillant: Detects when we should distil

_(462, 4)knowledge_:granulator.REFINE.IDENTITY_GRAINS: What kind of particles create IDENTITY grains

_(465, 4)knowledge_:granulator.REFINE.TEXT_GRAINS: What kind of particles create TEXT grains

_(477, 4)skill_:granulator.REFINE.get_grain_type: Categorizes particles

### Key behaviours

_(225, 4)behaviour_:granulator.GRANULATOR.refine: From purification we now have muddled comments and strings which will become the TEXTS

  and split Identities with sequences of NAME(.NAME...)s

  Refines NAMEs through distillation

 On the distillation process

- If we are not already distilling, see if we should
- If we are distilling, condense into previous grain
- Otherwise create a new grain

---

---

# *** CHAPTER - THE REGISTRAR ***

## THROUGHLINE

_(2, 0)throughline_:registrar

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

## DESCRIPTION, contexts and knowledge

_(24, 0)figuration_:registrar.REGISTRAR

The Registrar recognises and declares subject titles according to the evolving lineage of recorded subjects.



Some subjects (DENTS and PROGENITORS) do not receive titles, but they influence the shape and continuity of the lineage.



Other subjects (HONOURIFICS) are not recorded at all — they serve only to address true subjects, and are thus excluded from lineage.

_(34, 8)knowledge_:registrar.REGISTRAR.__init__.self._resilience: tracks how the heritage line waxes and wanes

_(37, 8)knowledge_:registrar.REGISTRAR.__init__.self._register: A new register is created for each registrant (grand forebear)

_(41, 8)disposition_:registrar.REGISTRAR.__init__.self._heir_apparent: are we currently looking for the true identity of an heir apparent, or else just recording subject titles

_(43, 8)knowledge_:registrar.REGISTRAR.__init__.self._heir: the true identity of an heir apparent

## LINEAGE CODEX

**This stage of Granulation uses the LINEAGE derived codex, which provides these pairings of knowledge and skills**

_(171, 4)knowledge_:registrar.LINEAGE.PROGENITORS: The subjects that (potentially) start a new generation in the lineage

_(201, 4)skill_:registrar.LINEAGE.is_progenitor: Matches progenitor type subjects only

_(174, 4)knowledge_:registrar.LINEAGE.HONOURIFICS: The ways in which subjects may be addressed, not actual subject identities

_(177, 4)knowledge_:registrar.LINEAGE.IDENTITIES: The subjects that may be true identities

_(180, 4)knowledge_:registrar.LINEAGE.DESCENDERS: The subjects that give rise to descendents

_(209, 4)skill_:registrar.LINEAGE.is_descender: Matches descender type subjects only

_(189, 4)knowledge_:registrar.LINEAGE.TRUE_SUBJECTS: True subjects - the things we want to record

_(217, 4)skill_:registrar.LINEAGE.is_true_identity: Matches subjects that are true identities (not honourifics)

_(193, 4)skill_:registrar.LINEAGE.is_true_subject: Matches with the subjects we want to record

_(243, 4)mechanism_:registrar.LINEAGE.subject_name: we DO need to know the actual name of a subject!

_(183, 4)knowledge_:registrar.LINEAGE.GROWTH: Represents a waxing in the current family-line's resilience

_(227, 4)skill_:registrar.LINEAGE.growth: Detects when the current family line grows

_(186, 4)knowledge_:registrar.LINEAGE.DECLINE: Represents a waning in the current family-line's resilience

_(235, 4)skill_:registrar.LINEAGE.decline: Detects when a current family line has declined

---

## Key behaviours

_(46, 4)behaviour_:registrar.REGISTRAR.record_history: Provides the current lineage relevant to a subject, IF this is a notable subject.

  But NOTE - what a topsy-turvey world we live in!

  Because we have to look forwards we find new progenitors before we find their identity!

  So instead of simply saying: 

  > Prepare for heir, seek heir, record heir...

  we have to say:

  > record (the current) heir, seek (another) heir, prepare for (next) heir

  

  Kind of backwards really, I guess it stems from 'invasion culture' wherein conquered peoples are dehumanised by being reduced to 'station' afore 'identity', m'lord!

 on how the code-tree grows and withers

- First, keep an eye on the resilience of the current family line
- Add any found heir to the lineage
- So that GOING FORWARD the title is recognised
- Once we find a new heir, keep it safe for now
- So the title is awarded on the next cycle
- Otherwise we lose sight of this heir's own lineage
- Have a look-see if we have met a new heir-apparent
- Finally all are remembered in the trace of lineage they leave behind 
- BUT it is only the true that get entitled

##  supporting mechanisms

_(121, 4)skill_:registrar.REGISTRAR._entitle: Joins up all the identities in our current lineage to form a single, recordable, title

registrar.REGISTRAR._lineage_fluxed

_(108, 4)disposition_:registrar.REGISTRAR._seek_heir_apparent: Switches our disposition from seeking an identity to seeking a progenitor

whilst setting the ccurrent found heir apparent

_(129, 4)disposition_:registrar.REGISTRAR._prepare_for_heir: Prepares a progenitor's new lineage, in case there is then a marriage

Switches our disposition from seeking a progenitor to seeking an identity

_(139, 4)skill_:registrar.REGISTRAR._record_heir: Fills in the new lineage, and sets the baseline of this family line's resilience,

which builds upon that of previous generations

_(151, 4)skill_:registrar.REGISTRAR._sign_off_record: Marks the end of a family line by removing its lineage

_(158, 4)flaw_:registrar.REGISTRAR._register_empty: Allows us to check if the register is empty before we try to remove a family line

---

---

# *** CHAPTER LEXICOGRAPHICS ***

## THROUGHLINE

_(9, 0)throughline_:lexicographer

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

## DESCRIPTION

_(43, 0)affordance_:lexicographics.LEXICOGRAPHICS

The core of a lexicographer's abilities

_(29, 0)figuration_:lexicographer.LEXICOGRAPHER

Sifts through a given set of 'entries' to generate:

- a lexicon of known lexicals(!), erm, I mean a list of things that can be known about

- the linguistical set of those things that have meaning

## KNOWLEDGE and CONTEXTS

_(170, 0)knowledge_:lexicographics.LexicalOccurence: holds an attestation contextualised lexical entity

_(208, 0)knowledge_:lexicographics.Lexeme: holds a lexeme - the canonical occurence, category and semantic content of a lexical

_(11, 0)knowledge_:lexicographics.ExpoTags: The types of semantic meaning we can use to adorn our code-base.



- CONTINUUM - alien facets that we use, typically within their own metaphor
- THROUGHLINE - the metaphoric interface, explaining the relationship between the module-metaphore and the world at large
- FIGURATIONs and AFFORDANCEs - high-order CHARACTERISATIONS providing a semantic package. I'm as yet somewhat undecided on their precise differentiation...
- KNOWLEDGE - Typically important datum or data classes
- BEHAVIOUR - a small package of sequenced actions
- MECHANISM - an action, e.g. getters/setters
- SKILL - an ability, e.g. inspect entity, filter list
- DISPOSITION - an indication (or detetcion), of state (or transition)
- PROSE - story woven around code sections
- FLAW - An exception or sentinel

_(1, 0)continuum_:lexicographics.dataclasses: allows us to create named structures for attestations, and lexemes

_(6, 0)continuum_:lexicographics.enum: allows us to create the ExpoTags (Enum) list

_(1, 0)continuum_:lexicographer.json: allows us to format and export our linguistic set as JSON

## KEY BEHAVIOURS

_(149, 4)behaviour_:lexicographer.LEXICOGRAPHER.extract: Sifts through the entries for TEXTs to generate the semantics which are combined to lexicals to ppprovide our lexemes

 On the extraction of meaning...

- Every entry has some kind of meaning, for meaning is a layered construct
- when the meaning relates to one of our lexemes, we're gonna need to find the following lexical (probably)
- At this point we only care about this TEXT's semantic content and the next IDENTITY's lexical value
- clean-up the extracted semantics...

_(180, 4)behaviour_:lexicographer.LEXICOGRAPHER._package_prose: Up to now we have preserved semantic PROSE and non-semantic comment-type texts so we can unpick the commentary from the code in order to build prose blocks.

This is where we collate comment texts within a prose section to form a single semantic prose block - throwing away comment type texts that are NOT inside a prose section.

 Some prose on packaging prose...

- At this point the TEXTs are still a little muddled, you know how strings like to tie themselves into knots right?
- Although we removed TEXTs that are not tagged as exposition, we elected to keep all in-line comments so we can block-up interwoven prose
- At least we now know that any TEXT that doesn't start with HASH, IS a true semantic exposition, so we can focus on the HASH lines here
- We will either keep, drop or merge the HASH lines - so we will end up with fewer TEXTs; lets start with an empty list that will hold the survivors
- and an empty package into which we build-up the texts to be merged.
- Now looking at each text, we initially have no impetus to merge them together...
- We will start merging if this is an in-line comment that introduces PROSE
- While we are merging we pour the lines into our package, without the comment marker which is now obviated, redundant, utterly useless to us.
- AND... a final flush if prose block reaches EOF

lexicographics.LEXICOGRAPHER._update_semantic_package:MECHANISM

lexicographics.LEXICOGRAPHER._update_survivors:MECHANISM

_(125, 4)disposition_:lexicographics.LEXICOGRAPHICS.is_prose_transition: Detects transitions into or out of prose blocks

_(142, 4)skill_:lexicographics.LEXICOGRAPHICS.extend_content: Extends the latest semantic with additional (prose) commentary.

  BUT if we somehow found a prose block before ANY other semantic, we will ttry to add the prose as its own semantic

  This is so we at least get to see the (mis-placed) element somewhere in the outputs, so we can fix it.

  Note, in this case it truly IS mis-placed, because (by defintion) prose annotates a previous semantic.

  Mis-placed prose in module B could even turn up annotating the last semantic of module A!

  The only defence I offer is that you at least get to see the prose SOMEWHERE...

  

  ...unless you don't. A mis-placed prose block will not be added at all IF it would overwrite an existing semantic.

  This ought to be an impossible scenario, thus the silent use of 'pass' in this code.

  FWIW: I'm sorry, sooooo sorry, if that ever trips you up ;^D

## Supporting behaviours

lexicographics.LEXICOGRAPHER.unpack_text_entry:BEHAVIOUR

lexicographics.LEXICOGRAPHER._nonjudgemental_clean:BEHAVIOUR

## Supporting skills and mechanisms

_(216, 4)mechanism_:lexicographics.Lexeme.from_parts: Creates a lexeme by extracting category from a semantic text

_(228, 4)skill_:lexicographics.Lexeme.summary: Summarises a lexeme to category and canonical reference

_(236, 4)mechanism_:lexicographics.Lexeme._dedent: The discovered semantics are indented, partly due to the requirements of the originating code, and partly for semantic clarity.

Here we remove the common margin (minimum indent) found within the semantic content.

lexicographics.LEXICOGRAPHER._is_expo:SKILL

---

---

**And once all done, how we get the detail preserved in files*:*

_(45, 4)behaviour_:lexicographer.LEXICOGRAPHER.save_to_file: Creates a json file containing the full linguistic set and a text file listing the canonicals

_(67, 4)behaviour_:lexicographer.LEXICOGRAPHER.list_expositions: returns a list of lexeme summaries from a linguistical set

_(84, 4)behaviour_:lexicographer.LEXICOGRAPHER.print_expositions: prints a linguistical set

_(95, 4)behaviour_:lexicographer.LEXICOGRAPHER.print_expo: formats and prints a single lexeme, indenting as per the depth of its attestation.

_(136, 4)mechanism_:lexicographer.LEXICOGRAPHER._indent: performs an identation of a semantic unit as decoration for direct printed output

---

---

doc ends.

