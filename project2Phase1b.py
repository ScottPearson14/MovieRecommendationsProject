####PHASE 1 B VISUALS
##BRADEN MILLER

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
    movieTups = sorted(Tups)
    movie = 1
    ratings = {}
    for tuples in movieTups:
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
    for idk in genres:
        result.append(idk/denom)
        
    return result
    

#MAIN
import matplotlib.pyplot as plt
import numpy as np
# create user, movie, and ratings lists and genre
userList = createUserList()
movieList = createMovieList()
ratingTuples = readRatings()
rLu, rLm = createRatingsDataStructure(len(userList), len(movieList), ratingTuples)
genreList = createGenreList()

# select genres
selectedGenres = ["Action", "Comedy", "Drama", "Horror", "Romance"]

# plot fraction of high ratings (4 or 5) for all
fractionsM = demGenreRatingFractions(userList, movieList, rLu, 'M', (0, 100), (4, 5))
fractionsF = demGenreRatingFractions(userList, movieList, rLu, 'F', (0, 100), (4, 5))
colors = ['blue','black']
# Set bar width and x-positions
barWidth = 0.4
r1 = np.arange(len(selectedGenres))
r2 = [x + barWidth for x in r1]
# Plot bars
for i, genre in enumerate(selectedGenres):
    genreIndex = genreList.index(genre)
    plt.bar(r1[i], fractionsM[genreIndex], color = colors[0], width = barWidth, label='Male' if i == 0 else None)
    plt.bar(r2[i], fractionsF[genreIndex], color = colors[1], width = barWidth, label='Female' if i == 0 else None)
# Set x-axis tick labels
plt.xticks([r + barWidth / 2 for r in range(len(selectedGenres))], selectedGenres)
plt.title(f"High Ratings for All Users")
plt.xlabel("Genre")
plt.ylabel("Fraction of High Ratings")
plt.legend()
plt.show()

# plot fraction of low ratings (1 or 2) for all
fractionsM = demGenreRatingFractions(userList, movieList, rLu, 'M', (0, 100), (1, 2))
fractionsF = demGenreRatingFractions(userList, movieList, rLu, 'F', (0, 100), (1, 2))
colors = ['blue','black']
# Set bar width and x-positions
barWidth = 0.4
r1 = np.arange(len(selectedGenres))
r2 = [x + barWidth for x in r1]
# Plot bars
for i, genre in enumerate(selectedGenres):
    genreIndex = genreList.index(genre)
    plt.bar(r1[i], fractionsM[genreIndex], color = colors[0], width = barWidth, label='Male' if i == 0 else None)
    plt.bar(r2[i], fractionsF[genreIndex], color = colors[1], width = barWidth, label='Female' if i == 0 else None)
# Set x-axis tick labels
plt.xticks([r + barWidth / 2 for r in range(len(selectedGenres))], selectedGenres)
plt.title(f"Low Ratings for All Users")
plt.xlabel("Genre")
plt.ylabel("Fraction of Low Ratings")
plt.legend()
plt.show()


# plot fraction of ratings (1 to 5) by 20-30
fractionsM = demGenreRatingFractions(userList, movieList, rLu, 'M', (20, 30), (1, 5))
fractionsF = demGenreRatingFractions(userList, movieList, rLu, 'F', (20, 30), (1, 5))
colors = ['blue','black']
# Set bar width and x-positions
barWidth = 0.4
r1 = np.arange(len(selectedGenres))
r2 = [x + barWidth for x in r1]
# Plot bars
for i, genre in enumerate(selectedGenres):
    genreIndex = genreList.index(genre)
    plt.bar(r1[i], fractionsM[genreIndex], color = colors[0], width = barWidth, label='Male' if i == 0 else None)
    plt.bar(r2[i], fractionsF[genreIndex], color = colors[1], width = barWidth, label='Female' if i == 0 else None)
# Set x-axis tick labels
plt.xticks([r + barWidth / 2 for r in range(len(selectedGenres))], selectedGenres)
plt.title(f"Ratings for 20-30 Year Olds")
plt.xlabel("Genre")
plt.ylabel("Fraction of Ratings")
plt.legend()
plt.show()


#plot ratings for 50-60
fractionsM = demGenreRatingFractions(userList, movieList, rLu, 'M', (50, 60), (1, 5))
fractionsF = demGenreRatingFractions(userList, movieList, rLu, 'F', (50, 60), (1, 5))
colors = ['blue','black']
# Set bar width and x-positions
barWidth = 0.4
r1 = np.arange(len(selectedGenres))
r2 = [x + barWidth for x in r1]
# Plot bars
for i, genre in enumerate(selectedGenres):
    genreIndex = genreList.index(genre)
    plt.bar(r1[i], fractionsM[genreIndex], color = colors[0], width = barWidth, label='Male' if i == 0 else None)
    plt.bar(r2[i], fractionsF[genreIndex], color = colors[1], width = barWidth, label='Female' if i == 0 else None)
# Set x-axis tick labels
plt.xticks([r + barWidth / 2 for r in range(len(selectedGenres))], selectedGenres)
plt.title(f"Ratings for 50-60 Year Olds")
plt.xlabel("Genre")
plt.ylabel("Fraction of Ratings")
plt.legend()
plt.show()

