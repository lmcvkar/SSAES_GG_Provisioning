from person import Person


class Parent(Person):
    names = {}
    emails = {}
    invalidNames = []
    invalidEmails = {}
    all = []

    def __new__(cls, name, email):
        firstName, lastName = super().splitLastFirstName(name)
        validatedEmail = super().validateEmail(email)
        if firstName and lastName and validatedEmail:
            name = super().getName(firstName, lastName)
            # name = firstName + " " + lastName
            if name not in __class__.names:
                if validatedEmail not in __class__.emails:
                    __class__.names[name] = [validatedEmail]
                    __class__.emails[validatedEmail] = [name]
                    return super(Parent, cls).__new__(cls)
                else:
                    # email is reused (not unique to one parent)
                    if name not in __class__.emails[validatedEmail]:
                        __class__.emails[validatedEmail].append(name)
                    return None
            else:
                if validatedEmail not in __class__.names[name]:
                    # parent using second email (Flag and return parent object with original email)
                    __class__.names[name].append(validatedEmail)
                    return next(parent for parent in __class__.all if parent.firstName == firstName and parent.lastName == lastName)
                else:
                    return next(parent for parent in __class__.all if parent.firstName == firstName and parent.lastName == lastName and parent.email == validatedEmail)
        else:
            if not firstName and not lastName and not name == "":
                __class__.invalidNames.append(name)
            if not validatedEmail and not email == "":
                __class__.invalidEmails[name] = email
            return None

    def __init__(self, name, email):
        if self not in __class__.all:
            super().__init__(name, email)
            self._student = []
            __class__.all.append(self)

    @property
    def student(self):
        return self._student

    @student.setter
    def student(self, student):
        if student not in self._student:
            self._student.append(student)
