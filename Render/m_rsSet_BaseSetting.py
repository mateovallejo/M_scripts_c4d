"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Add Quick RS Setting Preset - Make sure Advenced mode is active.
"""

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

def main():
    doc = c4d.documents.GetActiveDocument()
    renderdata = doc.GetActiveRenderData()

    # Iniciar bloque de undo
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderdata)
    
    # Obtener o agregar el VideoPost de Redshift
    vprs = FindAddVideoPost(renderdata, redshift.VPrsrenderer)
    if vprs is None:
        doc.EndUndo()
        return
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, vprs)
    
    # Cambiar al renderizador Redshift
    renderdata[c4d.RDATA_RENDERENGINE] = redshift.VPrsrenderer

    # Unified Sampling
    vprs[c4d.REDSHIFT_RENDERER_ENABLE_AUTOMATIC_SAMPLING] = False
    vprs[c4d.REDSHIFT_RENDERER_DIFFUSE_SAMPLING_CUT_OFF_THRESHOLD] = 0.01
    vprs[c4d.REDSHIFT_RENDERER_REFLECTION_SAMPLING_CUT_OFF_THRESHOLD] = 0.01
    vprs[c4d.REDSHIFT_RENDERER_REFRACTION_SAMPLING_CUT_OFF_THRESHOLD] = 0.01
    vprs[c4d.REDSHIFT_RENDERER_DIRECT_LIGHTING_SHADOW_CUT_OFF_THRESHOLD] = 0.01

    # Configuraciones nuevas solicitadas
    vprs[c4d.REDSHIFT_RENDERER_UNIFIED_ADAPTIVE_ERROR_THRESHOLD] = 0.1
    samples_max = 32
    vprs[c4d.REDSHIFT_RENDERER_UNIFIED_MAX_SAMPLES] = samples_max

    # Asignar el mismo valor de samples_max a los siguientes parámetros
    vprs[c4d.REDSHIFT_RENDERER_REFLECT_SAMPLES_COUNT] = samples_max
    vprs[c4d.REDSHIFT_RENDERER_REFRACT_SAMPLES_COUNT] = samples_max
    vprs[c4d.REDSHIFT_RENDERER_AO_SAMPLES_COUNT] = samples_max
    vprs[c4d.REDSHIFT_RENDERER_LIGHT_SAMPLES_COUNT] = samples_max
    vprs[c4d.REDSHIFT_RENDERER_VOLUME_SAMPLES_COUNT] = samples_max
    vprs[c4d.REDSHIFT_RENDERER_SINGLE_SCATTERING_SAMPLES_COUNT] = samples_max
    vprs[c4d.REDSHIFT_RENDERER_MULTIPLE_SCATTERING_SAMPLES_COUNT] = samples_max

    # Configurar el Global Illumination Secondary Engine a Brute Force.
    # En este ejemplo, el valor 4 corresponde al modo deseado.
    vprs[c4d.REDSHIFT_RENDERER_SECONDARY_GI_ENGINE] = 4
    vprs[c4d.REDSHIFT_RENDERER_BRUTE_FORCE_GI_NUM_RAYS] = samples_max * 4
    vprs[c4d.REDSHIFT_RENDERER_BLOCK_SIZE] = 512

    # Finalizar el bloque de undo
    doc.EndUndo()

    # Actualizar la interfaz
    c4d.EventAdd()

if __name__ == '__main__':
    main()
