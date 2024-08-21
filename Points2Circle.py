#***************************************************
# Points to Circle (COFFEE)
# David Wickenden 2007
# converted to Python - Daniel Sterckx 14-sept-2018
#***************************************************

import c4d

def main():

    radius = 50 # enter radius here

    if not op : return
    if not op.IsInstanceOf(c4d.Opolygon) : return

    doc.StartUndo()

    # step 1
    # we convert the selected points to edges
    # from the edges we create a spline

    settings = c4d.BaseContainer();
    settings[c4d.MDATA_CONVERTSELECTION_LEFT] = 0
    settings[c4d.MDATA_CONVERTSELECTION_RIGHT] = 1

    res = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_CONVERTSELECTION,
                                    list = [op],
                                    mode = c4d.MODIFY_POINTSELECTION,
                                    bc = settings,
                                    doc = doc,
                                    flags = c4d.MODELINGCOMMANDFLAGS_0)
    if res is False:
        print "P2C: Failed convert points to edges."
        return

    res = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_EDGE_TO_SPLINE,
                                    list = [op],
                                    mode = c4d.MODIFY_EDGESELECTION,
                                    bc = settings,
                                    doc = doc,
                                    flags = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO)
    if res is False:
        print "P2C: Failed edge to spline."
        return

    # step 2
    # we get the spline to process it

    spline = op.GetDown();
    if not spline:
        print "P2C: Failed to get the spline."
        return;
    if spline.IsInstanceOf(c4d.Opolygon) : return

    pointCnt = op.GetPointCount()
    pointSel = op.GetPointS()
    pointSelCnt = pointSel.GetCount()

    spPointCnt = spline.GetPointCount()
    spPointSel = spline.GetPointS()
    spPointSelCnt = spPointSel.GetCount()

    if spPointCnt != pointSelCnt: return

    # step 3
    # map the points of the spline to the original points
    # of the object, in order to be able to move the appropriate ones later

    pointMap = []

    sel = pointSel.GetAll(pointCnt)
    for pIndex, selected in enumerate(sel):
      if not selected: continue
      # find the matching point in the spline
      for spIndex in xrange(spPointCnt):
          if op.GetPoint(pIndex) == spline.GetPoint(spIndex):
              data = (pIndex, spIndex)
              pointMap.append(data)
              break

    # display the result (debug)
    #for m in pointMap:
    #    print m[0], m[1]

    # step 4
    # make the spline into a circle
    # apply the spline coordinates to the appropriate source points

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)

    vectorSum = c4d.Vector(0)
    for i in xrange(spPointCnt):
        p = spline.GetPoint(i)
        vectorSum += spline.GetPoint(i)

    spMg = spline.GetMg()
    vectorAv = vectorSum / spPointCnt
    vectorAv_g = spMg.Mul(vectorAv)
    refPointA = spline.GetPoint(0)
    refPointB = spline.GetPoint(1)
    refPointAg = spMg.Mul(refPointA)
    refPointBg = spMg.Mul(refPointB)

    m = c4d.Matrix()

    m.off = vectorAv_g
    m.v1 = (refPointAg - vectorAv_g).GetNormalized()
    mV1 = m.v1
    m.v3 = mV1.Cross((refPointBg - vectorAv_g).GetNormalized())
    mV3 = m.v3
    m.v2 = mV3.Cross(mV1).GetNormalized()

    angle = 6.283 / spPointCnt
    opMg = op.GetMg();

    mInv = ~m;
    opMgInv = ~opMg

    for pm in pointMap:
        pointA = spline.GetPoint(pm[1])
        pointAg = spMg.Mul(pointA)

        pointAl = mInv.Mul(pointAg)
        sn, cs = c4d.utils.SinCos(angle * (pm[1]))
        posAl_x = cs * radius;
        posAl_y = sn * radius;
        pointAlMod = c4d.Vector(posAl_x, posAl_y, pointAl.z)

        pointAg2 = m.Mul(pointAlMod)

        pointAl2 = opMgInv.Mul(pointAg2)
        op.SetPoint(pm[0], pointAl2)

    spline.Remove()
    op.Message(c4d.MSG_UPDATE)
    
    #c4d.CallCommand(200000089) # Scale

    doc.EndUndo()
    c4d.EventAdd()

    return

if __name__=='__main__':
    main()