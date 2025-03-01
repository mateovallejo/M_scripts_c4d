"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Multiplies samples by x2 ALT: Divides by /2.
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

def isAltPressed():
    """
    Retorna True si se detecta que la tecla ALT está presionada.
    """
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        qualifier = bc[c4d.BFM_INPUT_QUALIFIER]
        if qualifier & c4d.QALT:
            return True
    return False

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

    # Guardar el valor actual de Unified Max Samples (valor de referencia)
    current_samples_max = vprs[c4d.REDSHIFT_RENDERER_UNIFIED_MAX_SAMPLES]
    
    # Detectar si se presionó ALT
    alt_pressed = isAltPressed()
    
    # Calcular el nuevo valor de Unified Max Samples según si se presiona ALT o no
    if alt_pressed:
        new_samples_max = current_samples_max / 2.0
    else:
        new_samples_max = current_samples_max * 2
    new_samples_max = int(new_samples_max)
    
    # Actualizar Unified Max Samples con el nuevo valor calculado
    vprs[c4d.REDSHIFT_RENDERER_UNIFIED_MAX_SAMPLES] = new_samples_max

    # Definir los parámetros a actualizar y el factor adicional (por defecto 1; en el caso de Brute Force GI Rays, el factor es 2)
    params = {
       c4d.REDSHIFT_RENDERER_REFLECT_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_REFRACT_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_AO_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_LIGHT_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_VOLUME_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_SINGLE_SCATTERING_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_MULTIPLE_SCATTERING_SAMPLES_COUNT: 1,
       c4d.REDSHIFT_RENDERER_BRUTE_FORCE_GI_NUM_RAYS: 2
    }
    
    # Actualizar cada uno de los parámetros según la condición:
    # Si el valor actual del parámetro es mayor que current_samples_max, se le aplica la operación (multiplicar o dividir) al valor actual.
    # Si no, se asigna new_samples_max (o new_samples_max * factor, en el caso de GI Rays).
    for param_key, factor in params.items():
        old_val = vprs[param_key]
        if old_val > current_samples_max:
            if alt_pressed:
                new_val = old_val / 2.0
            else:
                new_val = old_val * 2
        else:
            new_val = new_samples_max * factor
        vprs[param_key] = int(new_val)
    
    # Finalizar el bloque de undo
    doc.EndUndo()
    
    # Preparar un diccionario para imprimir los valores finales de forma sencilla
    overrides = {
        "Unified Max Samples": vprs[c4d.REDSHIFT_RENDERER_UNIFIED_MAX_SAMPLES],
        "Overrides": vprs[c4d.REDSHIFT_RENDERER_UNIFIED_MAX_SAMPLES],
        "Reflect Samples": vprs[c4d.REDSHIFT_RENDERER_REFLECT_SAMPLES_COUNT],
        "Refract Samples": vprs[c4d.REDSHIFT_RENDERER_REFRACT_SAMPLES_COUNT],
        "AO Samples": vprs[c4d.REDSHIFT_RENDERER_AO_SAMPLES_COUNT],
        "Light Samples": vprs[c4d.REDSHIFT_RENDERER_LIGHT_SAMPLES_COUNT],
        "Volume Samples": vprs[c4d.REDSHIFT_RENDERER_VOLUME_SAMPLES_COUNT],
        "Single Scattering": vprs[c4d.REDSHIFT_RENDERER_SINGLE_SCATTERING_SAMPLES_COUNT],
        "Multiple Scattering": vprs[c4d.REDSHIFT_RENDERER_MULTIPLE_SCATTERING_SAMPLES_COUNT],
        "Brute Force GI Rays": vprs[c4d.REDSHIFT_RENDERER_BRUTE_FORCE_GI_NUM_RAYS]
    }
    
    # Lista de parámetros que no se imprimirán si son iguales a Unified Max Samples
    skip_if_equal = {
        "Reflect Samples", "Refract Samples", "AO Samples",
        "Light Samples", "Volume Samples", "Single Scattering",
        "Multiple Scattering"
    }
    # Valor de referencia de Unified Max Samples
    umax = overrides["Unified Max Samples"]
    
    print("---------------------rs Setting-----------------")
    # Se imprimen todos los parámetros, excepto aquellos de skip_if_equal que tengan el mismo valor que Unified Max Samples
    for key, value in overrides.items():
        if key in skip_if_equal and value == umax:
            continue
        print(f"{key}: {value}")
    
    print("------------------------------------------------")
    # Actualizar la interfaz
    c4d.EventAdd()

if __name__ == '__main__':
    main()
