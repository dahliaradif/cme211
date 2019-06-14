import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

def read_input_file():
    """Function that reads in the file describing the pipe geometry,
     obtaining the length, width, and h values."""
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines[:1]:
            data = line.split()
            length = float(data[0])
            width = float(data[1])
            h = float(data[2])
    f.close()
    return(length, width, h)


def read_solution_file():
    """Function that reads in the solution vector containing the final 
    vector of temperatures along the pipe, using a numpy array.The 
    array is reshaped to mimic the dimension and shape of the original pipe."""
    file = np.loadtxt(solution_file)
    numberOfEntries = len(file)
    numberOfRows = numberOfEntries / numberOfColumns
    array = np.reshape(file, (int(numberOfRows), int(numberOfColumns)))
    return(array, numberOfRows)

def compute_mean_temperature(array):
    """Function that computes and returns the mean temperature within 
    the pipe wall, to 5 decimal places."""
    globalMean = array.mean()
    return(round(globalMean,5))

def compute_mean_isoline(array, globalMean, numberOfRows):
    """Function that computes the coordinates along the width of the pipe
    of the mean temperature for each column of the solution array, using
    one dimensional linear interpolation."""
    y = np.linspace(0, width, numberOfRows)
    meanIsoline = []
    #interpolation for finding where the global mean appears in each column
    #where we standardize the row index to the width of the pipe
    for col in range(array.shape[1]):
        x = array[:,col] - globalMean
        index = np.interp(0, x, y)
        meanIsoline.append(index) 
    return (meanIsoline)

def create_plot(data, meanIsoline):
    """Function that creates the pseudocolour plot, with the axis matching
    the dimensions of the pipe wall. pcolor is used, and the mean isoline
    is layered over the plot."""
    x = np.linspace(0, length, numberOfColumns)
    y = np.linspace(0, width, numberOfRows)
    xStart = 0
    yStart = 0
    xEnd = length_width_h[0]
    yEnd = length_width_h[1]
    fig, ax = plt.subplots(1,1)
    ax.axis([xStart, xEnd, yStart-yEnd, 2*yEnd])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.2))
    #create pseudocolour plot
    c = ax.pcolor(x,y,data, cmap='jet') 
    fig.colorbar(c, ax = ax)
    ax.plot(x, meanIsoline, color='black')
    plt.savefig(output_file)

   
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  $ python3 postprocess.py <input file> <solution file> <image file>")
        sys.exit(0)
    input_file = sys.argv[1]
    solution_file = sys.argv[2]
    output_file = sys.argv[3]


length_width_h = read_input_file()
length = length_width_h[0]
width = length_width_h[1]
h = length_width_h[2]
numberOfColumns = length/h
A = read_solution_file()
array = A[0]
numberOfRows = A[1]
globalMean = compute_mean_temperature(array)
print("Input file processed: " + input_file)
print("Mean Temperature: " + str(globalMean))
meanIsoline = compute_mean_isoline(array, globalMean, numberOfRows)
create_plot(array, meanIsoline)
