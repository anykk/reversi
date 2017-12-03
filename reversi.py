import sys
from os import sep

try:
    from src.driver import *
except Exception as e:
    print("Game modules not found: \"{e}\"", file=sys.stderr)
    sys.exit()

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except Exception as e:
    print(f"PyQt5 not found: \"{e}\". Please use pip install command for install this package.",
          file=sys.stderr)
    sys.exit()

import sys
from os import sep
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from src.driver import *


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Reversi")
        self.setFixedSize(640, 480)
        self.center()

        game = Frame(8, BLACK, True, self)

        white_lcd = QtWidgets.QLCDNumber(self)
        black_lcd = QtWidgets.QLCDNumber(self)
        white_label = QtWidgets.QLabel("White:", self)
        white_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        black_label = QtWidgets.QLabel("Black:", self)
        black_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(game, 0, 0, 48, 48)
        layout.addWidget(white_label, 1, 50, 3, 9)
        layout.addWidget(white_lcd, 4, 50, 5, 9)
        layout.addWidget(black_label, 13, 50, 3, 9)
        layout.addWidget(black_lcd, 16, 50, 5, 9)

        self.setLayout(layout)

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

    def __init__(self, size, player, ai, parent=None):
        super().__init__(parent)
        self._game = Reversi(size, player, ai)
        self._game_over = False
        self.setFixedSize(460, 460)

    def paintEvent(self, event):
        # draw
        qp = QtGui.QPainter(self)
        qp.setBrush(QtGui.QColor(255, 255, 204))
        qp.drawRect(QtCore.QRectF(0, 0, self.height(), self.width()))

        for i in range(self._game.field.size):
            # draw field lines
            x = self.width() / self._game.field.size * i
            qp.drawLine(x, 0, x, self.height())

            y = self.height() / self._game.field.size * i
            qp.drawLine(0, y, self.width(), y)

        for height in range(self._game.field.size):
            for width in range(self._game.field.size):
                # draw disks
                w = self.width() / self._game.field.size
                h = self.height() / self._game.field.size

                y = h * height
                x = w * width

                rect = QtCore.QRectF(x, y, w, h)

                disk = self._game.field[height, width]
                if disk == WHITE:
                    qp.setBrush(QtGui.QColor(255, 255, 255))
                    qp.drawEllipse(rect)
                if disk == BLACK:
                    qp.setBrush(QtGui.QColor(0, 0, 0))
                    qp.drawEllipse(rect)

        for y, x in self._game.get_correct_moves():
            # draw possible moves
            w = self.width() / self._game.field.size
            h = self.height() / self._game.field.size
            rect = QtCore.QRectF(x * w, y * h, w, h)
            qp.setBrush(QtGui.QColor(255, 255, 153))
            qp.drawRect(rect)

    def pixels_to_field(self, x, y):
        # x and y in window but y and x in Field [n*n list]
        field_width = self.width() // self._game.field.size
        field_height = self.height() // self._game.field.size
        return y // field_height, x // field_width

    def mousePressEvent(self, event):
        if not self._game_over:
            try:
                coords = (self.pixels_to_field(event.x(), event.y()))
                self._game.make_move(coords)
                if self._game.ai:
                    self.repaint()
                    self._game.ai_move()
                self.update()
            except ValueError:
                return
            except RuntimeError:
                self._game_over = True
                self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    reversi = MainWindow()
    sys.exit(app.exec())
