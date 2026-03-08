import sys
import re
import argparse
import time
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTextBrowser, QStackedWidget
)
from PySide6.QtCore import Qt, QObject, Signal, QThread


# ---------------------------------------------------------
# ANSI COLOR PARSER
# Converts ANSI escape sequences into HTML <span> tags
# ---------------------------------------------------------
ANSI_COLORS = {
    "30": "black",
    "31": "red",
    "32": "green",
    "33": "yellow",
    "34": "blue",
    "35": "magenta",
    "36": "cyan",
    "37": "white",
    "90": "gray",
}

ansi_regex = re.compile(r"\x1b\[(\d+)m")

def ansi_to_html(text):
    """Convert ANSI color codes to HTML spans."""
    def repl(match):
        code = match.group(1)
        color = ANSI_COLORS.get(code, "white")
        return f'<span style="color:{color}">'

    text = ansi_regex.sub(repl, text)
    text = text.replace("\033[0m", "</span>")
    return text


# ---------------------------------------------------------
# THREAD-SAFE STREAM OBJECT
# ---------------------------------------------------------
class ConsoleStream(QObject):
    text_emitted = Signal(str, str)  # html_text, raw_text

    def __init__(self, color="white", logfile=None):
        super().__init__()
        self.color = color
        self.logfile = logfile

    def write(self, text):
        if not text.strip():
            return

        # Convert ANSI → HTML
        html = ansi_to_html(text)

        # Emit to GUI
        self.text_emitted.emit(html, text)

        # Mirror to log file
        if self.logfile:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(text)

    def flush(self):
        pass


# ---------------------------------------------------------
# QTextBrowser with hyperlink support
# ---------------------------------------------------------
class ColorConsole(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setOpenExternalLinks(True)  # enable clickable links

    def append_html(self, html):
        self.append(html)


# ---------------------------------------------------------
# Worker thread example
# ---------------------------------------------------------
class Worker(QObject):
    finished = Signal()

    def run(self):
        for i in range(5):
            print(f"\033[32mstdout message {i}\033[0m")
            time.sleep(0.4)

        print("\033[34mVisit: https://www.python.org\033[0m")

        time.sleep(0.5)
        raise ValueError("This is an example stderr error")


# ---------------------------------------------------------
# Main Window
# ---------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("Advanced PySide6 Console")

        # Stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Page 1
        page1 = QWidget()
        layout1 = QVBoxLayout(page1)
        btn_console = QPushButton("Open Console")
        btn_run = QPushButton("Run Threaded Test")
        layout1.addWidget(btn_console)
        layout1.addWidget(btn_run)

        # Page 2 (console)
        page2 = QWidget()
        layout2 = QVBoxLayout(page2)
        self.console = ColorConsole()
        layout2.addWidget(self.console)
        btn_back = QPushButton("Back")
        layout2.addWidget(btn_back)

        self.stack.addWidget(page1)
        self.stack.addWidget(page2)

        btn_console.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_run.clicked.connect(self.start_thread_test)

        # Create stdout/stderr streams
        self.stdout_stream = ConsoleStream(color="white", logfile=args.logfile)
        self.stderr_stream = ConsoleStream(color="red", logfile=args.logfile)

        self.stdout_stream.text_emitted.connect(self.console.append_html)
        self.stderr_stream.text_emitted.connect(self.console.append_html)

        # Redirect Python stdout/stderr
        sys.stdout = self.stdout_stream
        sys.stderr = self.stderr_stream

        # Initial messages
        print("\033[36mApplication started.\033[0m")
        print(f"\033[33mArgparse message:\033[0m {args.message}")

        if args.logfile:
            print(f"\033[35mLogging to file:\033[0m {args.logfile}")

    # Threaded example
    def start_thread_test(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()


# ---------------------------------------------------------
# argparse
# ---------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Advanced PySide6 Console")
    parser.add_argument(
        "-m", "--message",
        type=str,
        default="Hello from argparse!",
        help="Startup message"
    )
    parser.add_argument(
        "-l", "--logfile",
        type=str,
        default=None,
        help="Optional log file to mirror console output"
    )
    return parser.parse_args()


# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------
def main():
    args = parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(args)
    window.resize(700, 450)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

]
