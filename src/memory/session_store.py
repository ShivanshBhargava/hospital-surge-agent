class SessionStore:
    """
    Lightweight session memory for storing state during one orchestration cycle.
    """
    def __init__(self):
        self.state = {}

    def set(self, key: str, value):
        self.state[key] = value

    def get(self, key: str, default=None):
        return self.state.get(key, default)

    def clear(self):
        self.state = {}