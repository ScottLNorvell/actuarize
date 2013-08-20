import sunlight
from sunlight import congress
import datetime

def init_congress():
    sunlight.config.API_KEY = 'eac27a8195aa4449accab1e918afb1dc'

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

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

def get_gender_float(person):
    bday_str = person['birthday']
    bday = bday_str.split('-')
    born = datetime.date(int(bday[0]),
                         int(bday[1]),
                         int(bday[2]))
    age = calculate_age(born)
    sex = person['gender']
    if sex == 'M':
        gf = 1.0 * age
    elif sex == 'F':
        gf = -1.0 * age
    else:
        return None
    return gf

def get_name_str(person):
    title = person['title']
    first = person['first_name']
    middle = (person['middle_name'] or '')
    # Avoids extra space if middle = ''
    if middle:
        middle += ' ' 
    last = person['last_name']
    party = person['party']
    state = person['state']
    # concatenate
    name_str = title + " " + \
               first + " " + \
               middle + \
               last + " " + \
               party + " " + \
               state
    return name_str
    

# needs to return ages for actuary
# bioguide id's (to render picurls and bio links)
# string with rendered name, chamber, state , party
def get_congress_data(cong_list):
    
    ## Pos and net values based on birthdate
    ages = []

    ## Tuples of name_str,bioguide_id
    cong_info = []
    for person in cong_list:
        # get gender float (pos male or neg female) to use in actuarize
        gf = get_gender_float(person)
        name_str = get_name_str(person)
        bioguide_id = person['bioguide_id']
        ages.append(gf)
        cong_info.append((name_str,bioguide_id))
    return ages,cong_info

def get_by_state(state):
    p1 = congress.legislators(state=state, per_page=50, page=1)
    p2 = congress.legislators(state=state, per_page=50, page=2)
    return p1 + p2

def get_by_party(party):
    p1 = congress.legislators(party=party, per_page=50, page=1)
    p2 = congress.legislators(party=party, per_page=50, page=2)
    p3 = congress.legislators(party=party, per_page=50, page=3)
    return p1 + p2 + p3

