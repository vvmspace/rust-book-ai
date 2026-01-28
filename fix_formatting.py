import os
import re

RUS_DIR = 'rus'

def fix_formatting(content):
    lines = content.splitlines()
    temp_lines = []
    in_quote = False
    
    # Pass 1: Normalize quotes, add spacing, fix List-Hyphen issue
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_quote = stripped.startswith('>')
        
        if is_quote:
            if not in_quote:
                if temp_lines and temp_lines[-1].strip() != '':
                    temp_lines.append('')
                in_quote = True
            
            # Ensure space after >
            # Check for "> - " which creates a bullet list!
            if re.match(r'>\s*-\s+', line):
                # Replace the hyphen with em-dash
                line = re.sub(r'>\s*-\s+', '> — ', line, count=1)
            
            elif re.match(r'>[^ \t]', stripped):
                 line = line.replace('>', '> ', 1)
                 
        else:
            if in_quote and stripped != '':
                 temp_lines.append('')
            if stripped != '':
                 in_quote = False
        
        # FIX FOR LISTS
        # Check if line looks like a list item (numbered or bullet)
        # Regex: Start of line, optional whitespace, 1 or more digits + dot + space OR hyphen/star + space
        is_list_item = re.match(r'^\s*(\d+\.|-|\*)\s+', line)
        
        if is_list_item and temp_lines:
            prev_line = temp_lines[-1].strip()
            # If previous line is not empty, not a header, not a list item, not a fence... insert blank line
            # We want to break "Paragraph text.1. List item" into "Paragraph text.\n\n1. List item"
            # But we don't want to break "1. Item one\n2. Item two"
            
            is_prev_list_item = re.match(r'^\s*(\d+\.|-|\*)\s+', prev_line)
            is_prev_header = prev_line.startswith('#')
            is_prev_fence = prev_line.startswith('```')
            is_prev_empty = (prev_line == '')
            
            if not is_prev_empty and not is_prev_list_item and not is_prev_header and not is_prev_fence:
                # Add blank line contextually
                temp_lines.append('')

        temp_lines.append(line)

    # Pass 2: Add hard breaks (two spaces) for dialogue lines in quotes
    final_lines = []
    for i, line in enumerate(temp_lines):
        stripped = line.strip()
        
        if stripped.startswith('>'):
            if i + 1 < len(temp_lines):
                next_line = temp_lines[i+1].strip()
                if next_line.startswith('>'):
                    # Check for dialogue markers in next line
                    next_content = next_line[1:].strip()
                    
                    if (next_content.startswith('-') or 
                        next_content.startswith('*') or 
                        next_content.startswith('—') or 
                        next_content.startswith('–') or
                        re.match(r'\d+\.', next_content)):
                        
                        if not line.endswith('  '):
                            line = line.rstrip() + '  '
        
        final_lines.append(line)

    content = "\n".join(final_lines)
    content = re.sub(r'(\*\*.*?\*\*)\s*>\s*', r'\1\n\n> ', content)
    
    return content + "\n"

def main():
    print(f"Scanning {RUS_DIR} for formatting fixes...")
    
    for filename in os.listdir(RUS_DIR):
        if filename.endswith('.md'):
            path = os.path.join(RUS_DIR, filename)
            with open(path, 'r') as f:
                content = f.read()
            
            fixed = fix_formatting(content)
            
            if fixed != content:
                print(f"Fixing {filename}")
                with open(path, 'w') as f:
                    f.write(fixed)

if __name__ == "__main__":
    main()
