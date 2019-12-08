from shutil import copytree
from shutil import copy2
from shutil import rmtree

import os
import fileinput

from tkinter import *

## Build GUI
## https://www.tutorialspoint.com/python/python_gui_programming.htm
## https://likegeeks.com/python-gui-examples-tkinter-tutorial/

## User Input should be setting these 3 values
debugLogging = True

def log(isDebug, string):
    if (isDebug and debugLogging):
        print(string);
    elif not isDebug:
        print(string);

class CopierConfig:
    def __init__(self, debugLogging, source, target, replacements, ignoreFolders=[]):
        self.debugLogging = debugLogging
        self.source = source
        self.target = target
        self.replacements = replacements
        self.ignoreFolders = ignoreFolders

class Replacement:
    def __init__(self, findVal, replaceVal, folderPath=True, fileName=True, inFile=True, fileExtensions=[".java","pom.xml"]):
        self.findVal = findVal
        self.replaceVal = replaceVal
        self.folderPath = folderPath
        self.fileName = fileName
        self.inFile = inFile
        self.fileExtensions = fileExtensions
        
def performFolderNameRepalcements(copierConfig, folderName):
    strin = folderName;
    for replacement in copierConfig.replacements:
        if replacement.folderPath:
            strin = strin.replace(replacement.findVal,replacement.replaceVal)
    return strin;

def performFileNameRepalcements(copierConfig, fileName):
    strin = fileName;
    for replacement in copierConfig.replacements:
        if replacement.fileName:
            strin = strin.replace(replacement.findVal,replacement.replaceVal)
    return strin;

def performFileContentsRepalcements(copierConfig, filePath):
    replacementsToUse = [];
    for replacement in copierConfig.replacements:
        for ext in replacement.fileExtensions:
            if filePath.endswith(ext):
                replacementsToUse.append(replacement)
                log(True, 'Found Matching Extension:' +ext +' in ' + filePath)
                break
    if len(replacementsToUse) > 0:
        with fileinput.FileInput(filePath, inplace=True) as file:
            for line in file:
                for replacement in replacementsToUse:
                    if not replacement.inFile: ## todo filter out files that are not the required types.
                        continue
                    line = line.replace(replacement.findVal,replacement.replaceVal)
                print(line, end='')


## https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
def customFolderUpdate(copierConfig, dst):
    for fn in os.listdir(dst):
        if os.path.isdir(os.path.join(dst, fn)):
            replacedValue = performFolderNameRepalcements(copierConfig,fn)
            if replacedValue != fn:
                log(copierConfig.debugLogging, "Renaming " + replacedValue)
                ## todo add a check here to make sure the value has actually changed.
                os.rename(os.path.join(dst, fn),
                          os.path.join(dst, replacedValue))
                customFolderUpdate(copierConfig, os.path.join(dst, replacedValue))
            else :
                log(copierConfig.debugLogging, "Not Renaming " + fn)
                customFolderUpdate(copierConfig, os.path.join(dst, fn))
        else : ## its a file then, perform file name and contents replacement
            customFileUpdate(copierConfig, os.path.join(dst, fn))

##https://stackoverflow.com/questions/8735312/how-to-change-folder-names-in-python
def customFileUpdate(copierConfig, src):
    indy = src.rfind('\\')
    dstToReplace = src[indy:]
    dstToReplace = performFileNameRepalcements(copierConfig, dstToReplace)
    if dstToReplace != src[indy:]:
        log(True, 'Renaming:' + (src[:indy]+dstToReplace))
        destinationStr = (src[:indy]+dstToReplace)
        os.rename(src, destinationStr)
        performFileContentsRepalcements(copierConfig, destinationStr);
    else :
        performFileContentsRepalcements(copierConfig, src);

## external Method to call to start the process
def performCopy(copierConfig):
    if os.path.isdir(copierConfig.target):
        print('Deleting target dir as it already exists')
        rmtree(copierConfig.target,ignore_errors=True)
    
    ##https://docs.python.org/3/library/shutil.html
    ## Copy the folder structure
    copytree(copierConfig.source,
             copierConfig.target,
             False,
             None) ## maybe replace the custom function with the default one, and add my own logic for files in customDirectoryNameUpdate, giving me more control.
    
    ## maybe run a secondary process on the folders by walking the directory structure and updating them all.
    customFolderUpdate(copierConfig, copierConfig.target)
    
    log(True, "Process Complete")
    
## todo handle error for file already existing and remove it.


##source = 'C:/dev/test/calendar-power-custom-impl'
##target = 'C:/dev/test/calendar-power-custom-impl-copy'
##replacements = []
#### User Input should be setting these replacements
##replacements.append(Replacement('calendar','awesome'))
##replacements.append(Replacement('Calendar','Awesome'))
##copierConfig2 = CopierConfig(True,source,target,replacements)
##performCopy(copierConfig2);
