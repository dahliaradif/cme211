import sys
import random as random
import time as time

#This part of the code allows input from the command line. If the number of parameters is less than 6 (5 variables plus the program name) then the program exits. Otherwise, the program reads the input and assigns it to the variables accordingly.
if __name__ == "__main__": 
    if len(sys.argv) < 6:
        print("Usage:")
        print("  $ python3 generatedata.py <reference_length> <nreads> <read_length> <reference_file> <reads_file>")
        sys.exit(0)
    reference_length = int(sys.argv[1])
    nreads = int(sys.argv[2])
    reference_file = sys.argv[4]
    read_length = int(sys.argv[3])
    reads_file = sys.argv[5]
#The following functions (before generatedata) are used as functional decomposition for clarity and ease of understanding the code
#This is a function that generates a random read
def generateRead(read_length):
    read = "" #initialise an empty string
    M = ["A", "G", "C","T"] #Define an array containing the 4 bases of DNA. This makes accessing and adding each letter easier than writing an if statement for each outcome of the random number generator.
    while len(read) < read_length: #This ensures that we do not exceed the required read length
        i = random.randint(0,3)
        read = read + M[i] #Add a base to the read according to the random number generator
    return read

#This is a function that generates the reference according to the assignment specification
def generateReference(reference_length):
    reference = "" #initialise an empty string
    M = ["A", "G", "C","T"]
    referenceLength_long = int(0.75* reference_length)
    referenceLength_short = int(-0.25 *reference_length)
    while len(reference) < referenceLength_long: #the first 75% of the reference string is generated randomly
        x = random.randint(0,3)
        reference = reference + M[x]
    repeatedPart = reference[referenceLength_short:] #we slice the reference string to obtain the last third of the string, then add it to the end to form a repeated part 
    finalReference = reference + repeatedPart
    return finalReference

#This is a function that generates a read that aligns zero times, according to the assignment specification
def generateRead0(finalReference, read_length):
    read0 = generateRead(read_length) #calling the function generateRead for readability and clarity
    while finalReference.find(read0) >= 0: #condition for re-generating a read- finalReference.find(read) returns the smallest index for which the read substring appears in our reference string. If this is greater than 0, we have to regenerate the read, otherwise it is equal to -1 and we can use that read. 
        read0 = generateRead(read_length)
    return read0

#This is a function that generates a read that aligns once, according to the assignment specification
def generateRead1(finalReference, reference_length, read_length):
    i = random.randint(0, reference_length) #generate a random number in the first 50% of the reference 
    read1 = finalReference[i:i+read_length] #create a read by creating a substring of the reference, starting from the random number generated all the way through to the read length
    return read1

#This is a function that generates a read that aligns twice, according to the assignment specification
def generateRead2(finalReference, referenceLength_long, ref_minus_read,read_length):
    i = random.randint(referenceLength_long,ref_minus_read) #ensure that we start from a position in the last 25% of our index, but within 'read_length' from the end of the reference
    read2 = finalReference[i:i+read_length] #we slice the reference string to obtain our read
    return read2

# Main function
def generatedata (reference_length, nreads, read_length, reference_file, reads_file): 
    referenceLength_half = int(0.5*reference_length)
    referenceLength_long = int(0.75*reference_length)
    ref_minus_read = reference_length-read_length
    finalReference = generateReference(reference_length)  #Here, we generate our reference string by calling the function generateFunction. This is done for clarity and tidiness
    with open(reference_file,"w") as f_ref:  #we write out reference to the file "reference_file"
        f_ref.write(finalReference)
    totalNumberOfReads = 0 #counter for total number of reads generated, to use as the condiiton for the following while loop
    numberOfReads0 = 0 # the following are three counters for the reads that align 0 times, once, and twice respectively
    numberOfReads1 = 0
    numberOfReads2 = 0
    with open (reads_file, "w") as f_reads:
        while totalNumberOfReads < nreads: #while loop ensures we generate the specified number of reads
            read = ""
            x = random.random() #generates a random floating point in the range [0,1)
            if x <=0.15: #condition for zero-alignment - we want about 15% of reads to not align at all with the reference
                read = generateRead0(finalReference, read_length) #calling the function generateRead0 for readability and clarity
                numberOfReads0 +=1 #increment the number of reads that do not align
            elif 0.15 < x <= 0.9: #condition for once-alignment - we want about 75% of reads to align once with the reference
                read = generateRead1(finalReference, referenceLength_half,read_length)
                numberOfReads1 +=1 #increment the number of reads that align once
            elif x>0.9: #condition for twice-alignment - we wnat about 10% of reads to align twice with the reference
                read = generateRead2(finalReference,referenceLength_long, ref_minus_read, read_length)
                numberOfReads2 +=1 #increment the number of reads that align twice
            totalNumberOfReads +=1 #after each creation of a read, we increment the total number of reads 
            f_reads.write(read+"\n")
    f_reads.close()
    f_ref.close()
    print ("reference length: {0}" .format(reference_length))
    print ("number reads: {0}" .format(nreads))
    print ("read length: {0}" .format(read_length))
    print ("aligns 0: {0}" .format(numberOfReads0/totalNumberOfReads))
    print ("aligns 1: {0}" .format(numberOfReads1/totalNumberOfReads))
    print ("aligns 2: {0}" .format(numberOfReads2/totalNumberOfReads))

generatedata(reference_length, nreads, read_length, reference_file, reads_file)
