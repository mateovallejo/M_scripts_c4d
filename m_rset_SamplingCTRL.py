import c4d
import c4d.documents
import redshift

def FindVideoPost(renderData, pluginId):
    vp = renderData.GetFirstVideoPost()
    while vp is not None:
        if vp.IsInstanceOf(pluginId):
            return vp
        vp = vp.GetNext()
    return None

def FindAddVideoPost(renderData, vpPluginID):
    vp = FindVideoPost(renderData, vpPluginID)
    if vp is None:
        vp = c4d.documents.BaseVideoPost(vpPluginID)
        if vp is not None:
            renderData.InsertVideoPost(vp)
    return vp

def GetKeyMod():
    bc = c4d.BaseContainer()  # Inicializa un contenedor base
    keyMod = "None"  # Estado inicial del modificador de teclado
    # Verifica si se ha presionado alguna tecla
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QSHIFT:
            if qualifier & c4d.QCTRL:
                if qualifier & c4d.QALT:
                    keyMod = 'Alt+Ctrl+Shift'
                else:
                    keyMod = 'Ctrl+Shift'
            elif qualifier & c4d.QALT:
                keyMod = 'Alt+Shift'
            else:
                keyMod = 'Shift'
        elif qualifier & c4d.QCTRL:
            if qualifier & c4d.QALT:
                keyMod = 'Alt+Ctrl'
            else:
                keyMod = 'Ctrl'
        elif qualifier & c4d.QALT:
            keyMod = 'Alt'
        else:
            keyMod = 'None'
    return keyMod

def main():
    doc = c4d.documents.GetActiveDocument()
    renderdata = doc.GetActiveRenderData()

    vprs = FindAddVideoPost(renderdata, redshift.VPrsrenderer)
    if vprs is None:
        return

    # Cambiar al renderizador Redshift
    renderdata[c4d.RDATA_RENDERENGINE] = redshift.VPrsrenderer

    # Leer el valor actual del parámetro
    sampling = vprs[c4d.REDSHIFT_RENDERER_UNIFIED_ADAPTIVE_ERROR_THRESHOLD]

    # Detectar el modificador de tecla
    keyMod = GetKeyMod()
    print("Modificador de tecla detectado:", keyMod)  # Para depuración

    # Determinar el incremento basado en el valor actual de sampling
    if sampling <= 0.01:
        step = 0.001
    else:
        step = 0.005

    # Ajustar el valor basado en el modificador de tecla
    if keyMod == 'Ctrl':
        sampling_new = sampling - step
    else:
        sampling_new = sampling + step

    # Asegurarse de que el valor no sea negativo
    if sampling_new < 0:
        sampling_new = 0.001

    # Actualizar las configuraciones de renderizado con el nuevo valor
    vprs[c4d.REDSHIFT_RENDERER_UNIFIED_ADAPTIVE_ERROR_THRESHOLD] = sampling_new

    # Refrescar la interfaz
    c4d.EventAdd()

if __name__ == '__main__':
    main()
