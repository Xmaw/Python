from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
import sys

import docx2txt


class Deck:
    def __init__(self):
        self.deck = []
        self.size = 0

        # ----Get list elements from handle_file function----
        self.add_cards()
        print("size: ", self.size)

    def get_card(self, index):
        return self.deck[index]

    def add_cards(self):
        my_text = docx2txt.process("C:\\Users\\Elias\\Desktop\\Hej.docx")
        s = my_text.split("\n\n")
        s_temp = ""
        for word in s:
            s_temp += word + "\n"

        s1_temp = s_temp.split("\n")

        for word in s1_temp:
            s_temp = word.split('-')
            if len(s_temp) == 2:
                self.deck.append(Cards(s_temp[0], s_temp[1]))
                self.size += 1

    def print_size(self):
        print(self.size)


class Cards:
    def __init__(self, frontside, backside):
        self.fronside = frontside
        self.backside = backside

    def get_frontside(self):
        return self.fronside

    def get_backside(self):
        return self.backside


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.show_flag = False
        self.index = 0
        self.b_show = QtWidgets.QPushButton('Show')
        self.b_no = QtWidgets.QPushButton('No')
        self.b_yes = QtWidgets.QPushButton('Yes')
        self.list_word = []
        self.list_explanation = []

        # ----H_BOX to store the widgets in ----
        self.h_box = QtWidgets.QVBoxLayout()

        # ----Labels to display the text ----
        self.word_label = QLabel()
        self.word_label.resize(50, 50)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet("font: 20pt;")
        self.word_label.setWordWrap(True)
        print()
        self.word_label.setText(deck.get_card(self.index).get_frontside())

        self.setup_ui()

    def setup_ui(self):
        # ----Link buttons to the corresponding functions----
        self.b_show.clicked.connect(self.b_show_click)
        self.b_no.clicked.connect(self.b_no_click)
        self.b_yes.clicked.connect(self.b_yes_click)

        # ----Flag for displaying Word or Explenation-----

        self.h_box.addWidget(self.word_label)
        self.h_box.addWidget(self.b_show)
        self.h_box.addWidget(self.b_no)
        self.h_box.addWidget(self.b_yes)

        self.setLayout(self.h_box)
        self.setWindowTitle('Study Cards')
        self.show()

    def b_show_click(self):
        if not self.show_flag:
            self.word_label.setText(deck.get_card(self.index).get_backside())
            self.show_flag = True
        elif self.show_flag:
            self.word_label.setText(deck.get_card(self.index).get_frontside())
            self.show_flag = False

    def b_yes_click(self):
        self.update_index()
        self.word_label.setText(deck.get_card(self.index).get_frontside())

    def b_no_click(self):
        self.update_index()
        self.word_label.setText(deck.get_card(self.index).get_frontside())

    def update_index(self):
        self.index += 1
        if self.index == len(self.list_word):
            self.index = 0


deck = Deck()  # Creates the deck containing cards filled with information from a .docx file.
app = QtWidgets.QApplication(sys.argv)
a_window = Window()
a_window.resize(700, 700)
sys.exit(app.exec())
