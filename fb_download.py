
import facebook
from datetime import date
import datetime
from unidecode import unidecode
import logging


def get_timedif(updated):
    if updated:
        now = datetime.date.today()
        delta = now-updated
        return delta.days
    else:
        return 50

##############################################
### Gets Friends using facebook SDK "fql"
##############################################
    
def get_friends_fql(access_token):
    graph = facebook.GraphAPI(access_token)
    friends_data = \
        graph.fql("SELECT uid,name,birthday_date,sex FROM user WHERE uid in (SELECT uid2 FROM friend WHERE uid1 = me())")
        ## Here friend[uid] can be used to render photos! (tee hee!)
    return friends_data

##############################################
### Modification of Freinds fql
##############################################
    
def get_friends_fql2(access_token, user_id):
    graph = facebook.GraphAPI(access_token)
    fql_query = "SELECT name,uid,birthday_date,pic_square,pic_big,sex FROM user WHERE uid in (SELECT uid2 FROM friend WHERE uid1 = {0})".format(user_id)
    friends_data = graph.fql(fql_query)
        ## Here friend[uid] can be used to render photos! (tee hee!)
    return friends_data

##############################################
### extract ids from friends
##############################################

def extract_ids(friends):
    ids = []
    for friend in friends['data']:
        ids.append(friend['id'])
    return ids
  
##############################################
### Calcs age ***(use in code)***
##############################################

def calculate_age(born):
    today = date.today()
    try: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

##############################################
### Parses Bday from bday_str
##############################################
        
def parse_birthdate(bday_str):
    return datetime.datetime.strptime(bday_str, '%m/%d/%Y').date()

##############################################
### Filters for friends with valid birthday_dates
##############################################
  
def filter_friends(friend_list):
    filtered_list = []
    for friend in friend_list:
        if type(friend['birthday_date']) == type(u'str') and friend['sex'] != "":
            if len(friend['birthday_date']) > 5:
                born = parse_birthdate(friend['birthday_date'])
                friend['age'] = calculate_age(born)
                filtered_list.append(friend) # **is this "better"**
                if friend['sex'] == "female": # or the whatever the choice
                    friend['age'] *= -1.0 #Make it negative
                else:
                    friend['age'] *= 1.0
    
    return filtered_list

##############################################
### extracts ages and uid,name tuples
##############################################

# Old Code! Deletable...
def extract_ages_and_ids(filtered_friend_list):
    ages = []
    ids = []
    for friend in filtered_friend_list:
        ages.append(friend['age'])
        ids.append((friend['uid'],friend['name']))
    
    return ages, ids, len(ages)

##############################################
### Extracts ages and url,name tuples
##############################################

def extract_ages_and_ids2(filtered_friend_list):
    ages = []
    ids = []
    for friend in filtered_friend_list:
        uni_name = friend['name']
        name = unidecode(uni_name)
        logging.info('*** JUST UNIDECODED {}!!! ***'.format(name))
        ages.append(friend['age'])
        ids.append((friend['pic_big'],friend['pic_square'],name,friend['uid']))
    
    return ages, ids, len(ages)
