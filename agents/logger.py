from datetime import datetime

def log_event(event):
    with open("/root/ish-dev/logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] {event}\n")

def update_dna(event):
    with open("/root/ish-dev/DNA.md", "a") as f:
        f.write(f"\n[{datetime.now()}] {event}\n")

def update_roadmap(event):
    with open("/root/ish-dev/ROADMAP.md", "a") as f:
        f.write(f"\n- {event}\n")
