
import datetime
import json
import pickle
from urllib import urlencode

###############################################
### Actuary Tables
###############################################

bothtables=[[0.00756, 0.00052, 0.00035, 0.00025, 0.00020, 0.00018, 
             0.00017, 0.00016, 0.00014, 0.00011, 0.00009, 0.00010, 
             0.00015, 0.00027, 0.00043, 0.00061, 0.00078, 0.00094, 
             0.00107, 0.00119, 0.00131, 0.00142, 0.00149, 0.00151, 
             0.00148, 0.00143, 0.00140, 0.00138, 0.00137, 0.00139, 
             0.00141, 0.00143, 0.00147, 0.00152, 0.00158, 0.00165, 
             0.00174, 0.00186, 0.00202, 0.00221, 0.00243, 0.00267, 
             0.00291, 0.00317, 0.00344, 0.00373, 0.00405, 0.00441, 
             0.00480, 0.00524, 0.00573, 0.00623, 0.00671, 0.00714, 
             0.00756, 0.00800, 0.00853, 0.00917, 0.00995, 0.01086, 
             0.01190, 0.01301, 0.01413, 0.01522, 0.01635, 0.01760, 
             0.01906, 0.02073, 0.02265, 0.02482, 0.02729, 0.03001, 
             0.03289, 0.03592, 0.03918, 0.04292, 0.04715, 0.05173, 
             0.05665, 0.06206, 0.06821, 0.07522, 0.08302, 0.09163, 
             0.10119, 0.11183, 0.12367, 0.13679, 0.15124, 0.16702, 
             0.18414, 0.20255, 0.22224, 0.24314, 0.26520, 0.28709, 
             0.30846, 0.32891, 0.34803, 0.36544, 0.38371, 0.40289, 
             0.42304, 0.44419, 0.46640, 0.48972, 0.51421, 0.53992, 
             0.56691, 0.59526, 0.62502, 0.65628, 0.68909, 0.72354, 
             0.75972, 0.79771, 0.83759, 0.87947, 0.92345, 0.96962], 
            [0.00615, 0.00041, 0.00025, 0.00018, 0.00015, 0.00014, 
             0.00014, 0.00013, 0.00012, 0.00011, 0.00010, 0.00010, 
             0.00012, 0.00016, 0.00021, 0.00028, 0.00034, 0.00039, 
             0.00042, 0.00043, 0.00045, 0.00047, 0.00048, 0.00049, 
             0.00050, 0.00051, 0.00052, 0.00053, 0.00056, 0.00059, 
             0.00063, 0.00068, 0.00073, 0.00078, 0.00084, 0.00091, 
             0.00098, 0.00108, 0.00118, 0.00130, 0.00144, 0.00158, 
             0.00173, 0.00189, 0.00206, 0.00225, 0.00244, 0.00264, 
             0.00285, 0.00306, 0.00329, 0.00355, 0.00382, 0.00409, 
             0.00437, 0.00468, 0.00505, 0.00549, 0.00603, 0.00665, 
             0.00736, 0.00813, 0.00890, 0.00967, 0.01047, 0.01136, 
             0.01239, 0.01357, 0.01491, 0.01641, 0.01816, 0.02008, 
             0.02210, 0.02418, 0.02641, 0.02902, 0.03206, 0.03538, 
             0.03899, 0.04301, 0.04766, 0.05307, 0.05922, 0.06618, 
             0.07403, 0.08285, 0.09270, 0.10365, 0.11574, 0.12899, 
             0.14343, 0.15907, 0.17591, 0.19393, 0.21312, 0.23254, 
             0.25193, 0.27097, 0.28933, 0.30670, 0.32510, 0.34460, 
             0.36528, 0.38720, 0.41043, 0.43505, 0.46116, 0.48883, 
             0.51816, 0.54925, 0.58220, 0.61714, 0.65416, 0.69341, 
             0.73502, 0.77912, 0.82587, 0.87542, 0.92345, 0.96962]]

###############################################
### Utility Functions
###############################################

#returns probablility of death based on actuary tables 
def deathprob(age, years):
    #negative ages = female
    act=[]
    if age<0:
        act=bothtables[1]
        age=-1*age
    else:
        act=bothtables[0]
    while(len(act)<int(age+years+2)): # slower/bloatier but keeps things clean
        act.append(act[-1]**0.5)
    liveprob=1
    i=0
    iage=int(age)
    fage=age%1
    while i<=years-1:
        thisyear=(1-fage)*act[iage+i]+fage*act[iage+i+1]
        liveprob*=1-thisyear
        i+=1
    if years%1: # Amortizes risk of dying over a partial year, which is
                # 1-P(living last full year)^(year fraction)
        lastyear=(1-fage)*act[iage+i]+fage*act[iage+i+1]
        lastyearlive=1-lastyear
        lastyearlive=lastyearlive**((years%1))
        liveprob*=lastyearlive
    return 1-liveprob

# probability that all will die in "years" years
def proballdie(ages, years):
    probsliving=[]
    for i in ages:
        probsliving.append(1-deathprob(i, years))
    prod=1
    for i in probsliving:
        prod*=(1-i)
    return prod

# prob that any will die in "years" years
def probanydie(ages, years):
    probsliving=[]
    for i in ages:
        probsliving.append(1-deathprob(i, years))
    prod=1
    for i in probsliving:
        prod*=i
    return 1-prod

# calculates life expectancy based on probability (flag delineates 0=all or 1=any)
def calcexp(ages, prob, flag):
    i=0
    for interval in (10, 1, 0.1, 0.01):
        probs=0
        while(probs<prob):
            i+=interval
            if flag==0:
                probs=proballdie(ages, i)
            else:
                probs=probanydie(ages, i)
        i-=interval
    return i

###############################################
### sex string manipulators
###############################################

# makes female values a list of negative floats
def neg_fems(females):
    fem = females.split()
    result = []
    for female in fem:
        result.append(-1*float(female))
    return result

# makes male values a list of positive floats
def pos_males(males):
    mle = males.split()
    result = []
    for male in mle:
        result.append(float(male))
    return result

###############################################
### Get the date "years" years away
###############################################

def get_dates(years):
    result = (datetime.date.today() + \
              datetime.timedelta(days = 365.242191 * years )).year
    return result

###############################################
### Actuarize Dict for Template!
###############################################

def actuary_valdic(ages):
    # Someone's Years!
    sy05 = calcexp(ages, 0.05, 1)
    sy50 = calcexp(ages, 0.5, 1)
    sy95 = calcexp(ages, 0.95, 1)
    # Someone's Dates!
    sd05 = get_dates(sy05)
    sd50 = get_dates(sy50)
    sd95 = get_dates(sy95)
    
    valdic = dict(sy05=str(sy05),
              sy50=str(sy50),
              sy95=str(sy95),
              sd05=str(sd05),
              sd50=str(sd50),
              sd95=str(sd95))
    # example there is a 5% possibility that someone will die in {{sy05}} years (by {{sd05}})
    if len(ages)>1:
        # Everyone's Years!
        ey05 = calcexp(ages, 0.05, 0)
        ey50 = calcexp(ages, 0.5, 0)
        ey95 = calcexp(ages, 0.95, 0)
        # Everyone's Dates!
        ed05 = get_dates(ey05)
        ed50 = get_dates(ey50)
        ed95 = get_dates(ey95)

        #Add that to Valdic!
        valdic["ey05"]=str(ey05)
        valdic["ey50"]=str(ey50)
        valdic["ey95"]=str(ey95)
        valdic["ed05"]=str(ed05)
        valdic["ed50"]=str(ed50)
        valdic["ed95"]=str(ed95)
        # example there is a 5% possibility that someone will die in {{ey05}} years (by {{ed05}})
    
    years = 2045
       
    if years>datetime.date.today().year:
        years=years-datetime.date.today().year
    if len(ages)>1:
        p=100*proballdie(ages, years)
        printable=""
        if p<0.001:
            printable="<0.001"
        elif p>99.99:
            printable=">99.99"
        else:
            printable=str(p)[:5]
        valdic["evprintable"]=printable
        
    p=100*probanydie(ages, years)
    printable=""
    if p<0.001:
        printable="<0.001"
    elif p>99.99:
        printable=">99.99"
    else:
        printable=str(p)[:5]
    valdic["smprintable"]=printable
    valdic["years"]=str(years)
    pickled_ages = pickle.dumps(ages)
    valdic["age_url"] = urlencode(dict(ages=pickled_ages))
    return valdic

###############################################
### Json Datadics for api
###############################################

# json data dic for probanydie
def get_probany_data(ages):
    series = []
    for years in range(125):
        percent = round(100*probanydie(ages,years), 2)
        points = [years,percent]
        series.append(points)
        if percent > 99.99:
            break

    data = dict(label = 'Probability someone will die',
                data = series,
                color = '#6E8CCC')
    return json.dumps(data)

# json data dic for proballdie
def get_proball_data(ages):
    series = []
    last_data = [0,0]
    for years in range(125):
        percent = round(100*proballdie(ages,years), 2)
        if percent > 0.0:
            series.append(last_data)
            if percent > 99.99:
                points = [years,percent]
                series.append(points)
                break
        last_data = [years,percent]

    data = dict(label = 'Probability everyone will die',
                data = series,
                color = '#3B5998')
    return json.dumps(data)

# json data for slider functionality
def get_prob_percentages(ages,years):
    proball = round(100*proballdie(ages,years),2)
    probany = round(100*probanydie(ages,years),2)
    data = dict(proball=str(proball) + '%',
                probany=str(probany) + '%')
    return json.dumps(data)
