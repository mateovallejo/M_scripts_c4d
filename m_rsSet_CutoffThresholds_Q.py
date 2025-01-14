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
    vprs[c4d.REDSHIFT_RENDERER_DIFFUSE_SAMPLING_CUT_OFF_THRESHOLD] = 0.01
    vprs[c4d.REDSHIFT_RENDERER_REFLECTION_SAMPLING_CUT_OFF_THRESHOLD] = 0.01
    vprs[c4d.REDSHIFT_RENDERER_REFRACTION_SAMPLING_CUT_OFF_THRESHOLD] = 0.01
    vprs[c4d.REDSHIFT_RENDERER_DIRECT_LIGHTING_SHADOW_CUT_OFF_THRESHOLD] = 0.01
    


    # Refresh UI
    c4d.EventAdd()


if __name__ == '__main__':
    main()