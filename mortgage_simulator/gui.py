"""
ZetCode PyQt5 tutorial

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar, and a central widget.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QTextEdit


class Example(QMainWindow):
    """
    GUI class
    """

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        """
        init
        :return:
        """
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAct = QAction(QIcon("exit24.png"), "Exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit application")
        exitAct.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAct)

        toolbar = self.addToolBar("Exit")
        toolbar.addAction(exitAct)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle("Main window")
        self.show()


def main():
    app = QApplication(sys.argv)
    Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
