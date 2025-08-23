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

---
Note, this script hasn't really been authored... more lashed together so I can run my Proof-of-Concept. A production version would ofer a mucch improved interface, and more especially address my main irk: currently I have to be careful not to overwrite editorialisation added to the .txt output file; which is slightly complex but really we need workflow support in the tooling... a whole other dimension which will utterly obviate this entry script. So it is what it is (and that is, is pretty damn ugly).
'''

# CONTINUUM: filepath support
import sys
import os
from pathlib import Path
from pprint import pprint

# from _dynamic_narrative import TypeOracle

from granulator import GRANULATOR
from lexicographer import LEXICOGRAPHER

all_expositions = {}

def scan_files(root, dictout, indexout):
    lexicographer = LEXICOGRAPHER()

    # with TypeOracle() as oracle:
    footer = '=' * 80
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('_')]

        for file in filenames:
            if file.startswith('_'):
                continue
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                header = f"=== Narrate {full_path}:"
                print(header)

                with open(full_path, 'rb') as f:
                    granulator = GRANULATOR(f, full_path)
                    granulated = granulator.granulate()
                    if not granulated:
                        header += "- not granulated"
                        continue

                print(header)

                expositions = lexicographer.extract(granulated)
                all_expositions.update(expositions)

                # print(f"=== FOUND REFFERENCES:")
                # lexicographer.print_attestations(granulated)
                # print(footer)

                # print(f"=== FOUND IDENTITIES:")
                # lexicographer.print_identities(granulated)
                # print(footer)

        print(f"=== ALL FOUND EXPOSITIONS:")
        LEXICOGRAPHER.list_expositions(all_expositions)
        print(footer)


        LEXICOGRAPHER.save_to_file(all_expositions, dictout, indexout)

def confirm_overwrite(path):
    response = input(f"File '{path}' already exists. Overwrite? [y/N]: ").strip().lower()
    return response == 'y'

if __name__ == '__main__':
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

    if Path(json_path).exists() and not confirm_overwrite(json_path):
        print("Aborting to preserve existing JSON files.")
        sys.exit(1)

    if Path(txt_path).exists() and not confirm_overwrite(txt_path):
        txt_path = ''
        print("Will regenerate JSON only")

    print(f"Scan directory: {scan_dir}")
    print(f"Output base filename: {basefile}")

    scan_files(root=scan_dir, dictout=json_path, indexout=txt_path)
