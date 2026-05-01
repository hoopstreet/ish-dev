
# ============ GEMINI CLI STYLE INTERFACE ============
def gemini_style_mode():
    """Run in Gemini CLI style + single command mode"""
    if len(sys.argv) > 1:
        # Single command mode like 'gemini "question"'
        prompt = ' '.join(sys.argv[1:])
        print(f"\n🤖 Processing: {prompt}")
        print("━" * 60)
        response = ai_complete(prompt, [])
        print(f"\n{response}\n")
        return True
    return False

# Check for command-line arguments
if __name__ == "__main__" and len(sys.argv) > 1:
    if gemini_style_mode():
        sys.exit(0)
