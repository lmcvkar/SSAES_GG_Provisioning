from person import Person


class Student(Person):
    names = []
    all = []
    missingEmail = []

    def __new__(cls, firstName, lastName, grade):
        name = firstName + " " + lastName
        if name not in __class__.names:
            return super(Student, cls).__new__(cls)
        else:
            return next(student for student in __class__.all if student.firstName == firstName and student.lastName == lastName and student.grade == grade)

    def __init__(self, firstName, lastName, grade):
        if self not in __class__.all:
            super().__init__(firstName, lastName)
            self._grade = grade
            self._parent = []
            name = firstName + " " + lastName
            __class__.names.append(name)
            __class__.all.append(self)

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        self._grade = grade

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent not in self._parent:
            self._parent.append(parent)
