from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QGridLayout
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
        self.cards = []

        # ----Get list elements from add_cards function----
        self.file = "C:\\Users\\Elias\\Desktop\\School\\Nätverk\\FlashCards_Network.docx"
        self.load_from_file(self.file)

    def get_card(self, top_card):
        return self.cards[top_card]

    def load_from_file(self, file):
        my_text = docx2txt.process(file)
        for excerpt in my_text.split("\n\n"):
            s_temp = excerpt.split('-')
            if len(s_temp) == 2:
                self.cards.append(Cards(s_temp[0], s_temp[1]))

    def remove_card(self, index):
        del self.cards[index]

    def shuffle(self):
        shuffle(self.cards)

    def get_deck_size(self):
        return len(self.cards)


class Cards:
    def __init__(self, font, back):
        self.font = font
        self.back = back

    def get_front(self):
        return self.font

    def get_back(self):
        return self.back


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.show_flag = False
        self.b_flip = QtWidgets.QPushButton('Flip Card')
        self.b_no = QtWidgets.QPushButton('No')
        self.b_yes = QtWidgets.QPushButton('Yes')

        # ----Text Box ----
        self.v_box = QtWidgets.QVBoxLayout()

        # ----Button Box ----
        self.button_box = QtWidgets.QVBoxLayout()

        # ----Label to display size of deck ----
        self.deck_size_label = QLabel()
        self.deck_size_label.resize(200, 200)
        self.deck_size_label.setText("Cards in deck: " + str(deck.get_deck_size()))
        self.deck_size_label.move(450, 25)

        # ----Labels to display the text of the card ----
        self.word_label = QLabel()
        self.word_label.resize(50, 50)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet("font: 20pt;")
        self.word_label.setWordWrap(True)
        self.word_label.setText(deck.get_card(0).get_front())

        self.setup_ui()

    def setup_ui(self):
        # ----Link buttons to the corresponding functions----
        self.b_flip.clicked.connect(self.b_flip_click)
        self.b_no.clicked.connect(self.b_no_click)
        self.b_yes.clicked.connect(self.b_yes_click)

        self.v_box.addWidget(self.deck_size_label)
        self.v_box.addWidget(self.word_label)
        self.v_box.addStretch()

        self.button_box.addLayout(self.v_box)

        self.button_box.addWidget(self.b_flip)
        self.button_box.addWidget(self.b_yes)
        self.button_box.addWidget(self.b_no)

        self.setLayout(self.button_box)
        self.setWindowTitle('Study Cards')
        self.show()

    def b_flip_click(self):
        if self.show_flag:
            self.word_label.setText(deck.get_card(0).get_back())
            self.show_flag = False
        else:
            self.word_label.setText(deck.get_card(0).get_front())
            self.show_flag = True

    def b_yes_click(self):
        completed.append(deck.get_card(0))
        deck.remove_card(0)
        self.word_label.setText(deck.get_card(0).get_front())
        self.deck_size_label.setText("Cards in deck: " + str(deck.get_deck_size()))

        if deck.get_deck_size() == 0:
            self.you_won()

    def b_no_click(self):
        deck.shuffle()
        self.word_label.setText(deck.get_card(0).get_front())

    def you_won(self):
        for i in reversed(range(self.v_box.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()

        win_text = QLabel()
        win_text.setText("You were able to finish the whole deck of cards. Well done!")
        win_text.setStyleSheet('font: 20px')
        b_win_quit = QtWidgets.QPushButton('Quit')
        b_win_quit.clicked.connect(self.b_win_quit_clicked)

        self.v_box.addWidget(win_text)
        self.v_box.addWidget(b_win_quit)

    def b_win_quit_clicked(self):
        sys.exit()


if __name__ == '__main__':
    deck = Deck()  # Creates the deck containing cards filled with information from a .docx file.
    uncompleted = []
    completed = []

    app = QtWidgets.QApplication(sys.argv)
    a_window = Window()
    a_window.resize(700, 500)
    sys.exit(app.exec())
