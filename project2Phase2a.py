#BRADEN MILLER
#PHASE 2A



def createUserList():
    f = open('u.user')
    userList = []
    #go through users
    for users in f: 
        info = users.split('|')
        current = {} 
        #add needed things from split
        current['age'] = int(info[1])
        current['gender'] = info[2]
        current['occupation'] = info[3]
        current['zip'] = info[4][:len(info[4])-1]
        userList.append(current)
    return userList
        
def createMovieList():
    f = open('u.item', encoding = "windows-1252")
    movieList = [] 
    for movies in f:
        info = movies.split('|')
        current = {}
        #add needed things from split
        current['title'] = info[1]
        current['release date'] = info[2]
        current['video release date'] = info[3]
        current['IMDB url'] = info[4] 
        genreList = []
        i = 1
        while i < len(info):
            if str(info[i]).isdigit():
                genreList.append(int(info[i]))
            i += 1
        genreList.append(int(info[len(info)-1].replace('\n', '')))
        current['genre'] = genreList
        movieList.append(current)
    return movieList
        
def readRatings():
    f = open('u.data')
    ratingTuples = []
    for ratings in f:
        info = ratings.split()
        #add needed things from split
        user = int(info[0])
        movie = int(info[1])
        rating = int(info[2])
        currentTuple = (user, movie, rating)
        ratingTuples.append(currentTuple)
    return ratingTuples

def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    Tups = sorted(ratingTuples)
    rLu = []
    rLm = []
    ratings = {}
    user = 1
    for tuples in Tups:
        if tuples[0] == user:
            ratings[tuples[1]] = tuples[2]
        else:
            user += 1
            rLu.append(ratings)
            ratings = {}
            ratings[tuples[1]] = tuples[2]
    rLu.append(ratings)
    
    movieTuples = ratingTuples
    Tups = []
    for x in movieTuples:
        user = x[0]
        movie = x[1]
        rating = x[2]
        x = (movie, user, rating)
        Tups.append(x)
    movieT = sorted(Tups)
    movie = 1
    ratings = {}
    for tuples in movieT:
        if tuples[0] == movie:
            ratings[tuples[1]] = tuples[2]
        else:
            movie += 1
            rLm.append(ratings)
            ratings = {}
            ratings[tuples[1]] = tuples[2]
    rLm.append(ratings)
    res = [rLu, rLm]
    return res   

def createGenreList():
    f = open('u.genre')
    genreList = [] 
    for genres in f:
        info = genres.split('|')
        if info[0] != '\n':
            genreList.append(info[0])
    return genreList  
         

def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):  
    if ageRange[0] == ageRange[1]:
        return [None] * 19    
    validRateUsers = [] 
   
    i = 0 #userList
    for x in userList:
        if ((gender == 'A') or (x['gender'] == gender)) and (x['age'] < ageRange[1]) and (x['age'] >= ageRange[0]):
            validRateUsers.append(i)
        i += 1

    denom = 0 #ratethem
    for x in validRateUsers:
        denom += len(rLu[x])
    if denom == 0:
        return [None] * 19  
    moviesRated = [] 
   #check with movies
    for x in validRateUsers:     
        yuh = [] 
        for validMovies in rLu[x]:
            yuh += [validMovies]
        moviesRated.append(yuh)
    validMoviesWithRatings = [] 
    i = 0
    #check if rLu
    while i < len(moviesRated):
        j = 0
        for x in moviesRated[i]:
            if (rLu[validRateUsers[i]][x] <= ratingRange[1]) and (rLu[validRateUsers[i]][x] >= ratingRange[0]):
                validMoviesWithRatings.append(moviesRated[i][j])
            j += 1
        i += 1
    genres = [0] * 19 

    for x in validMoviesWithRatings:
        i = 0
        for genreVals in movieList[x-1]['genre']:
            if genreVals == 1:
                genres[i] += 1
            i += 1
    result = [] 
    for g in genres:
        result.append(g/denom)
        
    return result

######### phase 2 functions ###########
import random
import math
import matplotlib.pyplot as plt

def randomPrediction(u, m):
    #return random rating 1-5
    return random.randint(1, 5)

def meanUserRatingPrediction(u, m, rLu):
    num=0
    denom=0
    for rating in rLu[u-1]:
        num=num+rLu[u-1][rating]
        denom=denom+1
    return num/denom

def meanMovieRatingPrediction(u, m, rLm):
    num=0
    denom=0
    for rating in rLm[m-1]:
        num=num+rLm[m-1][rating]
        denom=denom+1
    return num/denom

def demRatingPrediction(u, m, userList, rLu):
    U=set()
    numerator=0
    denom=0
    userGender=userList[u-1]['gender']
    userAge=userList[u-1]['age']
    #initiclise
    userNumber=0
    for user in userList:
        if userGender==user['gender'] and (userAge-5<=user['age']<=userAge+5) and m in rLu[userNumber] and userNumber!=u-1:
            U.add(userNumber)
            numerator=numerator+rLu[userNumber][m]
            denom=denom+1
        userNumber=userNumber+1
    #if no one fits the criteria return none
    if len(U)==0:
        return None
    #now iterate through those users and determine
    return numerator / denom


def genreRatingPrediction(u, m, movieList, rLu):
    #get the genres of m
    mGenres = movieList[m-1]['genre']
    M = []
    #get the movies with a similar genre to m 
    for movies in range(len(movieList)):
        #the genre of the movies in movieList
        potential = movieList[movies]['genre']
        count = 0
        for i in range(len(potential)):
            #check to see if any of the genres in potential are also in m
            if (potential[i] == 1) and (mGenres[i] == 1):
                count += 1
        #if more than 1 genre is alike, add it to M
        if count >= 1:
            M.append(movies)
    if len(M) == 0:
        return None 
    M.remove(m-1)
    ratings = []
    thisHasBeenRated = []
    #check to see if a movie in M has been rated by u  
    for valid in M:
        if (valid + 1 in rLu[u-1]):
            #if m has been rated by u, append its rating to a list 
            thisHasBeenRated.append(valid)
            ratings.append(rLu[u-1][valid+1]) 
    if len(ratings) == 0:
        return None    
    res = sum(ratings)/len(ratings)
    return res


def partitionRatings(rawRatings, testPercent):
    testSize = int(len(rawRatings) * testPercent / 100)
    testSet = random.sample(rawRatings, testSize)
    trainingSet = [r for r in rawRatings if r not in testSet]
    return [trainingSet, testSet]


def rmse(actualRatings, predictedRatings):
    squareDiffs = []
    for i in range(len(actualRatings)):
        if predictedRatings[i] is not None:
            squareDiffs.append((actualRatings[i] - predictedRatings[i])**2)
    avg = sum(squareDiffs) / len(squareDiffs)
    return math.sqrt(avg)


