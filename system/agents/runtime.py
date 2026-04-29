import subprocess
import tempfile
import re
import time

try:
    from ai.router import ai
except:
    class FallbackAI:
        def ask(self, prompt):
            return "print('NO_AI_CONNECTED')"
    ai = FallbackAI()


class RuntimeAgent:

    def clean(self, text):
        if not text:
            return ""
        junk = ["⚠", "offline", "error", "failed", "queued", "NO_CODE", "Traceback"]
        for j in junk:
            text = text.replace(j, "")
        return text.strip()

    def extract_code(self, text):
        if not text:
            return None

        text = self.clean(text)

        blocks = re.findall(r"```(?:python)?(.*?)```", text, re.DOTALL)
        if blocks:
            return blocks[0].strip()

        if "import " in text or "def " in text or "print(" in text:
            return text.strip()

        return None

    def run_code(self, code):
        if not code:
            return "NO_CODE"

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                path = f.name

            result = subprocess.run(
                ["python3", path],
                capture_output=True,
                text=True,
                timeout=10
            )

            return result.stdout + result.stderr

        except Exception as e:
            return "EXEC_ERROR: " + str(e)

    def ask_ai(self, task):
        prompt = "ONLY PYTHON CODE. NO TEXT. TASK:\n" + str(task)
        return ai.ask(prompt)

    def execute(self, task):

        attempts = 0
        code = None
        output = ""

        while attempts < 3:

            response = self.ask_ai(task)
            response = self.clean(response)
            code = self.extract_code(response)

            output = self.run_code(code)

            if output and "Error" not in output and "Traceback" not in output:
                return output

            fix_prompt = "FIX ONLY PYTHON CODE:\n" + str(code) + "\nERROR:\n" + str(output)
            response = ai.ask(fix_prompt)
            response = self.clean(response)
            code = self.extract_code(response)

            output = self.run_code(code)

            if output and "Error" not in output and "Traceback" not in output:
                return output

            attempts += 1
            time.sleep(0.2)

        return output or "FAILED"
