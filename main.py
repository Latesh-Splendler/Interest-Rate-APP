from PyQt5.QtWidgets import (
    QPushButton, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTreeView, QMainWindow, QMessageBox, QFileDialog, QCheckBox
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os


class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp, self).__init__()
        self.setWindowTitle("My Interest Application")
        self.resize(850, 650)

        self.window = QWidget()

        # Input fields
        self.rate_text = QLabel("Interest Rate (%):")
        self.rate_input = QLineEdit()

        self.initial_text = QLabel("Initial Investment:")
        self.initial_input = QLineEdit()

        self.years_text = QLabel("Years to Invest:")
        self.years_input = QLineEdit()

        # Data display
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Year", "Total"])
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        # Buttons and dark mode toggle
        self.calc_button = QPushButton("Calculate")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save Data")
        self.dark_mode = QCheckBox("Dark Mode")

        # Chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Layouts
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        # Top row
        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.initial_text)
        self.row1.addWidget(self.initial_input)
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input)
        self.row1.addWidget(self.dark_mode)

        # Left and right columns
        self.col1.addWidget(self.tree_view)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)

        self.col2.addWidget(self.canvas)

        # Combine layouts
        self.row2.addLayout(self.col1)
        self.row2.addLayout(self.col2)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)

        self.window.setLayout(self.master_layout)
        self.setCentralWidget(self.window)

        # Signals
        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)
        self.dark_mode.stateChanged.connect(self.toggle_mode)

        # Initialize dark mode
        self.dark_mode.setChecked(True)
        self.apply_styles()

    def apply_styles(self):
        if self.dark_mode.isChecked():
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2E2E2E;
                    color: white;
                }
                QLabel, QPushButton, QLineEdit {
                    color: white;
                    background-color: #2E2E2E;
                }
                QTreeView {
                    background-color: #424242;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("")

    def toggle_mode(self):
        self.apply_styles()

    def calc_interest(self):
        try:
            interest_rate = float(self.rate_input.text())
            years = int(self.years_input.text())
            initial_investment = float(self.initial_input.text())
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
            return

        
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Year", "Total"])

        
        total = initial_investment
        for year in range(1, years + 1):
            total += total * (interest_rate / 100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])

        
        self.figure.clear()
        ax = self.figure.subplots()
        year_list = list(range(1, years + 1))
        totals = [initial_investment * (1 + interest_rate / 100) ** year for year in year_list]

        ax.plot(year_list, totals, marker="o")
        ax.set_title("Interest Chart")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw()

    def save_data(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            folder_path = os.path.join(dir_path, "Saved")
            os.makedirs(folder_path, exist_ok=True)

            
            file_path = os.path.join(folder_path, "result.csv")
            with open(file_path, "w") as file:
                file.write("Year,Total\n")
                for row in range(self.model.rowCount()):
                    year = self.model.item(row, 0).text()
                    total = self.model.item(row, 1).text()
                    file.write(f"{year},{total}\n")

            
            chart_path = os.path.join(folder_path, "Chart.png")
            self.figure.savefig(chart_path)

            QMessageBox.information(self, "Saved", f"Data saved to {file_path} and {chart_path}")
        else:
            QMessageBox.warning(self, "Error", "No directory selected.")

    def reset(self):
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.clear()
        self.figure.clear()
        plt.style.use('default')  
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    window = FinanceApp()
    window.show()
    app.exec_()
