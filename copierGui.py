from copier import *

rowPos = 0
replacementsGui = []

class ReplacementRowConfig:
    def __init__(self,findVal, replaceVal, folderPath, fileName, inFile, fileExtensions):
        self.findVal = findVal
        self.replaceVal = replaceVal
        self.folderPath = folderPath
        self.fileName = fileName
        self.inFile = inFile
        self.fileExtensions = fileExtensions
    def toReplacement(self):
        fileExtensionsTemp = self.fileExtensions.get().split(',')
        return Replacement(self.findVal.get(), self.replaceVal.get(), self.folderPath.get(), self.fileName.get(), self.inFile.get(), fileExtensionsTemp)

window = Tk()
window.title("Copier to make life easier")
window.geometry('750x200')

lblSrc = Label(window, text="Source")
lblSrc.grid(column=0, row=rowPos)

txtSrc = Entry(window,width=50)
txtSrc.grid(column=1, row=rowPos)
rowPos += 1

lblTarget = Label(window, text="Target")
lblTarget.grid(column=0, row=rowPos)

txtTarget = Entry(window,width=50)
txtTarget.grid(column=1, row=rowPos)
rowPos +=1
 
def clicked():
    lastActionVar.set("Clicked")
    source = txtSrc.get();
    target = txtTarget.get();
    if source is not None and source != '' and target is not None and target != '':
        replacements = []
        ## User Input should be setting these replacements
        for replacementRowConfig in replacementsGui:
             if replacementRowConfig.findVal is not None and replacementRowConfig.findVal != '' and \
                replacementRowConfig.replaceVal is not None and replacementRowConfig.replaceVal != '':
                replacements.append(replacementRowConfig.toReplacement())
        copierConfig2 = CopierConfig(True,source,target,replacements)
        performCopy(copierConfig2);
    else :
        print("Nothing set")
        
lastActionVar = StringVar(window, value="Last Action")
lastAction = Label(window, textvariable=lastActionVar)
lastAction.grid(column=1, row=rowPos)
 
btn = Button(window, text="Copy", command=clicked)
btn.grid(column=2, row=rowPos)
rowPos +=1

## replacements
temp = Label(window, text="Find")
temp.grid(column=0, row=rowPos)

temp = Label(window, text="Replace")
temp.grid(column=1, row=rowPos)

temp = Label(window, text="Folder Name")
temp.grid(column=2, row=rowPos)

temp = Label(window, text="File Name")
temp.grid(column=3, row=rowPos)

temp = Label(window, text="File Contents")
temp.grid(column=4, row=rowPos)

temp = Label(window, text="File Extensions")
temp.grid(column=5, row=rowPos)

def addReplacement():
    global rowPos
    rowPos+=1
    ## build a new row, add it to the ui
    findVal = Entry(window,width=12)
    findVal.grid(column=0, row=rowPos)

    replaceVal = Entry(window,width=12)
    replaceVal.grid(column=1, row=rowPos)

    folderPathBoolean=BooleanVar()
    folderPath = Checkbutton (window,onvalue = True, offvalue = False, variable=folderPathBoolean)
    folderPath.invoke()
    folderPath.grid(column=2, row=rowPos)

    fileNameBoolean=BooleanVar()
    fileName = Checkbutton (window,onvalue = True, offvalue = False, variable=fileNameBoolean)
    fileName.invoke()
    fileName.grid(column=3, row=rowPos)

    inFileBoolean=BooleanVar()
    inFile = Checkbutton (window,onvalue = True, offvalue = False, variable=inFileBoolean)
    inFile.invoke()
    inFile.grid(column=4, row=rowPos)

    v = StringVar(window, value='.java,pom.xml')
    fileExtensions = Entry(window,width=12, textvariable=v)
    fileExtensions.grid(column=5, row=rowPos)
    replacementsGui.append(ReplacementRowConfig(findVal, replaceVal, folderPathBoolean, fileNameBoolean, inFileBoolean, fileExtensions))

addReplacementButton = Button(window, text="Add", command=addReplacement)
addReplacementButton.grid(column=6, row=rowPos)
 
window.mainloop()
