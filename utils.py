#
# script contains utiltiy functions for the project
#

from PyQt5.QtWidgets import QFileDialog


def getFileFromDialog():
    """
    function open file chooser and 
    returns path of selected file
    """
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)

    if dlg.exec_():
        filenames = dlg.selectedFiles()
        return filenames
