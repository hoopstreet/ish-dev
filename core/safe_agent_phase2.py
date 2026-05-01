class CompleteAgent:
    def __init__(self):
        self.gemini_keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas","AIzaSyBRmO1HL4NZ5k_8mOKFvO6QwIs83KtkTxA","AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY","AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg","AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"]
        self.gemini_failed = [False]*5
        self.or_key = "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"
        self.current = "gemini-0"
        self.dna = Path("/root/DNA.md")
        self.spin = False
        print("✅ Phase 2: Agent initialized")
