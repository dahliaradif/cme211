import sys
import random as random
import time as time

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  $ python3 processdata.py <reference_file> <reads_file> <aligns_file>")
        sys.exit(0)
    reference_file = sys.argv[1]
    reads_file = sys.argv[2]
    aligns_file = sys.argv[3]


def processdata(reference_file, reads_file, aligns_file):
    #initialise values for these three reads in order to keep track of how many of each type there are
    numberOfReads0 = 0
    numberOfReads1 = 0
    numberOfReads2 = 0
    with open(aligns_file, "w") as f_aligns:
        with open(reference_file, "r") as f_ref:
            reference = f_ref.read()
            with open(reads_file, "r") as f_reads:
                # split lines eliminates the "\n" from each read
                read = f_reads.read().splitlines()
# For each read, we create an empty list, and append the read. This is a helpful way of keeping track of all of the alignement indices, and what read they correspond to
                starttime = time.time()
                referenceLength = len(reference)
                for line in read:
                    lineLength = len(line)
                    A = []
                    A.append(line)
                    index = 0
# In this loop, we check the entire reference for potential alignments. If the return value for the find function is < -1, we append the index to the corresponding read array, then increment the index by the read length.
# Otherwise, the index is -1. If this is the first index to have been returned for that read, we append -1, and then break. Otherwise, we have found all the occuring instances of the read in the reference, so we break.
                    while index < referenceLength:
                        index = reference.find(line, index)
                        if index > -1:
                            A.append(index)
                            index += (lineLength)
                        else:
                            if len(A)==1:
                                A.append(-1)
                                break
                            break
                    #This section of code increments each type of read accordingly, e.g. if the only index in A is -1, then we know this is a read that aligns 0 times.        
                    if A[1] == -1:
                        numberOfReads0 +=1
                    elif A[1] >=0 and len(A) ==2:
                        numberOfReads1 +=1
                    else:
                        numberOfReads2 +=1
                    # converts the array into the format required by the assignment specification, then writes it to the aligns file
                    alignment = ' ' .join(str(i) for i in A)
                    f_aligns.write(alignment+"\n")  
            f_reads.close()
        f_ref.close()
    f_aligns.close()   
            
    TotalNumberOfReads = numberOfReads0+numberOfReads1+numberOfReads2
    print("reference length: {0}" .format(referenceLength))
    print("number reads: {0}" .format(TotalNumberOfReads))
    print("aligns 0: {0}" .format(numberOfReads0/TotalNumberOfReads))
    print("aligns 1: {0}" .format(numberOfReads1/TotalNumberOfReads))
    print("aligns 2: {0}" .format(numberOfReads2/TotalNumberOfReads))
    print("elapsed time: {0}" .format(round(time.time() - starttime,6)))

processdata(reference_file, reads_file, aligns_file)  
