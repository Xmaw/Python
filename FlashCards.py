# TODO A Module Docstring would be nice
from PyQt5.QtCore import *  # TODO Explicit imports are preferred over *, so we know what names we introduce
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel
import sys
from random import shuffle
import docx2txt


class Deck:
    def __init__(self):
        # TODO The class itself is called Deck. maybe this list should be called "cards" or something?
        self.deck = []
        # TODO Unnecessary and error-prone to keep this separate. Use len(self.deck) instead.
        self.size = 0

        # TODO Unnecessary comment, imo
        # ----Get list elements from add_cards function----
        self.add_cards()

    # TODO Not really wrong to do this, but consider using self.deck[index] directly instead.
    # TODO After looking through the code more, this is only ever used with index 0, consider renaming it
    # to "top" or "top_card" or something.
    def get_card(self, index):
        # TODO This thows exception if index is out of range
        return self.deck[index]

    # TODO I think that this method could be called "load" or "load_from_file" or something
    def add_cards(self):
        # TODO This path should be a parameter, possibly with a default value
        # my_text = docx2txt.process("C:\\Users\\Elias\\Desktop\\School\\Nätverk\\FlashCards_Network.docx")
        my_text = docx2txt.process("/tmp/flashcards.docx")
        s = my_text.split("\n\n")
        # TODO This s_temp stuff seems unnecessary. Why not loop over my_text.split('\n\n') directly?
        s_temp = ""
        for word in s:
            s_temp += word + "\n"

        s1_temp = s_temp.split("\n")

        for word in s1_temp:
            s_temp = word.split('-')
            if len(s_temp) == 2:
                self.deck.append(Cards(s_temp[0], s_temp[1]))
                self.size += 1  # TODO Why keep this separate? len(self.deck) should be just fine?

    # TODO Unused?
    def print_size(self):
        print(self.size)

    def remove_card(self, index):
        del self.deck[index]

    def shuffle(self):
        shuffle(self.deck)


# TODO "Cards" should probably be named "Card"
# TODO (Also, you could use namedtuple from collections, or Python 3.7 @dataclass for simple classes like this)
class Cards:
    def __init__(self, frontside, backside):
        # TODO Nothing wrong with these names, but ".front" och ".back" is shorter and as good, imo.
        self.frontside = frontside
        self.backside = backside

    # TODO Plain accessor-methods are not normally used in Python, use card.front / card.back directly instead
    def get_frontside(self):
        return self.frontside

    def get_backside(self):
        return self.backside


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()  # TODO Consider the no-argument version of __super__()
        self.show_flag = False
        self.b_show = QtWidgets.QPushButton('Show')
        self.b_no = QtWidgets.QPushButton('No')
        self.b_yes = QtWidgets.QPushButton('Yes')
        self.list_word = []  # TODO Unused?
        self.list_explanation = []  # TODO Unused?
        # TODO Consider deck.shuffle()

        # ----H_BOX to store the widgets in ----
        self.h_box = QtWidgets.QVBoxLayout()

        # ----Labels to display the text ----
        self.word_label = QLabel()
        self.word_label.resize(50, 50)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet("font: 20pt;")
        self.word_label.setWordWrap(True)
        print()  # TODO What is this print() call doing?
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
            self.show_flag = True  # TODO A common way to toggle a boolean flag is self.show_flag = not self.show_flag
        elif self.show_flag:  # TODO "elif" suggests a third case, "else" might be good enough here
            self.word_label.setText(deck.get_card(0).get_frontside())
            self.show_flag = False

    def b_yes_click(self):
        # TODO Variable says 'completed', comment says 'uncompleted' Which is it? (And also, comments like these are
        # redundant, and they tend to be forgotten when variable names are updated etc.)
        # TODO deck.get_card(0) is used more than once, consider assigning to local variable (top_card = ... etc)
        completed.append(deck.get_card(0))  # Adds the card to the list of uncompleted FlashCards.
        deck.remove_card(0)
        self.word_label.setText(deck.get_card(0).get_frontside())

    def b_no_click(self):
        deck.shuffle()
        self.word_label.setText(deck.get_card(0).get_frontside())


# TODO Consider the idiom if __name__ == '__main__':, so that this module can be imported and reused
deck = Deck()  # Creates the deck containing cards filled with information from a .docx file.
uncompleted = []  # TODO Unused variable?
completed = []

app = QtWidgets.QApplication(sys.argv)
a_window = Window()  # TODO Not a big deal, but not that common to call things "a_" in Python. Consider "w" or "window".
a_window.resize(700, 700)
sys.exit(app.exec())
