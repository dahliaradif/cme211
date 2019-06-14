import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
#matplotlib.use('Agg')
import sys
import os

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

def read_files():
    directory = sorted(os.listdir("./" + path))
    images=[]
    for solution_file in directory:
        file = np.loadtxt("./" + path + "/" + solution_file)
        numberOfEntries = len(file)
        numberOfRows = numberOfEntries / numberOfColumns
        array = np.reshape(file, (int(numberOfRows), int(numberOfColumns)))
        images.append(array)
    return(images)

def computeAnimation(images):
    xStart = 0
    yStart = 0
    xEnd = length_width_h[0]
    yEnd = length_width_h[1]
    ims = []
    fig, ax = plt.subplots(1,1)
    ax.axis([xStart, xEnd, yStart-yEnd, 2*yEnd])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.3))
    for image in images:
        fig1 = plt.imshow(image, interpolation="nearest", origin="lower", cmap="jet", aspect="auto", extent=[xStart, xEnd, yStart, yEnd], animated = True)
        ims.append([fig1])
    plt.colorbar()
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)
    plt.show()
   
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  $ python3 postprocess.py <input file> <solution directory>")
        sys.exit(0)
    input_file = sys.argv[1]
    path = sys.argv[2]


length_width_h = read_input_file()
length = length_width_h[0]
width = length_width_h[1]
h = length_width_h[2]
numberOfColumns = length/h
images = read_files()
computeAnimation(images)

