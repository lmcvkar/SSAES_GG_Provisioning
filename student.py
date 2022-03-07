import csv
import re
from person import Person


class Student(Person):
    names = []
    all = []
    invalidNames = []
    invalidEmails = {}
    emailFile = None
    namesNotFoundInEmailFile = []

    def __new__(cls, name, grade):
        firstName, lastName = super().splitLastFirstName(name)
        if firstName and lastName:
            name = super().getName(firstName, lastName)
            if name not in __class__.names:
                __class__.names.append(name)
                return super(Student, cls).__new__(cls)
            else:
                return next(student for student in __class__.all if student.firstName == firstName and student.lastName == lastName and student.grade == grade)
        else:
            __class__.invalidNames.append(name)

    def __init__(self, name, grade):
        if self not in __class__.all:
            super().__init__(name)
            self._grade = grade
            self._parent = []
            __class__.all.append(self)
            if __class__.emailFile:
                self.getEmailFromFile()

    def getEmailFromFile(self):
        with open(__class__.emailFile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            name = super().getName(self.firstName, self.lastName)
            nameFound = False
            # while not self.email:
            for row in reader:
                # row = next(reader)
                if re.search(self.firstName, row['First Name [Required]']) and re.search(self.lastName, row['Last Name [Required]']) and row['Status [READ ONLY]'] == 'Active':
                    nameFound = True
                    email = super().validateEmail(
                        row['Email Address [Required]'])
                    if email:
                        self.email = email
                    else:
                        __class__.invalidEmails[name] = row['Email Address [Required]']
            if not nameFound:
                __class__.namesNotFoundInEmailFile.append(name)

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
