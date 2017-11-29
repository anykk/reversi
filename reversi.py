import sys
from os import sep
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from src.driver import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Reversi")
        self.setFixedSize(640, 480)
        self.center()

        window = QtWidgets.QWidget(parent=self)
        game = Frame(parent=window)
        self.setCentralWidget(window)

        white_lcd = QtWidgets.QLCDNumber(window)
        black_lcd = QtWidgets.QLCDNumber(window)
        white_label = QtWidgets.QLabel("White:", window)
        white_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        black_label = QtWidgets.QLabel("Black:", window)
        black_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(game, 0, 0, 48, 48)
        layout.addWidget(white_label, 1, 50, 3, 9)
        layout.addWidget(white_lcd, 4, 50, 5, 9)
        layout.addWidget(black_label, 13, 50, 3, 9)
        layout.addWidget(black_lcd, 16, 50, 5, 9)

        window.setLayout(layout)

        game.setFocusPolicy(QtCore.Qt.StrongFocus)

        buttonNew_game = QtWidgets.QPushButton("New game")
        buttonRestart = QtWidgets.QPushButton("Restart")
        buttonSave_game = QtWidgets.QPushButton("Save")
        buttonLoad_game = QtWidgets.QPushButton("Load")
        buttonExit = QtWidgets.QPushButton("Exit")

        layout.addWidget(buttonNew_game, 25, 50, 3, 9)
        layout.addWidget(buttonRestart, 28, 50, 3, 9)
        layout.addWidget(buttonSave_game, 31, 50, 3, 9)
        layout.addWidget(buttonLoad_game, 34, 50, 3, 9)
        layout.addWidget(buttonExit, 37, 50, 3, 9)

        buttonNew_game.clicked.connect(self._new_game)
        buttonRestart.clicked.connect(self._restart)
        buttonSave_game.clicked.connect(self._save)
        buttonLoad_game.clicked.connect(self._load)
        buttonExit.clicked.connect(self.close)

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
        filename, _ = QtWidgets.QFileDialog(self).getSaveFileName(self, "Save game",
                                                                  f".{sep}loads",
                                                                  "Text files (*.txt)")
        print(filename)

    def _load(self):
        filename, _ = QtWidgets.QFileDialog(self).getOpenFileName(self, "Load game",
                                                                  f".{sep}loads",
                                                                  "Text files (*.txt)")
        print(filename)

    def _records(self):
        print("1")

    def _about(self):
        print("help")


class Frame(QtWidgets.QFrame):
    """docstring"""
    def __init__(self, size=8, player=BLACK, parent=None):
        super().__init__(parent)
        self._game = Reversi(size, player)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        grid = QtGui.QPainterPath()
        grid.addRect(0, 0, self.height(), self.width())
        qp.fillPath(grid, QtGui.QColor(51, 204, 51))

        for i in range(len(self._game._field)):
            x = self.width() / len(self._game._field) * i
            qp.drawLine(x, 0, x, self.height())

            y = self.height() / len(self._game._field) * i
            qp.drawLine(0, y, self.width(), y)

        for height in range(len(self._game._field)):
            for width in range(len(self._game._field)):
                pieces_path = QtGui.QPainterPath()
                w = self.width() / len(self._game._field)
                h = self.height() / len(self._game._field)

                x = w * width
                y = h * height

                bounding_rect = QtCore.QRectF(x, y, w, h)

                piece = self._game._field[height, width]
                if piece == WHITE:
                    pieces_path.addEllipse(bounding_rect)
                    qp.fillPath(pieces_path, QtGui.QColor(255, 255, 255))
                elif piece == BLACK:
                    pieces_path.addEllipse(bounding_rect)
                    qp.fillPath(pieces_path, QtGui.QColor(0, 0, 0))

    def pixels_to_field(self, x, y):
        field_width = self.width() // len(self._game._field)
        field_height = self.height() // len(self._game._field)
        return x // field_width, y // field_height

    def mousePressEvent(self, event):
        self._game.make_move(self.pixels_to_field(event.y(), event.x()))
        self.repaint()
        self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    reversi = MainWindow()
    sys.exit(app.exec())

