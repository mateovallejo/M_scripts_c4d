"""
Author: Mateo Vallejo / Modificado por ChatGPT
Website:
Version: 1.0.2
Description-US: Repeat after and before, f-curve with Alt key alternative.
"""

import c4d

def isAltPressed():
    """
    Retorna True si se detecta que la tecla ALT está presionada.
    """
    bc = c4d.BaseContainer()
    # Se obtiene el estado del teclado pasando la constante BFM_INPUT_CHANNEL
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QALT:
            return True
    return False

def main():
    # Obtiene la selección activa en la línea de tiempo
    timeline_selection = doc.GetSelection()
    if not timeline_selection:
        return

    # Inicia una transacción para el historial de deshacer
    doc.StartUndo()
    try:
        if isAltPressed():
            # Si se presiona Alt, ejecuta Off Before y Off After
            c4d.CallCommand(465001148)  # Off Before
            c4d.CallCommand(465001154)  # Off After
        else:
            # En caso contrario, ejecuta Repeat After y Repeat Before
            c4d.CallCommand(465001157)  # Repeat After
            c4d.CallCommand(465001151)  # Repeat Before
    finally:
        # Finaliza la transacción de deshacer
        doc.EndUndo()
        # Actualiza la interfaz
        c4d.EventAdd()

if __name__ == '__main__':
    main()
