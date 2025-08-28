'''
WORLD:
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
'''

# CONTINUUM: to get CLI args and issue exit status
import sys
# CONTINUUM: for directory walking, and joining strings as paths
import os
# CONTINUUM: to make o/s independant path from string
from pathlib import Path

'''
THROUGHLINE:
A lash-up script in-lieu of real workflow support.
No metaphor here! We're just providing scafolding for the workhorse narrate scripts.
'''
from granulator import GRANULATOR
from lexicographer import LEXICOGRAPHER

# KNOWLEDGE: An initially empty dictionary that comes to hold the full linguistic set as Python script files are processed
all_expositions = {}

'''
BEHAVIOUR:
Seeks out files of interest that are then granulated so that expositions can be extracted into the full linguistic set.
'''
def scan_files(root, dictout, indexout):
    # PROSE:
    # During extraction the lexicographer is stateful, so we create an instance for it - BUT once we have the expositions for a given script we no longer need that state (since expositions are collated here) so we re-use the instance for each script.
    lexicographer = LEXICOGRAPHER()

    footer = '=' * 80
    # We walk sub-directories, excluding those that start with underscore which are probs holding areas for regressions etc...
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('_')]

        # We scan for Python scripts that do not start with underscore, since they're probably opaque suport files or some kind of transient
        for file in filenames:
            if file.startswith('_'):
                continue
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                header = f"=== Narrate {full_path}:"
                print(header)

                with open(full_path, 'rb') as f:
                    # We create a GRANULATOR instance for each file, but once we have the granulate we don't need it anymore - so these are just transient objects.
                    granulator = GRANULATOR(f, full_path)
                    granulated = granulator.granulate()
                    if not granulated:
                        header += "- not granulated"
                        continue

                print(header)

                # Once we have the granulate we employ the lexicographer to extract a dictionary of lexemes for this file...
                expositions = lexicographer.extract(granulated)
                # ...which we collate into our master dictionary
                all_expositions.update(expositions)

        # Once all files have been processed we get the LEXICOGRAPHER to list and save the full set of extracted lexemes
        print(f"=== ALL FOUND EXPOSITIONS:")
        LEXICOGRAPHER.list_expositions(all_expositions)
        print(footer)


        LEXICOGRAPHER.save_to_file(all_expositions, dictout, indexout)

'''
MECHANISM:
Just like one of those annoying 'are you sure?' prompts that we all end up regretting just saying 'YES' to one day...
'''
def confirm_overwrite(path):
    response = input(f"File '{path}' already exists. Overwrite? [y/N]: ").strip().lower()
    return response == 'y'

'''
BEHAVIOUR:
Nothing fancy here, scopes out the scene and tells the tale of any found scripts
'''
def tell_the_tale():
    # PROSE:
    # Are we sitting comfortably? Do we know who's story we are telling, and where we are recording it?
    if len(sys.argv) != 3:
        print("Usage: python narrate.py <scan_dir> <base_filename>")
        sys.exit(1)

    scan_dir = Path(sys.argv[1])
    basefile = sys.argv[2]

    if not scan_dir.is_dir():
        print(f"Scan directory '{scan_dir}' does not exist.")
        sys.exit(1)

    json_path = os.path.join(scan_dir, f"{basefile}.json")
    txt_path  = os.path.join(scan_dir, f"{basefile}.txt")

    # Did we tell this tale before and are we happy to overwrite or update it?
    if Path(json_path).exists() and not confirm_overwrite(json_path):
        print("Aborting to preserve existing JSON and TXT files.")
        sys.exit(1)

    # Then we will begin...
    print(f"Scan directory: {scan_dir}")
    print(f"Output base filename: {basefile}")

    scan_files(root=scan_dir, dictout=json_path, indexout=txt_path)

if __name__ == '__main__':
    tell_the_tale()
