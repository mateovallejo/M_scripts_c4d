"""
Go to end PreviewRange Frame


                                                                       
                                       )         )    )     )  (  (    
    )                (   (          ( /(      ( /( ( /(  ( /(  )\))(   
   (         (    (  )(  )\  `  )   )\())(    )(_)))\()) )(_))((_)()\  
   )\  '     )\   )\(()\((_) /(/(  (_))/ )\  ((_) ((_)\ ((_)   (()((_) 
 _((_))     ((_) ((_)((_)(_)((_)_\ | |_ ((_) |_  )/  (_)|_  )   | __|  
| '  \()    (_-</ _|| '_|| || '_ \)|  _|(_-<  / /| () |  / /    |__ \  
|_|_|_|_____/__/\__||_|  |_|| .__/  \__|/__/ /___|\__/  /___|   |___/  
      |_____|               |_|                                        

                                                           

"""

import c4d

def main():
    doc = c4d.documents.GetActiveDocument()

    end_time = doc[c4d.DOCUMENT_LOOPMAXTIME]

    # Set current time to end of range
    doc[c4d.DOCUMENT_TIME] = end_time

    # Update the timeline
    c4d.EventAdd()

if __name__ == '__main__':
    main()