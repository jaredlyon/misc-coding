import re
import os

# --- CONFIG ---
input_file = "frcp.txt"  # Path to your plain text file
output_dir = "output_md_frcp"  # Directory to save .md files

# --- Ensure output directory exists ---
os.makedirs(output_dir, exist_ok=True)

# --- Clear old files in output directory ---
for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

# --- Load input file ---
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# --- Split rules ---
rules = re.split(r"(?=^Rule\s\d+(?:\.\d+)?[A-Za-z]*\.)", content, flags=re.MULTILINE)

# --- Process each rule ---
for rule in rules:
    if not rule.strip().startswith("Rule "):
        continue

    # Match rule header with support for numbers like 4.1 and letters like 4.1A
    header_match = re.match(r"^Rule\s(\d+(?:\.\d+)?[A-Za-z]*)\. (.+)", rule)
    if not header_match:
        print("Skipping malformed rule:", rule[:100])
        continue

    rule_number = header_match.group(1)
    title_text = header_match.group(2).strip()

    # Filename and metadata
    filename = f"rule_{rule_number.lower()}.md"
    permalink = f"/frcp/rule_{rule_number.lower()}/"
    title_line = f"Rule {rule_number}. {title_text}"

    # Extract body (after the title line)
    body = rule.split("\n", 1)[1] if "\n" in rule else ""

    # --- Process each line for indentation ---
    processed_lines = []
    prev_indent_level = 0
    prev_line_type = None  # Track the type of the previous line

    for line in body.splitlines():
        line = line.rstrip()
        prefix = line[:5]  # For long markers like (xiv)

        line_type = None  # Track current line type for comparison

        if re.match(r"\([a-h]\)", prefix):
            indent_level = 0
            line_type = "lower"
        elif re.match(r"\(\d+\)", prefix):
            indent_level = 1
            line_type = "numeric"
        elif re.match(r"\([A-Z]\)", prefix):
            indent_level = 2
            line_type = "upper"
        elif re.match(r"\(([ivxlcdm]+)\)", prefix):
            line_type = "roman"
            if prev_line_type == "roman":
                indent_level = prev_indent_level  # same indent as previous
            else:
                indent_level = prev_indent_level + 1  # one deeper than previous
        else:
            indent_level = 0
            line_type = None

        indent = "&nbsp;&nbsp;" * indent_level
        processed_lines.append(indent + line)

        # Update tracking vars
        prev_indent_level = indent_level
        prev_line_type = line_type

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
