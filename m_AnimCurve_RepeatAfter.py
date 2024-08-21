"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Repeat after and before, f-curve.
"""

import c4d

def main():
    # Obtiene la selección activa en la línea de tiempo
    timeline_selection = doc.GetSelection()

    if not timeline_selection:
        return

    # Inicia una transacción para el historial de deshacer
    doc.StartUndo()

    try:
        # Aplica la opción "Repeat After"
        c4d.CallCommand(465001157)  # Repeat After

        # Aplica la opción "Repeat Before"
        c4d.CallCommand(465001151)  # Repeat Before

    finally:
        # Finaliza la transacción de deshacer
        doc.EndUndo()

        # Marca el documento como sucio para indicar cambios
        c4d.EventAdd()

if __name__ == '__main__':
    main()