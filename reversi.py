import sys
import logging
import pickle

LOGGER = logging.getLogger("reversi")
logging.basicConfig(filename="reversi.log", level=logging.INFO)

try:
    from driver import *
except Exception as e:
    LOGGER.error(e)
    sys.exit(f"Game modules not found: \"{e}\"")

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except Exception as e:
    LOGGER.error(e)
    sys.exit(f"PyQt5 not found: {e}. Please use pip install command for install this package.")


class MainWindow(QtWidgets.QWidget):
    """Main reversi window."""
    def __init__(self, parent=None):
        super().__init__(parent)
        LOGGER.info("Main window was initialized.")
        self._dialog = StartDialog()
        self._dialog.ok_button.clicked.connect(self._new_game)
        self._frame = Frame(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Reversi")
        self.setFixedSize(640, 480)
        self.center()

        white_lcd = QtWidgets.QLCDNumber(self)
        self._frame.white_score_msg[str].connect(white_lcd.display)
        black_lcd = QtWidgets.QLCDNumber(self)
        self._frame.black_score_msg[str].connect(black_lcd.display)

        current_turn_label = QtWidgets.QLabel(self)
        self._frame.current_player_msg[str].connect(current_turn_label.setText)

        white_label = QtWidgets.QLabel("White:", self)
        black_label = QtWidgets.QLabel("Black:", self)

        button_new_game = QtWidgets.QPushButton("New game")
        button_restart = QtWidgets.QPushButton("Restart")
        button_save_game = QtWidgets.QPushButton("Save")
        button_load_game = QtWidgets.QPushButton("Load")
        button_about = QtWidgets.QPushButton("About")
        button_exit = QtWidgets.QPushButton("Exit")

        layout = QtWidgets.QGridLayout()

        white_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        black_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        layout.addWidget(self._frame, 0, 0, 48, 48)
        layout.addWidget(current_turn_label, 1, 50, 2, 9)
        layout.addWidget(white_label, 3, 50, 3, 9)
        layout.addWidget(white_lcd, 7, 50, 5, 9)
        layout.addWidget(black_label, 14, 50, 3, 9)
        layout.addWidget(black_lcd, 18, 50, 5, 9)

        self._frame.setFocusPolicy(QtCore.Qt.StrongFocus)

        layout.addWidget(button_new_game, 25, 50, 3, 9)
        layout.addWidget(button_restart, 28, 50, 3, 9)
        layout.addWidget(button_save_game, 31, 50, 3, 9)
        layout.addWidget(button_load_game, 34, 50, 3, 9)
        layout.addWidget(button_about, 37, 50, 3, 9)
        layout.addWidget(button_exit, 40, 50, 3, 9)

        button_new_game.clicked.connect(self._dialog.show)
        button_restart.clicked.connect(self._restart)
        button_save_game.clicked.connect(self._save)
        button_load_game.clicked.connect(self._load)
        button_about.clicked.connect(self._about)
        button_exit.clicked.connect(self.close)

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _new_game(self):
        """Create new game with chose parameters."""
        self.hide()
        self._dialog.show()
        self._start_params = self._dialog.params
        self._dialog.hide()
        self._frame._game = Reversi(**self._start_params)
        self._frame.send_messages()
        self.update()
        self.show()

    def _restart(self):
        """Restart game with start parameters."""
        self._frame._game = Reversi(**self._start_params)
        self._frame.send_messages()
        self.update()
        LOGGER.info(f"Game was restarted with {self._start_params} parameters.")

    def _save(self):
        """Save game to .dat file."""
        filename, _ = QtWidgets.QFileDialog(self).getSaveFileName(self, "Save game",
                                                                  f"game_name",
                                                                  "DAT files (*.dat)")
        try:
            if filename:
                with open(filename, 'wb') as file:
                    pickle.dump(self._frame.game, file)
                    LOGGER.info(f"Game was saved into {filename} file.")
        except SaveError as exception:
            LOGGER.warning(exception)
            QtWidgets.QMessageBox.warning(self, "Error", f"Save error: {exception}.", QtWidgets.QMessageBox.Ok)

    def _load(self):
        """Load game from .dat file"""
        filename, _ = QtWidgets.QFileDialog(self).getOpenFileName(self, "Load game",
                                                                  f"game_name",
                                                                  "DAT files (*.dat)")
        try:
            if filename:
                with open(filename, 'rb') as file:
                    object_ = pickle.load(file)
                    if not type(object_) == Reversi:
                        raise LoadError("Incorrect .dat game file.")
                    self._frame._game = object_
                    self._frame.send_messages()
                    self.update()
                    LOGGER.info(f"Game was loaded from {filename} file.")
        except LoadError as exception:
            LOGGER.warning(exception)
            QtWidgets.QMessageBox.warning(self, "Error", f"Save error: {exception}.", QtWidgets.QMessageBox.Ok)

    def _about(self):
        QtWidgets.QMessageBox.information(self, "About the game",
                                          "This is python implementation of the Reversi/Othello game. "
                                          "You have simple rules if you chose classic mode: you can place "
                                          "your disk only any through a continuous series of opponent's disks, "
                                          "after them, you flip it and up your score. In extra mode both of players "
                                          "have different count of common disks - strategic blocks. Their count is "
                                          "limited, it depends on field size.",
                                          QtWidgets.QMessageBox.Ok)


class Frame(QtWidgets.QFrame):
    """Game widget."""
    white_score_msg = QtCore.pyqtSignal(str)
    black_score_msg = QtCore.pyqtSignal(str)
    current_player_msg = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, **params):
        super().__init__(parent)
        self._game = Reversi(**params)
        self.setFixedSize(460, 460)
        LOGGER.info(f"Game frame was initialized with {params} parameters.")

    @property
    def game(self):
        """Game property"""
        return self._game

    def send_messages(self):
        """Send messages to main window."""
        self.white_score_msg.emit(str(self._game.field.white_count))
        self.black_score_msg.emit(str(self._game.field.black_count))
        self.current_player_msg.emit("Current turn: " + self._game.str_player)
        LOGGER.info("Messages was sent from game frame to main window.")

    def paintEvent(self, event):
        # draw background
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
                if disk == EXTRA:
                    qp.setBrush(QtGui.QColor(178, 34, 34))
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
            if self._game.mode == "Extra":
                if event.button() == QtCore.Qt.LeftButton:
                    self._game.make_move(coords)
                elif event.button() == QtCore.Qt.RightButton:
                    self._game.place_extra(coords)
            else:
                self._game.make_move(coords)
            LOGGER.info(f"{self.game.str_player} made move to {coords} place.")
            self.send_messages()
            self.repaint()
            if self._game.opponent == "Ai":
                try:
                    self._game.ai_move()
                    LOGGER.info(f"{self.game.str_player} made move to {coords} place.")
                    self.send_messages()
                except NoMovesException:
                    LOGGER.info(f"No moves for {self._game.str_player}'s opponent")
                    QtWidgets.QMessageBox.warning(self, "Warning",
                                                  "Next player can't move.", QtWidgets.QMessageBox.Ok)
                    self._game.ai_move()
                    LOGGER.info(f"{self.game.str_player} made move to {coords} place.")
                    self.send_messages()
                self.repaint()
        except NoMovesException:
            LOGGER.info(f"No moves for {self._game.str_player}'s opponent")
            QtWidgets.QMessageBox.warning(self, "Warning",
                                          "Next player can't move.", QtWidgets.QMessageBox.Ok)
            return
        except MoveError:
            return
        except HaveNotExtraException:
            QtWidgets.QMessageBox.warning(self, "Warning",
                                          "Players haven't extra disks anymore.", QtWidgets.QMessageBox.Ok)
        except GameOverException:
            self.send_messages()
            self.current_player_msg.emit("Game over!")
            LOGGER.info(f"Game over. {self._game.winner}.")
            QtWidgets.QMessageBox.information(self, "Game over",
                                              f"'{self._game.winner}", QtWidgets.QMessageBox.Ok)


class StartDialog(QtWidgets.QDialog):
    """Start dialog window"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._params = {}
        self.init_ui()
        LOGGER.info("Start dialog was initialized.")

    @property
    def params(self):
        """Returns params from dialog."""
        return self._params

    def init_ui(self):
        self.setWindowTitle("Config")
        main_layout = QtWidgets.QVBoxLayout(self)

        self.size_label = QtWidgets.QLabel("Choose field size: ", self)
        self.size_box = QtWidgets.QSpinBox(self)
        self.size_box.valueChanged.connect(self.set_size_value)
        self.size_box.lineEdit().setReadOnly(True)
        self.size_box.setRange(4, 30)
        self.size_box.setSingleStep(2)
        self.size_box.setValue(8)

        main_layout.addWidget(self.size_label)
        main_layout.addWidget(self.size_box)

        player_box = QtWidgets.QGroupBox("Choose first player: ", self)
        player_layout = QtWidgets.QHBoxLayout(player_box)
        self.black_button = QtWidgets.QRadioButton("Black", player_box)
        self.black_button.toggled.connect(self.set_black)
        self.white_button = QtWidgets.QRadioButton("White", player_box)
        self.white_button.toggled.connect(self.set_white)
        self.black_button.setChecked(True)

        player_layout.addWidget(self.black_button)
        player_layout.addWidget(self.white_button)
        player_box.setLayout(player_layout)

        main_layout.addWidget(player_box)

        mode_box = QtWidgets.QGroupBox("Choose game mode: ", self)
        mode_layout = QtWidgets.QHBoxLayout(mode_box)
        self.classic_button = QtWidgets.QRadioButton("Classic", mode_box)
        self.classic_button.toggled.connect(self.set_classic)
        self.extra_button = QtWidgets.QRadioButton("Extra", mode_box)
        self.extra_button.toggled.connect(self.set_extra)
        self.classic_button.setChecked(True)

        mode_layout.addWidget(self.classic_button)
        mode_layout.addWidget(self.extra_button)
        mode_box.setLayout(mode_layout)

        main_layout.addWidget(mode_box)

        opponent_box = QtWidgets.QGroupBox("Choose opponent type: ", self)
        opponent_layout = QtWidgets.QHBoxLayout(opponent_box)
        self.ai_button = QtWidgets.QRadioButton("AI", opponent_box)
        self.ai_button.toggled.connect(self.set_ai)
        self.human_button = QtWidgets.QRadioButton("Human", opponent_box)
        self.human_button.toggled.connect(self.set_human)
        self.ai_button.setChecked(True)

        opponent_layout.addWidget(self.ai_button)
        opponent_layout.addWidget(self.human_button)
        opponent_box.setLayout(opponent_layout)

        main_layout.addWidget(opponent_box)

        lvl_box = QtWidgets.QGroupBox("Choose AI lvl: ", self)
        lvl_layout = QtWidgets.QHBoxLayout(lvl_box)
        self.easy_button = QtWidgets.QRadioButton("Easy", lvl_box)
        self.easy_button.toggled.connect(self.set_easy)
        self.medium_button = QtWidgets.QRadioButton("Medium", lvl_box)
        self.medium_button.toggled.connect(self.set_medium)
        self.hard_button = QtWidgets.QRadioButton("Hard", lvl_box)
        self.hard_button.toggled.connect(self.set_hard)

        lvl_layout.addWidget(self.easy_button)
        lvl_layout.addWidget(self.medium_button)
        lvl_layout.addWidget(self.hard_button)

        main_layout.addWidget(lvl_box)

        self.ok_button = QtWidgets.QPushButton("Ok", self)

        main_layout.addWidget(self.ok_button)

        self.setLayout(main_layout)
        self.show()

    def set_size_value(self):
        """Store size value."""
        self._params["size"] = int(self.size_box.value())

    def set_black(self):
        """Set player parameter to black."""
        self._params["player"] = BLACK

    def set_white(self):
        """Set player parameter to white."""
        self._params["player"] = WHITE

    def set_ai(self):
        """Set opponent parameter to AI."""
        self._params["opponent"] = "Ai"

    def set_human(self):
        """Set opponent parameter to Human."""
        self._params["opponent"] = "Human"

    def set_classic(self):
        """Set mode parameter to classic."""
        self._params["mode"] = "Classic"

    def set_extra(self):
        """Set mode parameter to extra."""
        self._params["mode"] = "Extra"

    def set_easy(self):
        """Set AI lvl to easy."""
        if not self.ai_button.isChecked():
            self.easy_button.setCheckable(False)
        self.easy_button.setCheckable(True)
        self._params["lvl"] = "Easy"

    def set_medium(self):
        """Set AI lvl to medium."""
        if not self.ai_button.isChecked():
            self.medium_button.setCheckable(False)
        self.medium_button.setCheckable(True)
        self._params["lvl"] = "Medium"

    def set_hard(self):
        """Set AI lvl to hard."""
        if not self.ai_button.isChecked():
            self.hard_button.setCheckable(False)
        self.hard_button.setCheckable(True)
        self._params["lvl"] = "Hard"


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    game = MainWindow()
    sys.exit(app.exec())
