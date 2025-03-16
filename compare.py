import csv
import time
import search
import fifteenpuzzle
from search import breadthFirstSearch, depthFirstSearch, uniformCostSearch
from fifteenpuzzle import FifteenPuzzleState, FifteenPuzzleSearchProblem, h2

num_scenarios = 1000

with open('scenarios.csv', 'r', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for _ in range(num_scenarios):
        puzzle = fifteenpuzzle.createRandomFifteenPuzzle(75)
        puzzle_values = [cell for row in puzzle.cells for cell in row]
        csv_writer.writerow(puzzle_values)


def solve_scenario(state):
    results = []
    
    #  Heuristics + BFS/DFS/UCS search functions
    methods = [
               (h2, 'A* with h2 (Manhattan Distance)'),
               (breadthFirstSearch, 'Breadth First Search'),
               (depthFirstSearch, 'Depth First Search'),
               (uniformCostSearch, 'Uniform Cost Search')]

    # Iterating through the methods
    for method, method_name in methods:
        problem = FifteenPuzzleSearchProblem(state)  # Initialize the problem

        if method == h2:
            print(f"Starting {method_name}...")
            path, expanded_nodes, fringe_size = aStarSearch(problem, method)
            print(f"Completed {method_name}.")
        else:  # BFS, DFS, UCS
            print(f"Starting {method_name}...")
            path, expanded_nodes, fringe_size = method(problem)  # Fringe size
            print(f"Completed {method_name}.")

        # Collect the metrics
        depth = len(path)  # Calculate depth based on path length
        results.append((method_name, depth, expanded_nodes, fringe_size))
    
    return results





if __name__ == '__main__':
    with open('scenarios.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        scenarios = list(csv_reader)

    

    names = ['Manhattan Distance', 'BFS', 'DFS', 'UCS']
    sum = [0.0] * len(names)
    num_scenarios = len(scenarios)



    for i, scenario in enumerate(scenarios):
        initial_state = FifteenPuzzleState([int(tile) for tile in scenario])
        results = solve_scenario(initial_state)

        print(f'Scenario {i + 1} - Initial State:')
        print(initial_state)

        header = ['Name', 'Depth', 'Expanded Nodes', 'Fringe Size']
        table_data = []

        for j, (name, result) in enumerate(zip(names, results)):
            method_name, depth, expanded_nodes, fringe_size = result  # Updated unpacking
            sum[j] += (depth + expanded_nodes + fringe_size)
            table_data.append([name, depth, expanded_nodes, fringe_size])


        # Calculate the maximum width for each column
        column_widths = []
        for i in range(len(header)):
            header_length = len(str(header[i]))
            max_row_length = max(len(str(row[i])) for row in table_data)
            max_length = max(header_length, max_row_length)
            column_widths.append(max_length)

        # Make the table
        
        format_string_parts = []
        for width in column_widths:
            format_string_part = f'{{:^{width}}}'
            format_string_parts.append(format_string_part)
        format_string = '|'.join(format_string_parts)

      
        header_line = format_string.format(*header)
        separator_line = '-' * len(header_line)

        print(header_line)
        print(separator_line)

       
        for row in table_data:
            print(format_string.format(*row))

        print(separator_line)
        print(separator_line)

    min_name = None
    min_value = float('inf')

    for name, sum in zip(names, sum):
        if sum < min_value:
            min_value = sum
            min_name = name

    # Determine the winning algorithm
    print(f'\nWinning Algorithm: {min_name}')
