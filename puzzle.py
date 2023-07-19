# (!!!) THE PROGRAM CHECK WHETHER BOARD IS SOLVABLE ONLY FOR 3X3 DIMENSION
import heapq
from math import ceil, sqrt


class Board:
    def __init__(self, initial):
        # board dimension
        self.d = int(sqrt(len(initial)))
        # current board and solved board
        self.current, self.solved = initial, list(range(1, self.d**2)) + [0]
        # moves of solution and depth of tree
        self.moves, self.depth = [], 1
        # (manhattan sum + depth) for possible board outcome; an index of empty square
        self.tempFunc = self.blankIndex = 0
        # possible moves on board;
        # "0" - initial setting when delete non-existing move for avoidance of error
        self.movement = [-1, 1, -self.d, self.d, 0]
        # outcomes of current board; add initial board to queue
        self.manhattan(self.current)
        self.outcomes = [(self.tempFunc, self.current, 0, 0, 0)]
        heapq.heapify(self.outcomes)
        self.wrangleOptimal()

    # return amount of moves to right position for square
    def rightPos(self, index, value):
        if index + 1 == value:
            return 0
        deltaY = abs(ceil(value / self.d) - ceil((index + 1) / self.d))
        x1 = self.d if value % self.d == 0 else value % self.d
        x0 = self.d if (index + 1) % self.d == 0 else (index + 1) % self.d
        deltaX = abs(x1 - x0)
        # return amount of vertical and horizontal moves
        return deltaX + deltaY

    # compute sum for possible board outcome
    def manhattan(self, outcome):
        self.tempFunc = 0
        for i in range(self.d**2):
            if not outcome[i] == 0:
                self.tempFunc += self.rightPos(i, outcome[i])

    # check whether board is unfeasible
    def feasible(self):
        self.tempFunc = 0
        copyOf = self.current.copy()
        copyOf.remove(0)
        for i in range(self.d**2 - 1):
            for j in range(i + 1, self.d**2 - 1):
                if copyOf[i] > copyOf[j]:
                    self.tempFunc += 1
        if self.tempFunc % 2 == 0:
            return True
        return False

    # add to outcomes all possible boards for current state
    def possibleBoards(self):
        self.blankIndex = self.current.index(0)
        for delta in self.movement:
            outcome = self.current.copy()
            # check correctness of movement and add possible state of board
            if self.blankIndex + delta < 0:
                continue
            if ((self.blankIndex + delta) // self.d != self.blankIndex // self.d)\
                    and (delta == 1 or delta == -1):
                continue
            try:
                outcome[self.blankIndex] = outcome[self.blankIndex+delta]
                outcome[self.blankIndex + delta] = 0
                self.manhattan(outcome)
                # add (1) func output, (2) possible board, (3) the backward move and
                # (4) the index in array of current state
                # for seek route of the best solution in all moves at the end
                heapq.heappush(self.outcomes, (self.depth + self.tempFunc, outcome,
                                               -delta, self.depth, len(self.moves) - 1))
            except IndexError:
                continue
        self.movement = [-1, 1, -self.d, self.d]

    # find optimal board in priority queue
    def wrangleOptimal(self):
        self.current, backwardMove, self.depth, boardIndex = heapq.heappop(self.outcomes)[1:]
        # add move
        self.moves.append((self.current, boardIndex))
        # change depth for next state of current board
        self.depth += 1
        # remove impossible move for next state
        self.movement.remove(backwardMove)

    def findSolution(self):
        while not self.current == self.solved:
            self.possibleBoards()
            self.wrangleOptimal()
        return self.moves


# print array as square table
def table(index, square, d=3):
    print(f"MOVE {index}")
    for i in range(d):
        for j in range(d):
            print(square[d*i + j], end=" ")
        print()


def main(_path):
    with open(_path, "r") as f:
        # get data and create object
        data, state, solution = "", [], []
        for line in f.readlines():
            data += line
        dataBoard = list(map(int, data.split()[1:]))
        print(dataBoard)
        board = Board(dataBoard)
        if board.feasible():
            # find the best route
            tree, _index = board.findSolution(), -1
            while not state == dataBoard:
                state = tree[_index][0]
                solution.append(state)
                _index = tree[_index][1]
            solution.reverse()
            for (n, array) in enumerate(solution):
                table(n, array)
        else:
            print("unfeasible")


if __name__ == "__main__":
    _path = "PazlTestFiles/puzzle3x3-unsolvable.txt"
    main(_path)


