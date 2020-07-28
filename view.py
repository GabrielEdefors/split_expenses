from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *


class View(QGroupBox):
    """ The main window of the GUI
    """

    def __init__(self, model):
        super().__init__()

        self.model = model
        self.setGeometry(300, 300, 400, 500)

        # Set window properties
        self.setWindowTitle('Split Expenses 2000')

        # Create subgroups
        self.button_group = ButtonGroup(self.model)
        self.input_group = InputGroup(self.model)

        # Create main layout of the window and add subgroups
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_group)
        main_layout.addWidget(self.button_group)
        self.setLayout(main_layout)


class ButtonGroup(QGroupBox):
    """ Group box containing calculate and the result

    """

    def __init__(self, model):
        super().__init__()

        self.model = model

        # Contents
        self.calculate_button = QPushButton("Calculate")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.calculate_button)
        self.setLayout(self.layout)

        # Controllers
        def calulate():
            self.model.calculate_owings()
        self.calculate_button.clicked.connect(calulate)


class InputGroup(QGroupBox):
    """ Group box containing input text boxes

    """

    def __init__(self, model):
        super().__init__()

        self.model = model

        # Input text boxes
        self.layout = QFormLayout()
        self.name_textbox = QLineEdit()
        self.expense_textbox = QLineEdit()
        self.add_button = QPushButton("Add Expense")
        self.layout.addRow("Name", self.name_textbox)
        self.layout.addRow("Amount", self.expense_textbox)
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

        # Controllers
        def new_expense():
            self.model.register_expense(self.name_textbox.text(), self.expense_textbox.text())

            # Empty text
            self.name_textbox.setText("")
            self.expense_textbox.setText("")

        self.add_button.clicked.connect(new_expense)



