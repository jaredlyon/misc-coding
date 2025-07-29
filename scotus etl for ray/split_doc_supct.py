import re
import os

# --- CONFIG ---
input_file = "sc bar.txt"  # Path to your plain text file
output_dir = "output_md_supct"  # Directory to save .md files

# --- Ensure output directory exists ---
os.makedirs(output_dir, exist_ok=True)

# --- Load input file ---
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# --- Split rules ---
rules = re.split(r"(?=^Rule\s\d+[A-Za-z]*\.)", content, flags=re.MULTILINE)

# --- Process each rule ---
for rule in rules:
    if not rule.strip().startswith("Rule "):
        continue

    header_match = re.match(r"^Rule (\d+[A-Za-z]*)\. (.+)", rule)
    if not header_match:
        print("Skipping malformed rule:", rule[:100])
        continue

    rule_number = header_match.group(1)
    title_text = header_match.group(2).strip()

    # Filename and metadata
    filename = f"rule_{rule_number.lower()}.md"
    permalink = f"/supct/rule_{rule_number.lower()}/"
    title_line = f"Rule {rule_number}. {title_text}"

    # Extract body (after the title line)
    body = rule.split("\n", 1)[1] if "\n" in rule else ""

    # Process each line for indentation
    processed_lines = []
    for line in body.splitlines():
        line = line.rstrip()
        prefix = line[:5]  # First 3 characters for indentation rules

        if re.match(r"\([a-z]\)", prefix):
            # Lowercase (a) – one indent
            indent = "    "
        elif re.match(r"\([A-Z]\)", prefix):
            # Uppercase (A) – two indents
            indent = "        "
        elif re.match(r"\(([ivxlcdm]+)\)", prefix):
            # roman
            indent = "        "
        else:
            indent = ""

        processed_lines.append(indent + line)

    # Compose full .md file content
    md_output = "\n".join([
        "---",
        "layout: rule",
        f'title: "{title_line}"',
        f"permalink: {permalink}",
        "---",
        "",
        "\n\n\n".join(processed_lines)
    ])

    # Write to .md file
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_output)

    print(f"✅ Wrote: {filename}")
