import sys
from os import sep
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from src.driver import *


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Reversi")
        self.setFixedSize(640, 480)
        self.center()

        game = Frame(parent=self)
        game.setFrameStyle(QtWidgets.QFrame.Box)

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
    def __init__(self, parent=None, size=8, player=BLACK, ai=True):
        super().__init__(parent=parent)
        self._game = Reversi(size, player, ai)
        self._game_over = False

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.fillRect(QtCore.QRect(0, 0, self.height() + 16, self.width() + 16), QtGui.QColor(51, 204, 51))

        for i in range(self._game.field().size()):
            x = self.width() / self._game.field().size() * i
            qp.drawLine(x, 0, x, self.height())

            y = self.height() / self._game.field().size() * i
            qp.drawLine(0, y, self.width(), y)

        for height in range(self._game.field().size()):
            for width in range(self._game.field().size()):
                pieces_path = QtGui.QPainterPath()
                w = self.width() / self._game.field().size()
                h = self.height() / self._game.field().size()

                x = w * width
                y = h * height

                bounding_rect = QtCore.QRectF(x, y, w, h)

                piece = self._game.field()[height, width]
                if piece == WHITE:
                    pieces_path.addEllipse(bounding_rect)
                    qp.fillPath(pieces_path, QtGui.QColor(255, 255, 255))
                if piece == BLACK:
                    pieces_path.addEllipse(bounding_rect)
                    qp.fillPath(pieces_path, QtGui.QColor(0, 0, 0))

    def pixels_to_field(self, x, y):
        field_width = self.width() // self._game.field().size()
        field_height = self.height() // self._game.field().size()
        return x // field_width, y // field_height

    def mousePressEvent(self, event):
        if self._game_over:
            return

        if not len(self._game.get_correct_moves()):
            return

        if self._game.ai() and self._game.current_player() == BLACK:
            try:
                coords = self.pixels_to_field(event.y(), event.x())
                self._game.make_move(coords)
                self.repaint()
                self._game.ai_move()
                self.repaint()
            except IndexError:
                pass
        else:
            try:
                self._game.ai_move()
                self.update()
                coords = self.pixels_to_field(event.y(), event.x())
                self._game.make_move(coords)
                self.update()
            except IndexError:
                pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    reversi = MainWindow()
    sys.exit(app.exec())