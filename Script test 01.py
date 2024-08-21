import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    objs = doc.GetActiveObjects(1)
    for obj in objs:
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
        obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2
    
    c4d.EventAdd()
    

if __name__=='__main__':
    main()
