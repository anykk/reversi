import sys
import logging


MAIN_LOG = logging.getLogger("reversi")
logging.basicConfig(filename="reversi.log")


try:
    from driver import *
except Exception as e:
    print(f"Game modules not found: \"{e}\"", file=sys.stderr)
    MAIN_LOG.error(e)
    sys.exit()

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except Exception as e:
    print(f"PyQt5 not found: {e}. Please use pip install command for install this package.",
          file=sys.stderr)
    MAIN_LOG.error(e)
    sys.exit()


class MainWindow(QtWidgets.QWidget):
    """docstring"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Reversi")
        self.setFixedSize(640, 480)
        self.center()

        self.central = Frame(Reversi(size=4, opponent="Ai"), self)

        white_lcd = QtWidgets.QLCDNumber(self)
        black_lcd = QtWidgets.QLCDNumber(self)

        white_label = QtWidgets.QLabel("White:", self)
        black_label = QtWidgets.QLabel("Black:", self)

        button_new_game = QtWidgets.QPushButton("New game")
        button_restart = QtWidgets.QPushButton("Restart")
        button_save_game = QtWidgets.QPushButton("Save")
        button_load_game = QtWidgets.QPushButton("Load")
        button_exit = QtWidgets.QPushButton("Exit")

        layout = QtWidgets.QGridLayout()

        white_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        black_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        layout.addWidget(self.central, 0, 0, 48, 48)
        layout.addWidget(white_label, 1, 50, 3, 9)
        layout.addWidget(white_lcd, 4, 50, 5, 9)
        layout.addWidget(black_label, 13, 50, 3, 9)
        layout.addWidget(black_lcd, 16, 50, 5, 9)

        self.central.setFocusPolicy(QtCore.Qt.StrongFocus)

        layout.addWidget(button_new_game, 25, 50, 3, 9)
        layout.addWidget(button_restart, 28, 50, 3, 9)
        layout.addWidget(button_save_game, 31, 50, 3, 9)
        layout.addWidget(button_load_game, 34, 50, 3, 9)
        layout.addWidget(button_exit, 37, 50, 3, 9)

        button_new_game.clicked.connect(self._new_game)
        button_restart.clicked.connect(self._restart)
        button_save_game.clicked.connect(self._save)
        button_load_game.clicked.connect(self._load)
        button_exit.clicked.connect(self.close)

        self.setLayout(layout)
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _new_game(self):
        # dialog
        # parameters
        pass

    def _restart(self):
        # new Frame with start parameters
        pass

    def _save(self):
        filename, _ = QtWidgets.QFileDialog(self).getSaveFileName(self, "Save game",
                                                                  f"game_name",
                                                                  "JSON files (*.json)")
        try:
            if filename:
                self.central.game.save(filename)
        except SaveError as e:
            MAIN_LOG.error(e)
            QtWidgets.QMessageBox.warning(self, "Error", f"Save error: {e}.", QtWidgets.QMessageBox.Ok)

    def _load(self):
        filename, _ = QtWidgets.QFileDialog(self).getOpenFileName(self, "Load game",
                                                                  f"game_name",
                                                                  "JSON files (*.json)")
        try:
            if filename:
                self.central.game.load(filename)
        except LoadError as e:
            MAIN_LOG.error(e)

    def _about(self):
        # help
        print("help")


class Frame(QtWidgets.QFrame):
    """docstring"""
    def __init__(self, driver, parent=None):
        super().__init__(parent)
        self._score_signal = QtCore.pyqtSignal(tuple)
        self._game = driver
        self.setFixedSize(460, 460)

    @property
    def game(self):
        return self._game

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
        try:
            coords = (self.pixels_to_field(event.x(), event.y()))
            self._game.make_move(coords)
            self.repaint()
            if self._game.opponent == "Ai":
                try:
                    self._game.ai_move()
                except NoMovesException:
                    QtWidgets.QMessageBox.warning(self, "Warning", "Next player can't move.", QtWidgets.QMessageBox.Ok)
                    self._game.ai_move()
                self.repaint()
        except NoMovesException:
            QtWidgets.QMessageBox.warning(self, "Warning", "Next player can't move.", QtWidgets.QMessageBox.Ok)
            return
        except MoveError:
            return
        except GameOverException:
            QtWidgets.QMessageBox.warning(self, "Game over", "Player won.", QtWidgets.QMessageBox.Ok)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    reversi = MainWindow()
    # a = Frame(Reversi(size=4, opponent="Ai"))
    # a.show()
    sys.exit(app.exec())
