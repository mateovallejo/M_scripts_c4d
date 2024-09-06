import c4d
from c4d import gui

def main():
    # Obtener los objetos seleccionados
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    
    # Iterar sobre los objetos seleccionados y establecer la rotación a 0
    for obj in selected_objects:
        obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_X] = 0
        obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Y] = 0
        obj[c4d.ID_BASEOBJECT_REL_ROTATION, c4d.VECTOR_Z] = 0

    # Actualizar la escena
    c4d.EventAdd()

if __name__ == '__main__':
    main()
