"""
Author: Mateo Vallejo
Website:
Version: 1.0.0
Description-US:Sets RS renderer bucket size to 64.
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

    vprs = FindAddVideoPost(renderdata, redshift.VPrsrenderer)
    if vprs is None:
        return

    # Switch renderer
    renderdata[c4d.RDATA_RENDERENGINE] = redshift.VPrsrenderer

    # Set some parameters
    vprs[c4d.REDSHIFT_RENDERER_BLOCK_SIZE] = 64


    # Refresh UI
    c4d.EventAdd()


if __name__ == '__main__':
    main()