    def _clean(self, t):
        if '```python' in t:
            t = t.split('```python')[1].split('```')[0]
        elif '```' in t:
            t = t.split('```')[1].split('```')[0]
        return t.strip()
    
    def fix(self, code, err):
        prompt = f"Fix this Python code. Return ONLY fixed code.\n\nCODE:\n{code}\n\nERROR:\n{err}\n\nFIXED:"
        for i in range(5):
            if not self.gemini_failed[i]:
                self._start(f"Gemini {i+1}")
                res, _ = self._call_gemini(prompt, i)
                if res:
                    self._stop(True, f"Gemini-{i+1}")
                    self.current = f"gemini-{i+1}"
                    return self._clean(res)
                self._stop(False, f"Key {i+1} failed")
        self._start("OpenRouter")
        res, _ = self._call_or(prompt)
        if res:
            self._stop(True, "OpenRouter")
            self.current = "openrouter"
            return self._clean(res)
        if 'a + b' in code:
            return code.repla
cat > /root/run_safe_agent.sh << 'EOF'
#!/bin/sh
echo "🔧 Building Complete Agent from Safe Phases..."
echo ""

# Combine all phases into one file
cat /root/safe_agent_phase1.py > /root/final_agent.py
echo "" >> /root/final_agent.py
cat /root/safe_agent_phase2.py >> /root/final_agent.py
echo "" >> /root/final_agent.py
cat /root/safe_agent_phase3.py >> /root/final_agent.py
echo "" >> /root/final_agent.py
cat /root/safe_agent_phase4.py >> /root/final_agent.py
echo "" >> /root/final_agent.py
cat /root/safe_agent_phase5.py >> /root/final_agent.py
echo "" >> /root/final_agent.py
cat /root/safe_agent_phase6.py >> /root/final_agent.py
echo "" >> /root/final_agent.py
cat /root/safe_agent_phase7.py >> /root/final_agent.py

echo "✅ Final agent assembled: /root/final_agent.py"
echo ""

# Create broken test file
echo 'def add(a,b): return a + b' > /root/broken.py
echo "📁 Test file created: /root/broken.py (has bug: a + b)"
echo ""

# Run the agent
python3 /root/final_agent.py
