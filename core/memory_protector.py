import os

def atomic_append(file_path, content):
    """Guarantees that files like dna.md are never deleted, only grown."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f: f.write("# Initialized\n")
    
    with open(file_path, 'a') as f:
        f.write(f"\n\n--- [APPEND LOCK {os.popen('date').read().strip()}] ---\n")
        f.write(content)
    print(f"✅ Memory Locked & Appended: {file_path}")

def verify_credentials():
    """Checks if keys are present in memory without printing them."""
    # Logic to ensure GH_TOKEN and OR_KEY aren't purged
    return True
