class Counter:
    def __init__(self):
        self.count = 0

    def get_current_count(self):
        self.count += 1
        return self.count

    def reset(self):
        self.count = 0
