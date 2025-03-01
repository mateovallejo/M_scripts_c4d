"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Sets sampling cutoff thresholds to 0.01. For faster render ALT: Revert to default.
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
    Returns True if the ALT key is pressed.
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

    vprs = FindAddVideoPost(renderdata, redshift.VPrsrenderer)
    if vprs is None:
        return

    # Switch renderer to Redshift
    renderdata[c4d.RDATA_RENDERENGINE] = redshift.VPrsrenderer

    # Determine the threshold value based on ALT key state
    threshold = 0.01
    if isAltPressed():
        threshold = 0.001

    # Set the cut-off threshold parameters
    vprs[c4d.REDSHIFT_RENDERER_DIFFUSE_SAMPLING_CUT_OFF_THRESHOLD] = threshold
    vprs[c4d.REDSHIFT_RENDERER_REFLECTION_SAMPLING_CUT_OFF_THRESHOLD] = threshold
    vprs[c4d.REDSHIFT_RENDERER_REFRACTION_SAMPLING_CUT_OFF_THRESHOLD] = threshold
    vprs[c4d.REDSHIFT_RENDERER_DIRECT_LIGHTING_SHADOW_CUT_OFF_THRESHOLD] = threshold

    # Refresh UI
    c4d.EventAdd()

if __name__ == '__main__':
    main()
