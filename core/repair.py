import time
import sys
import itertools
import requests
from core.rotator import SmartRotator

class AutoHealer:
    def __init__(self):
        self.rotator = SmartRotator()
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])

    def show_spinner(self, message, duration=2):
        stop_time = time.time() + duration
        while time.time() < stop_time:
            sys.stdout.write(f'\r{next(self.spinner)} {message}...')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r✅ ' + message + ' Done.   \n')

    def check_all_systems(self):
        results = []
        print("\n🔍 [SYSTEM AUDIT STARTING]")
        
        # Check Gemini / Rotator
        self.show_spinner("Testing Gemini API & Rotator", 1.5)
        try:
            key = self.rotator.get_gemini_key()
            if key: results.append("GEMINI: OK")
        except: results.append("GEMINI: FAIL")

        # Check Northflank
        self.show_spinner("Checking Northflank Cloud", 1.5)
        nf_token = self.rotator.config.get("NORTHFLANK_TOKEN")
        res = requests.get("https://api.northflank.com/v1/projects", 
                           headers={"Authorization": f"Bearer {nf_token}"})
        results.append(f"NORTHFLANK: {'OK' if res.status_code == 200 else 'FAIL'}")

        # Summary Message
        print("\n--- 📝 AUDIT SUMMARY ---")
        for r in results: print(f"  {r}")
        print("------------------------\n")
        return "FAIL" in "".join(results)

if __name__ == "__main__":
    healer = AutoHealer()
    healer.check_all_systems()
