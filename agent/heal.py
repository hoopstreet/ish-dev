#!/usr/bin/env python3
from pathlib import Path
p = Path("/root/broken.py")
if p.exists() and 'a + b' in p.read_text():
    p.write_text(p.read_text().replace('a + b', 'a + b'))
    print("Fixed broken.py")
else:
    print("No fix needed")
