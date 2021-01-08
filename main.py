
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


archiveName = 'rendu.zip'
students = [
'Maxime GIERLOWSKI', # GROUPE 3
'Lucas GISCOS',
'Julien GOARRE',
'Clément GORSKI',
'Lucas GOSALVES',
'Killian GUIGUEN',
'Pacôme HARISBOURE',
'Robin HILLIET',
'Xavier IRAZOQUI',
'Awad ISSILAME',
'Quentin JARDONNET',
'Jimmy JOURDE',
'Samia KHACHANI',
'Clementine KIFFER',
'Camille LABAZUY',
'Mathis LAGNY',
'Victor LAMBERT',
'Clément LE FOL',
'Hugo LE MOAL',
'Kylian LECHERE',
'Gao LIU',
'Paul LUGNIER',
'Min LUO',
'Van Quang LUU',
'Jordan LYKASO',
'Anne-Gaëlle MADEC',
'Yang WANG',
'Firas ZAAROURI',
 # GROUPE 4
'Laila ADDICHE',
'Romaric ALLEAUME',
'El Mehdi CHEIKH',
'Mounir DAOUDI',
'Anouar ELALAOUI',
'Salah Eddine ELASSIL',
'Alexis ESPINOUX',
'Maryam ESSABANNE',
'Timothé ETIQUE',
'Thibaut FAVIER',
'Lucas FERNANDEZ',
'Ugo FIGHIERA',
'Romain GABALDON',
'Pierre GAUDEAU',
'Victor GAUDIN',
'Timothée GAUDRAY',
'Mohammed HARTI',
'Romain MAIGRON',
'Roland-Emmanuel MAMBOUNDOU',
'Maxime MARCHANTE',
'Damien MARTINEZ',
'Ziheng WANG',
'Jie ZHAO',
'Liangwei ZHAO'
]

studentAssignmentFound = [False for x in range(len(students))]
studentCodeValidated = [True for x in range(len(students))]

html_validator_url = 'https://validator.w3.org/nu/?out=json'
css_validator_url = 'https://validator.w3.org/nu/?out=json'
delayBetweenRequest = 1 #s
currDir = os.getcwd()
pathToArchive = currDir + "\\" + archiveName
folderName = 'assignments'
pathToFolder = currDir + "\\" + folderName

def info(msg = "", topic = " INFO "):
    print(Back.WHITE + Fore.BLACK + topic +  Style.RESET_ALL + " " + msg)

def warn(msg = "", topic = " WARNING "):
    print(Back.YELLOW + Fore.BLACK + topic +  Style.RESET_ALL + " " + msg)

def ok(msg = "", topic = " O ", nbSpace = 0):
    print((' ' * nbSpace) + Back.GREEN + Fore.BLACK + topic +  Style.RESET_ALL + " " + msg)

def notOk(msg = "", topic = " X ", nbSpace = 0):
    print( (' ' * nbSpace) + Back.RED + Fore.BLACK + topic +  Style.RESET_ALL + " " + msg)

def err(msg = "", topic = " ERROR "):
    print(Back.RED + Fore.BLACK + topic +  Style.RESET_ALL + " " + msg)

print()
print("currently in directory '" + currDir + "'")
print("extracting archive '" + archiveName + "'...")
#check if archive exists in current directory
if os.path.exists(pathToArchive):
    # check if archive is not already extracted
    if os.path.exists(pathToFolder):
        shutil.rmtree(pathToFolder)
    # extract archive into folder   
    with zipfile.ZipFile(pathToArchive,"r") as zip_ref:
        zip_ref.extractall(pathToFolder)
        print("'" + archiveName + "' extracted into '" + folderName + "'.")
else :
    err("archive '" + archiveName + "' does not exist in current directory.")
    exit(1)

# move into assignment folder
os.chdir(pathToFolder)
# total assignments
nbTotalAssignment = len([name for name in os.listdir() if os.path.isdir(name)])
print()
print('Looking for your students in the ' + str(nbTotalAssignment) + ' assignements found in total...')
# relevant assignements
nbAssignement = 0
# assignments to delete
assignementsToDelete = []
# check assignment for each student
for entry in os.scandir(): 
    if entry.is_dir(): 
        receivedAssignment = False
        for i, student in enumerate(students):
            if entry.name.startswith(student):
                receivedAssignment = studentAssignmentFound[i] = True
                nbAssignement+=1
        if not receivedAssignment:
                assignementsToDelete.append(os.getcwd() + '\\' + entry.name)

#print result
for i, assignmentFound in enumerate(studentAssignmentFound):
     ok(students[i]) if assignmentFound else notOk(students[i])
     time.sleep(0.1)

print(str(nbAssignement) + '/' + str(len(students)) + " of your student assignements have been found.")
print()

# delete irrelevant assignment
for assignmentPath in assignementsToDelete: 
    shutil.rmtree(assignmentPath)

# Entering each assignment to unzip archive
for entry in os.scandir(): 
    if entry.is_dir(): 
        for root, dirs, files in os.walk(os.path.join(pathToFolder,entry.name)):
            for file in files:
                #append the file name to the list
                filePath = os.path.join(root,file)
                # check if assignment is in an archive
                if filePath.endswith('.zip'):
                    # extract archive into root folder
                    with zipfile.ZipFile(filePath,"r") as zip_ref:
                        zip_ref.extractall(root)
                    # remove archive
                    os.remove(filePath)


print("Validating HTML and CSS files in each student assignment...")
# Entering each assignment to unzip archive
for entry in os.scandir(): 
    if entry.is_dir(): 
        student = entry.name.split('_')[0]
        studentIndex = students.index(student)
        studentFileName = student + '_validation.txt'
        errors = 0
        warnings = 0
        
        filelist = []
        with open(studentFileName, 'w+') as f:
            for root, dirs, files in os.walk(os.path.join(pathToFolder,entry.name)):
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
                        ans = subprocess.check_output(cmd, encoding='UTF-8')
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
                            print("error while parsing file.")
                        time.sleep(delayBetweenRequest)

                    if filePath.endswith('.css'):
                        filelist.append(filePath)
                        filePathURL = filePath.replace('\\', '/')
                        cmd = ('curl --silent -H "Content-Type: text/css; charset=utf-8" --data-binary "@%s" %s'
                        % (filePathURL, css_validator_url))
                        #print(cmd)
                        ans = subprocess.check_output(cmd, encoding='UTF-8')
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
                            print("error while parsing file.")
                        time.sleep(delayBetweenRequest)

        if studentCodeValidated[studentIndex] :
            os.remove(studentFileName)
            ok(student)
        else :
            notOk(student)

studentPassed = [(found and validated) for found,validated in zip(studentAssignmentFound, studentCodeValidated)]
print(str(sum(studentPassed)) + '/' + str(len(studentCodeValidated)) + " of your students have valid HTML and CSS files (see '<student>_validation.log' for HTML and CSS error).")