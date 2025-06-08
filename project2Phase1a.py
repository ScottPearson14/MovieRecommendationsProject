#BRADEN MILLER
#PHASE 1A

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

