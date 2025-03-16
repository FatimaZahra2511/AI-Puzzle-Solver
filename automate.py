import csv
import time
import search
from fifteenpuzzle import FifteenPuzzleState, FifteenPuzzleSearchProblem, h1, h2, h3, h4, createRandomFifteenPuzzle

num_scenarios = 1000

# Generate 1000 random scenarios and save them to a CSV file
with open('scenarios.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)  # writes data into the CSV file
    for _ in range(num_scenarios):
        puzzle = createRandomFifteenPuzzle(75)
        puzzle_values = [cell for row in puzzle.cells for cell in row]  # It changes a 2D list into a 1D list
        csv_writer.writerow(puzzle_values)

def solve_scenario(initial_state):
    results = []  # Create an empty list
    
    for heuristic_func in [h1, h2, h3, h4]:
        problem = FifteenPuzzleSearchProblem(initial_state)
        start_time = time.time()
        path = search.aStarSearch(problem, heuristic_func)
        end_time = time.time()
        
        time_taken = end_time - start_time
        depth = len(path)
        expanded_nodes = problem.getExpandedNodesCount()
        fringe_size = problem.getFringeSize()
        
        
        current_state = initial_state
        for action in path:
            current_state = current_state.result(action)
        
        # Now check if the current state is actually the goal state
        solved = current_state.isGoal()
        
        results.append((heuristic_func.__name__, depth, expanded_nodes, fringe_size, time_taken, solved))
    return results

def main():
    with open('scenarios.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        scenarios = list(csv_reader)

    heuristic_names = ['Misplaced Tiles', 'Manhattan Distance', 'Euclidean Distance', 'Linear Conflict']
    heuristic_avg = [0.0] * len(heuristic_names)
    time_totals = [0.0] * len(heuristic_names)
    expanded_nodes_totals = [0.0] * len(heuristic_names)
    fringe_size_totals = [0.0] * len(heuristic_names)
    solved_counts = [0] * len(heuristic_names) 
    unsolved_counts = [0] * len(heuristic_names)
    
    num_scenarios = len(scenarios)

    for i, scenario in enumerate(scenarios):
        initial_state = FifteenPuzzleState([int(tile) for tile in scenario])
        
        results = solve_scenario(initial_state)

        print(f'Scenario {i + 1} - Initial State:')
        print(initial_state)

        header = ['Name', 'Depth', 'Expanded Nodes', 'Fringe Size', 'Time (s)', 'Solved']
        table_data = []

        for j, (heuristic_name, depth, expanded_nodes, fringe_size, time_taken, solved) in enumerate(results):
            heuristic_avg[j] += abs(depth)
            time_totals[j] += time_taken
            expanded_nodes_totals[j] += expanded_nodes
            fringe_size_totals[j] += fringe_size
            
            if solved:
                solved_counts[j] += 1
            else:
                unsolved_counts[j] += 1
            
            table_data.append([heuristic_name, depth, expanded_nodes, fringe_size, f'{time_taken:.4f}', 'Yes' if solved else 'No'])

        # Display the table for each scenario
        column_widths = [max(len(str(header[i])), max(len(str(row[i])) for row in table_data)) for i in range(len(header))]
        format_string = '|'.join(f'{{:^{width}}}' for width in column_widths)
        header_line = format_string.format(*header)
        separator_line = '-' * len(header_line)

        print(header_line)
        print(separator_line)
        for row in table_data:
            print(format_string.format(*row))
        print(separator_line)
        print(separator_line)

    # Calculate and display the averages for all puzzles
    print('\nAverage Values for All Scenarios:')
    print(f"{'Heuristic':<20}{'Avg Depth':<15}{'Avg Time (s)':<15}{'Avg Expanded':<15}{'Avg Fringe Size':<15}{'Solved':<10}{'Unsolved':<10}")
    
    min_combined_score = float('inf')
    winning_heuristic = None

    for heuristic_name, depth_total, time_total, expanded_total, fringe_total, solved, unsolved in zip(
        heuristic_names, heuristic_avg, time_totals, expanded_nodes_totals, fringe_size_totals, solved_counts, unsolved_counts):
        
        avg_depth = depth_total / num_scenarios if num_scenarios > 0 else 0
        avg_time = time_total / num_scenarios if num_scenarios > 0 else 0
        avg_expanded = expanded_total / num_scenarios if num_scenarios > 0 else 0
        avg_fringe = fringe_total / num_scenarios if num_scenarios > 0 else 0

        combined_score = avg_depth + avg_time + avg_expanded + avg_fringe

        print(f'{heuristic_name:<20}{avg_depth:<15.4f}{avg_time:<15.4f}{avg_expanded:<15.4f}{avg_fringe:<15.4f}{solved:<10}{unsolved:<10}')
        
        if combined_score < min_combined_score:
            min_combined_score = combined_score
            winning_heuristic = heuristic_name

    # Display the winning heuristic
    print(f'\nWinning Heuristic based on Combined Score: {winning_heuristic}')

if __name__ == '__main__':
    main()

