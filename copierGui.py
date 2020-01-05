from copier import *
from replacment import *

from tkinter import Tk, Text, TOP, BOTH, X, Y, N, LEFT, RIGHT
from tkinter.ttk import Frame, Label, Entry

rowPos = 0
replacementsGui = []
replacementsFrame = NONE

txtTarget = NONE
txtSrc = NONE
operationSrc = NONE
operationRes = NONE
rootMain = NONE
app = NONE
textVariables = []

## read this http://zetcode.com/tkinter/layout/
## https://stackoverflow.com/questions/37350971/tkinter-entry-not-showing-the-current-value-of-textvariable

class ReplacementRowConfig:
    def __init__(self,findVal, replaceVal, folderPath, fileName, inFile, fileExtensions):
        self.findVal = findVal
        self.replaceVal = replaceVal
        self.folderPath = folderPath
        self.fileName = fileName
        self.inFile = inFile
        self.fileExtensions = fileExtensions
        print("here"+self.fileExtensions.get())
    def toReplacement(self):
        print(self.fileExtensions.get())
        fileExtensionsTemp = self.fileExtensions.get().split(',')
        return Replacement(self.findVal.get(), self.replaceVal.get(), self.folderPath.get(), self.fileName.get(), self.inFile.get(), fileExtensionsTemp)


def clickedReplace():
    global txtSrc
    source = txtSrc.get();
    if source is not None and source != '':
        replacements = []
        for replacementRowConfig in replacementsGui:
             if replacementRowConfig.findVal is not None and replacementRowConfig.findVal != '' and \
                replacementRowConfig.replaceVal is not None and replacementRowConfig.replaceVal != '':
                replacements.append(replacementRowConfig.toReplacement())
        copierConfig2 = CopierConfig(True,source,source,replacements)
        performReplacement(copierConfig2);
    else :
        print("Nothing set")
 
def clickedCopy():
    global txtSrc
    global txtTarget
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


def addReplacement(val):
    global replacementsFrame
    global rootMain

    replacementFrameInstance = Frame(replacementsFrame)
    replacementFrameInstance.pack(fill=X)
    
    findVal = Entry(replacementFrameInstance,width=20)
    findVal.pack(side=LEFT, padx=5, pady=5,anchor=N)

    replaceVal = Entry(replacementFrameInstance,width=20)
    replaceVal.pack(side=LEFT, padx=5, pady=5,anchor=N)

    folderPathBoolean=BooleanVar()
    folderPath = Checkbutton (replacementFrameInstance,onvalue = True, offvalue = False, variable=folderPathBoolean, width=8)
    folderPath.invoke()
    folderPath.pack(side=LEFT, padx=5, pady=5,anchor=N)

    fileNameBoolean=BooleanVar()
    fileName = Checkbutton (replacementFrameInstance,onvalue = True, offvalue = False, variable=fileNameBoolean)
    fileName.invoke()
    fileName.pack(side=LEFT, padx=5, pady=5,anchor=N)

    inFileBoolean=BooleanVar()
    inFile = Checkbutton (replacementFrameInstance,onvalue = True, offvalue = False, variable=inFileBoolean, width=8)
    inFile.invoke()
    inFile.pack(side=LEFT, padx=5, pady=5,anchor=N)


    ve = StringVar(replacementFrameInstance, value=val)
    textVariables.append(ve) ## added this array because this value was being garbage collected and lost.
    fileExtensions = Entry(replacementFrameInstance, width=20, textvariable=ve)
    fileExtensions.pack(side=LEFT, padx=5, pady=5,anchor=N)
    replacementsGui.append(ReplacementRowConfig(findVal, replaceVal, folderPathBoolean, fileNameBoolean, inFileBoolean, fileExtensions))

def addJava():
    addReplacement('.java,pom.xml')

def addAng():
    addReplacement('.ts,.html,.css,.scss')

class Example(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global replacementsFrame
        global txtSrc
        global txtTarget
        global operationSrc
        global operationRes
        self.master.title("Copier to make life easier")
        self.pack(fill=BOTH, expand=True)

        window = Frame(self)
        window.pack(fill=X)

        ##window = Tk()
        ##window.title()
        ##window.geometry('750x200')
        ##window.pack(fill=BOTH, expand=True)

        sourceFrame = Frame(self)
        sourceFrame.pack(fill=X)

        lblSrc = Label(sourceFrame, text="Source", width=6)
        lblSrc.pack(side=LEFT, padx=5, pady=5,anchor=N)
        
        btn = Button(sourceFrame, text="RunJustReplace", command=clickedReplace)
        btn.pack(side=RIGHT, padx=5, pady=5, anchor=N)
        
        txtSrc = Entry(sourceFrame)
        txtSrc.pack(fill=X, padx=5, expand=True)


        targetFrame = Frame(self)
        targetFrame.pack(fill=X)
        
        lblTarget = Label(targetFrame, text="Target")
        lblTarget.pack(side=LEFT, padx=5, pady=5,anchor=N)

        btn = Button(targetFrame, text="CopyAndReplace", command=clickedCopy)
        btn.pack(side=RIGHT, padx=5, pady=5, anchor=N)

        txtTarget = Entry(targetFrame,width=50)
        txtTarget.pack(fill=X, padx=5, expand=True)
        
        ## replacements
        replacementsToolbaeFrame = Frame(self)
        replacementsToolbaeFrame.pack(fill=X)
        temp = Label(replacementsToolbaeFrame, text="Find", width=20)
        temp.pack(side=LEFT, padx=5, pady=5,anchor=N, )

        temp = Label(replacementsToolbaeFrame, text="Replace", width=20)
        temp.pack(side=LEFT, padx=5, pady=5,anchor=N)

        temp = Label(replacementsToolbaeFrame, text="Folder Name")
        temp.pack(side=LEFT, padx=5, pady=5,anchor=N)

        temp = Label(replacementsToolbaeFrame, text="File Name")
        temp.pack(side=LEFT, padx=5, pady=5,anchor=N)

        temp = Label(replacementsToolbaeFrame, text="File Contents" )
        temp.pack(side=LEFT, padx=5, pady=5,anchor=N)

        temp = Label(replacementsToolbaeFrame, text="File Extensions" ,width=20)
        temp.pack(side=LEFT, padx=5, pady=5,anchor=N)

        addReplacementButton = Button(replacementsToolbaeFrame, text="AddJava", command=addJava)
        addReplacementButton.pack(side=LEFT, padx=5, pady=5,anchor=N)

        addReplacementButton = Button(replacementsToolbaeFrame, text="AddAng", command=addAng)
        addReplacementButton.pack(side=LEFT, padx=5, pady=5,anchor=N)

        replacementsFrame = Frame(self)
        replacementsFrame.pack(fill=X, expand=True)

        ## OPERATIONS  
        operationsFrame2 = Frame(self)
        operationsFrame2.pack(fill=X)

        operationSrc = Text(operationsFrame2, width=40)
        operationSrc.pack(side=LEFT, padx=5)

        opButtonFrame = Frame(operationsFrame2)
        opButtonFrame.pack(side=LEFT, fill=Y, expand=True)

        dashToCC = Button(opButtonFrame, text="dashToCC", command=cleanCamelCaseBtn)
        dashToCC.pack(padx=5, pady=5)

        ccToDashButton = Button(opButtonFrame, text="cCToDash", command=camelCaseToDashBtn)
        ccToDashButton.pack(padx=5, pady=5)

        operationRes = Text(operationsFrame2, width=40)
        operationRes.pack(side=RIGHT, padx=5)

## Operation handlers for the buttons
def cleanCamelCaseBtn():
    inputValue=operationSrc.get("1.0","end-1c")
    outputValue = cleanCamelCase(inputValue)
    operationRes.delete("1.0", 'end')
    operationRes.insert("1.0", outputValue)

def camelCaseToDashBtn():
    inputValue=operationSrc.get("1.0","end-1c")
    outputValue = camelCaseToDash(inputValue)
    operationRes.delete("1.0", 'end')
    operationRes.insert("1.0", outputValue)

def main():
    global rootMain
    global app
    root = Tk()
    rootMain = root
    root.geometry('750x400')
    app = Example()
    root.mainloop()

if __name__ == '__main__':
    main()

##window.mainloop()

