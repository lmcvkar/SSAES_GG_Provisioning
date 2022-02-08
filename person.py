class Person():
    all = []

    def __init__(self, firstName, lastName, email=None):
        self.firstName = firstName
        self.lastName = lastName
        self._email = email
        __class__.all.append(self)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email
