#!/usr/bin/env python3
import json, subprocess, re
from pathlib import Path

class HoopstreetAI:
    def __init__(self):
        self.dna_path = "/root/ish-dev/docs/DNA.md"
        self.log_path = "/root/ish-dev/docs/logs.txt"
    
    def analyze_error(self, error_msg):
        """Analyze error and suggest fix"""
        errors = {
            "No such file": "Check file path, use ls to verify",
            "permission denied": "Run chmod +x on the file",
            "command not found": "Install missing package or check PATH",
            "syntax error": "Check bash/python syntax",
            "indentation": "Fix indentation (use 4 spaces)"
        }
        
        for key, suggestion in errors.items():
            if key in error_msg:
                return suggestion
        return "Check error message and retry"
    
    def suggest_improvements(self):
        """Suggest system improvements based on logs"""
        # Read recent logs
        with open(self.log_path, 'r') as f:
            logs = f.readlines()[-50:]
        
        suggestions = []
        error_count = sum(1 for line in logs if 'FAILED' in line)
        
        if error_count > 10:
            suggestions.append("High error rate detected + run option 3 (Heal)")
        
        return suggestions

if __name__ == "__main__":
    ai = HoopstreetAI()
    print("🤖 AI Assistant ready")
    print("Commands: analyze <error> | suggest")
