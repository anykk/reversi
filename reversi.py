import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Othello")
        self.resize(640, 480)
        self.center()
        self.setMinimumSize(QtCore.QSize(640, 480))
        self.setMaximumSize(QtCore.QSize(640, 480))

        window = QtWidgets.QWidget()
        self.setCentralWidget(window)
        game = QtWidgets.QFrame(window)

        white_lcd = QtWidgets.QLCDNumber(window)
        black_lcd = QtWidgets.QLCDNumber(window)
        white_label = QtWidgets.QLabel("White:", window)
        white_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        black_label = QtWidgets.QLabel("Black:", window)
        black_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        game.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        """
        layout = QtWidgets.QGridLayout()
        layout.addWidget(game, 0, 0, 48, 48)
        layout.addWidget(white_label, 5, 50, 2, 13)
        layout.addWidget(white_lcd, 8, 50, 7, 13)
        layout.addWidget(black_label, 20, 50, 2, 13)
        layout.addWidget(black_lcd, 23, 50, 7, 13)

        window.setLayout(layout)
        """
        game.setFocusPolicy(QtCore.Qt.StrongFocus)

        game.resize(460, 460)
        game.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
        game.setMidLineWidth(3)
        white_label.move(470, 30)
        white_label.resize(150, 18)
        white_lcd.move(470, 50)
        white_lcd.resize(150, 70)
        black_label.move(470, 180)
        black_label.resize(150, 18)
        black_lcd.move(470, 200)
        black_lcd.resize(150, 70)

        menubar = self.menuBar()
        menubar.setGeometry(QtCore.QRect(0, 0, 640, 3))
        gameMenu = menubar.addMenu("Game")
        toolsMenu = menubar.addMenu("Tools")
        helpMenu = menubar.addMenu("Help")

        actionNew_game = QtWidgets.QAction("New game", self)
        actionNew_game.setShortcut("Ctrl+N")
        actionRestart = QtWidgets.QAction("Restart", self)
        actionRestart.setShortcut("Ctrl+R")
        actionSave = QtWidgets.QAction("Save", self)
        actionSave.setShortcut("Ctrl+S")
        actionLoad = QtWidgets.QAction("Load", self)
        actionLoad.setShortcut("Ctrl+L")
        actionExit = QtWidgets.QAction("Exit", self)
        actionExit.setShortcut("Ctrl+E")
        actionRecords = QtWidgets.QAction("Records", self)
        actionRecords.setShortcut("Ctrl+Alt+R")
        actionAbout = QtWidgets.QAction("About", self)
        actionAbout.setShortcut("F1")

        gameMenu.addAction(actionNew_game)
        gameMenu.addAction(actionRestart)
        gameMenu.addAction(actionSave)
        gameMenu.addAction(actionLoad)
        gameMenu.addSeparator()
        gameMenu.addAction(actionExit)

        toolsMenu.addAction(actionRecords)
        helpMenu.addAction(actionAbout)
        menubar.addAction(gameMenu.menuAction())
        menubar.addAction(toolsMenu.menuAction())
        menubar.addAction(helpMenu.menuAction())

        actionNew_game.triggered.connect(self._new_game)
        actionRestart.triggered.connect(self._restart)
        actionSave.triggered.connect(self._save)
        actionLoad.triggered.connect(self._load)
        actionExit.triggered.connect(self.close)
        actionRecords.triggered.connect(self._records)
        actionAbout.triggered.connect(self._about)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _new_game(self):
        d = QtWidgets.QDialog(self)
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.show()

    def _restart(self):
        print("Game was restarted")

    def _save(self):
        filename, d = QtWidgets.QFileDialog(self).getSaveFileName()
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.show()

    def _load(self):
        filename, d = QtWidgets.QFileDialog(self).getOpenFileName()
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.show()

    def _records(self):
        print("1")

    def _about(self):
        print("help")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    reversi = MainWindow()
    sys.exit(app.exec())

