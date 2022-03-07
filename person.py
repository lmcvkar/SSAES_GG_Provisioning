import re


class Person():
    all = []
    reProg = re.compile(
        r"^[a-zA-Z0-9][a-zA-Z0-9-_\.]*[a-zA-Z0-9-_]@[a-zA-Z0-9][a-zA-Z0-9-_\.]*[a-zA-Z0-9]\.[a-zA-Z]{2,3}$")

    def __init__(self, name, email=None):
        firstName, lastName = __class__.splitLastFirstName(name)
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

    @classmethod
    def splitLastFirstName(cls, name):
        if ", " in name:
            lastName, firstMiddleName = name.split(", ")
            firstName = firstMiddleName.split(" ")[0]
            return firstName, lastName
        return None, None

    @classmethod
    def getName(cls, firstName, lastName):
        if firstName and lastName:
            return firstName + " " + lastName
        else:
            return None

    @classmethod
    def validateEmail(cls, email):
        result = __class__.reProg.match(email)
        if result:
            return result.string
        else:
            return None
