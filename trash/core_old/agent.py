import subprocess
from ai.router import ask
from ai.error_classifier import classify

def run(code):
    tmp="/tmp/v13.sh"
    open(tmp,"w").write(code)

    p = subprocess.run(["sh",tmp],capture_output=True,text=True)
    return p.returncode,p.stderr

def fix(code,error):
    err_type = classify(error)

    prompt = f"""
Fix this shell script.

Error type: {err_type}
Error:
{error}

Code:
{code}

Return ONLY fixed script.
"""
    return ask(prompt)

def main():
    print("💎 HOOPSTREET V13 AUTONOMOUS SYSTEM")

    lines=[]
    while True:
        l=input()
        if l=="END":
            break
        lines.append(l)

    code="\n".join(lines)

    for i in range(5):
        rc,err=run(code)

        if rc==0:
            print("✅ SUCCESS")
            return

        print("❌ ERROR:\n",err)

        new=fix(code,err)

        if not new:
            print("AI FAILED")
            return

        code=new

if __name__=="__main__":
    main()
