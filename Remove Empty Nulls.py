import c4d
from c4d import gui

def removeempty(obj):
    if not obj:
        return
    removeempty(obj.GetDown())
    removeempty(obj.GetNext())
    if not obj.GetDown():
        if obj.GetType()== c4d.Onull:
            if not obj.GetFirstTag():
                obj.Remove()
def main():
    obj = doc.GetFirstObject()
    removeempty(obj)
    c4d.EventAdd()
if __name__=='__main__':
    main()