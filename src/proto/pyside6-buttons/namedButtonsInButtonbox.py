from PySide6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt
import sys

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Run or Quit Example")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        # Some content
        layout.addWidget(QLabel("Do you want to run the process or quit?"))
        layout.addStretch()

        # Create button box without standard flags
        self.buttonBox = QDialogButtonBox()

        # Custom buttons with correct roles
        btn_run = QPushButton("Run")
        btn_quit = QPushButton("Quit")

        # Important: assign roles so signals work
        self.buttonBox.addButton(btn_run, QDialogButtonBox.AcceptRole)   # → triggers accepted()
        self.buttonBox.addButton(btn_quit, QDialogButtonBox.RejectRole)  # → triggers rejected()

        # Optional: make "Run" the default button (Enter key activates it)
        btn_run.setDefault(True)

        layout.addWidget(self.buttonBox)

        # Connect signals (same as with standard OK/Cancel)
        self.buttonBox.accepted.connect(self.accept)   # or your custom slot
        self.buttonBox.rejected.connect(self.reject)   # or your custom slot

        # Example: do something different based on which button
        btn_run.clicked.connect(lambda: print("User clicked RUN"))
        btn_quit.clicked.connect(lambda: print("User clicked QUIT"))

# Usage example
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CustomDialog()
    result = dialog.exec()

    if result == QDialog.Accepted:
        print("Dialog accepted (Run was clicked)")
    else:
        print("Dialog rejected (Quit was clicked)")
    sys.exit(app.exec())

