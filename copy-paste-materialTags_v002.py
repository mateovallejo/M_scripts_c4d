import c4d
from c4d import gui
# Welcome to the world of Python

def GetNextObject(op):
    if op==None:
        return None

    if op.GetDown():
        return op.GetDown()

    while not op.GetNext() and op.GetUp():
        op = op.GetUp()

    return op.GetNext()


def CopyTags(op):
    if op is None:
        return

    count = 0
    tagsDict = {}

    while op:
        if op.GetTag(c4d.Ttexture):
            count += 1
            tags = op.GetTags()
            textureTags = []
            for tag in tags:
                if tag.GetType() == c4d.Ttexture:
                    textureTags.append(tag)
            textureTags.reverse()
            #checking if entry with same name existed
            if tagsDict.get(op.GetName()):
                #if existed increase the counter
                tagsDict.get(op.GetName())[0] += 1
                tagsDict.get(op.GetName()).append(textureTags)
            #otherwise make a new entry, with 0 counter
            else:
                tagsDict[op.GetName()] = [0, textureTags]
        op = GetNextObject(op)

    return count, tagsDict

def PasteTags(op, tagsDict):
    if op is None:
        return

    count = 0

    while op:
        if tagsDict.get(op.GetName()) != None:
            count += 1
            lastTag = op.GetLastTag()
            for tag in tagsDict[op.GetName()][1]:
                tagClone = tag.GetClone()
                op.InsertTag(tagClone, lastTag)
                doc.AddUndo(c4d.UNDOTYPE_NEW, tagClone)
            #if there is only 1 entry, delete the block
            if tagsDict[op.GetName()][0] == 0:
                del tagsDict[op.GetName()]
            #otherwise delete the used entry
            else:
                tagsDict[op.GetName()][0] -= 1
                tagsDict[op.GetName()].pop(1)
        op = GetNextObject(op)
    return count

# Main function
def main():
    selectedObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if selectedObjects == None:
        print("You don't have any selected objects")
        return
    elif len(selectedObjects) != 2:
        print("Please select two objects")
        return

    sourceHierarchy = selectedObjects[0]
    targetHierarchy = selectedObjects[1]

    doc.StartUndo()

    copycount, tagsDict = CopyTags(sourceHierarchy.GetDown())
    print("Copied from " + str(copycount) + " objects.")

    pasteCount = PasteTags(targetHierarchy.GetDown(), tagsDict)
    print("Pasted To " + str(pasteCount) + " objects.")

    c4d.EventAdd()
    doc.EndUndo()

# Execute main()
if __name__=='__main__':
    main()