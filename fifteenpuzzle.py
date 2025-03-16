import search
import random

# Module Classes

class FifteenPuzzleState:
    """Start Change Task of creating the list"""
    def __init__(self, numbers):
        self.cells = []
        numbers = numbers[:]
        numbers.reverse()

        for row in range(4):
            self.cells.append([])
            for col in range(4):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col
        """End Change Task"""
    """Start Change Task of creating the list"""
    def isGoal(self):
        """Checks to see if the puzzle is in its goal state."""
        goal = [1, 2, 3, 4,
                5, 6, 7, 8,
                9, 10, 11, 12,
                13, 14, 15, 0]
        current = 0
        for row in range(4):
            for col in range(4):
                if self.cells[row][col] != goal[current]:
                    return False
                current += 1
        return True
        
    def legalMoves(self):
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 3:  # Adjusted boundary for 4 rows.
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 3:  # Adjusted boundary for 4 columns.
            moves.append('right')
        return moves
        """End Change Task"""
        
    def result(self, move):
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise Exception("Illegal Move")
            
        # Create the new puzzle state based on the current state
        newPuzzle = FifteenPuzzleState([0]*16)
        newPuzzle.cells = [values[:] for values in self.cells]
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    def __eq__(self, other):
        for row in range(4):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        lines = []
        horizontalLine = ('-' * (19))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# Search problem class for the Fifteen Puzzle
"""it inherits the methods from the search.py file and we need to implement them here"""
class FifteenPuzzleSearchProblem(search.SearchProblem):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.expanded_nodes_count = 0  # Initialize the counter for expanded nodes
        self.fringe_size = 0           # Initialize the fringe size
        self.fringe = []               # Initialize the fringe list

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        self.expanded_nodes_count += 1  # Increment the count of expanded nodes
        successors = []
        for action in state.legalMoves():
            successors.append((state.result(action), action, 1))
        return successors

    def getCostOfActions(self, actions):
        return len(actions)

    def updateFringeSize(self, fringe):
        # Update the maximum fringe size encountered during the search
        self.fringe_size = max(self.fringe_size, len(fringe))

    def getExpandedNodesCount(self):
        return self.expanded_nodes_count

    def getFringeSize(self):
        return self.fringe_size

# Heuristic functions
def h1(state, problem=None):
    """Number of misplaced tiles"""
    count = 0
    goal = [1, 2, 3, 4,
            5, 6, 7, 8,
            9, 10, 11, 12,
            13, 14, 15, 0]
    for row in range(4):
        for col in range(4):
            if state.cells[row][col] != goal[row * 4 + col] and state.cells[row][col] != 0:
                count += 1
    return count

def h2(state, problem=None):
    """Sum of Manhattan distances."""
    total_distance = 0
    for row in range(4):
        for col in range(4):
            p = state.cells[row][col]
            if p != 0:
                # Adjust the goal position for 0-based indexing
                goal_row = (p - 1) // 4
                goal_col = (p - 1) % 4
                total_distance += abs(row - goal_row) + abs(col - goal_col)
    return total_distance

def h3(state, problem=None):
    """Sum of Euclidean distances of tiles from their goal positions heuristic."""
    total_distance = 0
    for row in range(4):
        for col in range(4):
            p = state.cells[row][col]
            if p != 0:
                goal_row = (p - 1) // 4
                goal_col = (p - 1) % 4
                total_distance += ((row - goal_row) ** 2 + (col - goal_col) ** 2) ** 0.5
    return total_distance

def h4(state, problem=None):
    """Number of tiles out of row + Number of tiles out of column."""
    out_of_row = 0
    out_of_col = 0
    for row in range(4):
        for col in range(4):
            p = state.cells[row][col]
            if p != 0:
                goal_row = (p - 1) // 4
                goal_col = (p - 1) % 4
                if row != goal_row:
                    out_of_row += 1
                if col != goal_col:
                    out_of_col += 1
    return out_of_row + out_of_col

# Example of generating random puzzles and solving them
def createRandomFifteenPuzzle(moves=20):
    puzzle = FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for i in range(moves):
        puzzle = puzzle.result(random.choice(puzzle.legalMoves()))
    return puzzle

if __name__ == '__main__':
    puzzle = createRandomFifteenPuzzle(10)
    print('A random puzzle:')
    print(puzzle)

    problem = FifteenPuzzleSearchProblem(puzzle)

    for heuristic in [h1, h2, h3, h4]:
        print(f'Using heuristic: {heuristic.__name__}')
        path = search.aStarSearch(problem, heuristic)
        
        print('A* found a path of %d moves: %s' % (len(path), str(path)))
        curr = puzzle
        i = 1
        for action in path:
            curr = curr.result(action)
            print('After %d move%s: %s' % (i, ("", "s")[i > 1], action))
            print(curr)
            
            # Display the heuristic value
            h_value = heuristic(curr, problem)
            print(f"Heuristic value ({heuristic.__name__}) at this state: {h_value}")
            
            input("Press return for the next state...")   # Wait for key stroke
            i += 1

    # Display expanded nodes and fringe size
    print(f"Total Expanded Nodes: {problem.getExpandedNodesCount()}")
    print(f"Maximum Fringe Size: {problem.getFringeSize()}")

