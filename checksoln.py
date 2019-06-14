import sys
import numpy as np

if len(sys.argv) < 2:
    print('Usage:')
    print('  python3 checksoln.py [maze file] [solution file]')

maze_file = sys.argv[1]
solution_file = sys.argv[2]

# read in maze file
file = np.loadtxt(maze_file)
numberOfRows = int(file[0][0])
numberOfColumns = int(file[0][1])
maze = np.zeros((numberOfRows, numberOfColumns))
for i in range(1, len(file)):
    row = int(file[i][0])
    col = int(file[i][1])
    maze[row][col] = 1

# read in solution file
coordinates = []
solutionfile = np.loadtxt(solution_file)
for i in range(len(solutionfile)):
    coordinates.append((int(solutionfile[i][0]), int(solutionfile[i][1])))

# check that the first line of the maze is the entry point in the solution
entryPoint = coordinates[0]
row_start = entryPoint[0]
col_start = entryPoint[1]
if row_start == 0:
    if maze[row_start][col_start] == 1:
        print("Solution is invalid!")
else:
    print("Solution is invalid!")
    sys.exit(0)

# check that the exit is in fact the last row of the maze
exitPoint = coordinates[-1]
row_end = exitPoint[0]
col_end = exitPoint[1]
if row_end == (numberOfRows-1):
    if maze[row_end][col_end] == 1:
        print("Solution is invalid!")
else:
    print("Solution is invalid!")


# check that no walls are crossed in the solution
for i in range(len(coordinates)):
    row_i = coordinates[i][0]
    col_i = coordinates[i][1]
    # check that we stay within the bounds of the maze
    if row_i < numberOfRows and col_i < numberOfColumns:
        if maze[row_i, col_i] == 1:
            print("Solution is invalid!")
            sys.exit(0)
    else:
        print("Solution is invalid!")

# check that we move one position at a time
for i in range(len(coordinates)-1):
    j = i+1
    row_i = coordinates[i][0]
    col_i = coordinates[i][1]
    row_j = coordinates[j][0]
    col_j = coordinates[j][1]
    if (abs(row_i-row_j)) > 1 or (abs(col_i-col_j)) > 1:
        print("Solution is invalid!")
        sys.exit(0)
    else:
        if j == len(coordinates) - 1:
            print("Solution is valid!")
