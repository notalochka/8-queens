class Statistics:
    def __init__(self, top, time_w, dep=0):
        # матриця розстановки результату
        self.result_matr = []
        # кількість оброблених вершин
        self.tops = top
        # час роботи алгоритму
        self.time_of_work = time_w
        # глибина пошуку
        self.depth = dep
        # масив для покрокових розв'язків задачі
        self.steps = []

    # ініціалізація статистики після роботи алгоритму
    def init_statictic(self, result, steps, top, time_w, dep=0):
        self.result_matr = result
        self.tops = top
        self.time_of_work = time_w
        self.depth = dep
        for matrix in steps:
            copied_matrix = [[0] * 8 for _ in range(8)]  # Створити нову матрицю для копіювання
            for j in range(8):
                for k in range(8):
                    copied_matrix[j][k] = matrix[j][k]  # Копіювати значення в нову матрицю
            self.steps.append(copied_matrix)
    # копіювання статистики
    def copy_from(self, other):
        self.result_matr = other.result_matr
        self.tops = other.tops
        self.time_of_work = other.time_of_work
        self.depth = other.depth
        for matrix in other.steps:
            copied_matrix = [[0] * 8 for _ in range(8)]  # Створити нову матрицю для копіювання
            for j in range(8):
                for k in range(8):
                    copied_matrix[j][k] = matrix[j][k]  # Копіювати значення в нову матрицю
            self.steps.append(copied_matrix)