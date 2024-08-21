import c4d

def main():

    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    for obj in selected:
        if obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 0 or obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 2:
           obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
           obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1
        else:
           obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
           obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2


if __name__=='__main__':
    main()
    c4d.EventAdd()