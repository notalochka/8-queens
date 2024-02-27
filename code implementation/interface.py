import tkinter as tk
from tkinter import messagebox
from statistics_for_algorithm import Statistics
from algorithm import Algorithm
from chessboard import ChessBoard
# клас для відображення - інтерфейсна частина
class ChessboardGUI:
    def __init__(self):
        # статистика роботи алгоритму
        self.statistic = Statistics(0, 0)
        # розстановка ферзів у вигляді матриці
        self.chessboard_matrix = [[0] * 8 for _ in range(8)]
        # головне вікно програми
        self.win = tk.Tk()
        # фото для відображення клітинок на шаховій дошці
        self.photo1 = tk.PhotoImage(file="background.png")
        self.photo2 = tk.PhotoImage(file="queen (1).png")
        # кнопки на шаховій дошці
        self.buttons = [[None] * 8 for _ in range(8)]
        self.setup_window()
    # відображення головного вікна
    def setup_window(self):
        self.win.title('Головоломка: 8 ферзів')
        h = 800
        w = 600
        self.win.geometry(f"{h}x{w}+200+120")
        self.win.minsize(600, 500)
        self.win.maxsize(1000, 800)
        self.win.resizable(True, True)
        photo = tk.PhotoImage(file='icon.png')
        self.win.iconphoto(False, photo)
        self.win.config(bg='#D5F6FF')
        label = tk.Label(self.win, text="Задача розміщення 8 ферзів", bg='#D5F6FF', font=("Arial", 16, "bold"))
        label.pack()
        button_instr = tk.Button(self.win, text="Показати інструкцію",
                                 bg='#CCB6FF', font=("Arial", 12),
                                 activebackground='#FF49AA',
                                 command=self.show_instruction
                                 )
        button_instr.pack()
        win_right = tk.Frame(self.win)
        win_right.pack(side=tk.RIGHT, padx=50)
        label_algorithm = tk.Label(win_right, text="Обрати алгоритм:", font=("Arial", 14, "bold"))
        label_algorithm.pack()
        self.variant_algorithm = tk.IntVar()
        tk.Radiobutton(win_right, text="LDFS", font=("Arial", 12, "bold"), variable=self.variant_algorithm, value=1).pack()
        tk.Radiobutton(win_right, text="BFS", font=("Arial", 12, "bold"), variable=self.variant_algorithm, value=2).pack()
        tk.Radiobutton(win_right, text="IDS", font=("Arial", 12, "bold"), variable=self.variant_algorithm, value=3).pack()
        btn_solve = tk.Button(win_right, text="Розв'язати",
                              bg='#FF8D84', font=("Arial", 12),
                              activebackground='#FF0000',
                              command=lambda: self.button(self.variant_algorithm.get())
                              )
        btn_solve.pack()
        btn_stastictics = tk.Button(win_right, text="Показати статистику", bg='#FFB300', font=("Arial", 12),
                                    activebackground='#FF0000', command=self.show_statistics)
        btn_stastictics.pack(pady=30)
        btn_file = tk.Button(win_right, text="Зберегти статистику \nу текстовий файл", bg='#FFB300',
                                    font=("Arial", 12), activebackground='#FF0000', command=self.save_stat_to_file)
        btn_file.pack()

        win_left = tk.Frame(self.win)
        win_left.pack(side=tk.LEFT, padx=20)
        self.create_chessboard_buttons(win_left)



    # відображення шахової дошки
    def create_chessboard_buttons(self, frame):
        chessboard = tk.Frame(frame)
        chessboard.grid()
        colors = ["white", "gray"]
        for i in range(8):
            for j in range(8):
                color = colors[(i + j) % 2]
                self.buttons[i][j] = tk.Button(chessboard, height=50, width=50, image=self.photo1, bg=color)
                self.buttons[i][j].image_state = False  # Флаг состояния изображения
                self.buttons[i][j].config(command=lambda btn=self.buttons[i][j], row=i, col=j: self.change_image(btn, row, col))
                self.buttons[i][j].grid(row=i, column=j)
    # відображення вікна інструкції
    def show_instruction(self):
        window_instructions = tk.Toplevel()
        window_instructions.title('Інструкція')
        window_instructions.geometry("400x400")
        label1 = tk.Label(window_instructions, text="Інструкція до програми", font=("Arial", 13, "bold"))
        label1.pack()
        label3 = tk.Label(window_instructions, text="Задача про 8 ферзів полягає\n в розміщенні фігур на шахівниці,\n " \
                       "щоб жодна з восьми не ставила\n під удар один одного. \n" \
                       "Тобто, вони не повинні стояти\n в одній вертикалі, горизонталі чи діагоналі.\n\n", font=("Arial", 11))
        label3.pack()
        label2 = tk.Label(window_instructions, text="Для розв'язання задачі потрібно:", font=("Arial", 13, "bold"), fg='#770000')
        label2.pack()
        label4 = tk.Label(window_instructions, text="1. Розставити 8 ферзей, які не атакують \nодин одного по горизонталі та вертикалі"\
                                                    '''\n\n2. Обрати один з трьох алгоритмів\n\n3. Натиснути кнопку "Розв'язати"''',
                                                    font=("Arial", 11, "bold"),
                                                    bg='#FFF5D8',
                                                    width= 40,
                                                    height=7,
                                                    justify=tk.LEFT,
                                                    relief=tk.RAISED)
        label4.pack()
    # зміна кнопки шахової дошки - поява або видалення ферзя з клітинки


    def change_image(self, btn, row, col):
        if btn.image_state:
            btn.config(image=self.photo1)
            self.chessboard_matrix[row][col] = 0
            btn.image_state = False
        else:
            btn.config(image=self.photo2)
            self.chessboard_matrix[row][col] = 1
            btn.image_state = True
    # оновлення шахової дошки для відображення розв'язку у покроковому вигляді
    def update_chessboard_view(self):
        if self.statistic.steps:
            matrix = self.statistic.steps.pop(0)
            if matrix is not None:
                for i in range(8):
                    for j in range(8):
                        if matrix[i][j] == 1:
                            self.buttons[i][j].config(image=self.photo2)
                            self.buttons[i][j].image_state = True
                        else:
                            self.buttons[i][j].config(image=self.photo1)
                            self.buttons[i][j].image_state = False
                self.win.after(1000, self.update_chessboard_view)
    # загальний алгоритм розв'язку та відображення результатів
    def button(self, variant_algo):
        chessboard = ChessBoard()
        chessboard.create_board(self.chessboard_matrix)
        if chessboard.is_solvable():
            if chessboard.is_result():
                tk.messagebox.showinfo("Повідомлення", "Вітаю, ви розв'язали правильно!")
            else:
                algor = Algorithm
                if variant_algo == 1:
                    self.statistic.copy_from(algor.LDFS(chessboard))
                    self.chessboard_matrix = self.statistic.result_matr
                    self.update_chessboard_view()
                elif variant_algo == 2:
                    if chessboard.is_queen_main_diagonal() or chessboard.is_queen_symmetric_diagonal():
                        tk.messagebox.showinfo("Повідомлення",
                                               "Cистема не змогла знайти вирішення задачі\nСпробуйте задати іншу розстановку,\nщоб атакуючих ферзів було якомога менше")
                    else:
                        self.statistic.copy_from(algor.BFS(chessboard))
                        self.chessboard_matrix = self.statistic.result_matr
                        self.update_chessboard_view()
                elif variant_algo == 3:
                    if chessboard.is_queen_main_diagonal() or chessboard.is_queen_symmetric_diagonal():
                        tk.messagebox.showinfo("Повідомлення",
                                               "Cистема не змогла знайти вирішення задачі\nСпробуйте задати іншу розстановку,\nщоб атакуючих ферзів було якомога менше")
                    else:
                        self.statistic.copy_from(algor.IDS(chessboard))
                        self.chessboard_matrix = self.statistic.result_matr
                        self.update_chessboard_view()
                else:
                    tk.messagebox.showinfo("Помилка", "Алгоритм розв'язання не обрано!")
        else:
            tk.messagebox.showinfo("Помилка", "Неправильна розстановка ферзів!\n Переконайтесь, що ви:\n- розставили всі 8 ферзів\n- ферзі не атакують по горизонталі та вертикалі")
    # відображення статистики
    def show_statistics(self):
        if self.statistic.tops == 0:
            tk.messagebox.showinfo("Статистика","Статистики немає!\nСпершу розв'яжіть задачу")
        else:
            tk.messagebox.showinfo("Статистика",
                                   f"Кількість оброблених вершин - {self.statistic.tops}\n"
                                   f"Глибина - {self.statistic.depth}\n"
                                   f"Час виконання - {self.statistic.time_of_work:.2f} мс")
    # збереження розв'язку та статиски у текстовий файл
    def save_stat_to_file(self):
        with open("./statistics.txt", "w") as file:
            if self.statistic.tops == 0:
                file.write("Статистики немає!\nСпершу розв'яжіть задачу")
            else:
                file.write("Розв'язок:\n")
                for row in self.statistic.result_matr:
                    line = " ".join(str(element) for element in row)
                    file.write(line + "\n")
                file.write(f"Кількість оброблених вершин - {self.statistic.tops}\nЧас виконання - {self.statistic.time_of_work:.2f} мс\nГлибина - {self.statistic.depth}\n")
        tk.messagebox.showinfo("Повідомлення", "Статистика збережена у текстовий файл")