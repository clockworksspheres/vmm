
"""

Only accessed from ../vmctl.py - Only access this file from one directory up...

"""

import sys
import psutil
import re

from PySide6.QtWidgets import (QApplication, QMainWindow)

from vmmux.mainwindow_ui import Ui_MainWindow

sys.path.append("./..")

from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.run_commands import start_detached, RunWith

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
        self.rw = RunWith(self.logger)

        # Platform-specific combo items
        platform = sys.platform.lower()

        #####
        # Do not change the names in either dictionary in
        # any way, or this code will not work.  The strings
        # below must match the process name acquired by 
        # psutil.process_iter for the specific hypervisor.
        if platform.startswith("darwin"):
            self.ui.hypervisorComboBox.addItems(["VMware Fusion",
                                                 "UTM",
                                                 "VirtualBox"])
        elif platform.startswith("win"):
            self.ui.hypervisorComboBox.addItems(["VMware Workstation",
                                                 "HyperV",
                                                 "VirtualBox"])

        self.ui.actionComboBox.addItems(["start", "stop", "reset",
                                         "pause", "unpause",
                                         "status", "ip", "list"])
 
        # set the stacked widget to the index 0 for "start" action 
        self.ui.stackedWidget.setCurrentIndex(0)

        # Set the default state of the "hard" radio button to "selected"
        self.ui.hardRadioButton.setChecked(True)

        # Connect combo to stack
        self.ui.actionComboBox.currentIndexChanged.connect(self.handle_combo_action)

        # Connect run action button 
        self.ui.runPushButton.clicked.connect(self.spawn_vm)
        
        # Connect quit action button 
        self.ui.quitPushButton.clicked.connect(QApplication.quit)

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

    def spawn_vm(self):
        # build command
        current_hypervisor_index = self.ui.hypervisorComboBox.currentIndex()
        current_hypervisor_name = self.ui.hypervisorComboBox.currentText()
        current_action_index = self.ui.actionComboBox.currentIndex()

        if sys.platform.lower().startswith("darwin"):
            macHypervisors = { 0: "vmware", 1: "utm", 2: "virtualbox"}
            hypervisor = macHypervisors[current_hypervisor_index]

        elif sys.platform.lower().startswith("win32"):
            winHypervisors = { 0: "vmware", 1: "hyperv", 2: "virtualbox"}
            hypervisor = winHypervisors[current_hypervisor_index]

        matched = None
        hypervisorName = current_hypervisor_name.strip()
        for proc in psutil.process_iter(['pid', 'name']):
            #if re.match(re.escape(hypervisor), proc.info['name']):
            if hypervisorName == proc.info['name'].strip():
                print(f"{proc.info['name']}")
                matched = proc.info['name']

                action = self.ui.actionComboBox.currentText().strip()

                vm = self.ui.vmNameLineEdit.text().strip()

                args = {"hypervisor"}


                cmd = ["/usr/local/bin/vmctl", action, hypervisorName, vm]

                print(f"{cmd}")
                """self.rw.setCommand(cmd)
                out, err, retval = self.rw.communicate()
                print(f"{out}")
                print(f"{err}")
                print(f"{retval}")
                """
                start_detached(cmd)

        if not matched:
            print(f"Hypervisor {hypervisor} not running, start {hypervisor} first")


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



