    def _spin(self, msg):
        chars = ['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷']
        i = 0
        while self.spin:
            sys.stdout.write(f'\r{chars[i%8]} {msg}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def _start(self, msg):
        self.spin = True
        threading.Thread(target=self._spin, args=(msg,), daemon=True).start()
    
    def _stop(self, ok=True, msg=""):
        self.spin = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' '*50 + '\r')
        print(f"{'✅' if ok else '❌'} {msg}")
    print("✅ Phase 3: Spinner methods added")
