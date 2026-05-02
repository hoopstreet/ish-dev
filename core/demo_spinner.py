import sys, time, threading
from itertools import cycle

def show_spinner():
    spinner = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    for _ in range(30):
        sys.stdout.write(f'\r{next(spinner)} Working... ')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r✅ Done!     \n')

print("🎨 Visual Spinner Demo:")
print("-" * 30)
show_spinner()
print("\n✨ Spinner animation complete!")
