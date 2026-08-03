import c4d
from c4d import documents

def main():
    doc = documents.GetActiveDocument()
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)

    if not selected:
        print("No objects selected.")
        return

    doc.StartUndo()

    for obj in selected:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        current_state = obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG]
        obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = not current_state

    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()