import csv
import re
import sys
import time
import argparse
from parent import Parent
from student import Student


def splitLastFirstName(name):
    lastName, firstMiddleName = name.split(", ")
    firstName = firstMiddleName.split(" ")[0]
    return lastName, firstName


def parseStudentParentFile(fileName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lastName, firstName = splitLastFirstName(row['LastName FirstName'])
            student = Student(firstName, lastName, row['Grade Level'])
            lastName, firstName = splitLastFirstName(
                row['LastName FirstName 1'])
            parent = Parent(firstName, lastName, row['Email'])
            parent.student = student
            student.parent = parent
            if row['Email 1'] != row['Email'] and row['Email 1'] != "":
                lastName, firstName = splitLastFirstName(
                    row['LastName FirstName MiddleName'])
                parent = Parent(firstName, lastName, row['Email 1'])
                parent.student = student
                student.parent = parent
    csvfile.close()


def parseStudentEmailFile(fileName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for student in Student.all:
            csvfile.seek(0)
            for row in reader:
                if re.search(student.firstName, row['First Name [Required]']) and re.search(student.lastName, row['Last Name [Required]']) and row['Status [READ ONLY]'] == 'Active':
                    student.email = row['Email Address [Required]']
            if not student.email or student.email == "":
                Student.missingEmail.append(student)
    csvfile.close()


def printParentList():
    for parent in Parent.all:
        firstName = parent.firstName
        lastName = parent.lastName
        email = parent.email
        students = []
        for student in parent.student:
            students.append(student.firstName + " " + student.lastName)
        print(
            f"Parent: {firstName} {lastName}, {email},\tStudents: {', '.join(students)}")


def printStudentList():
    for student in Student.all:
        firstName = student.firstName
        lastName = student.lastName
        email = student.email
        parents = []
        for parent in student.parent:
            parents.append(parent.firstName + " " + parent.lastName)
        print(
            f"Student: {firstName} {lastName}, {email},\tParents: {', '.join(parents)}")


def writeAddParents(fileName):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['name', 'email', 'phone', 'parent_app', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for parent in Parent.all:
            parentName = parent.firstName + " " + parent.lastName
            email = parent.email
            writer.writerow(
                {'name': parentName, 'email': email, 'parent_app': 'enabled'})
    csvfile.close()


def writeAddRelationships(fileName):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['guardian_email', 'student_email',
                      'relationship', 'primary', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for parent in Parent.all:
            for student in parent.student:
                writer.writerow({'guardian_email': parent.email,
                                 'student_email': student.email, 'relationship': 'parent'})
    csvfile.close()


def generateOutputFiles():
    timeStamp = time.strftime('%Y%m%d%H%M')
    addParentsFile = 'Parents_Complete_' + timeStamp + '.csv'
    addRelationsipsFile = 'Relationships_Complete_' + timeStamp + '.csv'
    writeAddParents(addParentsFile)
    writeAddRelationships(addRelationsipsFile)


parser = argparse.ArgumentParser(
    description="Parse Parent and Student csv files, check for inconsistencies and optionally generate GoGuardian Parent provisioning csv files.")
parser.add_argument(
    "parent_file", help="CSV file containing student name and parent names and parent email addresses associated to the student.")
parser.add_argument(
    "student_file", help="CSV file containing student name, email address and grade.")
parser.add_argument("--print_parents", action="store_true",
                    help="print list of parents with emails and names of related students")
parser.add_argument("--print_students", action="store_true",
                    help="print list of students with emails and names of related parentss")
parser.add_argument("--generate-files", action="store_true",
                    help="generate complete Parent and Relationship files based on input files")
args = parser.parse_args()

studentParentFile = args.parent_file
studentEmailFile = args.student_file
parseStudentParentFile(studentParentFile)
parseStudentEmailFile(studentEmailFile)
if args.print_parents:
    printParentList()
if args.print_students:
    printStudentList()
if args.generate_files:
    generateOutputFiles()
