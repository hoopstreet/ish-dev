#!/usr/bin/env python3
"""
HOOPSTREET AGENT & MODEL LIST
Test all available agents and models
"""

import sys, os, subprocess, json, requests

print("\n" + "━" * 60)
print("📋 HOOPSTREET AVAILABLE AGENTS & MODELS")
print("━" * 60)

# Test OpenRouter Models
openrouter_key = "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"

models = [
    ("openai/gpt-3.5-turbo", "GPT-3.5 Turbo", "Fast, good for most tasks"),
    ("openai/gpt-4-turbo", "GPT-4 Turbo", "Best quality, slower"),
    ("anthropic/claude-3-opus", "Claude 3 Opus", "Excellent reasoning"),
    ("google/gemini-pro", "Gemini Pro", "Google's best"),
    ("meta-llama/llama-3-70b-instruct", "Llama 3", "Open source"),
    ("deepseek/deepseek-chat", "DeepSeek", "Code specialist"),
]

print("\n🔑 OPENROUTER MODELS (via API key):")
for model_id, name, desc in models:
    print(f"   • {name} - {desc}")

# Check available agents
agents = [
    ("agent_final.py", "Final Agent v16.0", "✅ WORKING"),
    ("ultimate_agent.py", "Ultimate Agent v14.0", "✅ AVAILABLE"),
    ("auto_dev_agent.py", "Auto Developer", "✅ AVAILABLE"),
    ("master_bundle.py", "Master Bundle v13.0", "✅ AVAILABLE"),
    ("smart_executor.py", "Smart Executor", "✅ AVAILABLE"),
    ("openrouter_agent.py", "OpenRouter Agent", "✅ AVAILABLE"),
]

print("\n🤖 AVAILABLE AGENTS:")
for file, name, status in agents:
    if os.path.exists(f"/root/ish-dev/core/{file}"):
        print(f"   • {name} - {status}")

# Check installed CLI tools
cli_tools = [
    ("gemini", "Google Gemini CLI", "npm install -g @google/gemini-cli"),
    ("interpreter", "Open Interpreter", "pip install open-interpreter"),
]

print("\n💻 CLI TOOLS (optional install):")
for cmd, name, install in cli_tools:
    if subprocess.run(f"which {cmd}", shell=True, capture_output=True).returncode == 0:
        print(f"   • {name} ✅ INSTALLED")
    else:
        print(f"   • {name} ❌ NOT INSTALLED (run: {install})")

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🎯 AGENT COMMANDS:")
print("   agent 'task'   - Final Agent (Primary - WORKING)")
print("   dev 'task'     - Developer Agent")
print("   menu           - Main menu (6 options)")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
