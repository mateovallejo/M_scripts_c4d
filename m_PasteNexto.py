import c4d
from c4d import documents, plugins

def main():
    def prefs(id):
        return plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

    temp = prefs(465001620)[c4d.PREF_INTERFACE_PASTEAT]#remember default paste behavior

    prefs(465001620)[c4d.PREF_INTERFACE_PASTEAT]=2#set to paste as child
    c4d.CallCommand(12108) # Paste

    prefs(465001620)[c4d.PREF_INTERFACE_PASTEAT]=temp#reset default paste behavior

if __name__=='__main__':
    main()