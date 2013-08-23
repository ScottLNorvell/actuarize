from tmdb3 import set_key, searchMovie, set_cache
import datetime
import re
from urllib import urlencode
import json
from unidecode import unidecode
from facebook_secrets import FB_SECRETS

def init_movie():
    #set_cache('null')
    set_key(FB_SECRETS['tmdb_key'])

def calculate_age(born):
    today = datetime.date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def get_movie_list(moviestr,n):
    movs = searchMovie(moviestr)
    movies = []
    for movie in movs[0:n+1]:
        movie_id=movie.id
        try:
            year = movie.releasedate.year
        except:
            year = ''
        title = movie.title
        # Error Handling for url-encoding non ascii titles!
        try:
            title = str(title)
        except:
            continue
        url = '/tmdb-actuarized?' + urlencode(dict(movie_id=movie_id,
                                                   movie=title,
                                                   year=year))
        movies.append((title,year,url))
    return movies

# gets movie redirect url if raw string of data...
def get_first_mov_url_noyear(moviestr):
    movs = searchMovie(moviestr)
    try:
        movie = movs[0]
    except:
        return None
    
    if not movie:
        return None
    
    movie_id=movie.id
    try:
        year = movie.releasedate.year
    except:
        year = ''
    title = movie.title
    # Error Handling for url-encoding non ascii titles!
    try:
        title = str(title)
    except:
        return None
    url = '/tmdb-actuarized?' + urlencode(dict(movie_id=movie_id,
                                               movie=title,
                                               year=year))
    
    return url
# Gets url from selected and pretty data!
def get_first_mov_url(moviestr, year, movie_id):
    
    url = '/tmdb-actuarized?' + urlencode(dict(movie_id=movie_id,
                                               movie=moviestr,
                                               year=year))
    
    return url


def get_autocomp_movies(moviestr,n):
    movs = searchMovie(moviestr)
    movies = []
    for movie in movs[0:n+1]:
        
        try:
            year = movie.releasedate.year
        except:
            year = ''
        uni_title = movie.title
        title = unidecode(uni_title)
        movie_id = movie.id
        movies.append(dict(value = title,
                           year = year,
                           movie_id = movie_id,
                           label = title + ' --- ({})'.format(year) ))
    return json.dumps(movies)

def get_sex_from_bio(bio):
    if not bio:
        return None
    actor = re.compile('[Aa]ctor[., ]')
    actress = re.compile('[Aa]ctress[., ]')
    male = actor.search(bio,0,200)
    female = actress.search(bio,0,200)
    if male:
        return 1.0
    elif female:
        return -1.0
    else:
        lower = bio.lower()
        he = lower.count(' he')
        his = lower.count(' his')
        she = lower.count(' she')
        her = lower.count(' her')
        male = he + his
        female = she + her
        if male > female:
            return 1.0
        elif female > male:
            return -1.0
        else:
            return None

def get_nm_pic_id(person):
    defaultpic = 'http://d3a8mw37cqal2z.cloudfront.net/assets/91c0541cff7ec/images/no-profile-{}.jpg'
    pics = person.profile
    name = unidecode(person.name)
    if pics:
        sizes = pics.sizes()
        pic_small = pics.geturl(sizes[0])
        pic_big = pics.geturl(sizes[-1])
    else:
        pic_small = defaultpic.format('w45')
        pic_big = defaultpic.format('w185')
    return (name,pic_small,pic_big,person.id)

def get_poster(movie):
    poster = movie.poster
    if poster:
        sizes = poster.sizes()
        posturl = poster.geturl(sizes[1])
        return posturl
    else:
        return None

#Gets cast ages and sexes
#Modify to return pos and neg ages (also dead ones tee hee)
def get_cast_data(moviestr , year):
    movies = searchMovie(moviestr, year=year)
    if not movies:
        return None
    firstmov = movies[0]
    cast = firstmov.cast
    if not cast:
        return None
    poster = get_poster(firstmov)
    movie_id = firstmov.id
    
    dead = []
    alive = []
    ages = []

    for person in cast:
        died = person.dayofdeath
        bio = person.biography
        if died:
            deaddata = get_nm_pic_id(person)
            dead.append(deaddata)
            continue
        born = person.dayofbirth
        
        if not born:
            continue
        sex = get_sex_from_bio(bio)
        if not sex:
            continue
        livedata = get_nm_pic_id(person)
        age = calculate_age(born)
        
        alive.append(livedata)
        ages.append(age*sex)
    if not ages:
        return None
    return poster,movie_id,dead,alive,ages




