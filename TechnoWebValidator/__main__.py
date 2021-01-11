
import os
import zipfile
import shutil
import sys
import time
import json
import urllib.parse
import subprocess
from colorama import init, Fore, Back, Style
init()


# fill this array with specific student names or let it blank to take all students
students = [
# 'Maxime GIERLOWSKI', # GROUPE 3
# 'Lucas GISCOS',
# 'Julien GOARRE',
# 'Clément GORSKI',
# 'Lucas GOSALVES',
# 'Killian GUIGUEN',
# 'Pacôme HARISBOURE',
# 'Robin HILLIET',
# 'Xavier IRAZOQUI',
# 'Awad ISSILAME',
# 'Quentin JARDONNET',
# 'Jimmy JOURDE',
# 'Samia KHACHANI',
# 'Clementine KIFFER',
# 'Camille LABAZUY',
# 'Mathis LAGNY',
# 'Victor LAMBERT',
# 'Clément LE FOL',
# 'Hugo LE MOAL',
# 'Kylian LECHERE',
# 'Gao LIU',
# 'Paul LUGNIER',
# 'Min LUO',
# 'Van Quang LUU',
# 'Jordan LYKASO',
# 'Anne-Gaëlle MADEC',
# 'Yang WANG',
# 'Firas ZAAROURI',
#  # GROUPE 4
# 'Laila ADDICHE',
# 'Romaric ALLEAUME',
# 'El Mehdi CHEIKH',
# 'Mounir DAOUDI',
# 'Anouar ELALAOUI',
# 'Salah Eddine ELASSIL',
# 'Alexis ESPINOUX',
# 'Maryam ESSABANNE',
# 'Timothé ETIQUE',
# 'Thibaut FAVIER',
# 'Lucas FERNANDEZ',
# 'Ugo FIGHIERA',
# 'Romain GABALDON',
# 'Pierre GAUDEAU',
# 'Victor GAUDIN',
# 'Timothée GAUDRAY',
# 'Mohammed HARTI',
# 'Romain MAIGRON',
# 'Roland-Emmanuel MAMBOUNDOU',
# 'Maxime MARCHANTE',
# 'Damien MARTINEZ',
# 'Ziheng WANG',
# 'Jie ZHAO',
# 'Liangwei ZHAO'
]

html_validator_url = 'https://validator.w3.org/nu/?out=json'
css_validator_url = 'https://validator.w3.org/nu/?out=json'
delayBetweenRequest = 2 #s

def validate(archiveName):
    currDir = os.path.split(archiveName)[0]
    folderName = 'assignments'
    pathToFolder = os.path.join(currDir, folderName)

    # create empty result file
    resultFileName = 'results.log'
    pathToResultFileName =  os.path.join(currDir, resultFileName)
    f = open(pathToResultFileName, "w+")
    f.write("")
    f.close()

    def verbose(msg=""):
        print(msg)
        f = open(pathToResultFileName, "a+")
        f.write(" %s \n" % msg)
        f.close()

    def info(msg = "", topic = " INFO "):
        print("%s%s%s%s %s" % (Back.WHITE, Fore.BLACK, topic, Style.RESET_ALL, msg))
        f = open(pathToResultFileName, "a+")
        f.write("%s %s \n" % (topic, msg))
        f.close()

    def warn(msg = "", topic = " WARNING "):
        print("%s%s%s%s %s" % (Back.YELLOW, Fore.BLACK, topic, Style.RESET_ALL, msg))
        f = open(pathToResultFileName, "a+")
        f.write("%s %s \n" % (topic, msg))
        f.close()

    def ok(msg = "", topic = " O ", nbSpace = 0):
        print("%*s%s%s%s %s" % (nbSpace, Back.GREEN, Fore.BLACK, topic, Style.RESET_ALL, msg))
        f = open(pathToResultFileName, "a+")
        f.write("%s %s \n" % (topic, msg))
        f.close()

    def notOk(msg = "", topic = " X ", nbSpace = 0):
        print("%*s%s%s%s %s" % (nbSpace, Back.RED, Fore.BLACK, topic, Style.RESET_ALL, msg))
        f = open(pathToResultFileName, "a+")
        f.write("%s %s \n" % (topic, msg))
        f.close()

    def err(msg = "", topic = " ERROR "):
        print("%s%s%s%s %s" % (Back.RED, Fore.BLACK, topic, Style.RESET_ALL, msg))
        f = open(pathToResultFileName, "a+")
        f.write("%s %s \n" % (topic, msg))
        f.close()

    verbose()
    verbose("Extracting archive '%s' into folder '%s'..." %(archiveName, pathToFolder))
    #check if archive exists in current directory
    if os.path.exists(archiveName):
        # check if archive is not already extracted
        if os.path.exists(pathToFolder):
            shutil.rmtree(pathToFolder)
        # extract archive into folder   
        try:
            with zipfile.ZipFile(archiveName,"r") as zip_ref:
                zip_ref.extractall(pathToFolder)
        except:
            err("'%s' is not a ZIP archive." % archiveName)
            exit(1)

    else :
        err("archive '%s' does not exist in current directory." % archiveName)
        exit(1)

    # total assignments
    nbTotalAssignment = len([entry.name for entry in os.scandir(pathToFolder) if os.path.isdir(entry.path)])
    # relevant assignements
    nbAssignement = 0
    # assignments to delete
    assignementsToDelete = []
    # if no student list given then take all students
    if not len(students):
        for entry in os.scandir(pathToFolder): 
            if entry.is_dir(): 
                splittedEntry = entry.name.split('_')
                if len(splittedEntry):
                    students.append(splittedEntry[0])

    studentAssignmentFound = [False for x in range(len(students))]
    studentCodeValidated = [True for x in range(len(students))]

    verbose()
    verbose('Looking for the assignment of %s students...' % nbTotalAssignment)

    # check assignment for each student
    for entry in os.scandir(pathToFolder):
        if entry.is_dir():
            receivedAssignment = False
            for i, student in enumerate(students):
                if entry.name.startswith(student):
                    receivedAssignment = studentAssignmentFound[i] = True
                    nbAssignement+=1
            if not receivedAssignment:
                    assignementsToDelete.append(entry.path)

    #print result
    for i, assignmentFound in enumerate(studentAssignmentFound):
        ok(students[i]) if assignmentFound else notOk(students[i])
        time.sleep(0.1)

    verbose("%s/%s student assignements found." % (nbAssignement, nbTotalAssignment))
    verbose()

    # delete student assignments that are not yours to evaluate
    for assignmentPath in assignementsToDelete: 
        shutil.rmtree(assignmentPath)

    # Entering each assignment to unzip existing archive
    for root, dirs, files in os.walk(pathToFolder):
        for fileName in files:
            # check if assignment is in an archive
            if fileName.endswith('.zip'):
                # get file path
                filePath = os.path.join(root, fileName)
                # extract archive into root folder
                with zipfile.ZipFile(filePath,"r") as zip_ref:
                    zip_ref.extractall(root)
                # remove archive
                os.remove(filePath)

    # Entering each assignment to delete _MACOSX directory
    directoriesToDelete = []
    for root, dirs, files in os.walk(pathToFolder):
        for dirName in dirs:
            if "__MACOSX" in dirName:
                directoriesToDelete.append(os.path.join(root, dirName))

    for directoryToDelete in directoriesToDelete:
        shutil.rmtree(directoryToDelete)

    verbose("Validating HTML and CSS files of each assignment...")
    # Entering each assignment to validate HTML and CSS files
    for entry in os.scandir(pathToFolder):
        if entry.is_dir(): 
            student = entry.name.split('_')[0]
            studentIndex = students.index(student)
            pathToStudentFileName = os.path.join(pathToFolder, student + '.log')
            filelist = []
            with open(pathToStudentFileName, 'w+') as f:
                for root, dirs, files in os.walk(entry.path):
                    for file in files:
                        #append the file name to the list
                        filePath = os.path.join(root,file)
                        # check if assignment is in an archive
                        if filePath.endswith('.html'):
                            filelist.append(filePath)
                            filePathURL = filePath.replace('\\', '/')
                            cmd = ('curl --silent -H "Content-Type: text/html; charset=utf-8" --data-binary "@%s" %s'
                            % (filePathURL, html_validator_url))
                            #print(cmd)
                            success = False
                            while not success:
                                try :
                                    ans = subprocess.check_output(cmd, encoding='utf-8')
                                    success = True
                                except:
                                    err('W3C request failed. Retry in 60 secs...')
                                    time.sleep(60)

                            try :
                                ansJson = json.loads(ans)
                                for msg in ansJson['messages']:
                                    if msg['type'] == 'error':
                                        if studentCodeValidated[studentIndex] :
                                            studentCodeValidated[studentIndex] = False
                                        if 'lastLine' in msg:
                                            line = file + ':'
                                            line += ('line %(lastLine)d: %(message)s' % msg)
                                            f.write(line + '\n')
                                        else:
                                            line = file + ':'
                                            line += ('%(type)s: %(message)s' % msg)
                                            f.write(line + '\n')
                            except:
                                verbose("error while parsing file.")
                            time.sleep(delayBetweenRequest)

                        if filePath.endswith('.css'):
                            filelist.append(filePath)
                            filePathURL = filePath.replace('\\', '/')
                            cmd = ('curl --silent -H "Content-Type: text/css; charset=utf-8" --data-binary "@%s" %s'
                            % (filePathURL, css_validator_url))
                            #print(cmd)
                            success = False
                            while not success:
                                try :
                                    ans = subprocess.check_output(cmd, encoding='utf-8')
                                    success = True
                                except:
                                    err('W3C request failed. Retry in 60 secs...')
                                    time.sleep(60)
                            try :
                                ansJson = json.loads(ans)
                                for msg in ansJson['messages']:
                                    if msg['type'] == 'error':
                                        if studentCodeValidated[studentIndex] :
                                            studentCodeValidated[studentIndex] = False
                                        if 'lastLine' in msg:
                                            line = file + ':'
                                            line += ('line %(lastLine)d: %(message)s' % msg)
                                            f.write(line + '\n')
                                        else:
                                            line = file + ':'
                                            line += ('%(type)s: %(message)s' % msg)
                                            f.write(line + '\n')
                            except:
                                verbose("error while parsing file.")
                            time.sleep(delayBetweenRequest)

            if studentCodeValidated[studentIndex] :
                os.remove(pathToStudentFileName)
                ok(student)
            else :
                notOk(student)

    studentPassed = [(found and validated) for found,validated in zip(studentAssignmentFound, studentCodeValidated)]
    verbose("%s/%s assignments with valid HTML and CSS files (see '%s/<student>.log' for HTML and CSS errors)." %(sum(studentPassed), len(studentCodeValidated), pathToFolder))

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('usage: %s <archive>.zip' % os.path.basename(sys.argv[0]))
        exit(1)
    else:
        validate(sys.argv[1])
        exit(0)