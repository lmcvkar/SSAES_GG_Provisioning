from person import Person


class Parent(Person):
    names = []
    emails = []
    all = []

    def __new__(cls, firstName, lastName, email):
        name = firstName + " " + lastName
        if name not in __class__.names and email not in __class__.emails:
            return super(Parent, cls).__new__(cls)
        else:
            return next(parent for parent in __class__.all if parent.firstName == firstName and parent.lastName == lastName and parent.email == email)

    def __init__(self, firstName, lastName, email):
        if self not in __class__.all:
            super().__init__(firstName, lastName, email)
            self._student = []
            name = firstName + " " + lastName
            __class__.names.append(name)
            __class__.emails.append(email)
            __class__.all.append(self)
        # else cases for gathering statistics about input data:
        # if name does not exist but email does: flag as shared email address
        # if name exists but email does not: flag as 2 emails for 1 user

    @property
    def student(self):
        return self._student

    @student.setter
    def student(self, student):
        if student not in self._student:
            self._student.append(student)
