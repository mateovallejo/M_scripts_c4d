import c4d

class ToggleSaveImageCommand(c4d.plugins.CommandData):
    
    def Execute(self, doc):
        # Obtén el documento actual
        doc = c4d.documents.GetActiveDocument()

        # Obtén la configuración de renderización
        render_data = doc.GetActiveRenderData()

        # Lee el estado actual del parámetro RDATA_SAVEIMAGE
        current_state = render_data[c4d.RDATA_SAVEIMAGE]

        # Cambia el estado del parámetro RDATA_SAVEIMAGE usando una declaración if
        if current_state == True:
            render_data[c4d.RDATA_SAVEIMAGE] = False
            c4d.gui.MessageDialog('Save OFF')
        elif current_state == False:
            render_data[c4d.RDATA_SAVEIMAGE] = True
            c4d.gui.MessageDialog('Save ON')

        # Actualiza el documento
        c4d.EventAdd()
        
        return True

    def GetState(self, doc):
        # Obtén el documento actual
        doc = c4d.documents.GetActiveDocument()

        # Obtén la configuración de renderización
        render_data = doc.GetActiveRenderData()

        # Lee el estado actual del parámetro RDATA_SAVEIMAGE
        current_state = render_data[c4d.RDATA_SAVEIMAGE]

        if current_state:
            return c4d.CMD_VALUE
        else:
            return 0

if __name__ == "__main__":
    c4d.plugins.RegisterCommandPlugin(id=32767,  # Asegúrate de reemplazar este ID con uno único
                                      str="Toggle Save Image",
                                      info=0,
                                      help="Toggle save image state",
                                      dat=ToggleSaveImageCommand(),
                                      icon=None)
