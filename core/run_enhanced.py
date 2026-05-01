#!/usr/bin/env python3
#!/usr/bin/env python3
import sys, re, os, time, threading
from pathlib import Path
from datetime import datetime

class PhaseRunner:
    def __init__(self):
        self.phases = []
        self.results = []
        self.spinner_running = False
        self.fixed_phases = []
        self.failed_phases = []
        
    def spinner(self, message, phase_num):
        chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        i = 0
        while self.spinner_running:
            sys.stdout.write(f'\r{chars[i%8]} Phase {phase_num}: {message}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def start_spinner(self, message, phase_num):
        self.spinner_running = True
        t = threading.Thread(target=self.spinner, args=(message, phase_num))
        t.daemon = True
        t.start()
    
    def stop_spinner(self, success=True, result=""):
        self.spinner_running = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' ' * 60 + '\r')
        if success:
            print(f"✅ {result}")
        else:
            print(f"❌ {result}")
    
    def read_code(self):
        print("📝 Paste your multi-phase code (type END on new line):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            except:
                break
        return "\n".join(lines)
    
    def detect_phases(self, code):
        phases = []
        current = []
        num = None
        for line in code.split('\n'):
            m = re.match(r'^\s*#\s*phase\s*(\d+)', line, re.I)
            if m:
                if current and num:
                    phases.append((num, '\n'.join(current)))
                num = int(m.group(1))
                current = [line]
            else:
                current.append(line)
        if current and num:
            phases.append((num, '\n'.join(current)))
        return phases if phases else [(1, code)]
    
    def run_phase_with_retry(self, num, code, max_retries=3):
        for attempt in range(1, max_retries + 1):
            self.start_spinner(f"Executing (attempt {attempt})", num)
            tmp = Path(f"/tmp/p{num}.sh")
            tmp.write_text(code)
            
            try:
                result = os.system(f"sh {tmp} 2>&1")
                tmp.unlink()
                
                if result == 0:
                    self.stop_spinner(True, f"Phase {num} completed (attempt {attempt})")
                    self.results.append((num, "SUCCESS", attempt))
                    return True
                else:
                    self.stop_spinner(False, f"Phase {num} failed (attempt {attempt})")
                    if attempt < max_retries:
                        print(f"   🔄 Auto-retrying Phase {num}...")
                        time.sleep(1)
                    else:
                        print(f"   💀 Phase {num} failed after {max_retries} attempts")
                        self.results.append((num, "FAILED", attempt))
                        return False
            except Exception as e:
                self.stop_spinner(False, f"Error: {e}")
                if attempt < max_retries:
                    print(f"   🔄 Retrying...")
                    time.sleep(1)
                else:
                    self.results.append((num, "ERROR", attempt))
                    return False
        return False
    
    def show_summary(self):
        print("\n" + "="*60)
        print("📊 EXECUTION SUMMARY")
        print("="*60)
        
        success_count = sum(1 for r in self.results if r[1] == "SUCCESS")
        fail_count = sum(1 for r in self.results if r[1] != "SUCCESS")
        
        print(f"\n✅ Successful phases: {success_count}")
        print(f"❌ Failed phases: {fail_count}")
        print(f"📋 Total phases: {len(self.results)}")
        
        if fail_count > 0:
            print("\n⚠️ FAILED PHASES:")
            for num, status, attempts in self.results:
                if status != "SUCCESS":
                    print(f"   Phase {num}: {status} after {attempts} attempts")
        
        print("\n📝 DNA LOG ENTRY:")
        print("-" * 40)
        timestamp = datetime.now().isoformat()
        print(f"Timestamp: {timestamp}")
        print(f"Total phases: {len(self.results)}")
        print(f"Success rate: {success_count}/{len(self.results)}")
        
        with open("/root/DNA.md", "a") as f:
            f.write(f"\n## Phase Execution - {timestamp}\n")
            f.write(f"Total: {len(self.results)} | Success: {success_count} | Failed: {fail_count}\n")
            for num, status, attempts in self.results:
                f.write(f"  Phase {num}: {status} (attempts: {attempts})\n")
            f.write("-" * 40 + "\n")
        
        print("\n✅ Summary saved to /root/DNA.md")
        print("="*60)
    
    def run(self):
        code = self.read_code()
        if not code.strip():
            print("❌ No code provided")
            return
        
        self.phases = self.detect_phases(code)
        print(f"\n📊 Detected {len(self.phases)} phase(s)")
        
        for num, phase_code in self.phases:
            print(f"\n{'='*40}")
            print(f"🎯 PHASE {num}/{len(self.phases)}")
            print(f"{'='*40}")
            
            success = self.run_phase_with_retry(num, phase_code)
            if not success:
                print(f"\n⚠️ Moving to next phase despite Phase {num} failure...")
            time.sleep(0.5)
        
        self.show_summary()
        print("\n🎉 ALL PHASES PROCESSED!")

if __name__ == "__main__":
    runner = PhaseRunner()
    runner.run()
