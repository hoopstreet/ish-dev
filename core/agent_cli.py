import subprocess, sys, os
def run_task(cmd):
    print('Starting Build...')
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return (p.returncode == 0, p.stdout if p.returncode == 0 else p.stderr)
if __name__ == '__main__':
    env_path = '/root/Ai-Coder/.env'
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write('TELEGRAM_TOKEN="8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"\n')
    if len(sys.argv) > 1:
        res, out = run_task(sys.argv[1])
        if res: print('\n[SUCCESS] System Stable.')
        else: print('\n[ERROR] ' + out[:50])
