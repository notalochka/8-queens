import random
import time
from statistics_for_algorithm import Statistics
from treenode import Node, ChessBoard
# клас з алгоритмами
class Algorithm:
    # алгоритм LDFS
    @staticmethod
    def LDFS(board) -> Statistics:
        steps = []
        statistics = Statistics(0, 0)
        start_time = time.time()
        childrenNum = (board.size*board.size) - board.size
        root = Node(board, childrenNum)
        stack = [root]
        top = 1
        currentDepth = 0
        flag = True
        while flag:
            tmp = stack[-1]
            currentDepth += 1
            succesBoards = tmp.board.make_successors_list()
            number = random.randint(0, len(succesBoards) - 1)
            tmp2 = tmp.add_board(succesBoards[number], number)
            tmp_board = ChessBoard()
            tmp_board.copy_from(tmp2.board)
            steps.append(tmp_board.get_board_matrix())
            if tmp2.board.is_result():
                flag = False
            stack.append(tmp2)
            top += childrenNum
        end_time = time.time()
        result = ChessBoard()
        result.copy_from(tmp2.board)
        execution_time = (end_time - start_time) * 1000
        statistics.init_statictic(result.get_board_matrix(), steps, top, execution_time, currentDepth)
        return statistics
    # алгоритм BFS
    @staticmethod
    def BFS(board) -> Statistics:
        steps = []
        statistics = Statistics(0, 0)
        start_time = time.time()
        childrenNum = (board.size*board.size) - board.size
        root = Node(board, childrenNum)
        queue = [root]
        top = 1
        currentDepth = 1
        flag = True
        s2 = len(root.board.make_successors_list())
        s = 0
        while flag:
            tmp = queue[0]
            queue = queue[1:]
            tmp_board = ChessBoard()
            tmp_board.copy_from(tmp.board)
            steps.append(tmp_board.get_board_matrix())
            succesBoards = tmp.board.make_successors_list()
            for i in range(len(succesBoards)):
                tmp2 = tmp.add_board(succesBoards[i], i)
                queue.append(tmp2)
                top += 1
                if tmp2.board.is_result():
                    flag = False
                    tmp_board.copy_from(tmp2.board)
                    steps.append(tmp2.board.get_board_matrix())
                    break
            if s == 0:
                currentDepth += 1
                s = s2
            else:
                s -= 1
                s2 += len(succesBoards)
        end_time = time.time()
        result = ChessBoard()
        result.copy_from(tmp2.board)
        execution_time = (end_time - start_time) * 1000
        statistics.init_statictic(result.get_board_matrix(), steps, top, execution_time, currentDepth)
        return statistics
    # допоміжний алгоритм DLS для алгоритму IDS
    @staticmethod
    def DLS(node, depth, top):
        if node.board.is_result():
            return node, top
        if depth > 0:
            succesBoards = node.board.make_successors_list()
            for i in range(len(succesBoards)):
                top +=1
                tmp = node.add_board(succesBoards[i], i)
                tmp2, top = Algorithm.DLS(tmp, depth - 1, top)
                if tmp2 is not None:
                    return tmp2, top
        return None, top
    # допоміжний алгоритм DLS для ініціалізації масиву кроків розв'язання
    @staticmethod
    def DLS_for_steps(node, depth, steps):
        if node.board.is_result():
            tmp_board = ChessBoard()
            tmp_board.copy_from(node.board)
            steps.append(tmp_board.get_board_matrix())
            return node, steps
        if depth > 0:
            succesBoards = node.board.make_successors_list()
            for i in range(len(succesBoards)):
                tmp = node.add_board(succesBoards[i], i)
                tmp_board = ChessBoard()
                tmp_board.copy_from(tmp.board)
                steps.append(tmp_board.get_board_matrix())
                tmp2, steps = Algorithm.DLS_for_steps(tmp, depth - 1, steps)
                if tmp2 is not None:
                    return tmp2, steps
        return None, steps
    # алгоритм IDS
    @staticmethod
    def IDS(board) -> Statistics:
        steps = []
        statistics = Statistics(0, 0)
        start_time = time.time()
        childrenNum = (board.size * board.size) - board.size
        root = Node(board, childrenNum)
        currentDepth = 0
        top = childrenNum+1
        flag = True
        result = ChessBoard()
        while flag:
            tmp, top = Algorithm.DLS(root, currentDepth, top)
            if tmp is not None:
                end_time = time.time()
                tmp, steps = Algorithm.DLS_for_steps(root, currentDepth, steps)
                result.copy_from(tmp.board)
                flag = False
            currentDepth += 1
        execution_time = (end_time - start_time) * 1000
        statistics.init_statictic(result.get_board_matrix(), steps, top, execution_time, currentDepth-1)
        return statistics