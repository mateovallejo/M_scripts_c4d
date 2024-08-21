import c4d, os
import c4d.documents as docs
from c4d import gui
# Welcome to the world of Python


# fileFormatMenu
def chooseExportMethodMenu():

    # menu items id
    IDM_MENU1 = c4d.FIRST_POPUP_ID
    IDM_MENU2 = c4d.FIRST_POPUP_ID + 1
    IDM_MENU3 = c4d.FIRST_POPUP_ID + 2
    IDM_MENU4 = c4d.FIRST_POPUP_ID + 3
    IDM_MENU5 = c4d.FIRST_POPUP_ID + 4
    IDM_MENU6 = c4d.FIRST_POPUP_ID + 5
    IDM_MENU7 = c4d.FIRST_POPUP_ID + 6
    IDM_MENU8 = c4d.FIRST_POPUP_ID + 7
    IDM_MENU9 = c4d.FIRST_POPUP_ID + 8
    IDM_MENU10 = c4d.FIRST_POPUP_ID + 9
    IDM_MENU11 = c4d.FIRST_POPUP_ID + 10
    IDM_MENU12 = c4d.FIRST_POPUP_ID + 11
    IDM_MENU13 = c4d.FIRST_POPUP_ID + 12
    IDM_MENU14 = c4d.FIRST_POPUP_ID + 13
    IDM_MENU15 = c4d.FIRST_POPUP_ID + 14

    # main menu
    menu = c4d.BaseContainer()
    menu.InsData(IDM_MENU1, "Cinema 4D (*.c4d)")
    menu.InsData(0, '')  # Append separator
    menu.InsData(IDM_MENU2, "3D Studio (*.3ds)")
    menu.InsData(IDM_MENU3, "Alembic (*.abc)")
    menu.InsData(IDM_MENU4, "Allplan (*.xml)")
    menu.InsData(IDM_MENU5, "Bullet (*.bullet)")
    menu.InsData(0, '')  # Append separator
    menu.InsData(IDM_MENU6, "COLLADA 1.4 (*.dae)")
    menu.InsData(IDM_MENU7, "COLLADA 1.5 (*.dae)")
    menu.InsData(0, '')  # Append separator
    menu.InsData(IDM_MENU8, "Direct 3D (*.x)")
    menu.InsData(IDM_MENU9, "DXF (*.dxf)")
    menu.InsData(IDM_MENU10, "FBX (*.fbx)")
    menu.InsData(IDM_MENU11, "Illustrator (*.ai)")
    menu.InsData(IDM_MENU12, "STL (*.stl)")
    menu.InsData(IDM_MENU13, "Volume (*.vdb)")
    menu.InsData(IDM_MENU14, "VRML 2 (*.wrl)")
    menu.InsData(IDM_MENU15, "Wavefront OBJ (*.obj)")

    # show dialog
    result = gui.ShowPopupDialog(cd=None, bc=menu, x=c4d.MOUSEPOS, y=c4d.MOUSEPOS)
    return result


def exportItems(objList, setupFolder, fileFormatEnding, cmdNr):

    tmpList = []
    itemCounter = 0
    saveCounter = 0

    for obj in objList:
        # check type
        if not isinstance(obj, c4d.BaseObject):
            print "Expected c4d.BaseObject, got %s." % obj.__class__.__name__ + " attached to: " \
                  + obj.GetObject().GetName()
        else:
            # some list-stuff
            tmpList.insert(0, obj)
            # create temp doc and insert selected obj into it
            theTempDoc = docs.IsolateObjects(doc, tmpList)
            # save temp doc in folder using the original project-filename & objectname
            path = str(setupFolder + obj.GetName() + str(fileFormatEnding))
            if docs.SaveDocument(theTempDoc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, cmdNr):
                saveCounter += 1
            # some list-stuff
            tmpList.remove(obj)
            # kill temp doc
            docs.KillDocument(theTempDoc)
            itemCounter += 1

    if itemCounter == saveCounter:
        print itemCounter, saveCounter
        gui.MessageDialog(str(itemCounter) + "  Selected items saved to: " + setupFolder)
    else:
        print itemCounter, saveCounter
        gui.MessageDialog("Something went wrong!\n" + "Out of " + str(itemCounter) + " items, "
                          + str(saveCounter) + " were saved to " + setupFolder)


# main
def main():

    # dict with menu id, formatending, command-code
    fileFormatDict = {900000: [".c4d", 1001026],
                  900001: [".3ds", 1001038],
                  900002: [".abc", 1028082],
                  900003: [".xml", 1016440],
                  900004: [".bullet", 180000105],
                  900005: [".dae", 1022316],
                  900006: [".dae", 1025755],
                  900007: [".x", 1001047],
                  900008: [".dxf", 1001036],
                  900009: [".fbx", 1026370],
                  900010: [".ai", 1012074],
                  900011: [".stl", 1001021],
                  900012: [".vdb", 1039865],
                  900013: [".wrl", 1001034],
                  900014: [".obj", 1030178]}

    # the doc
    doc = docs.GetActiveDocument()
    docPath = doc.GetDocumentPath()
    docName = doc.GetDocumentName()
    # list-stuff
    objList = doc.GetSelection()

    chosenExportMethod = chooseExportMethodMenu()

    # check if anything is selected
    if not objList:
        gui.MessageDialog("Nothing selected -> nothing saved")

    else:
        if chosenExportMethod in fileFormatDict:
            # create folder, if not present
            setupFolder = docPath + "\\" + docName[0:len(docName)-4] + "_objExport" + "\\"
            if not os.path.exists(setupFolder):
                os.makedirs(setupFolder)
            exportItems(objList, setupFolder, fileFormatDict[chosenExportMethod][0],
                          fileFormatDict[chosenExportMethod][1])
        else:
            pass



if __name__=='__main__':
    main()