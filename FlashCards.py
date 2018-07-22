from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QLabel
import sys
from random import shuffle
import docx2txt

"""
    This program is created for flashcards suitable for studying.
    It takes information from a .docx file and creates the front- and backside 
    of the study card in the following manner:
    
    Bacon - Something incredible tasty!
    
    'Bacon' becomes the front of the card and 'Something incredible tasty!' becomes the backside.
    Using the GUI the user can press three different buttons to navigate through the dock. 
    
    ---BUTTONS---
    'Show' - Switches between the front and the backside of the cards.
    'No' - Places the top card back in the deck and shuffles it.
    'Yes' - Removes the top card of the study deck and places in a separate deck for completed cards.
    
    Author: Elias Johansson
    
"""


class Deck:
    def __init__(self):
        self.deck = []
        self.size = 0

        # ----Get list elements from add_cards function----
        self.add_cards()

    def get_card(self, index):
        return self.deck[index]

    def add_cards(self):
        my_text = docx2txt.process("C:\\Users\\Elias\\Desktop\\School\\Nätverk\\FlashCards_Network.docx")
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

    def remove_card(self, index):
        del self.deck[index]

    def shuffle(self):
        shuffle(self.deck)


class Cards:
    def __init__(self, frontside, backside):
        self.frontside = frontside
        self.backside = backside

    def get_frontside(self):
        return self.frontside

    def get_backside(self):
        return self.backside


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.show_flag = False
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
        self.word_label.setText(deck.get_card(0).get_frontside())

        self.setup_ui()

    def setup_ui(self):
        # ----Link buttons to the corresponding functions----
        self.b_show.clicked.connect(self.b_show_click)
        self.b_no.clicked.connect(self.b_no_click)
        self.b_yes.clicked.connect(self.b_yes_click)

        self.h_box.addWidget(self.word_label)
        self.h_box.addWidget(self.b_show)
        self.h_box.addWidget(self.b_no)
        self.h_box.addWidget(self.b_yes)

        self.setLayout(self.h_box)
        self.setWindowTitle('Study Cards')
        self.show()

    def b_show_click(self):
        if not self.show_flag:
            self.word_label.setText(deck.get_card(0).get_backside())
            self.show_flag = True
        elif self.show_flag:
            self.word_label.setText(deck.get_card(0).get_frontside())
            self.show_flag = False

    def b_yes_click(self):
        completed.append(deck.get_card(0))  # Adds the card to the list of uncompleted FlashCards.
        deck.remove_card(0)
        self.word_label.setText(deck.get_card(0).get_frontside())

    def b_no_click(self):
        deck.shuffle()
        self.word_label.setText(deck.get_card(0).get_frontside())


deck = Deck()  # Creates the deck containing cards filled with information from a .docx file.
uncompleted = []
completed = []

app = QtWidgets.QApplication(sys.argv)
a_window = Window()
a_window.resize(700, 700)
sys.exit(app.exec())
