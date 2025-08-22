import sys
import os
from pathlib import Path
import json

def rehydrate_and_render(path, output_path):
    # Load lexeme data
    with open(path + '.json', 'r', encoding='utf-8') as jf:
        lexeme_dict = json.load(jf)

    # Load editorial lines
    with open(path + '.txt', 'r', encoding='utf-8') as tf:
        editorial_lines = [line.rstrip() for line in tf]

    # Render to markdown
    with open(output_path, 'w', encoding='utf-8') as out:
        for line in editorial_lines:
            if not line.strip():
                out.write('\n')  # Preserve blank lines
                continue

            if not ':' in line:
                out.write(line.rstrip() + '\n\n')
                continue

            key, category = line.rsplit(':', 1)
            key = key.strip()
            category = category.strip()
            lexeme = lexeme_dict.get(key)

            if lexeme:
                # depth = max(2, key.count('.'))
                # header_prefix = '#' * min(depth, 6)
                # out.write(f"{header_prefix} _{category.lower()}_:{key}\n\n")
                # out.write(f"{lexeme['content'].rstrip()}\n\n")

                depth = key.count('.')
                if category.upper().strip() in ['THROUGHLINE', 'FIGURATION', 'AFFORDANCE']:
                    separator = '\n\n'
                else:
                    separator = ': '

                out.write(f"_{lexeme['reference']}{category.lower()}_:{key}{separator}{lexeme['content'].rstrip()}\n\n")
            else:
                out.write(line.rstrip() + '\n\n')


def confirm_overwrite(path):
    response = input(f"File '{path}' already exists. Overwrite? [y/N]: ").strip().lower()
    return response == 'y'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python narrate.py <base_filename>")
        sys.exit(1)

    basefile = sys.argv[1]

    json_path = f"{basefile}.json"
    txt_path = f"{basefile}.txt"
    md_path = f"{basefile}.md"

    if Path(md_path).exists() and not confirm_overwrite(md_path):
        print("Aborting to preserve existing markdown file.")
        sys.exit(1)

    for path in [json_path, txt_path]:
        if not Path(path).exists():
            print("Aborting due to missing file: {path}.")
            sys.exit(1)

    print(f"Inputs: {json_path}, {txt_path}")
    print(f"Output: {md_path}")

    rehydrate_and_render(basefile, md_path)