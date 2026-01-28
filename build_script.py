import os
import re
import subprocess
import sys

# Paths
SRC_SUMMARY = 'src/SUMMARY.md'
RUS_DIR = 'rus'
BUILD_DIR = 'build_epub'

def extract_links(summary_path):
    links = []
    with open(summary_path, 'r') as f:
        for line in f:
            match = re.search(r'\[.*?\]\((.*?)\)', line)
            if match:
                path = match.group(1)
                links.append(path)
    return links

def get_anchor_content(file_path, anchor):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"// FILE NOT FOUND: {file_path}"
    
    start_marker = f"ANCHOR: {anchor}"
    end_marker = f"ANCHOR_END: {anchor}"
    
    content = []
    capture = False
    found = False
    for line in lines:
        if end_marker in line:
            capture = False
        if capture:
            content.append(line)
        if start_marker in line:
            capture = True
            found = True
            
    if not found:
        return f"// ANCHOR {anchor} NOT FOUND IN {file_path}"

    return "".join(content)

def process_includes(content, file_dir):
    # 1. Process custom <Listing> tags to make them visible in EPUB
    def replace_listing(match):
        attrs = match.group(1)
        number = re.search(r'number="(.*?)"', attrs)
        caption = re.search(r'caption="(.*?)"', attrs)
        filename = re.search(r'file-name="(.*?)"', attrs)
        
        parts = []
        if number:
            parts.append(f"Листинг {number.group(1)}")
        if caption:
            parts.append(caption.group(1))
            
        header = ""
        if parts:
            header = f"\n**{': '.join(parts)}**"
        
        if filename:
            header += f" *({filename.group(1)})*"
            
        return header + "\n"

    content = re.sub(r'<Listing\s+(.*?)>', replace_listing, content)
    content = re.sub(r'</Listing>', '', content)

    # 2. Process {{#include}} directives
    def replace_include(match):
        directive = match.group(1) # rustdoc_include or include
        path_spec = match.group(2)
        
        parts = path_spec.split(':')
        rel_path = parts[0]
        anchor = parts[1] if len(parts) > 1 else None

        # Resolve path
        abs_path = os.path.normpath(os.path.join(file_dir, rel_path))
        
        if anchor:
            included_text = get_anchor_content(abs_path, anchor)
        else:
            try:
                with open(abs_path, 'r') as f:
                    included_text = f.read()
            except FileNotFoundError:
                return f"<!-- INCLUDE FAILED: {abs_path} -->"

        return included_text

    pattern = re.compile(r'\{\{#(rustdoc_|)?include\s+(.*?)\}\}')
    return pattern.sub(replace_include, content)

def main():
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
        
    links = extract_links(SRC_SUMMARY)
    
    processed_files = []
    
    print(f"Found {len(links)} chapters in SUMMARY.md")
    
    for link in links:
        rus_path = os.path.join(RUS_DIR, link)
        if os.path.exists(rus_path):
            with open(rus_path, 'r') as f:
                content = f.read()
            
            new_content = process_includes(content, RUS_DIR)
            
            out_path = os.path.join(BUILD_DIR, link)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
            with open(out_path, 'w') as f:
                f.write(new_content)
            
            processed_files.append(out_path)
        else:
            print(f"Skipping {rus_path} (not found)")

    # Run Pandoc
    cmd = [
        'pandoc',
        '--toc',
        '--metadata', 'title=The Rust Programming Language (RU)',
        '--metadata', 'author=Steve Klabnik, Carol Nichols, et al. (Translated by AI)',
        '--metadata', 'lang=ru',
        '--resource-path=src:rus',
        '--css=epub.css', # Apply custom CSS
        '--highlight-style=kate', # Enable Syntax Highlighting
        '-o', 'rust-book-ru.epub'
    ] + processed_files
    
    print("Running pandoc...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Pandoc Error:")
        print(result.stderr)
    else:
        print("Done! rust-book-ru.epub created.")

if __name__ == "__main__":
    main()
