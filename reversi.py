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
        self.params, self.driver = self._new_game()
        self.central = Frame(self.driver, self)

        self.white_lcd = QtWidgets.QLCDNumber(self)
        self.black_lcd = QtWidgets.QLCDNumber(self)

        self.white_label = QtWidgets.QLabel("White:", self)
        self.black_label = QtWidgets.QLabel("Black:", self)

        self.button_new_game = QtWidgets.QPushButton("New game")
        self.button_restart = QtWidgets.QPushButton("Restart")
        self.button_save_game = QtWidgets.QPushButton("Save")
        self.button_load_game = QtWidgets.QPushButton("Load")
        self.button_exit = QtWidgets.QPushButton("Exit")

        self.layout = QtWidgets.QGridLayout()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Reversi")
        self.setFixedSize(640, 480)
        self.center()

        self.white_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.black_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        self.layout.addWidget(self.central, 0, 0, 48, 48)
        self.layout.addWidget(self.white_label, 1, 50, 3, 9)
        self.layout.addWidget(self.white_lcd, 4, 50, 5, 9)
        self.layout.addWidget(self.black_label, 13, 50, 3, 9)
        self.layout.addWidget(self.black_lcd, 16, 50, 5, 9)

        self.setLayout(self.layout)

        self.central.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.layout.addWidget(self.button_new_game, 25, 50, 3, 9)
        self.layout.addWidget(self.button_restart, 28, 50, 3, 9)
        self.layout.addWidget(self.button_save_game, 31, 50, 3, 9)
        self.layout.addWidget(self.button_load_game, 34, 50, 3, 9)
        self.layout.addWidget(self.button_exit, 37, 50, 3, 9)

        self.button_new_game.clicked.connect(self._new_game)
        self.button_restart.clicked.connect(self._restart)
        self.button_save_game.clicked.connect(self._save)
        self.button_load_game.clicked.connect(self._load)
        self.button_exit.clicked.connect(self.close)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _new_game(self):
        dialog = StartDialog()
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.show()
        params = dialog.get_params()
        return params, Reversi(*params)

    def _restart(self):
        pass

    def _save(self):
        filename, _ = QtWidgets.QFileDialog(self).getSaveFileName(self, "Save game",
                                                                  f"game_name",
                                                                  "JSON files (*.json)")
        try:
            if filename:
                self.central.driver.save(filename)
        except SaveError as e:
            MAIN_LOG.error(e)

    def _load(self):
        filename, _ = QtWidgets.QFileDialog(self).getOpenFileName(self, "Load game",
                                                                  f"game_name",
                                                                  "JSON files (*.json)")
        try:
            if filename:
                self.central.driver.load(filename)
        except LoadError as e:
            MAIN_LOG.error(e)

    def _about(self):
        # help
        print("help")


class Frame(QtWidgets.QFrame):
    """docstring"""
    def __init__(self, driver, parent=None):
        super().__init__(parent)

        self._driver = driver
        self.setFixedSize(460, 460)

    @property
    def driver(self):
        return self._driver

    def paintEvent(self, event):
        # draw
        qp = QtGui.QPainter(self)
        qp.setBrush(QtGui.QColor(255, 255, 204))
        qp.drawRect(QtCore.QRectF(0, 0, self.height(), self.width()))

        for i in range(self._driver.field.size):
            # draw field lines
            x = self.width() / self._driver.field.size * i
            qp.drawLine(x, 0, x, self.height())

            y = self.height() / self._driver.field.size * i
            qp.drawLine(0, y, self.width(), y)

        for height in range(self._driver.field.size):
            for width in range(self._driver.field.size):
                # draw disks
                w = self.width() / self._driver.field.size
                h = self.height() / self._driver.field.size

                y = h * height
                x = w * width

                rect = QtCore.QRectF(x, y, w, h)

                disk = self._driver.field[height, width]
                if disk == WHITE:
                    qp.setBrush(QtGui.QColor(255, 255, 255))
                    qp.drawEllipse(rect)
                if disk == BLACK:
                    qp.setBrush(QtGui.QColor(0, 0, 0))
                    qp.drawEllipse(rect)

        for y, x in self._driver.get_correct_moves():
            # draw possible moves
            w = self.width() / self._driver.field.size
            h = self.height() / self._driver.field.size
            rect = QtCore.QRectF(x * w, y * h, w, h)
            qp.setBrush(QtGui.QColor(255, 255, 153))
            qp.drawRect(rect)

    def pixels_to_field(self, x, y):
        # x and y in window but y and x in Field [n*n list]
        field_width = self.width() // self._driver.field.size
        field_height = self.height() // self._driver.field.size
        return y // field_height, x // field_width

    def mousePressEvent(self, event):
        try:
            coords = (self.pixels_to_field(event.x(), event.y()))
            self._driver.make_move(coords)
            if self._driver.mode == "AI":
                self.repaint()
                self._driver.ai_move()
            self.update()
        except MoveError:
            return
        except GameOverException:
            self.update()


class StartDialog(QtWidgets.QDialog):
    """docstring"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.params = {"size": None, "player": None, "mode": None}
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.size_label = QtWidgets.QLabel("Choose field size: ", self)
        self.size_box = QtWidgets.QSpinBox(self)
        self.size_box.valueChanged.connect(self.size)
        self.size_box.setValue(8)

        self.main_layout.addWidget(self.size_label)
        self.main_layout.addWidget(self.size_box)

        self.color_box = QtWidgets.QGroupBox("Choose color: ", self)
        self.color_layout = QtWidgets.QHBoxLayout(self.color_box)
        self.black_button = QtWidgets.QRadioButton("Black", self.color_box)
        self.black_button.toggled.connect(self.black)
        self.white_button = QtWidgets.QRadioButton("White", self.color_box)
        self.white_button.toggled.connect(self.white)
        self.black_button.setChecked(True)

        self.color_box.setLayout(self.color_layout)

        self.color_layout.addWidget(self.black_button)
        self.color_layout.addWidget(self.white_button)

        self.main_layout.addWidget(self.color_box)

        """
        self.type_box = QtWidgets.QGroupBox("Choose type: ", self)
        self.type_layout = QtWidgets.QHBoxLayout(self.type_box)
        self.color_box.setLayout(self.type_layout)
        """

        self.mode_box = QtWidgets.QGroupBox("Choose mode: ", self)
        self.mode_layout = QtWidgets.QHBoxLayout(self.mode_box)
        self.ai_button = QtWidgets.QRadioButton("AI", self.mode_box)
        self.ai_button.toggled.connect(self.ai)
        self.hotseat_button = QtWidgets.QRadioButton("HotSeat", self.mode_box)
        self.hotseat_button.toggled.connect(self.hotseat)
        self.ai_button.setChecked(True)

        self.color_box.setLayout(self.mode_layout)

        self.mode_layout.addWidget(self.ai_button)
        self.mode_layout.addWidget(self.hotseat_button)

        self.main_layout.addWidget(self.mode_box)

        self.ok_button = QtWidgets.QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.get_params)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)

        self.main_layout.addWidget(self.ok_button)
        self.main_layout.addWidget(self.cancel_button)

        self.setLayout(self.main_layout)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Config")
        """

        ui

        """
        self.show()

    def size(self):
        self.params["size"] = self.size_box.value()

    def black(self):
        self.params["player"] = BLACK

    def white(self):
        self.params["player"] = WHITE

    def ai(self):
        self.params["mode"] = "AI"

    def hotseat(self):
        self.params["mode"] = "HotSeat"

    def get_params(self):
        if not self.params["size"] % 2 == 0:
            QtWidgets.QMessageBox.information(self, 'Error', 'Incorrect size', QtWidgets.QMessageBox.Ok)
            return
        return self.params.values()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # reversi = MainWindow()
    dialog = StartDialog()
    sys.exit(app.exec())
