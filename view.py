from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from model import TooFewPersonsError
import os


class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model

        # Set window properties
        self.setWindowTitle('Split Expenses 2000')
        self.resize(200, 200)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'icon.png'))

        # View box
        self.view = View(model)
        self.setCentralWidget(self.view)

        # Borrowed code snippet ====================
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
        QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        # Borrowed code snippet ====================

        # Add menu bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('File')

        # Actions for menu bar
        quit_action = QAction('Quit', self)
        self.file_menu.addAction(quit_action)

        # Emit signal to close window if triggered
        quit_action.triggered.connect(self.close)


class View(QGroupBox):
    """ The main window of the GUI
    """

    def __init__(self, model):
        super().__init__()

        self.model = model

        # Create subgroups
        self.button_group = ButtonGroup(self.model, self)
        self.input_group = InputGroup(self.model)

        # Create main layout of the window and add subgroups
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.input_group)
        self.main_layout.addWidget(self.button_group)
        self.setLayout(self.main_layout)

    def too_few_persons_inform(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message = "Must be at least two persons!"
        message_box.setText(message)
        message_box.exec_()


class ButtonGroup(QGroupBox):
    """ Group box containing calculate and the result

    """

    def __init__(self, model, parent):
        super().__init__()

        self.model = model
        self.parent = parent

        # Connect logic
        self.model.show_result.connect(self.show_result)

        # Contents
        self.calculate_button = QPushButton("Calculate")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.calculate_button)
        self.setLayout(self.layout)

        # Controllers
        def calculate():

            # Only compute if more than one person in group
            try:
                self.model.compute()
            except TooFewPersonsError:
                self.parent.too_few_persons_inform()

        self.calculate_button.clicked.connect(calculate)

    def show_result(self, negative_persons):

        nr_negative_persons = len(negative_persons)

        # Remove calculate button
        self.calculate_button.setParent(None)

        # Add a table with as many rows as negative persons
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(nr_negative_persons)
        self.tableWidget.setColumnCount(1)

        # Remove headers and let column 1 fill the width
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()

        # Add a message for each person owing another person
        for i, neg_person in enumerate(negative_persons):
            for pos_person_name, pos_person_value in neg_person.owes.items():
                row_str = f"{neg_person.name} should pay {pos_person_name} {int(pos_person_value)}"
                self.tableWidget.setItem(i, 0, QTableWidgetItem(row_str))

        self.layout.addWidget(self.tableWidget)

        # Add a button for resetting the window
        self.reset_button = QPushButton("Reset")
        self.layout.addWidget(self.reset_button)
        self.setLayout(self.layout)

        # Controller for reset button
        def reset():
            self.model.reset_group()

            # Create a new view and close the previous
            view = View(self.model)
            view.showNormal()
            self.parent.close()
        self.reset_button.clicked.connect(reset)


class InputGroup(QGroupBox):
    """ Group box containing input text boxes

    """

    def __init__(self, model):
        super().__init__()

        self.model = model

        # Stack the boxes vertically
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

            # Add the data to the group instance
            self.model.register_expense(self.name_textbox.text(), self.expense_textbox.text())

            # Empty text
            self.name_textbox.setText("")
            self.expense_textbox.setText("")
        self.add_button.clicked.connect(new_expense)






