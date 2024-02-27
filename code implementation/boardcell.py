# клас клітини на шаховій дошці
class BoardCell:
    def __init__(self, x, y, is_occupied):
        # номер рядка
        self.row = x
        # номер стовпця
        self.column = y
        # змінна, яка визначає чи є в клітині ферзь
        self.isOccupied = False
        if is_occupied == 1:
            self.isOccupied = True