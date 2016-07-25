# this is the gui for the measurment pc

import ctypes
import sys

from PyQt4 import QtGui

from src.gui import qt_b26_gui

#work around to change taskbar icon
#myappid = 'lukinlab.b26.pythonlab' # arbitrary string
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QtGui.QApplication(sys.argv)
# fname = 'c:\\b26_tmp\\pythonlab_config_dummy.b26'
# fname = 'c:\\b26_tmp\\pythonlab_config3a.b26'
fname = 'c:\\b26_tmp\\pythonlab_config_1.b26'

fname = 'c:\\b26_tmp\\pythonlab_config_safsafaf1.b26'

# fname = "C:\\Users\\Experiment\\PycharmProjects\\PythonLab\\b26_files\\pythonlab_config.b26"
try:
    ex = qt_b26_gui.ControlMainWindow(fname)

    app.setWindowIcon(QtGui.QIcon('magnet_and_nv.ico'))

    ex.show()
    ex.raise_()
    sys.exit(app.exec_())

except ValueError, e:
    print(e.message)
    if not e.message == 'No config file was provided. abort loading gui...':
        raise e
