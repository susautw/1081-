class IllegalOperation(Exception):
    def __init__(self):
        super().__init__("Illegal operation.")
