import csv
import sys
import time


class Guardian():
    all = {}
    # names = []
    # emails = []

    def __init__(self, name, email, appStatus):
        self.name = name
        self.email = email
        self.appStatus = appStatus
        if email not in __class__.all:
            __class__.all[email] = self
            # __class__.names.append(name)
            # __class__.emails.append(email)


def readUpdatedParentData(fileName):
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Guardian(row['name'], row['email'], row['parent_app'])
    csvfile.close()
    return len(Guardian.all)


def readExistingParentData(fileName):
    unchanged = []
    changed = []
    toBeDeleted = []
    toBeAdded = []
    existingNumber = 0
    guardians = Guardian.all.copy()
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existingNumber += 1
            email = row['email']
            if email in guardians:
                if guardians[email].name == row['name'] and guardians[email].appStatus == row['parent_app']:
                    unchanged.append(guardians.pop(email))
                else:
                    toBeDeleted.append(
                        Guardian(row['name'], row['email'], row['parent_app']))
                    changed.append(toBeDeleted[-1])
            else:
                toBeDeleted.append(
                    Guardian(row['name'], row['email'], row['parent_app']))
        toBeAdded += list(guardians.values())
    csvfile.close()
    return existingNumber, unchanged, changed, toBeAdded, toBeDeleted


def writeDeleteParents(fileName, toBeRemoved):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['name', 'email', 'phone', 'parent_app', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for parent in toBeRemoved:
            writer.writerow(
                {'name': parent.name, 'email': parent.email, 'delete': 'delete'})
    csvfile.close()


def writeAddParents(fileName, toBeAdded):
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['name', 'email', 'phone', 'parent_app', 'delete']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for parent in toBeAdded:
            writer.writerow(
                {'name': parent.name, 'email': parent.email, 'parent_app': 'enabled'})
    csvfile.close()


existingParentsFile = sys.argv[1]
updatedParentsFile = sys.argv[2]
timeStamp = time.strftime('%Y%m%d%H%M')
deleteParentsFileName = "Delete_Parents_" + timeStamp + ".csv"
addParentsFileName = "Add_Parents_" + timeStamp + ".csv"

updatedNumberOfParents = readUpdatedParentData(updatedParentsFile)
existingNumberOfParents, unchangedParents, changedParents, parentsToBeAdded, parentsToBeDeleted = readExistingParentData(
    existingParentsFile)

print(f"Existing Number:\t{existingNumberOfParents}")
print(f"Updated Number:\t{updatedNumberOfParents}")
print(f"Unchanged:\t{len(unchangedParents)}")
print(f"Changed:\t{len(changedParents)}")
print(f"To Be Removed:\t{len(parentsToBeDeleted)}")
print(f"To Be Added:\t{len(parentsToBeAdded)}")

writeDeleteParents(deleteParentsFileName, parentsToBeDeleted)
writeAddParents(addParentsFileName, parentsToBeAdded)
