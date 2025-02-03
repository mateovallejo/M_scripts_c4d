# douwe for yader 2014
# to use in the Script Manager
# select a Hair Object and click Execute

import c4d

def main():
    hair = doc.GetActiveObject()
    if hair.GetType() == 1017305:    # If selected object is of the type Hair
        gds = hair.GetGuides()       # then get the Guides and store them in the variable "gds"
        gdscount = gds.GetCount()    # get the count of those Guides and store them in the variable "gdscount"
        segcount = gds.GetSegmentCount() # get the segment count of those Guides and store them in "segcount"
        pnts = gds.GetPoints()    # get the points of those Guides and store them in "pnts"
        spl = c4d.SplineObject(gdscount,c4d.SPLINETYPE_CUBIC)     # allocate/create spline in memory with as 
                                                                  # many points as the variable "gdscount" gives us 
                                                                # and make our Spline Cubic and store it inside the variable "spl"
        for i in xrange(0, gdscount):     # now iterate from zero and what's inside the variable gdscount
            spl.SetPoint(i, pnts[i*(segcount+1)])   # now set the position of the splines points to those of the Guides points
        doc.InsertObject(spl)     # insert our spline into the scene
        c4d.CallCommand(1017488) # Select All Guides
        c4d.CallCommand(12109) # Delete All Guides so we can paint new ones
    else:
        print " Make sure to select a Hair Object ! "
        return
    spl.Message(c4d.MSG_UPDATE) # update Spline object
    c4d.EventAdd() # tell C4D that something happened and should redraw
    print "Complete"

if __name__=='__main__':
    main()