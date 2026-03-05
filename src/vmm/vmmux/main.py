
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
            self.ui.hypervisorComboBox.addItems(["VMware Fusion",
                                                 "UTM",
                                                 "Virtualbox"])
        elif platform.startswith("win"):
            self.ui.hypervisorComboBox.addItems(["VMware Workstation",
                                                 "HyperV",
                                                 "Virtualbox"])

        self.ui.actionComboBox.addItems(["start", "stop", "restart",
                                         "pause", "unpause",
                                         "status", "ip", "list"])
 
        self.ui.stackedWidget.setCurrentIndex(0)

        # Connect combo to stack
        self.ui.actionComboBox.currentIndexChanged.connect(self.handle_combo_action)

    def handle_combo_action(self, index):
        """
        """
        if index == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
        elif index in (1, 2):
            self.ui.stackedWidget.setCurrentIndex(1)
        elif index in (3, 4):
            self.ui.stackedWidget.setCurrentIndex(2)
        elif index in (5, 6, 7):
            self.ui.stackedWidget.setCurrentIndex(3)
        else:
            raise IndexError



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



