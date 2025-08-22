import sys
import os
from pathlib import Path
from pprint import pprint

# from _dynamic_narrative import TypeOracle

from granulator import GRANULATOR
from lexicographics import LEXICOGRAPHER, ExpoTags

all_expositions = {}

def scan_files(root, dictout, indexout):
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

                expositions = LEXICOGRAPHER.extract(granulated)
                all_expositions.update(expositions)

                # print(f"=== FOUND REFFERENCES:")
                # LEXICOGRAPHER.print_attestations(granulated)
                # print(footer)

                # print(f"=== FOUND IDENTITIES:")
                # LEXICOGRAPHER.print_identities(granulated)
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
