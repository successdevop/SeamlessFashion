class SeamlessFashionErrors(Exception):
    pass

class EmailAlreadyExistsError(SeamlessFashionErrors):
    pass

class UsernameAlreadyTakenError(SeamlessFashionErrors):
    pass

class PhoneNumberAlreadyExistsError(SeamlessFashionErrors):
    pass

class InvalidPasswordError(SeamlessFashionErrors):
    pass

class DatabaseIntegrityError(SeamlessFashionErrors):
    pass