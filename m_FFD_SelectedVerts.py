import c4d
from c4d import utils

def main():
    # Verifica si se seleccionó un objeto
    if op is None:
        return

    # Verifica si el objeto es un objeto poligonal
    if not op.CheckType(c4d.Opolygon):
        return

    # Obtiene la selección de vértices
    bs = op.GetPointS()

    # Inicializa las variables min y max
    min_vec = c4d.Vector(float('inf'), float('inf'), float('inf'))
    max_vec = c4d.Vector(float('-inf'), float('-inf'), float('-inf'))

    # Itera sobre cada punto en la selección
    for i, point in enumerate(op.GetAllPoints()):
        if bs.IsSelected(i):
            # Transforma las coordenadas locales del punto a globales
            global_point = op.GetMg() * point

            # Actualiza las coordenadas min y max
            min_vec.x = min(min_vec.x, global_point.x)
            min_vec.y = min(min_vec.y, global_point.y)
            min_vec.z = min(min_vec.z, global_point.z)
            max_vec.x = max(max_vec.x, global_point.x)
            max_vec.y = max(max_vec.y, global_point.y)
            max_vec.z = max(max_vec.z, global_point.z)

    # Calcula el centro y el tamaño del bounding box
    center = (min_vec + max_vec) / 2
    size = max_vec - min_vec

    # Crea un nuevo deformador FFD
    ffd = c4d.BaseObject(c4d.Offd)

    # Ajusta el tamaño y la posición del FFD al bounding box
    ffd[c4d.FFDOBJECT_SIZE] = size
    ffd.SetAbsPos(center)

    # Inserta el FFD en el documento
    ffd.InsertUnder(op)

    doc.SetActiveObject(ffd)  # Establecer el FFD como objeto activo
    c4d.CallCommand(12236)  # Comando para seleccionar el objeto activo (Select All)
    
    # Actualiza el documento
    c4d.EventAdd()

    # Resetea el bounding box
    c4d.CallButton(ffd, c4d.FFDOBJECT_RESET)

# Ejecuta la función principal
if __name__=='__main__':
    main()