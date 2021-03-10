class InputError(Exception):
    """Exception raised when input format is inadequate."""
    def __init__(self, message):
        self.message = message
        
class ExistingUserException(Exception):
    """Exception raised applied when user already exists."""
    def __init__(self, message):
        self.message = message