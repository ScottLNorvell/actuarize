from base import BaseHandler
from actuary_fb import actuary_valdic



###############################################
### Utility Functions
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
### class to handle no login fun test
###############################################

class ActuaryNoLogin(BaseHandler):
    def get(self):
        self.render('fb-form.html')
    
    def post(self):
        males = self.request.get('males')
        females = self.request.get('females')
        ages = neg_fems(females) + pos_males(males)
        data = actuary_valdic(ages)
        self.render('actuarized.html', **data)
        
        
        