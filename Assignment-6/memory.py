from models import UserPreference

class MemoryStore:
    def __init__(self):
        self.user_preference: UserPreference | None = None

    def store_preference(self, preference: UserPreference):
        self.user_preference = preference

    def get_preference(self) -> UserPreference | None:
        return self.user_preference