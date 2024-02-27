from chessboard import ChessBoard
# клас вершини дерева
class Node:
    def __init__(self, board, successorsNum):
        # масив нащадків
        self.successors: list[Node] = [None] * successorsNum
        # розстановка вузла
        self.board = ChessBoard()
        self.board.copy_from(board)
        # кількість нащадків
        self.successorsNum = successorsNum
    # додавання вузла до масиву нащадків
    def add_board(self, board, pos):
        self.successors[pos] = Node(board, self.successorsNum)
        return self.successors[pos]

