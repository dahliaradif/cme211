import math as math
import sys
import time as time

def CreateMovieDictionary(data_file):
    #In fullMovieDict, we create a nested dictionary- outer key is movie index
    #and inner key is a dictionary containing a 'sum of ratings' key
    #and 'user ratings' key which also contains dictionaries of user/ratings
    fullMovieDict = dict()
    listOfMovies = []
    numberOfUsers = set() #a set allows us to add users without worrying 
    #about duplicates,as sets only keep unique items.
    with open(data_file, "r") as f:
            lines = f.readlines()
            numberOfLines = 0
            for  movie in  (lines):
                numberOfLines+=1 # to keep track of total number of 
            #lines in the file
                movieSplit = movie.split()
            #The counter allows us to keep a record of the sum of 
            #ratings for each movie. This will let us calculate the 
            #average rating much more easily than having to reiterate 
            #through the entire dictionary again and collecting the 
            #ratings
                counter=0
                movieID = int(movieSplit[1])
                userID = int(movieSplit[0])
                rating = int(movieSplit[2])
                numberOfUsers.add(userID)
                if movieID in fullMovieDict:
                    fullMovieDict[movieID]["Sum of Ratings"] += rating 
                    fullMovieDict[movieID]["User Ratings"][userID] = rating
                else:
                #If the movie index has not been added as a key, then 
                #create an empty dictionary and add a key called 'Sum Of 
                #Ratings' and 'User Ratings', whose latter value is a 
                #dictionary in itself.
                # Within this dictionary, the keys are users and the 
                # value is the corresponding rating
                    userDict={} 
                    fullMovieDict[movieID]= userDict
                    counter+=rating
                    fullMovieDict[movieID]["Sum of Ratings"] = counter
                    fullMovieDict[movieID]["User Ratings"] = {}
                    fullMovieDict[movieID]["User Ratings"][userID] = rating
                    listOfMovies.append(movieID) #Keep a record of movie 
                    #IDs, so that we can create a sorted
                    #version of movie IDs in order to faciliate the 
                    #comparisons of movies
                    
             #Allows us a way of 'sorting' the dictionary to help with 
             #the process of iteration
            sortedListOfMovies = sorted(listOfMovies)
            movieDictAndList = (fullMovieDict, sortedListOfMovies, numberOfLines, numberOfUsers)
    f.close()
    return movieDictAndList

def ComputeAverageRating(fullMovieDict, movieID):#function to compute average rating of a specific movie
    sumOfRatings= fullMovieDict[movieID]["Sum of Ratings"]
    numberOfRatings = len(fullMovieDict[movieID]['User Ratings'])
    averageRating = sumOfRatings / (numberOfRatings) #divide by the 
    #total number of people who watched that movie
    return averageRating

#In this function, we compute the numerator and denominator of the 
#adjusted cosine similarity, using the two arrays of corresponding user 
#ratings for movies i and j
def ComputeCoefficent(A,B, r_i, r_j):
    numerator = 0
    denominatorA = 0
    denominatorB = 0
    for k in range(0, len(A)):
        x = A[k] - r_i
        y = B[k] - r_j
        numerator += (x*y)
        denominatorA += (x**2)
        denominatorB += (y**2)
    denominator = math.sqrt(denominatorA * denominatorB)
    return(numerator, denominator)

def ComputeSimilarity(fullMovieDict,i,j, user_thresh):
#i, j correspond to two different movie indices
#Here we compute the average ratings of movie i and j
    r_i = (ComputeAverageRating(fullMovieDict,i))  
    r_j = (ComputeAverageRating(fullMovieDict,j))
    A=[]
    B=[]
    #In this if-else statement, we create two lists for movies i and j 
    #whereby each entry of i and the corresponding entry of j contains 
    #the ratings that the same user gave to each movie. We then compute 
    #the adjusted cosine coefficient using the formula given in the 
    #assignment

    if len(fullMovieDict[i]['User Ratings']) < user_thresh or len(fullMovieDict[j]['User Ratings']) < user_thresh: 
        return (0,0)
    else:
        for user in fullMovieDict[i]['User Ratings']:
            if user in fullMovieDict[j]['User Ratings']:
                A.append(fullMovieDict[i]['User Ratings'][user])
                B.append(fullMovieDict[j]['User Ratings'][user])
        n =len(A)
        if n < user_thresh: #if number of users is less than the 
#specified user threshold,then we cannot compare
            return (0,0)
        else:
            numeratorAndDenominator = ComputeCoefficent(A,B, r_i, r_j) 
#this function returns a tuple so we assign the return values to 
#numerator and denominator respectively
            numerator = numeratorAndDenominator[0]
            denominator = numeratorAndDenominator[1]
            if denominator == 0:
 #return 0 if the denominator is 0, as the calculation is not possible
                return (0,0)
            else:
                P_ij = round((numerator /denominator),2) #formatting purposes
            P_ijAndUsers = (P_ij, n) 
#this is a tuple containing the coefficient, and also the length of A
#i.e. the number of people who watched and rated both movies
            return P_ijAndUsers

  #This code writes the output in the specfied format, returning the 
  #required information
  # (movie number, similarity coefficient, and number of similar users) 
  # for those movies that meet the user threshold. Otherwise, we return 
  # nothing for that movie
def WriteToFile(finalCoeffList, output_file):
    with open(output_file, "w") as f_out:
        n = len(finalCoeffList)
        for i in range(0, n):
            if finalCoeffList[i][1][1]==0:       
                f_out.write(str(finalCoeffList[i][0]) + "\n")
            else:
                output = ' ' .join(str(k) for k in finalCoeffList[i])
                f_out.write(output + "\n")
    f_out.close()
    return f_out

def similarity(data_file, output_file, user_thresh):
    startTime = time.time()
#Create a nested dictionary
    fullMovieDictandList = CreateMovieDictionary(data_file) 
#assign each return value of CreateMovieDictionary to separate objects
    fullMovieDict = fullMovieDictandList[0]
    listOfMovies = fullMovieDictandList[1]
    numberOfLines = fullMovieDictandList[2]
    numberOfUsers = len(fullMovieDictandList[3])
 #We require this for the print statmenet 
    numberOfMovies = len(listOfMovies)
    finalCoeffList = [[k]for k in listOfMovies]
 #initialise a list of lists- the first entry of each list is the movie 
 #index. Since listOfMovies was sorted, this list will be too
    for i in range(0,numberOfMovies):
        for j in range(i+1, numberOfMovies):
 #We do not need to compare i and j twice, as the formula is 
 #symmetrical, so the second forloop starts at j=i+1 ComputeSimilarity 
 #returns a tuple- the coefficient for movies i and j, and the number of
 #people who watched both
            P_ijAndUsers = ComputeSimilarity(fullMovieDict,listOfMovies[i], listOfMovies[j], user_thresh)
            P_ij = P_ijAndUsers[0]
            numberOfCommonUsers = P_ijAndUsers[1]
            #The following logic is required to make sure that for each 
            #i and j, we add the movie with the maximum matching 
            #coefficient
            if len(finalCoeffList[i])==1:
 #the entry for movie i is just its index, so we add a second element, 
 #namely (movie j index, cosine similarity coefficient, and number of 
 #commmon users)
                finalCoeffList[i].append((listOfMovies[j],P_ij, numberOfCommonUsers))
            elif finalCoeffList[i][1][1] ==0:
 #e.g., 0 is bigger than a negative P_ij, but it is a result of not 
 #meeting the user threshold, so we shouldn't replace the current value
                finalCoeffList[i][1]=((listOfMovies[j],P_ij, numberOfCommonUsers))
 #same logic for movie j (as the coefficient for movie i is the same for 
 #movie j)
            elif P_ij > finalCoeffList[i][1][1] and P_ij !=0:
                finalCoeffList[i][1]=((listOfMovies[j],P_ij, numberOfCommonUsers))
            if len(finalCoeffList[j])==1:
                finalCoeffList[j].append((listOfMovies[i],P_ij, numberOfCommonUsers))
            elif finalCoeffList[j][1][1] ==0:
                finalCoeffList[j][1]= ((listOfMovies[i],P_ij, numberOfCommonUsers))
            elif P_ij > finalCoeffList[j][1][1] and P_ij !=0:
                finalCoeffList[j][1]=((listOfMovies[i],P_ij, numberOfCommonUsers))
#once the list is populated, we write to the output file, calling the 
#function WriteToFile
    WriteToFile(finalCoeffList, output_file)
    endTime = (time.time()-startTime)

    print("Input MovieLens file: {0}" .format(data_file))
    print("Output file for similarity data: {0}" .format(output_file))
    print("Minimum number of common users: {0}" .format(user_thresh))
    print("Read {0} lines with total of {1} movies and {2} users" .format(numberOfLines, len(fullMovieDict), numberOfUsers))
    print("Computed similarities in {0} seconds" .format(round(endTime,7)))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("  $ python3 similarity.py <data_file> <output_file> [user_thresh (default = 5)]")
        sys.exit(0)
    data_file = sys.argv[1]
    output_file = sys.argv[2]
    user_thresh = int(sys.argv[3])
    similarity(data_file, output_file, user_thresh)

