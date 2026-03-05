
import sys

from PySide6.QtWidgets import (QApplication, QMainWindow)

from mainwindow_ui import Ui_MainWindow

sys.path.append("./..")

from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp


class VmCtlUi(QMainWindow):
    """ 
    The Main Window dialog for the ramdisk.
    """
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = CyLogger()
        self.logger.initializeLogs()


        # Platform-specific combo items
        platform = sys.platform.lower()

        if platform.startswith("darwin"):
            self.ui.actionComboBox.addItems(["VMware Fusion",
                                             "UTM",
                                             "Virtualbox"])
        elif platform.startswith("win"):
            self.ui.actionComboBox.addItems(["VMware Workstation",
                                             "HyperV",
                                             "Virtualbox"])



if __name__=="__main__":
    app = QApplication(sys.argv)
    print("started app...")
    window = VmCtlUi()
    print("initiated window")
    window.show()
    print("showing window...")
    window.raise_()
    print("raising_ window")
    sys.exit(app.exec())



