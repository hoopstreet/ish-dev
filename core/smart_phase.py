#!/usr/bin/env python3
import sys, re, time, os
from pathlib import Path

class PhaseExecutor:
    def __init__(self):
        self.phases = []
        self.current_phase = 0
        self.log_file = Path("/root/phase_log.txt")
    
    def detect_phases(self, code_block):
        """Auto-detect phase boundaries in code"""
        phases = []
        
        # Method 1: Look for Phase X markers
        phase_pattern = r'#{2,}\s*Phase\s*(\d+)[:\s]*'
        matches = list(re.finditer(phase_pattern, code_block, re.IGNORECASE))
        
        if matches:
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i+1].start() if i+1 < len(matches) else len(code_block)
                phases.append({
                    'num': int(match.group(1)),
                    'code': code_block[start:end].strip(),
                    'type': 'marked'
                })
        else:
            # Method 2: Split by EOF markers or large empty lines
            parts = re.split(r'\n(?:EOF|END|---)\n', code_block)
            if len(parts) > 1:
                for i, part in enumerate(parts):
                    if part.strip():
                        phases.append({
                            'num': i+1,
                            'code': part.strip(),
                            'type': 'separator'
                        })
            else:
                # Method 3: Split by class/function definitions (heuristic)
                lines = code_block.split('\n')
                current = []
                phase_num = 1
                for line in lines:
                    current.append(line)
                    if len(current) > 30 or (line.strip().startswith('class ') and len(current) > 5):
                        if current:
                            phases.append({
                                'num': phase_num,
                                'code': '\n'.join(current),
                                'type': 'auto'
                            })
                            current = []
                            phase_num += 1
                if current:
                    phases.append({
                        'num': phase_num,
                        'code': '\n'.join(current),
                        'type': 'auto'
                    })
        
        return phases
    
    def execute_phase(self, phase, phase_num, total):
        """Execute a single phase safely"""
        print(f"\n{'='*50}")
        print(f"📦 EXECUTING PHASE {phase_num}/{total}")
        print(f"📋 Type: {phase['type']}")
        print(f"📏 Size: {len(phase['code'])} chars")
        print(f"{'='*50}")
        
        # Save phase to temp file
        temp_file = Path(f"/root/phase_{phase_num}.py")
        temp_file.write_text(phase['code'])
        
        # Execute the phase
        try:
            result = os.system(f"python3 {temp_file} 2>&1")
            if result == 0:
                print(f"✅ Phase {phase_num} executed successfully")
                self._log(f"Phase {phase_num}: SUCCESS", phase['type'])
                return True
            else:
                print(f"❌ Phase {phase_num} failed with exit code {result}")
                self._log(f"Phase {phase_num}: FAILED (code {result})", phase['type'])
                return False
        except Exception as e:
            print(f"❌ Phase {phase_num} error: {e}")
            self._log(f"Phase {phase_num}: ERROR - {e}", phase['type'])
            return False
        finally:
            # Cleanup temp file
            if temp_file.exists():
                os.remove(temp_file)
    
    def _log(self, message, phase_type):
        with open(self.log_file, 'a') as f:
            from datetime import datetime
            f.write(f"{datetime.now().isoformat()} | {message} | Type: {phase_type}\n")
    
    def run_full_code(self, code_block, auto_confirm=True):
        """Main entry point - automatically splits and runs code"""
        print("\n" + "🔍"*25)
        print
cat > /root/auto_phase.sh << 'EOF'
#!/bin/sh
echo "╔════════════════════════════════════════════╗"
echo "║    🧠 AUTO PHASE DETECTOR FOR iSH         ║"
echo "║   Handles large code blocks automatically ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check if file argument provided
if [ -n "$1" ] && [ -f "$1" ]; then
    echo "📁 Reading from file: $1"
    python3 /root/smart_phase.py < "$1"
else
    echo "📝 Paste your code (type 'END' when finished):"
    echo ""
    python3 /root/smart_phase.py
fi
