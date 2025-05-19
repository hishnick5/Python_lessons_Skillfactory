import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDateEdit, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate


def edit_numb(numb):
    return numb if numb <= 22 else edit_numb(numb - 22)


def calculate(input_data):
    day = input_data.day()
    month = input_data.month()
    year = input_data.year()

    day_str = f"{day:02d}"
    month_str = f"{month:02d}"
    year_str = str(year)

    full_date = f"{day_str}.{month_str}.{year_str}"
    pure = full_date.replace('.', '').replace('0', '')
    destiny = str(sum([int(i) for i in pure]))
    while len(destiny) > 1:
        destiny = str(sum([int(i) for i in destiny]))

    arkan = sum([int(i) for i in pure])
    arkan = edit_numb(arkan)

    a = day
    b = month
    c = sum([int(i) for i in year_str])
    if a > 22: a = edit_numb(a)
    if c > 22: c = edit_numb(c)
    d = a + b + c
    d = edit_numb(d)

    # Числа достижений
    ch_d1 = edit_numb(abs(a + b))
    ch_d2 = edit_numb(abs(a + c))
    ch_d3 = edit_numb(abs(ch_d1 + ch_d2))
    ch_d4 = edit_numb(abs(b + c))

    # Кармические узлы
    karmic1 = edit_numb(abs(a - b))
    karmic2 = edit_numb(abs(a - c))
    karmic3 = edit_numb(abs(karmic1 - karmic2))
    karmic4 = edit_numb(abs(b - c))
    karmic5 = edit_numb(abs(karmic1 + karmic2 + karmic3 + karmic4))

    # Периоды
    period1 = 36 - int(destiny)
    period2 = period1 + 9
    period3 = period2 + 9

    # Денежный код
    def reduce(num):
        while len(num) > 1:
            num = str(sum([int(i) for i in num]))
        return num
    day_r = reduce(str(day))
    month_r = reduce(str(month))
    year_r = reduce(year_str)
    concat = reduce(day_r + month_r + year_r)
    money_code = day_r + month_r + year_r + concat
    num_1 = reduce(str(int(month_r) + int(year_r)))
    num_5 = reduce(str(int(year_r) + int(concat)))
    num_2 = reduce(str(int(num_1) + int(year_r)))
    num_4 = reduce(str(int(year_r) + int(num_5)))
    num_6 = reduce(str(int(num_1) + int(num_5)))
    fin_code = num_1 + num_2 + year_r + num_4 + num_5 + num_6

    table = [
        [f"Супер способности ({a})", f"ЧД 1 ({ch_d1})", f"КУ 1 ({karmic1})", f"0 - {period1}"],
        [f"Задача на жизнь ({b})", f"ЧД 2 ({ch_d2})", f"КУ 2 ({karmic2})", f"{period1} - {period2}"],
        [f"Энергия года ({c})", f"ЧД 3 ({ch_d3})", f"КУ 3 ({karmic3})", f"{period2} - {period3}"],
        [f"Предназначение ({d})", f"ЧД 4 ({ch_d4})", f"КУ 4 ({karmic4})", f"{period3} - ∞"],
        [f"$ канал/код: {fin_code}", f"Аркан: {arkan}", f"КУ 5 ({karmic5})", f"Число судьбы ({destiny})"]
    ]
    return full_date, table


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт по дате рождения")
        self.resize(1000, 500)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Выберите дату рождения:")
        self.label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.label)

        self.date_picker = QDateEdit(calendarPopup=True)
        self.date_picker.setDisplayFormat("dd.MM.yyyy")
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setFont(QFont("Arial", 12))
        self.date_picker.setFixedWidth(self.width() // 5)  # 1/5 ширины
        self.layout.addWidget(self.date_picker)

        self.button = QPushButton("Рассчитать")
        self.button.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.button)

        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget::item {
                border: 2px solid blue;
                padding: 4px;
            }
            QHeaderView::section {
                font-weight: bold;
                background-color: #e0eaff;
                border: 1px solid #999;
            }
        """)
        self.table.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.table)

        self.button.clicked.connect(self.calculate)

    def calculate(self):
        selected_date = self.date_picker.date()
        try:
            full_date, data = calculate(selected_date)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Что-то пошло не так\n{str(e)}")
            return

        headers = [f"Путь по дате: {full_date}", "Число Достижений", "Кармический Узел", "Период"]
        self.table.setColumnCount(4)
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
