import os
from pprint import pprint

# from _dynamic_narrative import TypeOracle

from granulator import GRANULATOR
from lexicographics import LEXICOGRAPHER, ExpoTags

all_expositions = {}

def scan_files(scan_count=-1, root="."):
    all_identities = {}

    # with TypeOracle() as oracle:
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

                identities, expositions = LEXICOGRAPHER.extract(granulated)
                all_identities.update(identities)
                all_expositions.update(expositions)

                # print("POWDER:")
                # granulator.dump_powder()

                if scan_count < 0:
                    continue # i.e. scan all
                scan_count -= 1
                if scan_count <= 0:
                    break

        footer = '=' * 80
        # print(f"=== ALL FOUND IDENTITIES:")
        # for identity in all_identities.values():
            # pprint(identity)
        # print(footer)

        print(f"=== ALL FOUND EXPOSITIONS:")
        LEXICOGRAPHER.list_expositions(all_expositions)
        print(footer)

        print(f"=== FOUND THROUGHLINES:")
        LEXICOGRAPHER.print_expositions(all_expositions, ExpoTags.THROUGHLINE)
        print(footer)

        LEXICOGRAPHER.save_to_file(all_expositions, 'expo')

if __name__ == '__main__':
    files_to_scan = -1
    print(f"SCAN {files_to_scan}")
    scan_files(files_to_scan, root='.')
    # with TypeOracle() as oracle:
        # scan_files(files_to_scan, root='.')
