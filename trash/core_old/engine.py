import subprocess
from ai.router import ask
from ai.classifier import classify

def run(code):
    path="/tmp/v15.sh"
    open(path,"w").write(code)

    p=subprocess.run(["sh",path],capture_output=True,text=True)
    return p.returncode,p.stderr

def fix(code,err):
    t=classify(err)

    prompt=f"""
You are V15 Autonomous Dev AI.

Error Type: {t}

ERROR:
{err}

CODE:
{code}

Return ONLY corrected shell script.
"""
    return ask(prompt)

def main():
    print("💎 V15 SELF-WRITING AI OS")

    lines=[]
    while True:
        l=input()
        if l=="END":
            break
        lines.append(l)

    code="\n".join(lines)

    for i in range(7):
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
