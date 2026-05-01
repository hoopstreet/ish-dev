import re
import os
from datetime import datetime

DNA_PATH = "/root/Ai-Coder/DNA.md"
ROADMAP_PATH = "/root/Ai-Coder/ROADMAP.md"

def bump_version():
    with open(DNA_PATH, 'r') as f:
        content = f.read()
    
    # Find current version
    match = re.search(r'\[v(\d+)\.(\d+)\.(\d+)\]', content)
    if match:
        major, minor, patch = map(int, match.groups())
        new_version = f"v{major}.{minor}.{patch + 1}"
        
        # Update DNA.md
        new_entry = f"## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}\n- **Auto-Update**: Roadmap and DNA synchronized.\n"
        updated_dna = re.sub(r'(# 🧬 DNA\.md — SYSTEM EVOLUTIONARY LOG\n\n)', r'\1' + new_entry, content)
        
        with open(DNA_PATH, 'w') as f:
            f.write(updated_dna)
            
        # Update ROADMAP.md header
        with open(ROADMAP_PATH, 'r') as f:
            roadmap = f.read()
        updated_roadmap = re.sub(r'\(v\d+\.\d+\.\d+\)', f"({new_version})", roadmap)
        with open(ROADMAP_PATH, 'w') as f:
            f.write(updated_roadmap)
            
        print(f"🚀 Version bumped to {new_version} across system.")
        return new_version
    return None

if __name__ == "__main__":
    bump_version()
