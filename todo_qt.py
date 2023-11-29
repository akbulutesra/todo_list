import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QListWidget
import sqlite3 as sql 

class TodoApp(QWidget):

    taskList = []

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()
        self.loadTasks()

    def initDB(self):
        self.conn = sql.connect('tasks.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS tasks (task TEXT)')
        self.conn.commit()

    def loadTasks(self):
        self.c.execute('SELECT task FROM tasks')
        tasks = self.c.fetchall()
        for task in tasks:
            self.listWidget.addItem(task[0])

    def initUI(self):
        vbox = QVBoxLayout()

        self.display = QLineEdit()

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)

        self.button = QPushButton('Add', self)
        self.button.move(20, 80)
        self.button.clicked.connect(self.addClicked)

        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.move(20, 80)
        self.deleteButton.clicked.connect(self.deleteTask)

        self.clearButton = QPushButton('Clear All', self)
        self.clearButton.move(20, 80)
        self.clearButton.clicked.connect(self.clearall)

                # Add other widgets before the QListWidget
        vbox.addWidget(self.textbox)  # Add the textbox to the layout
        vbox.addWidget(self.button)   # Add the button to the layout
        vbox.addWidget(self.deleteButton)
        vbox.addWidget(self.clearButton)

        self.listWidget = QListWidget(self)
        vbox.addWidget(self.listWidget)  # Add the list widget last
        self.listWidget.addItems(self.taskList)

        self.setLayout(vbox)  # Set the layout for the window/widget

    def addClicked(self):
        textboxValue = self.textbox.text()

        if textboxValue != "":
            self.taskList.append(textboxValue)
            self.textbox.setText("")
            self.listWidget.addItem(textboxValue)
            self.c.execute('INSERT INTO tasks (task) VALUES (?)', (textboxValue,))
            self.conn.commit()

    def deleteTask(self):
        row = self.listWidget.currentRow()
        task = self.listWidget.item(row).text()
        self.listWidget.takeItem(row)
        self.c.execute('DELETE FROM tasks WHERE task = ?', (task,))
        self.conn.commit()
    
    def clearall(self):
        self.listWidget.clear()
        self.c.execute('DELETE FROM tasks')
        self.conn.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo = TodoApp()
    todo.show()
    sys.exit(app.exec_())