from boardcell import BoardCell

# клас шахової дошки
class ChessBoard:
    # розмір шахової дошки - кількість ферзів
    size = 8

    # конструктор створення порожньої розстановки
    def __init__(self):
        self.grid = [[BoardCell(i, j, 0) for j in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].isOccupied = False

    # ініціалізація дошки з вхідної розстановки
    def create_board(self, inner_positions):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = BoardCell(i, j, inner_positions[i][j])

    # копіювання дошки
    def copy_from(self, previous_board):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].isOccupied = previous_board.grid[i][j].isOccupied

    # перетворення дошки на матрицю розстановки
    def get_board_matrix(self):
        board_matrix = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].isOccupied:
                    board_matrix[i][j] = 1
        return board_matrix

    # перевірка чи є дошка розв'язком
    def is_result(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].isOccupied:
                    if self.is_queen_diagonal(i, j):
                        return False
        return True

    # перевірка, чи дошка відповідає вимогам для розв'язання алгоритмом
    def is_solvable(self) -> bool:
        num_queens = 0

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].isOccupied:
                    num_queens += 1
                    if self.is_queen_row_col(i, j):
                        return False
        if num_queens == self.size:
            return True
        else:
            return False

    # перевірка чи є в заданому рядку а колонці ферзь
    def is_queen_row_col(self, row, col) -> bool:
        for i in range(col):
            if self.grid[row][i].isOccupied:
                return True

        for i in range(col + 1, self.size):
            if self.grid[row][i].isOccupied:
                return True

        for i in range(row):
            if self.grid[i][col].isOccupied:
                return True

        for i in range(row + 1, self.size):
            if self.grid[i][col].isOccupied:
                return True

        return False

    # перевірка чи є фігура на головній діагоналі
    def is_queen_main_diagonal(self) -> bool:
        for i in range(self.size):
            if not self.grid[i][i].isOccupied:
                return False
        return True

    # перевірка чи є фігура на симетричній головній діагоналі
    def is_queen_symmetric_diagonal(self) -> bool:
        for i in range(self.size):
            j = self.size - 1 - i
            if not self.grid[i][j].isOccupied:
                return False
        return True

    # перевірка чи є фігура на заданій діагоналі
    def is_queen_diagonal(self, row, col) -> bool:
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if self.grid[i][j].isOccupied:
                return True
            i -= 1
            j -= 1

        i, j = row + 1, col + 1
        while i < self.size and j < self.size:
            if self.grid[i][j].isOccupied:
                return True
            i += 1
            j += 1

        i, j = row + 1, col - 1
        while i < self.size and j >= 0:
            if self.grid[i][j].isOccupied:
                return True
            i += 1
            j -= 1

        i, j = row - 1, col + 1
        while i >= 0 and j < self.size:
            if self.grid[i][j].isOccupied:
                return True
            i -= 1
            j += 1

        return False

    # кількість ферзів, які погрожують один одному
    def num_of_treats(self) -> int:
        num = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].isOccupied:
                    if self.is_queen_diagonal(i, j):
                        num += 1
        return num

    # створення нащадка за вказаними клітинками та орієнтацією
    def create_successor(self, pos1, pos2, orientation):
        if orientation == 0:
            for i in range(0, self.size):
                self.grid[i][pos1], self.grid[i][pos2] = self.grid[i][pos2], self.grid[i][pos1]
        elif orientation == 1:
            for i in range(0, self.size):
                self.grid[pos1][i], self.grid[pos2][i] = self.grid[pos2][i], self.grid[pos1][i]

    # створення масиву нащадків
    def make_successors_list(self):
        num_of_treats = self.size
        max_successors_num = (self.size * self.size) - self.size
        position = 0
        res_list: list[ChessBoard] = []
        tmp_arr = []
        for orientation in range(2):
            for i in range(self.size - 1):
                for j in range(i + 1, self.size):
                    tmp_board = ChessBoard()
                    tmp_board.copy_from(self)
                    tmp_board.create_successor(i, j, orientation)
                    if num_of_treats >= tmp_board.num_of_treats():
                        num_of_treats = tmp_board.num_of_treats()
                    tmp_arr.append(tmp_board)
                    position += 1

        for i in range(max_successors_num):
            if tmp_arr[i].num_of_treats() == num_of_treats:
                res_list.append(tmp_arr[i])

        return res_list