import csv
import time
import argparse
import json
import os
from parent import Parent
from student import Student


def parseStudentParentFile(fileName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            student = Student(row['LastName FirstName'], row['Grade Level'])
            if student:
                parent1 = Parent(row['LastName FirstName 1'], row['Email'])
                if parent1:
                    parent1.student = student
                    student.parent = parent1
                parent2 = Parent(
                    row['LastName FirstName MiddleName'], row['Email 1'])
                if parent2:
                    parent2.student = student
                    student.parent = parent2
    csvfile.close()


def getStudentsWithNoParents():
    nameList = []
    for student in Student.all:
        if student.parent == []:
            nameList.append(student.getName(
                student.firstName, student.lastName))
    return nameList


def getStudentsWithInvalidNames():
    return Student.invalidNames


def getStudentsWithInvalidEmails():
    return Student.invalidEmails


def getStudentsWithNoEmailAddress():
    nameList = []
    for student in Student.all:
        name = student.getName(student.firstName, student.lastName)
        if not student.email and name not in Student.namesNotFoundInEmailFile and name not in Student.invalidEmails:
            nameList.append(name)
    return nameList


def getStudentsWithNamesNotFoundInEmailFile():
    return Student.namesNotFoundInEmailFile


def getParentsWithInvalidNames():
    return Parent.invalidNames


def getParentsWithInvalidEmails():
    return Parent.invalidEmails


def getParentsSharingEmailAddress():
    emailDict = {}
    for email in Parent.emails:
        if len(Parent.emails[email]) > 1:
            emailDict[email] = Parent.emails[email]
    return emailDict


def getParentsWithMultipleEmailAddresses():
    nameDict = {}
    for name in Parent.names:
        if len(Parent.names[name]) > 1:
            nameDict[name] = Parent.names[name]
    return nameDict


def getStatistics(verbose, statOn):
    statistics = {}
    messages = {'Warning': 0, 'Error': 0, 'OK': 0}
    with open(os.path.join(os.path.dirname(__file__), "statistics.json")) as jsonfile:
        data = json.load(jsonfile)
    maxMessageLength = 0
    for stat in data:
        messageLength = len(data[stat]['message'])
        if messageLength > maxMessageLength:
            maxMessageLength = messageLength
        functionName = "get" + stat[0].capitalize() + stat[1:]
        if functionName in globals():
            function = globals()[functionName]
            statistics[stat] = data[stat]
            statistics[stat]['items'] = function()
            statistics[stat]['count'] = len(statistics[stat]['items'])
    for stat in statistics:
        status = 'OK'
        if statistics[stat]['count'] > 0:
            status = statistics[stat]['severity']
        messages[status] = messages[status] + 1
        if statOn:
            print(
                f"{statistics[stat]['message']:{maxMessageLength}} {statistics[stat]['count']:9} [{status.center(7)}]")
            if verbose:
                print(statistics[stat]['verbose'])
            if not status == "OK":
                for item in statistics[stat]['items']:
                    if type(statistics[stat]['items']) is dict:
                        print(item, statistics[stat]['items'][item])
                    else:
                        print(item)
                if verbose:
                    print(statistics[stat]['suggestion'])
    return messages


def printParentList():
    for parent in Parent.all:
        firstName = parent.firstName
        lastName = parent.lastName
        email = parent.email
        students = {}
        for student in parent.student:
            if student.email:
                studentName = student.getName(
                    student.firstName, student.lastName)
                students[studentName] = student.email
        print(
            f"Parent: {firstName} {lastName}, {email},\tStudents: {students}")


def printStudentList():
    for student in Student.all:
        firstName = student.firstName
        lastName = student.lastName
        email = student.email
        parents = []
        for parent in student.parent:
            parents.append(parent.getName(parent.firstName, parent.lastName))
        if email and not parents == []:
            print(
                f"Student: {firstName} {lastName}, {email},\tParents: {', '.join(parents)}")


def writeAddParents(fileName):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['name', 'email', 'phone', 'parent_app', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for parent in Parent.all:
            parentName = parent.getName(parent.firstName, parent.lastName)
            email = parent.email
            if parentName and email:
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
                if student.email:
                    writer.writerow({'guardian_email': parent.email,
                                     'student_email': student.email, 'relationship': 'parent'})
    csvfile.close()


def generateOutputFiles(messages, verbose):
    numWarnings = messages['Warning']
    numErrors = messages['Error']
    if numWarnings > 0 or numErrors > 0:
        print(
            f"There are {numErrors} errors and {numWarnings} warnings for the input files.")
        print("Files generated in these conditions will be incomplete.")
        answer = input("Would you like to procede anyway? [y/N]: ")
        if answer not in ("Yes", "yes", "Y", "y", "YES"):
            print("Exiting: Files will not be generated.")
            return
    timeStamp = time.strftime('%Y%m%d%H%M')
    addParentsFile = 'Parents_Complete_' + timeStamp + '.csv'
    addRelationshipsFile = 'Relationships_Complete_' + timeStamp + '.csv'
    if verbose:
        print("Generating Parent File: {addParentsFile}")
    writeAddParents(addParentsFile)
    if verbose:
        print("Generating Relationship File: {addRelationshipsFile}")
    writeAddRelationships(addRelationshipsFile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse Parent and Student csv files, check for inconsistencies and optionally generate GoGuardian Parent provisioning csv files.")
    parser.add_argument(
        "parent_file", help="CSV file containing student name and parent names and parent email addresses associated to the student.")
    parser.add_argument(
        "student_file", help="CSV file containing student name, email address and grade.")
    parser.add_argument("-S", "--no_statistics", action="store_false",
                        help="do not print statistics related to the sanity of the input files. Default is to print statistics")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="provide details about statistics and file generation")
    parser.add_argument("-p", "--print_parents", action="store_true",
                        help="print list of parents with emails and names of related students")
    parser.add_argument("-s", "--print_students", action="store_true",
                        help="print list of students with emails and names of related parents")
    parser.add_argument("-g", "--generate_files", action="store_true",
                        help="generate complete Parent and Relationship files based on input files")
    args = parser.parse_args()

    studentParentFile = args.parent_file
    studentEmailFile = args.student_file
    verbose = args.verbose
    statistics = args.no_statistics
    Student.emailFile = studentEmailFile
    parseStudentParentFile(studentParentFile)
    messages = getStatistics(verbose, statistics)
    if args.print_parents:
        printParentList()
    if args.print_students:
        printStudentList()
    if args.generate_files:
        generateOutputFiles(messages, verbose)
