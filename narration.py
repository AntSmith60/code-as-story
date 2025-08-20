import json
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

            if ':' in line:
                key, category = line.rsplit(':', 1)
                key = key.strip()
                category = category.strip()
                lexeme = lexeme_dict.get(key)

                depth = key.count('.') + 1
                depth = max(1, depth - 1)
                header_prefix = '#' * min(depth, 6)

                if lexeme:
                    out.write(f"{header_prefix} {key} · *{category}*\n\n")
                    out.write(f"{lexeme['content'].rstrip()}\n\n")
                else:
                    out.write(f"{header_prefix} {key} · *[Missing]*\n\n")
                    out.write(f"> ⚠️ Lexeme not found in archive.\n\n")
            else:
                # Treat as editorial glue—write as-is
                out.write(line + '\n')

if __name__ == '__main__':
    rehydrate_and_render('expo', 'narration.md')