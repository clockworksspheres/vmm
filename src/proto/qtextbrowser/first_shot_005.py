import sys
import re
import argparse

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTextBrowser, QStackedWidget
)
from PySide6.QtCore import QObject, Signal


# ---------------------------------------------------------
# ANSI COLOR PARSER
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
    "91": "lightcoral",
    "92": "lightgreen",
    "93": "khaki",
    "94": "lightskyblue",
    "95": "violet",
    "96": "lightcyan",
    "97": "white",
}

# Matches ESC[<codes>m, e.g. \x1b[31m or \x1b[1;31m
ansi_regex = re.compile(r"\x1b\[(\d+(?:;\d+)*)m")

# URL detection
url_regex = re.compile(r"(https?://[^\s]+)")


def linkify(text):
    """Wrap URLs in <a> tags."""
    def repl(m):
        url = m.group(1)
        return f'<a href="{url}">{url}</a>'
    return url_regex.sub(repl, text)


def ansi_to_html(text):
    """Convert ANSI escape sequences to HTML spans and linkify URLs."""
    html = ""
    last_end = 0

    for match in ansi_regex.finditer(text):
        start, end = match.span()
        codes = match.group(1).split(";")

        # Append text before the ANSI code
        segment = text[last_end:start]
        segment = linkify(segment)
        html += segment

        # Determine color (foreground only)
        color = None
        for code in codes:
            if code in ANSI_COLORS:
                color = ANSI_COLORS[code]

        if color:
            html += f'<span style="color:{color}">'
        else:
            html += "<span>"

        last_end = end

    # Append remaining text
    tail = text[last_end:]
    tail = linkify(tail)
    html += tail

    # Close spans on reset
    html = html.replace("\x1b[0m", "</span>")

    return html


# ---------------------------------------------------------
# STREAM OBJECT (thread-safe even without threads)
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

        html = ansi_to_html(text)
        self.text_emitted.emit(html, text)

        if self.logfile:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(text + "\n")

    def flush(self):
        pass


# ---------------------------------------------------------
# QTextBrowser with hyperlink support
# ---------------------------------------------------------
class ColorConsole(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setOpenLinks(True)

    def append_html(self, html):
        self.append(html)


# ---------------------------------------------------------
# Main Window (NO THREADS)
# ---------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("Advanced PySide6 Console (No Threads)")

        # Stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Page 1
        page1 = QWidget()
        layout1 = QVBoxLayout(page1)
        btn_console = QPushButton("Open Console")
        btn_demo = QPushButton("Run Demo Output")
        layout1.addWidget(btn_console)
        layout1.addWidget(btn_demo)

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
        btn_demo.clicked.connect(self.demo_output)

        # Create stdout/stderr streams
        self.stdout_stream = ConsoleStream(color="white", logfile=args.logfile)
        self.stderr_stream = ConsoleStream(color="red", logfile=args.logfile)

        self.stdout_stream.text_emitted.connect(self.console.append_html)
        self.stderr_stream.text_emitted.connect(self.console.append_html)

        # Redirect Python stdout/stderr
        sys.stdout = self.stdout_stream
        sys.stderr = self.stderr_stream

        # Initial messages
        print("\x1b[36mApplication started.\x1b[0m")
        print(f"\x1b[33mArgparse message:\x1b[0m {args.message}")

        if args.logfile:
            print(f"\x1b[35mLogging to file:\x1b[0m {args.logfile}")

    # Demo output without threads
    def demo_output(self):
        print("\x1b[32mThis is green text.\x1b[0m")
        print("\x1b[31mThis is red text.\x1b[0m")
        print("\x1b[34mClickable link: https://www.qt.io\x1b[0m")
        print("\x1b[93mBright yellow text.\x1b[0m")
        print("\x1b[1;31mBold red (SGR 1;31) — parsed correctly.\x1b[0m")
        print("Normal text again.")


# ---------------------------------------------------------
# argparse
# ---------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Advanced PySide6 Console (No Threads)")
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


