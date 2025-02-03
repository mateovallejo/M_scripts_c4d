"""
Author: Mateo Vallejo
Website:
Version: 0.1.0
Description-US:Reset selected objects visibility.
"""

import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    doc.StartUndo()
    objs = doc.GetActiveObjects(1)
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
        obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2
    
    c4d.EventAdd()
    doc.EndUndo()
    

if __name__=='__main__':
    main()
