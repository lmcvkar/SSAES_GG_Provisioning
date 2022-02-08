import csv
import sys
import time


class Relationship():
    def __init__(self, guardianEmail, studentEmail, relationship):
        self.guardianEmail = guardianEmail
        self.studentEmail = studentEmail
        self.relationship = relationship


class Existing(Relationship):
    all = []

    def __init__(self, guardianEmail, studentEmail, relationship):
        super().__init__(guardianEmail, studentEmail, relationship)
        __class__.all.append(self)


class Updated(Relationship):
    all = []

    def __init__(self, guardianEmail, studentEmail, relationship):
        super().__init__(guardianEmail, studentEmail, relationship)
        __class__.all.append(self)


def readUpdatedRelationshipData(fileName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Updated(row['guardian_email'],
                    row['student_email'], row['relationship'])
    csvfile.close()
    return Updated.all


def readExistingRelationshipData(fileName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Existing(row['guardian_email'],
                     row['student_email'], row['relationship'])
    csvfile.close()
    return Existing.all


def compareRelationshipData(existingFile, updatedFile):
    existingList = readExistingRelationshipData(existingFile)
    updatedList = readUpdatedRelationshipData(updatedFile)
    toBeDeleted = existingList.copy()
    toBeAdded = updatedList.copy()
    unchanged = []
    for existing in existingList:
        for updated in updatedList:
            if existing.guardianEmail == updated.guardianEmail and existing.studentEmail == updated.studentEmail:
                unchanged.append(updated)
                toBeAdded.remove(updated)
                toBeDeleted.remove(existing)
    return toBeAdded, toBeDeleted, unchanged, existingList, updatedList


def printRelationShips(list):
    for relationship in list:
        print(relationship.guardianEmail,
              relationship.studentEmail, relationship.relationship)


def countRelationships(dict):
    count = 0
    for guardianEmail in dict:
        count += len(dict[guardianEmail])
    return count


def writeDeleteRelationships(fileName, toBeRemoved):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['guardian_email', 'student_email',
                      'relationship', 'primary', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for relationship in toBeRemoved:
            writer.writerow({
                'guardian_email': relationship.guardianEmail,
                'student_email': relationship.studentEmail,
                'relationship': relationship.relationship,
                'delete': 'delete'
            })
    csvfile.close()


def writeAddRelationships(fileName, toBeAdded):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['guardian_email', 'student_email',
                      'relationship', 'primary', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for relationship in toBeAdded:
            writer.writerow({
                'guardian_email': relationship.guardianEmail,
                'student_email': relationship.studentEmail,
                'relationship': relationship.relationship
            })
    csvfile.close()


existingRelationshipsFile = sys.argv[1]
updatedRelationshipsFile = sys.argv[2]
timeStamp = time.strftime('%Y%m%d%H%M')
deleteRelationshipsFileName = "Delete_Relationships_" + timeStamp + ".csv"
addRelationshipsFileName = "Add_Relationships_" + timeStamp + ".csv"

relationshipsToBeAdded, relationshipsToBeDeleted, unchangedRelationships, existingRelationships, updatedRelationships = compareRelationshipData(
    existingRelationshipsFile, updatedRelationshipsFile)

print(f"Existing Number:\t{len(existingRelationships)}")
print(f"Updated Number:\t{len(updatedRelationships)}")
print(f"Unchanged:\t{len(unchangedRelationships)}")
print(f"To Be Removed:\t{len(relationshipsToBeDeleted)}")
print(f"To Be Added:\t{len(relationshipsToBeAdded)}")

writeDeleteRelationships(deleteRelationshipsFileName, relationshipsToBeDeleted)
writeAddRelationships(addRelationshipsFileName, relationshipsToBeAdded)
